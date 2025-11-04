import strawberry
from datetime import datetime, timezone
import logging

from app.api.graphql.types import (
    CreateCommunicationInput,
    CreateCommunicationPayload,
    Communication as GQLCommunication,
    Opportunity as GQLOpportunity,
    OpportunityType as GQLOpportunityType,
    OpportunityStatus as GQLOpportunityStatus,
    CommunicationType as GQLCommunicationType,
)
from app.models.communication import CommunicationType as DBCommunicationType
from app.services.ai_service import OpportunityDetector, AIServiceError
from app.services.opportunity_service import OpportunityService
from app.utils.database import get_db

logger = logging.getLogger(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_communication(
        self,
        info,
        input: CreateCommunicationInput
    ) -> CreateCommunicationPayload:
        """Create communication and analyze for opportunities"""

        # Input validation
        if len(input.content) < 50:
            raise ValueError("Content must be at least 50 characters long")

        if len(input.content) > 10000:
            raise ValueError("Content must not exceed 10,000 characters")

        if not input.client_name or len(input.client_name.strip()) == 0:
            raise ValueError("Client name is required")

        try:
            # Get database session
            db_gen = get_db()
            db = await db_gen.__anext__()

            try:
                # Convert GraphQL enum to DB enum
                source_type_map = {
                    GQLCommunicationType.EMAIL: DBCommunicationType.EMAIL,
                    GQLCommunicationType.MEETING: DBCommunicationType.MEETING,
                    GQLCommunicationType.NOTE: DBCommunicationType.NOTE,
                }
                db_source_type = source_type_map[input.source_type]

                # Initialize services
                ai_detector = OpportunityDetector()
                opp_service = OpportunityService(db=db, ai_detector=ai_detector)

                # Create communication and analyze opportunities
                communication, opportunities = await opp_service.create_communication_with_opportunities(
                    content=input.content,
                    client_name=input.client_name,
                    source_type=db_source_type
                )

                logger.info(
                    f"Successfully created communication {communication.id} with {len(opportunities)} opportunities"
                )

                # Convert DB models to GraphQL types
                gql_communication = GQLCommunication(
                    id=str(communication.id),
                    content=communication.content,
                    client_name=communication.client_name,
                    source_type=input.source_type,
                    created_at=communication.created_at,
                    updated_at=communication.updated_at,
                )

                gql_opportunities = []
                for opp in opportunities:
                    # Map DB enum to GraphQL enum
                    type_map = {
                        "REAL_ESTATE": GQLOpportunityType.REAL_ESTATE,
                        "EMPLOYMENT_LAW": GQLOpportunityType.EMPLOYMENT_LAW,
                        "MERGERS_AND_ACQUISITIONS": GQLOpportunityType.MERGERS_AND_ACQUISITIONS,
                        "INTELLECTUAL_PROPERTY": GQLOpportunityType.INTELLECTUAL_PROPERTY,
                        "LITIGATION": GQLOpportunityType.LITIGATION,
                    }

                    status_map = {
                        "NEW": GQLOpportunityStatus.NEW,
                        "REVIEWING": GQLOpportunityStatus.REVIEWING,
                        "CONTACTED": GQLOpportunityStatus.CONTACTED,
                        "CLOSED": GQLOpportunityStatus.CLOSED,
                        "ARCHIVED": GQLOpportunityStatus.ARCHIVED,
                    }

                    gql_opp = GQLOpportunity(
                        id=str(opp.id),
                        title=opp.title,
                        description=opp.description,
                        opportunity_type=type_map[opp.opportunity_type.value],
                        confidence=float(opp.confidence),
                        estimated_value=opp.estimated_value,
                        extracted_text=opp.extracted_text,
                        status=status_map[opp.status.value],
                        detected_at=opp.detected_at,
                        created_at=opp.created_at,
                    )
                    gql_opportunities.append(gql_opp)

                return CreateCommunicationPayload(
                    communication=gql_communication,
                    opportunities=gql_opportunities
                )

            finally:
                # Clean up database session
                try:
                    await db_gen.aclose()
                except StopAsyncIteration:
                    pass

        except AIServiceError as e:
            logger.error(f"AI service error: {e}")
            raise Exception(f"Failed to analyze communication: {str(e)}")

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error creating communication: {e}")
            raise Exception(f"Failed to create communication: {str(e)}")

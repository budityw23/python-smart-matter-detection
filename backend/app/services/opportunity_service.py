from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import logging

from app.models.communication import Communication, CommunicationType
from app.models.opportunity import Opportunity, OpportunityType
from app.services.ai_service import OpportunityDetector
from app.protobuf.helpers import create_opportunity_notification

logger = logging.getLogger(__name__)

# Mapping from AI service types to DB enums
TYPE_MAPPING = {
    "real_estate": OpportunityType.REAL_ESTATE,
    "employment_law": OpportunityType.EMPLOYMENT_LAW,
    "m&a": OpportunityType.MERGERS_AND_ACQUISITIONS,
    "ip": OpportunityType.INTELLECTUAL_PROPERTY,
    "litigation": OpportunityType.LITIGATION,
}


class OpportunityService:
    """Service for managing opportunities"""

    def __init__(self, db: AsyncSession, ai_detector: OpportunityDetector):
        self.db = db
        self.ai_detector = ai_detector

    async def create_communication_with_opportunities(
        self,
        content: str,
        client_name: str,
        source_type: CommunicationType
    ) -> tuple[Communication, List[Opportunity]]:
        """
        Create communication and analyze for opportunities.

        Returns:
            Tuple of (Communication, List[Opportunity])
        """
        # Create communication
        communication = Communication(
            content=content,
            client_name=client_name,
            source_type=source_type
        )
        self.db.add(communication)
        await self.db.flush()  # Get ID without committing

        logger.info(f"Created communication {communication.id}")

        # Analyze for opportunities
        try:
            extracted_opps = await self.ai_detector.analyze_communication(
                content=content,
                client_name=client_name
            )

            opportunities = []
            for opp_data in extracted_opps:
                opportunity = Opportunity(
                    communication_id=communication.id,
                    title=opp_data["title"],
                    description=opp_data["description"],
                    opportunity_type=TYPE_MAPPING[opp_data["type"]],
                    confidence=opp_data["confidence"],
                    estimated_value=opp_data.get("estimated_value"),
                    extracted_text=opp_data["extracted_text"],
                )
                self.db.add(opportunity)
                opportunities.append(opportunity)

            await self.db.commit()
            await self.db.refresh(communication)

            # Refresh opportunities to get IDs
            for opp in opportunities:
                await self.db.refresh(opp)

            logger.info(f"Created {len(opportunities)} opportunities")

            return communication, opportunities

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating opportunities: {e}")
            raise

    def should_notify(self, opportunity: Opportunity) -> bool:
        """Determine if opportunity should trigger notification"""
        # Notify if confidence >= 70%
        return opportunity.confidence >= 70

    def create_notification_message(
        self,
        opportunity: Opportunity,
        client_name: str
    ) -> Optional[bytes]:
        """
        Create protobuf notification message for an opportunity.

        Args:
            opportunity: Opportunity instance
            client_name: Name of the client

        Returns:
            Serialized protobuf message bytes if should notify, None otherwise
        """
        if not self.should_notify(opportunity):
            return None

        return create_opportunity_notification(opportunity, client_name)

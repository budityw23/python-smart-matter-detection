import strawberry
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.graphql.types import (
    Opportunity as GQLOpportunity,
    OpportunityConnection,
    OpportunityEdge,
    PageInfo,
    Communication as GQLCommunication,
    OpportunityStats,
    TypeCount,
    OpportunityType as GQLOpportunityType,
    OpportunityStatus as GQLOpportunityStatus,
)
from app.models.opportunity import Opportunity, OpportunityType, OpportunityStatus
from app.models.communication import Communication


async def convert_opportunity_to_gql(opp: Opportunity) -> GQLOpportunity:
    """Convert SQLAlchemy model to GraphQL type"""
    return GQLOpportunity(
        id=str(opp.id),
        title=opp.title,
        description=opp.description,
        opportunity_type=GQLOpportunityType[opp.opportunity_type.value],
        confidence=float(opp.confidence),
        estimated_value=opp.estimated_value,
        extracted_text=opp.extracted_text,
        status=GQLOpportunityStatus[opp.status.value],
        detected_at=opp.detected_at,
        created_at=opp.created_at,
    )


@strawberry.type
class Query:
    @strawberry.field
    async def opportunities(
        self,
        info,
        min_confidence: Optional[float] = None,
        type: Optional[GQLOpportunityType] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> OpportunityConnection:
        """Query opportunities with filters and pagination"""

        # Get database session from context
        db = info.context["db"]

        # Build query
        query = select(Opportunity).options(
            selectinload(Opportunity.communication)
        )

        # Apply filters
        if min_confidence is not None:
            query = query.where(Opportunity.confidence >= min_confidence)

        if type is not None:
            query = query.where(
                Opportunity.opportunity_type == OpportunityType[type.value]
            )

        # Order by confidence desc, detected_at desc
        query = query.order_by(
            Opportunity.confidence.desc(),
            Opportunity.detected_at.desc()
        )

        # Get total count
        count_query = select(func.count()).select_from(Opportunity)
        if min_confidence is not None:
            count_query = count_query.where(Opportunity.confidence >= min_confidence)
        if type is not None:
            count_query = count_query.where(
                Opportunity.opportunity_type == OpportunityType[type.value]
            )

        result = await db.execute(count_query)
        total_count = result.scalar()

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        result = await db.execute(query)
        opportunities = result.scalars().all()

        # Convert to GraphQL types
        edges = [
            OpportunityEdge(
                node=await convert_opportunity_to_gql(opp),
                cursor=str(opp.id)
            )
            for opp in opportunities
        ]

        # Calculate pagination info
        has_next = (offset + limit) < total_count
        has_prev = offset > 0

        return OpportunityConnection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=has_prev
            ),
            total_count=total_count
        )

    @strawberry.field
    async def opportunity(
        self,
        info,
        id: strawberry.ID
    ) -> Optional[GQLOpportunity]:
        """Get single opportunity by ID"""
        db = info.context["db"]

        query = select(Opportunity).where(Opportunity.id == id)
        result = await db.execute(query)
        opp = result.scalar_one_or_none()

        if not opp:
            return None

        return await convert_opportunity_to_gql(opp)

    @strawberry.field
    async def opportunity_stats(self, info) -> OpportunityStats:
        """Get dashboard statistics"""
        db = info.context["db"]

        # Total count
        total_result = await db.execute(
            select(func.count()).select_from(Opportunity)
        )
        total_count = total_result.scalar()

        # High confidence count (>= 80)
        high_conf_result = await db.execute(
            select(func.count())
            .select_from(Opportunity)
            .where(Opportunity.confidence >= 80)
        )
        high_confidence_count = high_conf_result.scalar()

        # Count by type
        by_type_result = await db.execute(
            select(
                Opportunity.opportunity_type,
                func.count(Opportunity.id)
            ).group_by(Opportunity.opportunity_type)
        )

        by_type = [
            TypeCount(
                type=GQLOpportunityType[opp_type.value],
                count=count
            )
            for opp_type, count in by_type_result
        ]

        return OpportunityStats(
            total_count=total_count,
            high_confidence_count=high_confidence_count,
            by_type=by_type
        )

import strawberry
from typing import List, Optional
from datetime import datetime
from enum import Enum


@strawberry.enum
class CommunicationType(Enum):
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    NOTE = "NOTE"


@strawberry.enum
class OpportunityType(Enum):
    REAL_ESTATE = "REAL_ESTATE"
    EMPLOYMENT_LAW = "EMPLOYMENT_LAW"
    MERGERS_AND_ACQUISITIONS = "MERGERS_AND_ACQUISITIONS"
    INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY"
    LITIGATION = "LITIGATION"


@strawberry.enum
class OpportunityStatus(Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    CONTACTED = "CONTACTED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


@strawberry.type
class Communication:
    id: strawberry.ID
    content: str
    client_name: str
    source_type: CommunicationType
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    async def opportunities(self, info) -> List["Opportunity"]:
        # Will be populated by dataloader or direct query
        return []


@strawberry.type
class Opportunity:
    id: strawberry.ID
    title: str
    description: str
    opportunity_type: OpportunityType
    confidence: float
    estimated_value: Optional[str]
    extracted_text: str
    status: OpportunityStatus
    detected_at: datetime
    created_at: datetime

    @strawberry.field
    async def communication(self, info) -> Optional[Communication]:
        # Will be populated by dataloader or direct query
        return None


@strawberry.type
class OpportunityEdge:
    node: Opportunity
    cursor: str


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool


@strawberry.type
class OpportunityConnection:
    edges: List[OpportunityEdge]
    page_info: PageInfo
    total_count: int


@strawberry.type
class TypeCount:
    type: OpportunityType
    count: int


@strawberry.type
class OpportunityStats:
    total_count: int
    high_confidence_count: int
    by_type: List[TypeCount]


@strawberry.input
class CreateCommunicationInput:
    content: str
    client_name: str
    source_type: CommunicationType


@strawberry.type
class CreateCommunicationPayload:
    communication: Communication
    opportunities: List[Opportunity]

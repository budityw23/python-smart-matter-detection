from sqlalchemy import String, Text, Numeric, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from .base import Base


class OpportunityType(str, enum.Enum):
    REAL_ESTATE = "REAL_ESTATE"
    EMPLOYMENT_LAW = "EMPLOYMENT_LAW"
    MERGERS_AND_ACQUISITIONS = "MERGERS_AND_ACQUISITIONS"
    INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY"
    LITIGATION = "LITIGATION"


class OpportunityStatus(str, enum.Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    CONTACTED = "CONTACTED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    communication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("communications.id", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    opportunity_type: Mapped[OpportunityType] = mapped_column(
        SQLEnum(OpportunityType),
        nullable=False
    )
    confidence: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    estimated_value: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OpportunityStatus] = mapped_column(
        SQLEnum(OpportunityStatus),
        default=OpportunityStatus.NEW,
        nullable=False
    )
    detected_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    communication: Mapped["Communication"] = relationship(
        back_populates="opportunities"
    )

    # Indexes
    __table_args__ = (
        Index('idx_opportunities_confidence', 'confidence'),
        Index('idx_opportunities_type', 'opportunity_type'),
        Index('idx_opportunities_detected_at', 'detected_at'),
        Index('idx_opportunities_communication_id', 'communication_id'),
    )

    def __repr__(self):
        return f"<Opportunity(id={self.id}, type={self.opportunity_type})>"

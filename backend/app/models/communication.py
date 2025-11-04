from sqlalchemy import String, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid
import enum

from .base import Base


class CommunicationType(str, enum.Enum):
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    NOTE = "NOTE"


class Communication(Base):
    __tablename__ = "communications"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    client_name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_type: Mapped[CommunicationType] = mapped_column(
        SQLEnum(CommunicationType),
        nullable=False
    )

    # Relationship
    opportunities: Mapped[List["Opportunity"]] = relationship(
        back_populates="communication",
        cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index('idx_communications_created_at', 'created_at'),
        Index('idx_communications_client_name', 'client_name'),
    )

    def __repr__(self):
        return f"<Communication(id={self.id}, client={self.client_name})>"

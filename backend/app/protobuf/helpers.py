"""Protobuf helper functions for serialization/deserialization"""

from app.protobuf import messages_pb2
from app.models.opportunity import OpportunityType as DBOpportunityType
from datetime import datetime
from typing import Optional


# Mapping between DB enum and Protobuf enum
OPPORTUNITY_TYPE_MAP = {
    DBOpportunityType.REAL_ESTATE: messages_pb2.REAL_ESTATE,
    DBOpportunityType.EMPLOYMENT_LAW: messages_pb2.EMPLOYMENT_LAW,
    DBOpportunityType.MERGERS_AND_ACQUISITIONS: messages_pb2.MERGERS_AND_ACQUISITIONS,
    DBOpportunityType.INTELLECTUAL_PROPERTY: messages_pb2.INTELLECTUAL_PROPERTY,
    DBOpportunityType.LITIGATION: messages_pb2.LITIGATION,
}


def create_opportunity_notification(opportunity, client_name: str) -> bytes:
    """
    Create protobuf notification message from an Opportunity model instance.

    Args:
        opportunity: Opportunity model instance
        client_name: Name of the client

    Returns:
        Serialized protobuf message as bytes
    """
    notification = messages_pb2.OpportunityNotification(
        opportunity_id=str(opportunity.id),
        title=opportunity.title,
        type=OPPORTUNITY_TYPE_MAP.get(
            opportunity.opportunity_type,
            messages_pb2.UNKNOWN
        ),
        confidence=float(opportunity.confidence),
        client_name=client_name,
        timestamp=int(datetime.utcnow().timestamp()),
        description=opportunity.description
    )
    return notification.SerializeToString()


def parse_opportunity_notification(data: bytes) -> dict:
    """
    Parse protobuf notification message from bytes.

    Args:
        data: Serialized protobuf message bytes

    Returns:
        Dictionary with notification data
    """
    notification = messages_pb2.OpportunityNotification()
    notification.ParseFromString(data)

    return {
        "opportunity_id": notification.opportunity_id,
        "title": notification.title,
        "type": messages_pb2.OpportunityType.Name(notification.type),
        "confidence": notification.confidence,
        "client_name": notification.client_name,
        "timestamp": notification.timestamp,
        "description": notification.description,
    }

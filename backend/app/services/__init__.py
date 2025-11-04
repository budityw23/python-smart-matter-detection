"""Services module for business logic"""

from app.services.ai_service import OpportunityDetector, AIServiceError
from app.services.opportunity_service import OpportunityService

__all__ = [
    "OpportunityDetector",
    "AIServiceError",
    "OpportunityService",
]

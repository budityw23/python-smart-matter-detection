import strawberry
from datetime import datetime, timezone

from app.api.graphql.types import (
    CreateCommunicationInput,
    CreateCommunicationPayload,
    Communication as GQLCommunication,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_communication(
        self,
        info,
        input: CreateCommunicationInput
    ) -> CreateCommunicationPayload:
        """Create communication and analyze for opportunities"""

        # TODO: Implement in Step 3
        # For now, return stub response

        return CreateCommunicationPayload(
            communication=GQLCommunication(
                id="stub-id",
                content=input.content,
                client_name=input.client_name,
                source_type=input.source_type,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            opportunities=[]
        )

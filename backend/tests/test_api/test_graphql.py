import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "smart-matter-detector"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.asyncio
async def test_opportunity_stats_empty_database(client: AsyncClient):
    """Test opportunityStats query with empty database"""
    query = """
        query {
            opportunityStats {
                totalCount
                highConfidenceCount
                byType {
                    type
                    count
                }
            }
        }
    """

    response = await client.post(
        "/graphql",
        json={"query": query}
    )

    assert response.status_code == 200
    data = response.json()

    # Should not have errors
    assert "errors" not in data or data["errors"] is None

    # Check the data
    stats = data["data"]["opportunityStats"]
    assert stats["totalCount"] == 0
    assert stats["highConfidenceCount"] == 0
    assert stats["byType"] == []


@pytest.mark.asyncio
async def test_opportunities_query_empty_database(client: AsyncClient):
    """Test opportunities query with empty database"""
    query = """
        query {
            opportunities {
                edges {
                    node {
                        id
                        title
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    hasPreviousPage
                }
                totalCount
            }
        }
    """

    response = await client.post(
        "/graphql",
        json={"query": query}
    )

    assert response.status_code == 200
    data = response.json()

    # Should not have errors
    assert "errors" not in data or data["errors"] is None

    # Check the data
    opportunities = data["data"]["opportunities"]
    assert opportunities["totalCount"] == 0
    assert opportunities["edges"] == []
    assert opportunities["pageInfo"]["hasNextPage"] is False
    assert opportunities["pageInfo"]["hasPreviousPage"] is False


@pytest.mark.asyncio
async def test_opportunity_query_not_found(client: AsyncClient):
    """Test opportunity query for non-existent ID"""
    query = """
        query {
            opportunity(id: "00000000-0000-0000-0000-000000000000") {
                id
                title
            }
        }
    """

    response = await client.post(
        "/graphql",
        json={"query": query}
    )

    assert response.status_code == 200
    data = response.json()

    # Should return null for non-existent opportunity
    assert data["data"]["opportunity"] is None


@pytest.mark.asyncio
async def test_create_communication_mutation_stub(client: AsyncClient):
    """Test createCommunication mutation (stub implementation)"""
    mutation = """
        mutation {
            createCommunication(input: {
                content: "This is a test communication with more than 50 characters to meet the minimum requirement"
                clientName: "Test Client"
                sourceType: EMAIL
            }) {
                communication {
                    id
                    content
                    clientName
                    sourceType
                }
                opportunities {
                    id
                }
            }
        }
    """

    response = await client.post(
        "/graphql",
        json={"query": mutation}
    )

    assert response.status_code == 200
    data = response.json()

    # Should not have errors
    assert "errors" not in data or data["errors"] is None

    # Check stub response
    result = data["data"]["createCommunication"]
    assert result["communication"]["id"] == "stub-id"
    assert result["communication"]["clientName"] == "Test Client"
    assert result["communication"]["sourceType"] == "EMAIL"
    assert result["opportunities"] == []

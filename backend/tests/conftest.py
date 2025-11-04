import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient

from app.main import app
from app.models.base import Base
from app.utils.database import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://nexl:nexl123@localhost:5432/nexl_opportunities_test"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

# Create test session factory
test_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with test_session_maker() as session:
        yield session

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with overridden database dependency."""
    from fastapi import FastAPI
    from strawberry.fastapi import GraphQLRouter
    from app.api.graphql.schema import schema

    # Create a test app with test database session
    test_app = FastAPI()

    async def get_test_context():
        return {"db": db_session}

    graphql_router = GraphQLRouter(schema, context_getter=get_test_context)
    test_app.include_router(graphql_router, prefix="/graphql")

    # Add health endpoint
    @test_app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "smart-matter-detector"}

    @test_app.get("/")
    async def root():
        return {"message": "Smart Matter Opportunity Detector API"}

    async with AsyncClient(app=test_app, base_url="http://test") as test_client:
        yield test_client

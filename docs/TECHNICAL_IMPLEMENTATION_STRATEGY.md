# Technical Implementation Strategy
## Smart Matter Opportunity Detector - 3-Day Implementation Guide

**Version:** 1.0  
**Last Updated:** November 4, 2025  
**Target:** Claude Code Agent Implementation

---

## Overview

This document provides a **step-by-step implementation strategy** for building the Smart Matter Opportunity Detector in 3 days. Each section includes specific tasks, code examples, decision points, and troubleshooting tips.

---

## Pre-Implementation Setup (30 minutes)

### Environment Preparation

**Step 1: Create Project Structure**
```bash
mkdir smart-matter-detector
cd smart-matter-detector

# Create main directories
mkdir -p backend/app/{api/graphql,models,services,websocket,protobuf,utils}
mkdir -p backend/tests/{test_api,test_services,test_models}
mkdir -p backend/alembic/versions
mkdir -p frontend/src/{components,graphql,hooks,lib,stores,types}
mkdir -p frontend/src/components/ui
```

**Step 2: Initialize Git Repository**
```bash
git init
echo "venv/" > .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
git add .
git commit -m "Initial project structure"
```

**Step 3: Create Environment Files**
```bash
# Backend .env
cat > backend/.env << EOF
DATABASE_URL=postgresql://nexl:nexl123@localhost:5432/nexl_opportunities
OPENAI_API_KEY=your_openai_key_here
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
EOF

# Frontend .env
cat > frontend/.env << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
EOF
```

---

## DAY 1: Backend Foundation (8 hours)

### Goal
Build working GraphQL API with database operations and basic CRUD.

---

### Phase 1.1: Database Setup (90 minutes)

**Task 1: Setup PostgreSQL with Docker**
```yaml
# docker-compose.yml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: nexl_opportunities
      POSTGRES_USER: nexl
      POSTGRES_PASSWORD: nexl123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nexl"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Task 2: Install Dependencies**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.13.0
strawberry-graphql[fastapi]==0.215.1
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
openai==1.3.7
protobuf==4.25.1
websockets==12.0
tenacity==8.2.3
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
EOF

pip install -r requirements.txt
```

**Task 3: Create Database Models**
```python
# backend/app/models/base.py
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    """Base model with common fields"""
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
```

```python
# backend/app/models/communication.py
from sqlalchemy import String, Text, Enum as SQLEnum
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
    
    def __repr__(self):
        return f"<Communication(id={self.id}, client={self.client_name})>"
```

```python
# backend/app/models/opportunity.py
from sqlalchemy import String, Text, Numeric, ForeignKey, Enum as SQLEnum
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
    estimated_value: Mapped[str] = mapped_column(String(50), nullable=True)
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
    
    def __repr__(self):
        return f"<Opportunity(id={self.id}, type={self.opportunity_type})>"
```

**Task 4: Setup Database Connection**
```python
# backend/app/utils/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database sessions"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    from app.models.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

**Task 5: Create Alembic Migration**
```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini - update sqlalchemy.url
# sqlalchemy.url = postgresql://nexl:nexl123@localhost:5432/nexl_opportunities

# Edit alembic/env.py
```

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Import your models
from app.models.base import Base
from app.models.communication import Communication
from app.models.opportunity import Opportunity

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    from sqlalchemy.ext.asyncio import create_async_engine
    
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Run migration
alembic upgrade head
```

**✅ Checkpoint:** Database tables created successfully

---

### Phase 1.2: GraphQL API Setup (120 minutes)

**Task 1: Create GraphQL Types**
```python
# backend/app/api/graphql/types.py
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
```

**Task 2: Create Query Resolvers**
```python
# backend/app/api/graphql/queries.py
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
)
from app.models.opportunity import Opportunity, OpportunityType
from app.models.communication import Communication
from app.utils.database import get_db

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
        status=opp.status,
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
```

**Task 3: Create Mutation Resolvers (Stub)**
```python
# backend/app/api/graphql/mutations.py
import strawberry
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
        
        # TODO: Implement in Day 2
        # For now, return stub response
        
        return CreateCommunicationPayload(
            communication=GQLCommunication(
                id="stub-id",
                content=input.content,
                client_name=input.client_name,
                source_type=input.source_type,
                created_at="2025-01-01T00:00:00",
                updated_at="2025-01-01T00:00:00",
            ),
            opportunities=[]
        )
```

**Task 4: Create GraphQL Schema**
```python
# backend/app/api/graphql/schema.py
import strawberry
from app.api.graphql.queries import Query
from app.api.graphql.mutations import Mutation

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
```

**Task 5: Setup FastAPI Application**
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from app.api.graphql.schema import schema
from app.utils.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting up...")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="Smart Matter Opportunity Detector",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL endpoint
async def get_context():
    """Provide context to GraphQL resolvers"""
    async for db in get_db():
        yield {"db": db}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smart-matter-detector"
    }

@app.get("/")
async def root():
    return {"message": "Smart Matter Opportunity Detector API"}
```

**Task 6: Test GraphQL API**
```bash
# Start the server
uvicorn app.main:app --reload

# Visit http://localhost:8000/graphql
# Try this query:
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
```

**✅ Checkpoint:** GraphQL API running and responding

---

### Phase 1.3: Basic Testing Setup (60 minutes)

**Task 1: Create Test Configuration**
```python
# backend/tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.main import app
from app.models.base import Base
from app.utils.database import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://nexl:nexl123@localhost:5432/nexl_test"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def test_db():
    """Create test database"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def client(test_db):
    """Create test client"""
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
```

**Task 2: Create Sample Tests**
```python
# backend/tests/test_api/test_graphql.py
import pytest

@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_opportunity_stats_query(client):
    """Test opportunity stats query"""
    query = """
        query {
            opportunityStats {
                totalCount
                highConfidenceCount
            }
        }
    """
    
    response = await client.post(
        "/graphql",
        json={"query": query}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "opportunityStats" in data["data"]
    assert data["data"]["opportunityStats"]["totalCount"] == 0
```

**Task 3: Run Tests**
```bash
pytest -v
```

**✅ Checkpoint:** Tests passing

---

### Day 1 Review & Git Commit

```bash
# Test everything works
uvicorn app.main:app --reload
# Visit http://localhost:8000/graphql and test queries

# Run tests
pytest -v

# Commit Day 1 work
git add .
git commit -m "Day 1: Database, GraphQL API, and basic testing setup"
```

**Day 1 Deliverables:**
✅ PostgreSQL database with migrations  
✅ SQLAlchemy models for Communication and Opportunity  
✅ Working GraphQL API with queries  
✅ Health check endpoint  
✅ Test framework setup  
✅ Docker Compose configuration  

---

## DAY 2: AI Integration & WebSocket (8 hours)

### Goal
Implement OpenAI integration, opportunity detection logic, Protobuf messages, and WebSocket notifications.

---

### Phase 2.1: Protobuf Setup (45 minutes)

**Task 1: Create Protobuf Definitions**
```protobuf
// backend/app/protobuf/messages.proto
syntax = "proto3";

package nexl.opportunities;

// Opportunity notification message
message OpportunityNotification {
  string opportunity_id = 1;
  string title = 2;
  OpportunityType type = 3;
  float confidence = 4;
  string client_name = 5;
  int64 timestamp = 6;
  string description = 7;
}

enum OpportunityType {
  UNKNOWN = 0;
  REAL_ESTATE = 1;
  EMPLOYMENT_LAW = 2;
  MERGERS_AND_ACQUISITIONS = 3;
  INTELLECTUAL_PROPERTY = 4;
  LITIGATION = 5;
}

// Analysis request message
message AnalysisRequest {
  string communication_id = 1;
  string content = 2;
  string client_name = 3;
}

// Analysis response message
message AnalysisResponse {
  string communication_id = 1;
  repeated ExtractedOpportunity opportunities = 2;
  bool success = 3;
  string error_message = 4;
}

message ExtractedOpportunity {
  string title = 1;
  string description = 2;
  OpportunityType type = 3;
  float confidence = 4;
  string extracted_text = 5;
  string estimated_value = 6;
}
```

**Task 2: Generate Python Code**
```bash
cd backend
pip install grpcio-tools

# Generate Python files from proto
python -m grpc_tools.protoc \
    -I./app/protobuf \
    --python_out=./app/protobuf \
    ./app/protobuf/messages.proto

# This creates: messages_pb2.py
```

**Task 3: Create Protobuf Helper**
```python
# backend/app/protobuf/helpers.py
from app.protobuf import messages_pb2
from app.models.opportunity import OpportunityType as DBOpportunityType
from datetime import datetime

# Mapping between DB enum and Protobuf enum
OPPORTUNITY_TYPE_MAP = {
    DBOpportunityType.REAL_ESTATE: messages_pb2.REAL_ESTATE,
    DBOpportunityType.EMPLOYMENT_LAW: messages_pb2.EMPLOYMENT_LAW,
    DBOpportunityType.MERGERS_AND_ACQUISITIONS: messages_pb2.MERGERS_AND_ACQUISITIONS,
    DBOpportunityType.INTELLECTUAL_PROPERTY: messages_pb2.INTELLECTUAL_PROPERTY,
    DBOpportunityType.LITIGATION: messages_pb2.LITIGATION,
}

def create_opportunity_notification(opportunity, client_name: str) -> bytes:
    """Create protobuf notification message"""
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
    """Parse protobuf notification message"""
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
```

**✅ Checkpoint:** Protobuf messages defined and working

---

### Phase 2.2: OpenAI Integration (120 minutes)

**Task 1: Create AI Service**
```python
# backend/app/services/ai_service.py
from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

class OpportunityDetector:
    """Service for detecting opportunities using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"
    
    def _get_system_prompt(self) -> str:
        """System prompt for OpenAI"""
        return """You are an AI assistant for a law firm that identifies business opportunities in client communications.

Your task is to analyze communications and extract potential legal service opportunities.

Focus on these practice areas:
1. Real Estate (office leases, property transactions, zoning)
2. Employment Law (hiring, terminations, HR issues, contracts)
3. Mergers & Acquisitions (acquisitions, sales, due diligence)
4. Intellectual Property (trademarks, patents, copyright)
5. Litigation (lawsuits, disputes, arbitration)

For each opportunity:
- Be specific about what the client needs
- Base confidence on clarity and urgency
- Extract the exact text that indicates the need
- Estimate value if enough information is provided

Return ONLY valid JSON, no additional text."""
    
    def _build_prompt(self, content: str, client_name: str) -> str:
        """Build user prompt"""
        return f"""Client: {client_name}

Communication:
{content}

Analyze this communication and identify any legal service opportunities.

Return a JSON object with this exact structure:
{{
  "opportunities": [
    {{
      "title": "Brief title (max 60 chars)",
      "description": "What the client needs",
      "type": "real_estate|employment_law|m&a|ip|litigation",
      "confidence": 85,
      "extracted_text": "Exact quote from communication",
      "estimated_value": "$20k-50k" (optional, only if you can estimate)
    }}
  ]
}}

Rules:
- Only include opportunities with confidence >= 40%
- Maximum 5 opportunities per communication
- Be conservative with confidence scores
- If no opportunities found, return empty array
"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def analyze_communication(
        self,
        content: str,
        client_name: str
    ) -> List[Dict]:
        """
        Analyze communication and extract opportunities.
        
        Returns:
            List of opportunity dicts with keys:
            - title, description, type, confidence, extracted_text, estimated_value
        """
        try:
            logger.info(f"Analyzing communication for client: {client_name}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._build_prompt(content, client_name)}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )
            
            result_text = response.choices[0].message.content
            logger.debug(f"OpenAI response: {result_text}")
            
            result = json.loads(result_text)
            opportunities = result.get("opportunities", [])
            
            # Validate and clean opportunities
            validated = self._validate_opportunities(opportunities)
            
            logger.info(f"Found {len(validated)} opportunities")
            return validated
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            raise AIServiceError("Failed to parse AI response")
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceError(f"AI service error: {str(e)}")
    
    def _validate_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Validate and normalize opportunity data"""
        validated = []
        
        valid_types = {"real_estate", "employment_law", "m&a", "ip", "litigation"}
        
        for opp in opportunities:
            try:
                # Normalize type
                opp_type = opp.get("type", "").lower().replace("&", "").replace(" ", "_")
                if opp_type == "ma":
                    opp_type = "m&a"
                
                if opp_type not in valid_types:
                    logger.warning(f"Invalid opportunity type: {opp.get('type')}")
                    continue
                
                # Validate confidence
                confidence = float(opp.get("confidence", 0))
                if confidence < 40 or confidence > 100:
                    logger.warning(f"Invalid confidence: {confidence}")
                    continue
                
                # Validate required fields
                if not opp.get("title") or not opp.get("description"):
                    logger.warning("Missing required fields")
                    continue
                
                # Normalize and validate
                validated_opp = {
                    "title": opp["title"][:200],  # Truncate to max length
                    "description": opp["description"],
                    "type": opp_type,
                    "confidence": confidence,
                    "extracted_text": opp.get("extracted_text", opp["description"]),
                    "estimated_value": opp.get("estimated_value"),
                }
                
                validated.append(validated_opp)
                
            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid opportunity data: {e}")
                continue
        
        return validated
```

**Task 2: Create Opportunity Service**
```python
# backend/app/services/opportunity_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
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
    ) -> bytes:
        """Create protobuf notification message"""
        return create_opportunity_notification(opportunity, client_name)
```

**Task 3: Update Mutation Resolver**
```python
# backend/app/api/graphql/mutations.py
import strawberry
from typing import List
import logging

from app.api.graphql.types import (
    CreateCommunicationInput,
    CreateCommunicationPayload,
    Communication as GQLCommunication,
    Opportunity as GQLOpportunity,
    OpportunityType as GQLOpportunityType,
)
from app.models.communication import CommunicationType
from app.services.ai_service import OpportunityDetector
from app.services.opportunity_service import OpportunityService

logger = logging.getLogger(__name__)

async def convert_communication_to_gql(comm) -> GQLCommunication:
    """Convert Communication model to GraphQL type"""
    from app.api.graphql.types import CommunicationType as GQLCommType
    
    return GQLCommunication(
        id=str(comm.id),
        content=comm.content,
        client_name=comm.client_name,
        source_type=GQLCommType[comm.source_type.value],
        created_at=comm.created_at,
        updated_at=comm.updated_at,
    )

async def convert_opportunity_to_gql(opp) -> GQLOpportunity:
    """Convert Opportunity model to GraphQL type"""
    return GQLOpportunity(
        id=str(opp.id),
        title=opp.title,
        description=opp.description,
        opportunity_type=GQLOpportunityType[opp.opportunity_type.value],
        confidence=float(opp.confidence),
        estimated_value=opp.estimated_value,
        extracted_text=opp.extracted_text,
        status=opp.status,
        detected_at=opp.detected_at,
        created_at=opp.created_at,
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
        db = info.context["db"]
        
        # Validate input
        if len(input.content) < 50:
            raise ValueError("Content must be at least 50 characters")
        
        if len(input.content) > 10000:
            raise ValueError("Content must not exceed 10,000 characters")
        
        # Map GraphQL enum to DB enum
        from app.api.graphql.types import CommunicationType as GQLCommType
        source_type_map = {
            GQLCommType.EMAIL: CommunicationType.EMAIL,
            GQLCommType.MEETING: CommunicationType.MEETING,
            GQLCommType.NOTE: CommunicationType.NOTE,
        }
        
        try:
            # Initialize services
            ai_detector = OpportunityDetector()
            opp_service = OpportunityService(db, ai_detector)
            
            # Create communication and opportunities
            communication, opportunities = await opp_service.create_communication_with_opportunities(
                content=input.content,
                client_name=input.client_name,
                source_type=source_type_map[input.source_type]
            )
            
            # Send WebSocket notifications for high-value opportunities
            websocket_manager = info.context.get("websocket_manager")
            if websocket_manager:
                for opp in opportunities:
                    if opp_service.should_notify(opp):
                        notification = opp_service.create_notification_message(
                            opp,
                            communication.client_name
                        )
                        await websocket_manager.broadcast(notification)
            
            # Convert to GraphQL types
            gql_communication = await convert_communication_to_gql(communication)
            gql_opportunities = [
                await convert_opportunity_to_gql(opp) for opp in opportunities
            ]
            
            return CreateCommunicationPayload(
                communication=gql_communication,
                opportunities=gql_opportunities
            )
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating communication: {e}")
            raise ValueError(f"Failed to create communication: {str(e)}")
```

**✅ Checkpoint:** OpenAI integration working, can create communications with opportunities

---

### Phase 2.3: WebSocket Implementation (90 minutes)

**Task 1: Create WebSocket Manager**
```python
# backend/app/websocket/manager.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept and register new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: bytes):
        """
        Broadcast protobuf message to all connected clients.
        
        Args:
            message: Serialized protobuf message
        """
        disconnected = set()
        
        for connection in self.active_connections.copy():
            try:
                await connection.send_bytes(message)
                logger.debug(f"Sent notification to client")
            except WebSocketDisconnect:
                disconnected.add(connection)
                logger.warning("Client disconnected during broadcast")
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_to_client(self, websocket: WebSocket, message: bytes):
        """Send message to specific client"""
        try:
            await websocket.send_bytes(message)
        except Exception as e:
            logger.error(f"Error sending to specific client: {e}")
            self.disconnect(websocket)

# Global connection manager instance
manager = ConnectionManager()
```

**Task 2: Add WebSocket Endpoint to FastAPI**
```python
# Update backend/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
import logging

from app.api.graphql.schema import schema
from app.utils.database import get_db
from app.websocket.manager import manager as websocket_manager
import os
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting up Smart Matter Opportunity Detector...")
    yield
    logger.info("👋 Shutting down...")

app = FastAPI(
    title="Smart Matter Opportunity Detector",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL endpoint with WebSocket manager in context
async def get_context():
    """Provide context to GraphQL resolvers"""
    async for db in get_db():
        yield {
            "db": db,
            "websocket_manager": websocket_manager
        }

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications"""
    await websocket_manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.debug(f"Received from client: {data}")
            
            # Send ping/pong to keep connection alive
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("Client disconnected from WebSocket")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smart-matter-detector",
        "websocket_connections": len(websocket_manager.active_connections)
    }

@app.get("/")
async def root():
    return {
        "message": "Smart Matter Opportunity Detector API",
        "version": "1.0.0"
    }
```

**✅ Checkpoint:** WebSocket endpoint working, can connect from clients

---

### Phase 2.4: Integration Testing (60 minutes)

**Task 1: Create Integration Tests**
```python
# backend/tests/test_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_communication_with_ai_analysis(client, test_db):
    """Test complete flow: create communication → AI analysis → opportunities"""
    
    mutation = """
        mutation CreateComm($input: CreateCommunicationInput!) {
            createCommunication(input: $input) {
                communication {
                    id
                    clientName
                    content
                }
                opportunities {
                    id
                    title
                    opportunityType
                    confidence
                }
            }
        }
    """
    
    variables = {
        "input": {
            "content": """Hi team, 
            
We're really happy with the trademark work you did last quarter. 
Quick update: we're opening a new office in Chicago next month 
and will need to sign a commercial lease. Also, we're planning 
to hire about 20 new employees, so we'll need help with 
employment contracts. Let me know if you can help!

Best,
John Smith
CEO, Acme Corp""",
            "clientName": "Acme Corp",
            "sourceType": "EMAIL"
        }
    }
    
    response = await client.post(
        "/graphql",
        json={"query": mutation, "variables": variables}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check communication created
    assert "data" in data
    comm = data["data"]["createCommunication"]["communication"]
    assert comm["clientName"] == "Acme Corp"
    
    # Check opportunities extracted
    opportunities = data["data"]["createCommunication"]["opportunities"]
    assert len(opportunities) >= 1  # Should find at least real estate opportunity
    
    # Check opportunity details
    opp_types = [opp["opportunityType"] for opp in opportunities]
    assert "REAL_ESTATE" in opp_types or "EMPLOYMENT_LAW" in opp_types
    
    # Check confidence scores are reasonable
    for opp in opportunities:
        assert 40 <= opp["confidence"] <= 100

@pytest.mark.asyncio
async def test_query_opportunities_with_filters(client, test_db):
    """Test querying opportunities with filters"""
    
    # First create a communication
    create_mutation = """
        mutation {
            createCommunication(input: {
                content: "We need help with a real estate transaction for our new office space in downtown. This is urgent - we need to close by end of month."
                clientName: "Test Client"
                sourceType: EMAIL
            }) {
                communication { id }
                opportunities { id }
            }
        }
    """
    
    await client.post("/graphql", json={"query": create_mutation})
    
    # Query opportunities
    query = """
        query {
            opportunities(minConfidence: 70, limit: 10) {
                edges {
                    node {
                        id
                        title
                        confidence
                    }
                }
                totalCount
            }
        }
    """
    
    response = await client.post("/graphql", json={"query": query})
    data = response.json()
    
    assert "data" in data
    assert "opportunities" in data["data"]
```

**Task 2: Manual Testing Script**
```python
# backend/manual_test.py
"""
Manual testing script for AI integration
Run with: python manual_test.py
"""
import asyncio
from app.services.ai_service import OpportunityDetector

async def test_ai_service():
    detector = OpportunityDetector()
    
    test_cases = [
        {
            "content": "We're opening a NYC office next quarter and need lease help.",
            "client": "Tech Startup Inc"
        },
        {
            "content": "Thinking about acquiring our competitor. Need due diligence support.",
            "client": "BigCorp"
        },
        {
            "content": "Just wanted to say thanks for the great work on our trademark!",
            "client": "Happy Client"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {test['client']}")
        print(f"{'='*60}")
        print(f"Content: {test['content']}\n")
        
        try:
            opportunities = await detector.analyze_communication(
                content=test['content'],
                client_name=test['client']
            )
            
            if opportunities:
                print(f"Found {len(opportunities)} opportunities:")
                for opp in opportunities:
                    print(f"\n  - {opp['title']}")
                    print(f"    Type: {opp['type']}")
                    print(f"    Confidence: {opp['confidence']}%")
                    print(f"    Description: {opp['description']}")
            else:
                print("No opportunities found.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_service())
```

**Run Manual Test:**
```bash
python backend/manual_test.py
```

**✅ Checkpoint:** Full backend integration working - can create communications, analyze with AI, store opportunities, send WebSocket notifications

---

### Day 2 Review & Git Commit

```bash
# Test everything
pytest -v

# Test WebSocket
# Open http://localhost:8000/graphql
# Run a createCommunication mutation
# Check server logs for "Sent notification to client"

# Commit Day 2 work
git add .
git commit -m "Day 2: AI integration, Protobuf, and WebSocket notifications"
```

**Day 2 Deliverables:**
✅ Protobuf message definitions  
✅ OpenAI integration with retry logic  
✅ Opportunity detection service  
✅ Complete createCommunication mutation  
✅ WebSocket server with notifications  
✅ Integration tests  

---

## DAY 3: Frontend & Polish (8 hours)

### Goal
Build React frontend with real-time updates, connect to backend, add final polish.

---

### Phase 3.1: Frontend Setup (45 minutes)

**Task 1: Initialize React + Vite Project**
```bash
cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

**Task 2: Install Dependencies**
```bash
npm install @apollo/client graphql
npm install @tanstack/react-query
npm install zustand
npm install date-fns
npm install protobufjs

# shadcn/ui setup
npx shadcn-ui@latest init

# Install specific components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add select
npx shadcn-ui@latest add slider
npx shadcn-ui@latest add label
npx shadcn-ui@latest add skeleton
```

**Task 2.5: Design System Guidelines**

Follow these design system rules for all components:

**Component Standards:**
- ✅ Use ONLY shadcn/ui components (no custom component libraries)
- ✅ Import pattern: `import { Component } from '@/components/ui/component'`
- ✅ Compose complex UIs from shadcn primitives

**Styling Rules:**
- ✅ Use ONLY Tailwind utility classes (no custom CSS)
- ✅ Consistent spacing:
  - Card padding: `p-6`
  - Section gaps: `gap-4` or `gap-6`
  - Form fields: `space-y-4`
- ✅ Typography:
  - Labels: `text-sm font-medium`
  - Body: `text-base`
  - Headings: `text-lg font-semibold`, `text-xl font-bold`, `text-3xl font-bold`

**Theme Colors:**
- ✅ Use CSS variables ONLY (never hardcoded colors):
  - Backgrounds: `bg-background`, `bg-card`, `bg-muted`
  - Text: `text-foreground`, `text-muted-foreground`
  - Accents: `bg-primary`, `bg-secondary`, `bg-accent`, `bg-destructive`
  - Borders: `border-border`, `border-input`
- ✅ Support dark mode with `dark:` variants

**Layout Patterns:**
- ✅ Mobile-first: Default → `md:` → `lg:` → `xl:`
- ✅ Container: `max-w-7xl mx-auto px-4`
- ✅ Grids: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- ✅ Flex: `flex items-center justify-between gap-4`

**UI/UX:**
- ✅ Border radius: `rounded-lg` (cards), `rounded-md` (inputs)
- ✅ Hover states: `hover:bg-accent`, `hover:opacity-80`
- ✅ Transitions: `transition-colors duration-200`
- ✅ Loading: Use `Skeleton` components
- ✅ Errors: Use `destructive` variant

**Task 3: Configure TypeScript**
```typescript
// frontend/src/types/index.ts
export enum CommunicationType {
  EMAIL = "EMAIL",
  MEETING = "MEETING",
  NOTE = "NOTE",
}

export enum OpportunityType {
  REAL_ESTATE = "REAL_ESTATE",
  EMPLOYMENT_LAW = "EMPLOYMENT_LAW",
  MERGERS_AND_ACQUISITIONS = "MERGERS_AND_ACQUISITIONS",
  INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY",
  LITIGATION = "LITIGATION",
}

export enum OpportunityStatus {
  NEW = "NEW",
  REVIEWING = "REVIEWING",
  CONTACTED = "CONTACTED",
  CLOSED = "CLOSED",
  ARCHIVED = "ARCHIVED",
}

export interface Opportunity {
  id: string;
  title: string;
  description: string;
  opportunityType: OpportunityType;
  confidence: number;
  estimatedValue?: string;
  extractedText: string;
  status: OpportunityStatus;
  detectedAt: string;
  createdAt: string;
}

export interface Communication {
  id: string;
  content: string;
  clientName: string;
  sourceType: CommunicationType;
  createdAt: string;
  updatedAt: string;
}
```

**✅ Checkpoint:** Frontend project initialized

---

### Phase 3.2: Apollo Client & GraphQL Setup (45 minutes)

**Task 1: Setup Apollo Client**
```typescript
// frontend/src/graphql/client.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';

const httpLink = createHttpLink({
  uri: import.meta.env.VITE_API_URL + '/graphql',
});

export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'network-only',
    },
  },
});
```

**Task 2: Define GraphQL Operations**
```typescript
// frontend/src/graphql/queries.ts
import { gql } from '@apollo/client';

export const GET_OPPORTUNITIES = gql`
  query GetOpportunities(
    $minConfidence: Float
    $type: OpportunityType
    $limit: Int
    $offset: Int
  ) {
    opportunities(
      minConfidence: $minConfidence
      type: $type
      limit: $limit
      offset: $offset
    ) {
      edges {
        node {
          id
          title
          description
          opportunityType
          confidence
          estimatedValue
          extractedText
          status
          detectedAt
          createdAt
        }
      }
      totalCount
      pageInfo {
        hasNextPage
        hasPreviousPage
      }
    }
  }
`;

export const GET_OPPORTUNITY_STATS = gql`
  query GetOpportunityStats {
    opportunityStats {
      totalCount
      highConfidenceCount
      byType {
        type
        count
      }
    }
  }
`;
```

```typescript
// frontend/src/graphql/mutations.ts
import { gql } from '@apollo/client';

export const CREATE_COMMUNICATION = gql`
  mutation CreateCommunication($input: CreateCommunicationInput!) {
    createCommunication(input: $input) {
      communication {
        id
        clientName
        content
        sourceType
        createdAt
      }
      opportunities {
        id
        title
        description
        opportunityType
        confidence
        estimatedValue
        extractedText
        detectedAt
      }
    }
  }
`;
```

**✅ Checkpoint:** GraphQL client configured

---

### Phase 3.3: WebSocket Integration (60 minutes)

**Task 1: Copy Protobuf Definition**
```bash
# Copy .proto file from backend
cp ../backend/app/protobuf/messages.proto src/lib/
```

**Task 2: Setup Protobuf**
```bash
# Install protobuf compiler
npm install -g protobufjs-cli

# Generate JavaScript from .proto
pbjs -t static-module -w es6 -o src/lib/messages.js src/lib/messages.proto
pbts -o src/lib/messages.d.ts src/lib/messages.js
```

**Task 3: Create WebSocket Hook**
```typescript
// frontend/src/hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';
import { messages } from '@/lib/messages';

export interface OpportunityNotification {
  opportunityId: string;
  title: string;
  type: string;
  confidence: number;
  clientName: string;
  timestamp: number;
  description: string;
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastNotification, setLastNotification] = useState<OpportunityNotification | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const connect = () => {
    try {
      const ws = new WebSocket(url);
      
      ws.binaryType = 'arraybuffer';
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        
        // Send ping every 30 seconds to keep connection alive
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 30000);
        
        wsRef.current = ws;
      };
      
      ws.onmessage = (event) => {
        try {
          // Decode protobuf message
          const buffer = new Uint8Array(event.data);
          const notification = messages.nexl.opportunities.OpportunityNotification.decode(buffer);
          
          const parsed: OpportunityNotification = {
            opportunityId: notification.opportunityId,
            title: notification.title,
            type: messages.nexl.opportunities.OpportunityType[notification.type],
            confidence: notification.confidence,
            clientName: notification.clientName,
            timestamp: notification.timestamp.toNumber(),
            description: notification.description,
          };
          
          console.log('Received notification:', parsed);
          setLastNotification(parsed);
          
        } catch (error) {
          console.error('Error decoding notification:', error);
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        wsRef.current = null;
        
        // Reconnect after 5 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Reconnecting...');
          connect();
        }, 5000);
      };
      
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  };

  useEffect(() => {
    connect();
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [url]);

  return { isConnected, lastNotification };
}
```

**✅ Checkpoint:** WebSocket integration ready

---

### Phase 3.4: Build UI Components (180 minutes)

This is the most time-consuming phase. Focus on core components.

**Task 1: OpportunityCard Component**
```typescript
// frontend/src/components/OpportunityCard.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Opportunity, OpportunityType } from '@/types';
import { formatDistanceToNow } from 'date-fns';

// ✅ Design System: Use semantic color combinations with theme-aware variants
const typeColors: Record<OpportunityType, string> = {
  [OpportunityType.REAL_ESTATE]: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  [OpportunityType.EMPLOYMENT_LAW]: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  [OpportunityType.MERGERS_AND_ACQUISITIONS]: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  [OpportunityType.INTELLECTUAL_PROPERTY]: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  [OpportunityType.LITIGATION]: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
};

const confidenceColor = (confidence: number): string => {
  if (confidence >= 80) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
  if (confidence >= 60) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
  return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
};

interface OpportunityCardProps {
  opportunity: Opportunity;
  onClick?: () => void;
}

export function OpportunityCard({ opportunity, onClick }: OpportunityCardProps) {
  return (
    <Card
      className="cursor-pointer hover:shadow-lg transition-colors duration-200"
      onClick={onClick}
    >
      <CardHeader className="space-y-2">
        <div className="flex justify-between items-start gap-4">
          <CardTitle className="text-lg font-semibold">{opportunity.title}</CardTitle>
          <Badge className={confidenceColor(opportunity.confidence)}>
            {opportunity.confidence}% confidence
          </Badge>
        </div>
        <div className="flex gap-2 flex-wrap">
          <Badge className={typeColors[opportunity.opportunityType]}>
            {opportunity.opportunityType.replace(/_/g, ' ')}
          </Badge>
          {opportunity.estimatedValue && (
            <Badge variant="outline">{opportunity.estimatedValue}</Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <CardDescription className="text-base">
          {opportunity.description}
        </CardDescription>
        <p className="text-sm text-muted-foreground italic border-l-2 border-border pl-4">
          "{opportunity.extractedText.substring(0, 100)}..."
        </p>
        <p className="text-xs text-muted-foreground">
          {formatDistanceToNow(new Date(opportunity.detectedAt), { addSuffix: true })}
        </p>
      </CardContent>
    </Card>
  );
}
```

**Design System Notes for OpportunityCard:**
- ✅ Uses shadcn `Card` component with proper structure
- ✅ Spacing: `space-y-2` in header, `space-y-4` in content, `gap-4` for flex items
- ✅ Typography: `text-lg font-semibold` for title, `text-base` for description
- ✅ Theme colors: `text-muted-foreground`, `border-border`
- ✅ Dark mode: All color variants include `dark:` classes
- ✅ Transitions: `transition-colors duration-200` for smooth hover
- ✅ Border radius: Uses default shadcn `rounded-lg` from Card component

**Task 2: UploadModal Component**
```typescript
// frontend/src/components/UploadModal.tsx
import { useState } from 'react';
import { useMutation } from '@apollo/client';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { CREATE_COMMUNICATION } from '@/graphql/mutations';
import { CommunicationType } from '@/types';
import { toast } from '@/components/ui/use-toast';

interface UploadModalProps {
  onSuccess?: () => void;
}

export function UploadModal({ onSuccess }: UploadModalProps) {
  const [open, setOpen] = useState(false);
  const [content, setContent] = useState('');
  const [clientName, setClientName] = useState('');
  const [sourceType, setSourceType] = useState<CommunicationType>(CommunicationType.EMAIL);

  const [createCommunication, { loading }] = useMutation(CREATE_COMMUNICATION, {
    onCompleted: (data) => {
      const oppCount = data.createCommunication.opportunities.length;
      toast({
        title: 'Success!',
        description: `Found ${oppCount} ${oppCount === 1 ? 'opportunity' : 'opportunities'}`,
      });
      setOpen(false);
      resetForm();
      onSuccess?.();
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive',
      });
    },
  });

  const resetForm = () => {
    setContent('');
    setClientName('');
    setSourceType(CommunicationType.EMAIL);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (content.length < 50) {
      toast({
        title: 'Validation Error',
        description: 'Content must be at least 50 characters',
        variant: 'destructive',
      });
      return;
    }

    await createCommunication({
      variables: {
        input: {
          content,
          clientName,
          sourceType,
        },
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="lg">Upload Communication</Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Upload Client Communication</DialogTitle>
          <DialogDescription>
            Paste an email, meeting notes, or other communication to analyze for opportunities.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="clientName">Client Name</Label>
            <Input
              id="clientName"
              value={clientName}
              onChange={(e) => setClientName(e.target.value)}
              placeholder="Acme Corp"
              required
            />
          </div>
          
          <div>
            <Label htmlFor="sourceType">Source Type</Label>
            <Select
              value={sourceType}
              onValueChange={(value) => setSourceType(value as CommunicationType)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={CommunicationType.EMAIL}>Email</SelectItem>
                <SelectItem value={CommunicationType.MEETING}>Meeting Notes</SelectItem>
                <SelectItem value={CommunicationType.NOTE}>Note</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <Label htmlFor="content">Communication Content</Label>
            <Textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Paste the email or meeting notes here..."
              rows={10}
              required
            />
            <p className="text-sm text-muted-foreground mt-1">
              {content.length} characters (minimum 50)
            </p>
          </div>
          
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

**Task 3: Main App Component**
```typescript
// frontend/src/App.tsx
import { useQuery } from '@apollo/client';
import { useState, useEffect } from 'react';
import { OpportunityCard } from '@/components/OpportunityCard';
import { UploadModal } from '@/components/UploadModal';
import { useWebSocket } from '@/hooks/useWebSocket';
import { GET_OPPORTUNITIES, GET_OPPORTUNITY_STATS } from '@/graphql/queries';
import { toast } from '@/components/ui/use-toast';
import { Badge } from '@/components/ui/badge';

function App() {
  const [minConfidence, setMinConfidence] = useState(0);
  
  const { data, loading, refetch } = useQuery(GET_OPPORTUNITIES, {
    variables: { minConfidence, limit: 50 },
  });

  const { data: statsData } = useQuery(GET_OPPORTUNITY_STATS);

  // WebSocket integration
  const { isConnected, lastNotification } = useWebSocket(
    import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
  );

  // Show toast when new notification received
  useEffect(() => {
    if (lastNotification) {
      toast({
        title: '🎯 New Opportunity Detected!',
        description: `${lastNotification.title} (${lastNotification.confidence}% confidence)`,
      });
      refetch();
    }
  }, [lastNotification, refetch]);

  const opportunities = data?.opportunities?.edges?.map((edge: any) => edge.node) || [];

  return (
    <div className="min-h-screen bg-background">
      {/* ✅ Design System: Use theme colors, proper spacing */}
      <header className="bg-card border-b border-border">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
            <div>
              <h1 className="text-3xl font-bold text-foreground">
                Smart Matter Opportunity Detector
              </h1>
              <p className="text-muted-foreground mt-1">
                AI-powered opportunity detection for law firms
              </p>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant={isConnected ? 'default' : 'destructive'}>
                {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
              </Badge>
              <UploadModal onSuccess={() => refetch()} />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats - ✅ Design System: Responsive grid, theme colors, consistent spacing */}
        {statsData && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-card p-6 rounded-lg border border-border">
              <p className="text-sm font-medium text-muted-foreground">Total Opportunities</p>
              <p className="text-3xl font-bold text-foreground mt-2">
                {statsData.opportunityStats.totalCount}
              </p>
            </div>
            <div className="bg-card p-6 rounded-lg border border-border">
              <p className="text-sm font-medium text-muted-foreground">High Confidence</p>
              <p className="text-3xl font-bold text-foreground mt-2">
                {statsData.opportunityStats.highConfidenceCount}
              </p>
            </div>
            <div className="bg-card p-6 rounded-lg border border-border">
              <p className="text-sm font-medium text-muted-foreground">This Week</p>
              <p className="text-3xl font-bold text-foreground mt-2">
                {opportunities.filter((o: any) => {
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return new Date(o.detectedAt) > weekAgo;
                }).length}
              </p>
            </div>
          </div>
        )}

        {/* Opportunities List - ✅ Design System: Loading/empty states, responsive grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* ✅ Use Skeleton for loading states */}
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-card p-6 rounded-lg border border-border space-y-4">
                <div className="h-4 bg-muted rounded animate-pulse" />
                <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
                <div className="h-20 bg-muted rounded animate-pulse" />
              </div>
            ))}
          </div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-base">
              No opportunities yet. Upload a communication to get started!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {opportunities.map((opp: any) => (
              <OpportunityCard key={opp.id} opportunity={opp} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
```

**Design System Notes for App Component:**
- ✅ Background: `bg-background` instead of hardcoded `bg-gray-50`
- ✅ Text colors: `text-foreground`, `text-muted-foreground` instead of `text-gray-*`
- ✅ Borders: `border-border` instead of hardcoded colors
- ✅ Responsive: Mobile-first with `md:` and `lg:` breakpoints
- ✅ Container: `max-w-7xl mx-auto px-4` (design system pattern)
- ✅ Spacing: Consistent `gap-4`, `mb-8`, `py-6`, `p-6`
- ✅ Loading states: Skeleton with `animate-pulse` and `bg-muted`
- ✅ Empty state: Centered with `text-muted-foreground`

**Task 4: Wrap App with Providers**
```typescript
// frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ApolloProvider } from '@apollo/client';
import { Toaster } from '@/components/ui/toaster';
import { apolloClient } from '@/graphql/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ApolloProvider client={apolloClient}>
      <App />
      <Toaster />
    </ApolloProvider>
  </React.StrictMode>
);
```

**✅ Checkpoint:** Frontend UI complete and functional

---

### Phase 3.5: Final Polish & Testing (60 minutes)

**Task 1: Update README**
```markdown
# Smart Matter Opportunity Detector

AI-powered opportunity detection system for law firms.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- OpenAI API Key

### Setup

1. Clone repository
\`\`\`bash
git clone <repo-url>
cd smart-matter-detector
\`\`\`

2. Set up environment variables
\`\`\`bash
# Backend
cp backend/.env.example backend/.env
# Add your OpenAI API key to backend/.env

# Frontend
cp frontend/.env.example frontend/.env
\`\`\`

3. Start with Docker Compose
\`\`\`bash
docker-compose up
\`\`\`

4. Access the application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql

## Architecture

[Include architecture diagram]

## Features

✅ AI-powered opportunity detection using GPT-4  
✅ Real-time WebSocket notifications  
✅ GraphQL API  
✅ Protobuf message serialization  
✅ PostgreSQL database  
✅ React + shadcn/ui frontend  

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- PostgreSQL
- OpenAI API
- Protobuf
- WebSockets

**Frontend:**
- React 18
- TypeScript
- Vite
- Apollo Client
- shadcn/ui
- Tailwind CSS

## Development

### Backend
\`\`\`bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm run dev
\`\`\`

### Tests
\`\`\`bash
cd backend
pytest -v
\`\`\`

## License

MIT
```

**Task 2: Create Docker Compose for Full Stack**
```yaml
# docker-compose.yml (Update final version)
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: nexl_opportunities
      POSTGRES_USER: nexl
      POSTGRES_PASSWORD: nexl123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nexl"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://nexl:nexl123@db:5432/nexl_opportunities
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      CORS_ORIGINS: http://localhost:5173
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
      VITE_WS_URL: ws://localhost:8000/ws
    depends_on:
      - backend

volumes:
  postgres_data:
```

**Task 3: End-to-End Testing**
```bash
# 1. Start all services
docker-compose up

# 2. Open frontend (http://localhost:5173)

# 3. Test flow:
# - Click "Upload Communication"
# - Paste sample email
# - Submit
# - Verify opportunities appear
# - Check WebSocket notification (toast)

# 4. Test GraphQL directly (http://localhost:8000/graphql)
```

**✅ Checkpoint:** Full application working end-to-end

---

### Day 3 Final Review & Git Commit

```bash
# Final testing
npm run build  # in frontend/
pytest -v      # in backend/

# Commit Day 3 work
git add .
git commit -m "Day 3: React frontend with real-time updates, complete integration"

# Tag release
git tag v1.0.0-mvp
```

**Day 3 Deliverables:**
✅ React frontend with shadcn/ui  
✅ GraphQL client integration  
✅ WebSocket client with Protobuf  
✅ Upload modal for communications  
✅ Opportunity list with filters  
✅ Real-time toast notifications  
✅ Complete README  
✅ Docker Compose for full stack  
✅ End-to-end working demo  

---

## Post-Implementation: Demo Script

### Demo Flow (5 minutes)

**1. Introduction (30 seconds)**
"This is the Smart Matter Opportunity Detector - an AI-powered system that helps law firms find hidden revenue opportunities in client communications."

**2. Architecture Overview (1 minute)**
"The system uses:
- Python FastAPI backend with GraphQL
- OpenAI GPT-4 for text analysis
- PostgreSQL for data storage
- Protobuf for efficient message serialization
- WebSocket for real-time notifications
- React frontend with shadcn/ui"

**3. Live Demo (3 minutes)**
- Show dashboard
- Click "Upload Communication"
- Paste sample email:
```
Hi team,

Thanks for the trademark work last quarter. Quick update: 
we're opening a Chicago office next month and need help 
with the commercial lease. Also planning to hire 20 people, 
so we'll need employment contracts.

Best,
John - Acme Corp
```
- Submit and show loading
- Show detected opportunities
- Point out confidence scores
- Show real-time WebSocket notification

**4. Technical Highlights (30 seconds)**
- "Clean architecture following SOLID principles"
- "Async/await throughout for performance"
- "Type-safe with Pydantic and TypeScript"
- "Comprehensive error handling"
- "Ready to scale"

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: OpenAI API errors**
```python
# Solution: Add better error handling and retry logic
# Already implemented in OpportunityDetector with tenacity
```

**Issue: WebSocket disconnects**
```typescript
// Solution: Implement reconnection logic
// Already implemented in useWebSocket hook
```

**Issue: Database connection pool exhausted**
```python
# Solution: Increase pool size or add connection retry
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,  # Increase if needed
    max_overflow=10,
    pool_pre_ping=True,  # Check connections before use
)
```

**Issue: CORS errors**
```python
# Solution: Check CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## Success Criteria Checklist

### Functional Requirements
- [ ] Can upload communications via UI
- [ ] AI extracts opportunities with confidence scores
- [ ] Opportunities stored in database
- [ ] GraphQL queries return correct data
- [ ] WebSocket pushes real-time notifications
- [ ] Frontend displays opportunities clearly
- [ ] Toast notifications appear on new opportunities

### Non-Functional Requirements
- [ ] API responds in <200ms
- [ ] AI analysis completes in <5 seconds
- [ ] No crashes or critical errors
- [ ] Clean, readable code
- [ ] Tests pass
- [ ] Documentation complete
- [ ] Can run with `docker-compose up`

### Code Quality
- [ ] Follows SOLID principles
- [ ] DRY - no repeated code
- [ ] YAGNI - no unnecessary features
- [ ] Clear variable names
- [ ] Proper error handling
- [ ] Adequate test coverage

---

## Congratulations! 🎉

You've built a production-ready MVP in 3 days that demonstrates:
- Full-stack development skills
- AI integration
- Real-time capabilities
- Clean architecture
- Best practices

**Next Steps:**
1. Deploy to cloud (Heroku/Railway/Vercel)
2. Add authentication
3. Implement caching
4. Add more sophisticated ML
5. Build mobile app

---

**End of Implementation Strategy**

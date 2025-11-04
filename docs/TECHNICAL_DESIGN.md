# Technical Design Document
## Smart Matter Opportunity Detector

**Version:** 1.0 MVP  
**Last Updated:** November 4, 2025  
**Architecture:** Microservices (Simplified)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  React + Vite + shadcn/ui + Tailwind + Apollo Client        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ GraphQL (HTTP)
                     │ WebSocket
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│                    FastAPI + Strawberry                      │
├──────────────────────┬──────────────────────┬───────────────┤
│   GraphQL Endpoint   │  WebSocket Server    │  Health Check │
└──────────────────────┴──────────────────────┴───────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Business   │ │   AI Service │ │  Notification│
│    Logic     │ │   (OpenAI)   │ │   Service    │
│              │ │              │ │  (WebSocket) │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       │                │                │
       ├────────────────┴────────────────┤
       │        Protobuf Messages        │
       └────────────────┬────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   PostgreSQL     │
              │   Database       │
              └──────────────────┘
```

### 1.2 Component Breakdown

**Frontend (React SPA)**
- Purpose: User interface for viewing opportunities and uploading communications
- Tech: React 18, Vite, Apollo Client, shadcn/ui
- Responsibilities: UI rendering, state management, WebSocket client

**API Gateway (FastAPI)**
- Purpose: Single entry point for all client requests
- Tech: FastAPI, Strawberry GraphQL
- Responsibilities: Request routing, GraphQL resolution, authentication (future)

**AI Service (OpenAI Integration)**
- Purpose: Analyze text and extract opportunities
- Tech: OpenAI Python SDK, Protobuf
- Responsibilities: Text processing, opportunity detection, confidence scoring

**Notification Service (WebSocket)**
- Purpose: Push real-time updates to connected clients
- Tech: FastAPI WebSockets, Protobuf
- Responsibilities: Maintain connections, broadcast notifications

**Database (PostgreSQL)**
- Purpose: Persistent data storage
- Tech: PostgreSQL 15+, SQLAlchemy ORM
- Responsibilities: Store communications, opportunities, contacts

---

## 2. Technology Stack & Justification

### 2.1 Backend Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **Python 3.11+** | Primary language | Job requirement, excellent AI/ML libraries |
| **FastAPI** | Web framework | Fast, async support, auto-docs, type safety |
| **Strawberry GraphQL** | GraphQL library | Type-safe, Pythonic, modern |
| **SQLAlchemy 2.0** | ORM | Industry standard, async support |
| **Alembic** | Migrations | Works seamlessly with SQLAlchemy |
| **PostgreSQL 15** | Database | Reliable, full-text search, JSON support |
| **Protobuf** | Message format | Efficient serialization, job requirement |
| **OpenAI SDK** | AI integration | Best-in-class for text analysis |
| **pytest** | Testing | Standard Python testing framework |
| **uvicorn** | ASGI server | Fast, production-ready |

### 2.2 Frontend Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **React 18** | UI framework | Component-based, large ecosystem |
| **Vite** | Build tool | Fast HMR, modern, simple config |
| **TypeScript** | Language | Type safety, better DX |
| **Apollo Client** | GraphQL client | Best-in-class GraphQL integration |
| **shadcn/ui** | Component library | Beautiful, accessible, customizable |
| **Tailwind CSS** | Styling | Utility-first, fast development |
| **Zustand** | State management | Simple, minimal boilerplate |

### 2.4 Frontend Design System

#### Component Standards
**shadcn/ui Components Only**
- Use shadcn/ui components exclusively for all UI elements
- Import pattern: `import { Button } from '@/components/ui/button'`
- Core components: Button, Card, Input, Dialog, Select, Tabs, Badge, Textarea, Label, Toast
- Compose complex UIs from shadcn primitives (no custom component libraries)

#### Styling Guidelines
**Tailwind Utility Classes Only**
- No custom CSS files or styled-components
- Use only Tailwind utility classes for all styling
- Consistent spacing scale:
  - Card/Container padding: `p-6`
  - Section gaps: `gap-4` or `gap-6`
  - Form field spacing: `space-y-4`
  - Section margins: `mb-4`, `mb-6`, `mb-8`
- Typography scale:
  - Labels: `text-sm font-medium`
  - Body text: `text-base`
  - Headings: `text-lg font-semibold`, `text-xl font-bold`, `text-3xl font-bold`
- Font weights: `font-medium` for labels, `font-semibold` for subheadings, `font-bold` for headings

#### Theme & Colors
**CSS Variable-Based Theming**
- Use theme color variables (never hardcoded colors):
  - Backgrounds: `bg-background`, `bg-card`, `bg-muted`, `bg-popover`
  - Text: `text-foreground`, `text-muted-foreground`, `text-card-foreground`
  - Accents: `bg-primary`, `bg-secondary`, `bg-accent`, `bg-destructive`
  - Borders: `border-border`, `border-input`
- Dark mode support with `dark:` variants (e.g., `dark:bg-gray-800`)
- Maintain WCAG AA accessibility standards (4.5:1 contrast ratio minimum)
- Semantic color usage:
  - Primary: Main actions, CTA buttons
  - Secondary: Supporting actions
  - Destructive: Errors, deletions
  - Muted: Disabled states, placeholders

#### Layout Patterns
**Responsive Design**
- Mobile-first approach with progressive enhancement
- Breakpoint usage:
  - Mobile: Default (no prefix)
  - Tablet: `md:` (768px+)
  - Desktop: `lg:` (1024px+)
  - Wide: `xl:` (1280px+)
- Container pattern: `max-w-7xl mx-auto px-4`
- Grid layouts: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- Flex patterns: `flex items-center justify-between gap-4`

#### UI/UX Principles
**Visual Consistency**
- Border radius:
  - Cards/Panels: `rounded-lg`
  - Inputs/Buttons: `rounded-md`
  - Badges: `rounded-full`
- Shadows: Use shadcn defaults (`shadow`, `shadow-md`, `shadow-lg`)
- Transitions: `transition-colors duration-200` for hover states

**Interactive States**
- Hover: `hover:bg-accent`, `hover:opacity-80`, `hover:shadow-lg`
- Focus: `focus:ring-2 focus:ring-primary focus:outline-none`
- Active: `active:scale-95` for buttons
- Disabled: `disabled:opacity-50 disabled:cursor-not-allowed`

**Loading & Feedback**
- Loading states: Use Skeleton components from shadcn/ui
- Error states: Use `destructive` variant with clear error messages
- Success states: Toast notifications with `success` styling
- Empty states: Centered layout with muted text and icons

**Component Patterns**
```typescript
// Card pattern
<Card className="p-6">
  <CardHeader>
    <CardTitle className="text-xl font-bold">Title</CardTitle>
    <CardDescription className="text-muted-foreground">Description</CardDescription>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Content */}
  </CardContent>
</Card>

// Form pattern
<form className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="field" className="text-sm font-medium">Label</Label>
    <Input id="field" className="w-full" />
  </div>
</form>

// Button pattern
<Button
  variant="default" // or "secondary", "destructive", "outline", "ghost"
  size="default" // or "sm", "lg", "icon"
  className="w-full md:w-auto"
>
  Action
</Button>
```

### 2.3 DevOps Stack

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **Docker** | Containerization | Consistent environments |
| **docker-compose** | Orchestration | Easy multi-service setup |
| **GitHub Actions** | CI/CD | Free, integrated with GitHub |

---

## 3. Database Design

### 3.1 Entity Relationship Diagram

```
┌─────────────────────┐
│   communications    │
├─────────────────────┤
│ id (PK)             │
│ content             │
│ client_name         │
│ source_type         │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐
│   opportunities     │
├─────────────────────┤
│ id (PK)             │
│ communication_id(FK)│
│ title               │
│ description         │
│ opportunity_type    │
│ confidence          │
│ estimated_value     │
│ extracted_text      │
│ status              │
│ detected_at         │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

### 3.2 Table Definitions

**communications**
```sql
CREATE TABLE communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL CHECK (char_length(content) >= 50),
    client_name VARCHAR(200) NOT NULL,
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('EMAIL', 'MEETING', 'NOTE')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_communications_created_at ON communications(created_at DESC);
CREATE INDEX idx_communications_client_name ON communications(client_name);
```

**opportunities**
```sql
CREATE TABLE opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    communication_id UUID NOT NULL REFERENCES communications(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    opportunity_type VARCHAR(50) NOT NULL CHECK (
        opportunity_type IN (
            'REAL_ESTATE',
            'EMPLOYMENT_LAW',
            'MERGERS_AND_ACQUISITIONS',
            'INTELLECTUAL_PROPERTY',
            'LITIGATION'
        )
    ),
    confidence DECIMAL(5,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    estimated_value VARCHAR(50),
    extracted_text TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'NEW' CHECK (status IN ('NEW', 'REVIEWING', 'CONTACTED', 'CLOSED', 'ARCHIVED')),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_opportunities_confidence ON opportunities(confidence DESC);
CREATE INDEX idx_opportunities_type ON opportunities(opportunity_type);
CREATE INDEX idx_opportunities_detected_at ON opportunities(detected_at DESC);
CREATE INDEX idx_opportunities_communication_id ON opportunities(communication_id);
```

### 3.3 Why No Vector Database?

**Decision: Use PostgreSQL only (no pgvector or separate vector DB)**

**Reasoning:**
1. **YAGNI Principle**: We're doing exact keyword matching and OpenAI analysis, not semantic search
2. **Simplicity**: One database to manage, deploy, and backup
3. **Time Constraint**: 3 days - don't add complexity unnecessarily
4. **PostgreSQL Full-Text Search**: Sufficient for filtering opportunities by keywords
5. **Future-Proof**: Can add pgvector extension later if semantic search needed

**When to add vector DB (post-MVP):**
- Need semantic similarity search ("find opportunities similar to this one")
- Building recommendation engine
- Clustering related opportunities

---

## 4. API Design

### 4.1 GraphQL Schema

```graphql
# Types
type Communication {
  id: ID!
  content: String!
  clientName: String!
  sourceType: CommunicationType!
  opportunities: [Opportunity!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Opportunity {
  id: ID!
  communication: Communication!
  title: String!
  description: String!
  opportunityType: OpportunityType!
  confidence: Float!
  estimatedValue: String
  extractedText: String!
  status: OpportunityStatus!
  detectedAt: DateTime!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OpportunityConnection {
  edges: [OpportunityEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OpportunityEdge {
  node: Opportunity!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

type OpportunityStats {
  totalCount: Int!
  highConfidenceCount: Int!
  byType: [TypeCount!]!
}

type TypeCount {
  type: OpportunityType!
  count: Int!
}

# Enums
enum CommunicationType {
  EMAIL
  MEETING
  NOTE
}

enum OpportunityType {
  REAL_ESTATE
  EMPLOYMENT_LAW
  MERGERS_AND_ACQUISITIONS
  INTELLECTUAL_PROPERTY
  LITIGATION
}

enum OpportunityStatus {
  NEW
  REVIEWING
  CONTACTED
  CLOSED
  ARCHIVED
}

# Inputs
input CreateCommunicationInput {
  content: String!
  clientName: String!
  sourceType: CommunicationType!
}

input UpdateOpportunityInput {
  id: ID!
  status: OpportunityStatus
}

# Queries
type Query {
  opportunities(
    minConfidence: Float
    type: OpportunityType
    status: OpportunityStatus
    limit: Int = 20
    offset: Int = 0
  ): OpportunityConnection!
  
  opportunity(id: ID!): Opportunity
  
  communication(id: ID!): Communication
  
  opportunityStats: OpportunityStats!
}

# Mutations
type Mutation {
  createCommunication(input: CreateCommunicationInput!): CreateCommunicationPayload!
  
  updateOpportunity(input: UpdateOpportunityInput!): UpdateOpportunityPayload!
}

# Payloads
type CreateCommunicationPayload {
  communication: Communication!
  opportunities: [Opportunity!]!
}

type UpdateOpportunityPayload {
  opportunity: Opportunity!
}

# Scalars
scalar DateTime
```

### 4.2 REST Endpoints (Minimal)

```
GET  /health           - Health check
GET  /ws              - WebSocket connection
POST /graphql         - GraphQL endpoint
```

---

## 5. Protobuf Message Definitions

### 5.1 Message Schema

```protobuf
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

### 5.2 Usage Pattern

```python
# Service A: Send analysis request
request = AnalysisRequest(
    communication_id=str(comm_id),
    content=content,
    client_name=client_name
)
serialized = request.SerializeToString()
# Send via Redis pub/sub or direct call

# Service B: Process and respond
response = AnalysisResponse(
    communication_id=request.communication_id,
    opportunities=[...],
    success=True
)
```

---

## 6. AI Integration Design

### 6.1 OpenAI Integration Pattern

```python
from openai import OpenAI
from typing import List
import json

class OpportunityDetector:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
    async def analyze_communication(
        self,
        content: str,
        client_name: str
    ) -> List[dict]:
        """
        Analyze text and extract opportunities.
        Returns list of opportunities with confidence scores.
        """
        prompt = self._build_prompt(content, client_name)
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=1000
        )
        
        result = json.loads(response.choices[0].message.content)
        return self._validate_opportunities(result.get("opportunities", []))
    
    def _get_system_prompt(self) -> str:
        return """You are an AI assistant for a law firm that identifies 
        business opportunities in client communications. Analyze the text 
        and extract opportunities with high accuracy."""
    
    def _build_prompt(self, content: str, client_name: str) -> str:
        return f"""
        Client: {client_name}
        
        Communication:
        {content}
        
        Identify legal service opportunities. For each opportunity, provide:
        1. title: Brief title (max 60 chars)
        2. description: What the client needs
        3. type: One of [real_estate, employment_law, m&a, ip, litigation]
        4. confidence: Score 0-100 based on clarity and urgency
        5. extracted_text: Exact quote from communication
        6. estimated_value: Rough estimate if possible (e.g., "$20k-50k")
        
        Return JSON:
        {{
            "opportunities": [
                {{
                    "title": "...",
                    "description": "...",
                    "type": "...",
                    "confidence": 85,
                    "extracted_text": "...",
                    "estimated_value": "..."
                }}
            ]
        }}
        """
```

### 6.2 Error Handling Strategy

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_openai_with_retry(prompt: str):
    """Retry logic for OpenAI API calls"""
    try:
        return await openai_client.chat.completions.create(...)
    except openai.RateLimitError:
        raise AIServiceError("Rate limit exceeded")
    except openai.APIError as e:
        raise AIServiceError(f"OpenAI API error: {str(e)}")
```

---

## 7. WebSocket Design

### 7.1 Connection Management

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: bytes):
        """Broadcast protobuf message to all connected clients"""
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_bytes(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        self.active_connections -= disconnected

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### 7.2 Notification Flow

```
1. New opportunity created (confidence ≥ 70%)
   ↓
2. Build OpportunityNotification protobuf message
   ↓
3. Serialize to bytes
   ↓
4. ConnectionManager.broadcast(message)
   ↓
5. All connected clients receive notification
   ↓
6. Frontend displays toast notification
```

---

## 8. Project Structure

### 8.1 Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # FastAPI dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── graphql/
│   │       ├── __init__.py
│   │       ├── schema.py       # Strawberry schema
│   │       ├── queries.py      # Query resolvers
│   │       ├── mutations.py    # Mutation resolvers
│   │       └── types.py        # GraphQL types
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── communication.py    # SQLAlchemy models
│   │   └── opportunity.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # OpenAI integration
│   │   ├── opportunity_detector.py
│   │   └── notification_service.py
│   │
│   ├── websocket/
│   │   ├── __init__.py
│   │   └── manager.py          # WebSocket connection manager
│   │
│   ├── protobuf/
│   │   ├── __init__.py
│   │   ├── messages.proto      # Protobuf definitions
│   │   └── messages_pb2.py     # Generated Python code
│   │
│   └── utils/
│       ├── __init__.py
│       ├── database.py         # DB connection
│       └── logging.py          # Logging config
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_api/
│   ├── test_services/
│   └── test_models/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml              # Poetry dependencies
├── pytest.ini
└── README.md
```

### 8.2 Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   │
│   ├── components/
│   │   ├── ui/                 # shadcn components
│   │   ├── OpportunityCard.tsx
│   │   ├── OpportunityList.tsx
│   │   ├── UploadModal.tsx
│   │   └── Filters.tsx
│   │
│   ├── graphql/
│   │   ├── queries.ts          # GraphQL queries
│   │   ├── mutations.ts        # GraphQL mutations
│   │   └── client.ts           # Apollo client setup
│   │
│   ├── hooks/
│   │   ├── useWebSocket.ts     # WebSocket hook
│   │   └── useOpportunities.ts
│   │
│   ├── lib/
│   │   ├── protobuf.ts         # Protobuf decoder
│   │   └── utils.ts            # Utilities
│   │
│   ├── stores/
│   │   └── notificationStore.ts # Zustand store
│   │
│   └── types/
│       └── index.ts            # TypeScript types
│
├── public/
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 9. Code Best Practices Implementation

### 9.1 SOLID Principles

**Single Responsibility**
```python
# GOOD: Each class has one job
class OpportunityDetector:
    """Only responsible for detecting opportunities"""
    def analyze(self, text: str) -> List[Opportunity]: ...

class OpportunityRepository:
    """Only responsible for data access"""
    def save(self, opportunity: Opportunity): ...
    def find_by_id(self, id: str): ...

# BAD: Violates SRP
class OpportunityService:
    def analyze_and_save_and_notify(self, text: str): ...
```

**Dependency Inversion**
```python
# GOOD: Depend on abstractions
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    async def analyze(self, text: str) -> List[dict]: ...

class OpenAIProvider(AIProvider):
    async def analyze(self, text: str) -> List[dict]:
        # OpenAI implementation
        pass

class OpportunityService:
    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider

# BAD: Depend on concrete implementation
class OpportunityService:
    def __init__(self):
        self.openai_client = OpenAI()  # Tightly coupled
```

### 9.2 KISS & DRY Examples

```python
# KISS: Simple is better
def calculate_confidence(keywords: List[str], text: str) -> float:
    """Simple keyword matching for confidence"""
    matches = sum(1 for kw in keywords if kw.lower() in text.lower())
    return min(matches * 20, 100)  # Simple formula

# DRY: Extract common patterns
def create_graphql_error(message: str, code: str) -> dict:
    """Reusable error format"""
    return {
        "message": message,
        "extensions": {"code": code}
    }

# Usage
if not communication:
    raise create_graphql_error("Communication not found", "NOT_FOUND")
```

### 9.3 Error Handling Pattern

```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class Result:
    """Result type for explicit error handling"""
    success: bool
    data: Optional[any] = None
    error: Optional[str] = None

async def create_communication(input: dict) -> Result:
    try:
        # Validate early (Fail Fast)
        if len(input['content']) < 50:
            return Result(success=False, error="Content too short")
        
        # Business logic
        comm = await repository.create(input)
        
        return Result(success=True, data=comm)
    
    except DatabaseError as e:
        logger.error(f"DB error: {e}")
        return Result(success=False, error="Database error")
```

---

## 10. Testing Strategy

### 10.1 Test Pyramid

```
         ┌──────────┐
         │    E2E   │  (5%) - Full flow tests
         └──────────┘
       ┌──────────────┐
       │ Integration  │  (25%) - API + DB tests
       └──────────────┘
    ┌────────────────────┐
    │   Unit Tests       │  (70%) - Functions, classes
    └────────────────────┘
```

### 10.2 Key Test Cases

**Unit Tests**
```python
def test_opportunity_detector_extracts_real_estate():
    detector = OpportunityDetector()
    text = "We're opening a new office in NYC next quarter"
    
    opportunities = detector.analyze(text)
    
    assert len(opportunities) == 1
    assert opportunities[0].type == "REAL_ESTATE"
    assert opportunities[0].confidence >= 80

def test_confidence_calculator():
    calc = ConfidenceCalculator()
    
    # High confidence: explicit need + timeline
    assert calc.calculate("need office lease by Q2") > 80
    
    # Low confidence: vague
    assert calc.calculate("might need something") < 50
```

**Integration Tests**
```python
@pytest.mark.asyncio
async def test_create_communication_flow(client, db_session):
    # Arrange
    input_data = {
        "content": "Client mentioned expanding to Chicago...",
        "clientName": "Acme Corp",
        "sourceType": "EMAIL"
    }
    
    # Act
    response = await client.post("/graphql", json={
        "query": CREATE_COMMUNICATION_MUTATION,
        "variables": {"input": input_data}
    })
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["createCommunication"]["communication"]["id"]
    assert len(data["data"]["createCommunication"]["opportunities"]) > 0
```

---

## 11. Deployment Architecture

### 11.1 Docker Compose Setup

```yaml
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
      DATABASE_URL: postgresql://nexl:nexl123@db:5432/nexl_opportunities
      OPENAI_API_KEY: ${OPENAI_API_KEY}
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

volumes:
  postgres_data:
```

### 11.2 Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://nexl:nexl123@localhost:5432/nexl_opportunities
OPENAI_API_KEY=sk-...
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
```

---

## 12. Performance Optimization

### 12.1 Database Optimization

```python
# Use select_related to avoid N+1 queries
opportunities = await session.execute(
    select(Opportunity)
    .options(selectinload(Opportunity.communication))
    .filter(Opportunity.confidence >= min_confidence)
)

# Database connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

### 12.2 Caching Strategy

```python
from functools import lru_cache
import redis

# Simple in-memory cache for stats
@lru_cache(maxsize=1)
def get_opportunity_stats_cached():
    return calculate_stats()

# Redis for distributed caching (future)
redis_client = redis.Redis(host='localhost', port=6379)
```

---

## 13. Security Considerations

### 13.1 Input Validation

```python
from pydantic import BaseModel, Field, validator

class CommunicationInput(BaseModel):
    content: str = Field(..., min_length=50, max_length=10000)
    client_name: str = Field(..., min_length=1, max_length=200)
    source_type: str
    
    @validator('source_type')
    def validate_source_type(cls, v):
        allowed = ['EMAIL', 'MEETING', 'NOTE']
        if v not in allowed:
            raise ValueError(f'source_type must be one of {allowed}')
        return v
```

### 13.2 SQL Injection Prevention

```python
# GOOD: Using ORM (parameterized queries)
opportunities = await session.execute(
    select(Opportunity)
    .where(Opportunity.opportunity_type == opp_type)
)

# BAD: Raw SQL with string formatting
query = f"SELECT * FROM opportunities WHERE type = '{opp_type}'"
```

---

## 14. Monitoring & Logging

### 14.1 Logging Strategy

```python
import logging
import structlog

# Structured logging
logger = structlog.get_logger()

logger.info(
    "opportunity_detected",
    opportunity_id=opp_id,
    confidence=confidence,
    type=opp_type,
    client_name=client_name
)
```

### 14.2 Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database
        await db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
```

---

## 15. Development Workflow

### 15.1 Local Setup Steps

```bash
# 1. Clone repository
git clone <repo-url>

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Generate protobuf
protoc --python_out=. app/protobuf/messages.proto

# 4. Run migrations
alembic upgrade head

# 5. Start backend
uvicorn app.main:app --reload

# 6. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### 15.2 Git Workflow

```
main (production-ready)
  └── develop (integration branch)
       ├── feature/graphql-api
       ├── feature/ai-integration
       └── feature/websocket-notifications
```

---

## 16. Known Limitations & Trade-offs

### MVP Limitations

1. **No Authentication**: Anyone can access the API
   - Trade-off: Faster development, focus on core features
   - Future: Add JWT-based auth

2. **Single User**: No multi-tenancy
   - Trade-off: Simpler data model
   - Future: Add organization/user context

3. **Synchronous OpenAI Calls**: May block requests
   - Trade-off: Simpler implementation
   - Future: Use Celery for background processing

4. **No Caching**: Every query hits database
   - Trade-off: Always fresh data
   - Future: Redis caching layer

5. **Basic Error Messages**: Generic errors to users
   - Trade-off: Simpler error handling
   - Future: Detailed, actionable error messages

---

## 17. Future Enhancements (Post-MVP)

### Phase 2 Features
- User authentication & authorization
- Email integration (Gmail, Outlook)
- Advanced analytics dashboard
- Opportunity assignment workflow
- Export to CSV/PDF

### Phase 3 Features
- Multi-tenancy support
- Mobile-responsive design
- Calendar integration
- Slack/Teams notifications
- Custom opportunity types

### Technical Improvements
- Add Redis caching
- Implement Celery for async jobs
- Add pgvector for semantic search
- Comprehensive monitoring (Prometheus/Grafana)
- CI/CD pipeline

---

## Appendix A: Quick Reference

### Useful Commands

```bash
# Backend
uvicorn app.main:app --reload          # Start dev server
alembic revision --autogenerate        # Create migration
alembic upgrade head                   # Run migrations
pytest                                 # Run tests
pytest --cov=app tests/                # Run with coverage

# Frontend
npm run dev                            # Start dev server
npm run build                          # Production build
npm run preview                        # Preview production build

# Docker
docker-compose up                      # Start all services
docker-compose down                    # Stop all services
docker-compose logs -f backend         # View logs
```

### Key URLs

- Backend API: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql
- WebSocket: ws://localhost:8000/ws
- Frontend: http://localhost:5173

---

**Document End**

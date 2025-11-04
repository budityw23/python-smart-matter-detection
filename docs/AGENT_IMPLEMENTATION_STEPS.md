# Agent Implementation Steps
## Smart Matter Opportunity Detector - 6-Step Implementation Plan

**Version:** 1.0
**Last Updated:** November 4, 2025
**Approach:** Incremental implementation with testing at each step

---

## Overview

This document breaks down the project implementation into **6 manageable steps**, each taking approximately 2-4 hours and producing a testable deliverable. After each step, you can verify functionality before proceeding.

---

## Step 1: Database Foundation & Models (2-3 hours)

### Objective
Create the database schema, models, and migrations without any API layer.

### Agent Prompt

```
use context7

**Task:** Implement Step 1 - Database Foundation for Smart Matter Opportunity Detector

**Read First:**
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 20-385 - Database Setup)
- docs/TECHNICAL_DESIGN.md (section 3 - Database Design)

**Use Context7 for:**
- SQLAlchemy 2.0 async ORM patterns
- Alembic async migrations
- PostgreSQL UUID and ENUM types
- Python type hints and Pydantic

**What to Implement:**

1. **Project Structure:**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   ├── base.py
   │   │   ├── communication.py
   │   │   └── opportunity.py
   │   └── utils/
   │       ├── __init__.py
   │       └── database.py
   ├── alembic/
   ├── tests/
   │   └── test_models/
   ├── .env
   ├── requirements.txt
   ├── alembic.ini
   └── docker-compose.yml
   ```

2. **Database Models:**
   - `Communication` model with all fields from spec
   - `Opportunity` model with relationships
   - Proper enums for CommunicationType, OpportunityType, OpportunityStatus
   - All indexes defined

3. **Database Connection:**
   - Async engine setup
   - Session maker
   - get_db() dependency function

4. **Alembic Setup:**
   - Initialize Alembic
   - Configure for async
   - Generate initial migration
   - Apply migration

5. **Docker Compose:**
   - PostgreSQL 15-alpine service
   - Health check
   - Volume for persistence

**Deliverables:**
- [ ] Complete backend folder structure
- [ ] SQLAlchemy models defined
- [ ] Alembic migration applied successfully
- [ ] PostgreSQL running in Docker
- [ ] Can connect to database

**Test Commands:**
```bash
# Start database
docker-compose up -d db

# Check database is healthy
docker-compose ps

# Run migration
cd backend
source venv/bin/activate
alembic upgrade head

# Verify tables created
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"
```

**Success Criteria:**
✅ PostgreSQL container running and healthy
✅ Alembic migration applied without errors
✅ Tables exist: communications, opportunities
✅ Can query tables (even if empty)

**Expected Tables:**
```sql
nexl_opportunities=# \dt
                List of relations
 Schema |         Name         | Type  | Owner
--------+----------------------+-------+-------
 public | alembic_version      | table | nexl
 public | communications       | table | nexl
 public | opportunities        | table | nexl
```

Return a summary of what was created and confirmation that migrations work.
```

### Verification Steps After Step 1

```bash
# 1. Check Docker container
docker-compose ps
# Expected: db service running (healthy)

# 2. Verify database tables
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"
# Expected: communications, opportunities, alembic_version tables

# 3. Check table structure
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\d communications"
# Expected: All columns (id, content, client_name, source_type, created_at, updated_at)

# 4. Verify indexes
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\di"
# Expected: Indexes on created_at, confidence, opportunity_type, detected_at
```

### Expected Output
- ✅ Docker container running
- ✅ 3 tables created (communications, opportunities, alembic_version)
- ✅ All columns match schema
- ✅ Indexes created
- ✅ No migration errors

---

## Step 2: GraphQL API Foundation (2-3 hours)

### Objective
Create a working GraphQL API with queries (no mutations yet), test with GraphQL playground.

### Agent Prompt

```
use context7

**Task:** Implement Step 2 - GraphQL API Foundation

**Read First:**
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 386-800 - GraphQL Setup)
- docs/TECHNICAL_DESIGN.md (section 4.1 - GraphQL Schema)

**Use Context7 for:**
- Strawberry GraphQL 0.215+ (types, queries, async resolvers)
- FastAPI 0.104+ (lifespan, middleware, CORS)
- GraphQL best practices

**What to Implement:**

1. **GraphQL Types** (app/api/graphql/types.py):
   - All Strawberry types: Communication, Opportunity, OpportunityConnection
   - All enums: CommunicationType, OpportunityType, OpportunityStatus
   - Connection types: OpportunityEdge, PageInfo
   - Stats types: OpportunityStats, TypeCount

2. **Query Resolvers** (app/api/graphql/queries.py):
   - `opportunities()` - with filters (minConfidence, type, limit, offset)
   - `opportunity(id)` - get single opportunity
   - `opportunityStats()` - dashboard statistics
   - Helper: `convert_opportunity_to_gql()`

3. **Stub Mutations** (app/api/graphql/mutations.py):
   - `createCommunication()` - stub that returns dummy data
   - Just needs to be valid GraphQL, doesn't need to work yet

4. **Schema** (app/api/graphql/schema.py):
   - Combine Query and Mutation into Strawberry schema

5. **FastAPI App** (app/main.py):
   - Create FastAPI app with lifespan
   - Add CORS middleware
   - Add GraphQL router at /graphql
   - Add health check at /health
   - Add context with database session

6. **Testing** (tests/test_api/test_graphql.py):
   - Test health endpoint
   - Test opportunityStats query
   - Test fixtures setup

**Deliverables:**
- [ ] Complete GraphQL type system
- [ ] Working query resolvers
- [ ] GraphQL playground accessible
- [ ] Health check working
- [ ] Tests passing

**Test Commands:**
```bash
# Start server
cd backend
uvicorn app.main:app --reload

# In browser, visit:
# http://localhost:8000/graphql

# Test this query in playground:
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

# Run tests
pytest tests/test_api/test_graphql.py -v
```

**Success Criteria:**
✅ Server starts without errors
✅ GraphQL playground loads at /graphql
✅ Health endpoint returns {"status": "healthy"}
✅ opportunityStats query returns {"totalCount": 0, "highConfidenceCount": 0}
✅ Tests pass

Return GraphQL schema overview and test results.
```

### Verification Steps After Step 2

```bash
# 1. Start server
uvicorn app.main:app --reload
# Expected: Server starts on port 8000

# 2. Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"smart-matter-detector"}

# 3. Open GraphQL playground
# Browser: http://localhost:8000/graphql
# Expected: GraphiQL interface loads

# 4. Run test query
# In playground:
query {
  opportunities(limit: 10) {
    edges { node { id title } }
    totalCount
  }
}
# Expected: Returns empty array, totalCount: 0

# 5. Run tests
pytest tests/test_api/test_graphql.py -v
# Expected: All tests pass
```

### Expected Output
- ✅ Server running on port 8000
- ✅ GraphQL playground accessible
- ✅ Queries return valid (empty) data
- ✅ All tests passing
- ✅ No GraphQL schema errors

---

## Step 3: OpenAI Integration & Business Logic (3-4 hours)

### Objective
Implement AI service for opportunity detection and business logic services.

### Agent Prompt

```
use context7

**Task:** Implement Step 3 - OpenAI Integration & Opportunity Detection

**Read First:**
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 1062-1339 - OpenAI Integration)
- docs/TECHNICAL_DESIGN.md (section 6 - AI Integration Design)

**Use Context7 for:**
- OpenAI Python SDK 1.3+ (async chat completions, structured output)
- Tenacity 8.2+ (retry decorators)
- Python best practices for API integration

**What to Implement:**

1. **AI Service** (app/services/ai_service.py):
   - `OpportunityDetector` class
   - `analyze_communication()` method with OpenAI API
   - `_get_system_prompt()` - AI instructions
   - `_build_prompt()` - user prompt builder
   - `_validate_opportunities()` - response validation
   - Retry logic with @retry decorator
   - `AIServiceError` exception class
   - Comprehensive logging

2. **Opportunity Service** (app/services/opportunity_service.py):
   - `OpportunityService` class
   - `create_communication_with_opportunities()` - main workflow
   - `should_notify()` - notification rules (confidence >= 70%)
   - Type mapping from AI output to DB enums
   - Database transaction handling

3. **Update Mutation** (app/api/graphql/mutations.py):
   - Replace stub `createCommunication` with real implementation
   - Call AI service to analyze text
   - Save communication and opportunities to database
   - Return GraphQL types
   - Add input validation

4. **Manual Test Script** (backend/manual_test.py):
   - Test script with 3 sample communications
   - Print extracted opportunities
   - Show confidence scores

5. **Environment Config:**
   - Add OPENAI_API_KEY to .env
   - Add to .env.example

**Important:**
- Use gpt-4-turbo-preview or gpt-4o model
- Set temperature=0.3 for consistency
- Use JSON mode for structured output
- Validate confidence scores (40-100)
- Filter minimum confidence 40%

**Deliverables:**
- [ ] OpportunityDetector working with OpenAI
- [ ] OpportunityService with database integration
- [ ] createCommunication mutation functional
- [ ] Manual test script results
- [ ] Validation and error handling

**Test Commands:**
```bash
# Add API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> backend/.env

# Run manual test
python backend/manual_test.py

# Test via GraphQL
# In playground:
mutation {
  createCommunication(input: {
    content: "We're opening a new Chicago office next month and need help with the commercial lease."
    clientName: "Acme Corp"
    sourceType: EMAIL
  }) {
    communication { id clientName }
    opportunities {
      id
      title
      opportunityType
      confidence
      description
    }
  }
}

# Check database
docker-compose exec db psql -U nexl -d nexl_opportunities -c "SELECT COUNT(*) FROM opportunities;"
```

**Success Criteria:**
✅ OpenAI API calls succeed
✅ Opportunities extracted from sample text
✅ Confidence scores between 40-100
✅ Opportunities saved to database
✅ createCommunication mutation returns data
✅ At least 1-3 opportunities detected per sample

Return sample output showing detected opportunities with confidence scores.
```

### Verification Steps After Step 3

```bash
# 1. Run manual test
python backend/manual_test.py
# Expected: Shows detected opportunities with types and confidence

# 2. Test mutation via GraphQL
# Use mutation above
# Expected: Returns communication + opportunities array

# 3. Verify database has data
docker-compose exec db psql -U nexl -d nexl_opportunities -c "SELECT title, confidence, opportunity_type FROM opportunities LIMIT 5;"
# Expected: Shows saved opportunities

# 4. Check AI response time
# Expected: <5 seconds per communication

# 5. Test error handling
# Try with invalid API key
# Expected: Proper error message, retry attempts logged
```

### Expected Output
- ✅ AI successfully analyzes text
- ✅ Opportunities extracted with reasonable confidence
- ✅ Data saved to database
- ✅ Retry logic works on failures
- ✅ Validation catches bad data

---

## Step 4: Protobuf & WebSocket Implementation (2-3 hours)

### Objective
Add real-time notification system with Protobuf messages over WebSocket.

### Agent Prompt

```
use context7

**Task:** Implement Step 4 - Protobuf Messages & WebSocket Server

**Read First:**
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 943-1059, 1460-1629)
- docs/TECHNICAL_DESIGN.md (section 5 - Protobuf, section 7 - WebSocket)

**Use Context7 for:**
- Protobuf 4.25+ (message definitions, Python generation)
- FastAPI WebSockets (connection management, async)
- Python asyncio patterns

**What to Implement:**

1. **Protobuf Messages** (app/protobuf/messages.proto):
   - OpportunityNotification message
   - OpportunityType enum
   - AnalysisRequest message
   - AnalysisResponse message
   - ExtractedOpportunity message

2. **Generate Protobuf Code:**
   ```bash
   python -m grpc_tools.protoc \
     -I./app/protobuf \
     --python_out=./app/protobuf \
     ./app/protobuf/messages.proto
   ```

3. **Protobuf Helpers** (app/protobuf/helpers.py):
   - `create_opportunity_notification()` - serialize to bytes
   - `parse_opportunity_notification()` - deserialize from bytes
   - Enum mapping (DB types ↔ Protobuf types)

4. **WebSocket Manager** (app/websocket/manager.py):
   - `ConnectionManager` class
   - `connect()` - accept new connections
   - `disconnect()` - remove connections
   - `broadcast()` - send to all clients
   - `send_to_client()` - send to specific client
   - Track active connections

5. **FastAPI WebSocket Endpoint** (app/main.py):
   - Add WebSocket route at /ws
   - Handle connect/disconnect
   - Ping/pong keep-alive
   - Error handling

6. **Update Mutation** (app/api/graphql/mutations.py):
   - Add WebSocket manager to context
   - Send notifications for high-confidence opportunities
   - Use Protobuf serialization

7. **Update Service** (app/services/opportunity_service.py):
   - Add `create_notification_message()` method
   - Check `should_notify()` before sending

**Deliverables:**
- [ ] Protobuf messages defined and generated
- [ ] WebSocket server running
- [ ] Connection manager working
- [ ] Notifications sent on opportunity creation
- [ ] Can connect with WebSocket client

**Test Commands:**
```bash
# Install websocat (WebSocket client)
# On Ubuntu:
sudo snap install websocat

# Connect to WebSocket
websocat ws://localhost:8000/ws

# In another terminal, create communication via GraphQL
# mutation { createCommunication(...) }

# Expected: Binary protobuf message received in websocat

# Test with browser console:
const ws = new WebSocket('ws://localhost:8000/ws');
ws.binaryType = 'arraybuffer';
ws.onmessage = (event) => {
  console.log('Received:', new Uint8Array(event.data));
};
```

**Success Criteria:**
✅ Protobuf code generated successfully
✅ WebSocket endpoint accepts connections
✅ Can connect with websocat/browser
✅ Notifications sent when opportunity created (confidence >= 70%)
✅ Binary protobuf messages received
✅ Connection manager tracks clients

Return WebSocket test results and sample notification payload.
```

### Verification Steps After Step 4

```bash
# 1. Generate protobuf
cd backend
python -m grpc_tools.protoc -I./app/protobuf --python_out=./app/protobuf ./app/protobuf/messages.proto
# Expected: messages_pb2.py created

# 2. Start server
uvicorn app.main:app --reload

# 3. Connect WebSocket
websocat ws://localhost:8000/ws
# Expected: Connection established

# 4. Create high-confidence opportunity
# GraphQL mutation with text that generates 70%+ confidence
# Expected: Binary message received in websocat

# 5. Check server logs
# Expected: "Client connected", "Sent notification to client"

# 6. Test multiple connections
# Open 2 websocat connections
# Create opportunity
# Expected: Both connections receive notification
```

### Expected Output
- ✅ WebSocket server running
- ✅ Can establish connections
- ✅ Notifications sent for high-value opportunities
- ✅ Binary protobuf format working
- ✅ Multiple clients supported

---

## Step 5: Frontend Foundation & Components (3-4 hours)

### Objective
Create React frontend with shadcn/ui components, following design system strictly.

### Agent Prompt

```
use context7

**Task:** Implement Step 5 - Frontend with Design System Compliance

**Read First:**
- docs/DESIGN_SYSTEM.md (ENTIRE FILE - MANDATORY)
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 1845-2290)

**Use Context7 for:**
- React 18 (hooks, state, effects)
- Vite (configuration, build)
- shadcn/ui (ALL components)
- Tailwind CSS 3+ (utilities, theme)
- TypeScript (types, interfaces)

**CRITICAL REQUIREMENTS:**
This is the most important step for visual quality.
You MUST follow docs/DESIGN_SYSTEM.md EXACTLY.

**What to Implement:**

1. **Project Setup:**
   ```bash
   npm create vite@latest frontend -- --template react-ts
   cd frontend
   npm install
   ```

2. **Install Dependencies:**
   - @apollo/client, graphql
   - shadcn/ui (button, card, dialog, input, textarea, badge, toast, select, label, skeleton)
   - Tailwind CSS
   - date-fns

3. **shadcn/ui Setup:**
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add button card dialog input textarea badge toast select label skeleton
   ```

4. **TypeScript Types** (src/types/index.ts):
   - All enums (CommunicationType, OpportunityType, OpportunityStatus)
   - Interfaces (Opportunity, Communication)

5. **Components** (src/components/):
   - **OpportunityCard.tsx:**
     - ✅ Use Card from shadcn/ui
     - ✅ Theme colors ONLY (bg-card, text-foreground, text-muted-foreground)
     - ✅ Dark mode variants (dark:bg-*, dark:text-*)
     - ✅ Spacing: space-y-2, space-y-4, gap-4
     - ✅ Typography: text-lg font-semibold, text-base, text-sm
     - ✅ Badge with confidence color coding
     - ✅ Type badge with semantic colors + dark mode
     - ✅ Border radius: rounded-lg (card), rounded-md (badges)
     - ✅ Transition: transition-colors duration-200

   - **UploadModal.tsx:**
     - ✅ Use Dialog from shadcn/ui
     - ✅ Form with space-y-4
     - ✅ Label with text-sm font-medium
     - ✅ Input/Textarea from shadcn
     - ✅ Button variants (default, outline)
     - ✅ Validation (min 50 chars)
     - ✅ Loading state
     - ✅ Toast notifications

6. **Main App** (src/App.tsx):
   - ✅ Background: bg-background (NOT bg-gray-50)
   - ✅ Header: bg-card, border-border
   - ✅ Container: max-w-7xl mx-auto px-4
   - ✅ Grid: grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4
   - ✅ Stats cards with theme colors
   - ✅ Loading skeleton (bg-muted, animate-pulse)
   - ✅ Empty state (text-muted-foreground)
   - ✅ Responsive: flex-col md:flex-row

7. **Design System Verification:**
   Before returning, verify EVERY component against checklist:
   - [ ] No hardcoded colors (no bg-white, text-black, bg-gray-*)
   - [ ] All colors use theme variables
   - [ ] Dark mode variants present
   - [ ] Consistent spacing (p-6, gap-4, space-y-4)
   - [ ] Correct typography scale
   - [ ] Only shadcn/ui components
   - [ ] Only Tailwind utilities (no custom CSS)
   - [ ] Mobile-first responsive

**Deliverables:**
- [ ] Complete React + Vite project
- [ ] All shadcn/ui components installed
- [ ] OpportunityCard component (design system compliant)
- [ ] UploadModal component (design system compliant)
- [ ] App.tsx with layout (design system compliant)
- [ ] TypeScript types defined
- [ ] No console errors

**Test Commands:**
```bash
cd frontend
npm run dev

# Visit http://localhost:5173
# Check DevTools:
# - No console errors
# - Verify CSS variables used (not hardcoded colors)
# - Test dark mode toggle (if implemented)
```

**Success Criteria:**
✅ UI loads without errors
✅ All colors use theme variables (verify in DevTools)
✅ Dark mode support implemented
✅ Responsive on mobile/tablet/desktop
✅ Only shadcn components used
✅ No custom CSS files
✅ Typography follows scale
✅ Spacing is consistent

**BEFORE RETURNING:**
Review EVERY component line-by-line against docs/DESIGN_SYSTEM.md.
Report any deviations with justification.
```

### Verification Steps After Step 5

```bash
# 1. Start frontend
cd frontend
npm run dev
# Expected: Vite dev server on port 5173

# 2. Open in browser
# http://localhost:5173
# Expected: UI loads without errors

# 3. Check DevTools Console
# Expected: No errors

# 4. Inspect element colors
# Right-click any element → Inspect
# Check computed styles
# Expected: Colors use CSS variables (--background, --foreground, etc.)
# NOT hardcoded (#ffffff, rgb(255,255,255))

# 5. Test responsive
# DevTools → Toggle device toolbar
# Test mobile (375px), tablet (768px), desktop (1024px)
# Expected: Layout adapts properly

# 6. Verify design system
# Check each component:
grep -r "bg-white" src/  # Should return NOTHING
grep -r "bg-gray-50" src/  # Should return NOTHING
grep -r "text-black" src/  # Should return NOTHING
# If any found, design system violated!

# Expected: All use bg-background, bg-card, text-foreground, etc.
```

### Expected Output
- ✅ Clean, professional UI
- ✅ All theme colors used correctly
- ✅ Dark mode ready
- ✅ Fully responsive
- ✅ No design system violations
- ✅ Loading/empty states present

---

## Step 6: Frontend Integration & Final Polish (2-3 hours)

### Objective
Connect frontend to backend, integrate Apollo Client, WebSocket with Protobuf, final testing.

### Agent Prompt

```
use context7

**Task:** Implement Step 6 - Frontend Integration & Complete E2E Flow

**Read First:**
- docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 1930-2709 - Apollo & WebSocket)
- docs/DESIGN_SYSTEM.md (verify all components)

**Use Context7 for:**
- Apollo Client 3+ (queries, mutations, cache, hooks)
- WebSocket API (browser native)
- protobufjs (JavaScript protobuf decoding)

**What to Implement:**

1. **Apollo Client Setup** (src/graphql/client.ts):
   - Create Apollo Client with HTTP link
   - InMemoryCache configuration
   - Network-only fetch policy

2. **GraphQL Operations:**
   - **Queries** (src/graphql/queries.ts):
     - GET_OPPORTUNITIES
     - GET_OPPORTUNITY_STATS
   - **Mutations** (src/graphql/mutations.ts):
     - CREATE_COMMUNICATION

3. **WebSocket Hook** (src/hooks/useWebSocket.ts):
   - Connect to ws://localhost:8000/ws
   - Handle binary protobuf messages
   - Auto-reconnect on disconnect
   - Decode OpportunityNotification
   - Return isConnected, lastNotification

4. **Protobuf Setup:**
   - Copy messages.proto from backend
   - Generate JavaScript:
     ```bash
     npm install -g protobufjs-cli
     pbjs -t static-module -w es6 -o src/lib/messages.js src/lib/messages.proto
     pbts -o src/lib/messages.d.ts src/lib/messages.js
     ```

5. **Connect App.tsx:**
   - Import useQuery for opportunities and stats
   - Implement useWebSocket hook
   - useEffect to show toast on notification
   - Refetch opportunities on notification
   - Handle loading/error states

6. **Connect UploadModal:**
   - Use useMutation for CREATE_COMMUNICATION
   - Handle success (show toast, close modal, refetch)
   - Handle errors (show error toast)
   - Form validation
   - Clear form on success

7. **Main Entry** (src/main.tsx):
   - Wrap app in ApolloProvider
   - Add Toaster component
   - Import global CSS

8. **Environment Variables:**
   - Create .env:
     ```
     VITE_API_URL=http://localhost:8000
     VITE_WS_URL=ws://localhost:8000/ws
     ```

9. **Final Testing:**
   - End-to-end flow test
   - Error handling test
   - WebSocket reconnection test
   - Dark mode test (if implemented)

**Deliverables:**
- [ ] Apollo Client integrated
- [ ] GraphQL queries/mutations working
- [ ] WebSocket receiving notifications
- [ ] Protobuf decoding working
- [ ] Full E2E flow functional
- [ ] Toast notifications working
- [ ] Error handling complete

**Test Commands:**
```bash
# 1. Start backend
cd backend
uvicorn app.main:app --reload

# 2. Start frontend
cd frontend
npm run dev

# 3. E2E Test Flow:
# - Open http://localhost:5173
# - Click "Upload Communication"
# - Paste sample text:
"Hi team, we're opening a Chicago office next month and need help with the lease.
Also hiring 20 people, so employment contracts needed."
# - Click Analyze
# - Wait for processing
# - Verify:
#   ✓ Toast appears: "Found X opportunities"
#   ✓ Opportunities appear in grid
#   ✓ Stats update
#   ✓ WebSocket badge shows "Connected"
#   ✓ If high confidence, notification toast appears

# 4. Test WebSocket in DevTools Console:
const ws = new WebSocket('ws://localhost:8000/ws');
ws.binaryType = 'arraybuffer';
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', new Uint8Array(e.data));

# 5. Test error handling:
# - Stop backend
# - Try to upload
# - Verify: Error toast appears
# - Start backend
# - Verify: WebSocket reconnects
```

**Success Criteria:**
✅ Can upload communication via UI
✅ AI analyzes and extracts opportunities
✅ Opportunities appear in dashboard immediately
✅ WebSocket notification received (for high confidence)
✅ Toast notifications work correctly
✅ Stats update in real-time
✅ Error handling graceful
✅ WebSocket auto-reconnects
✅ No console errors
✅ Full dark mode support (if implemented)

**Final Quality Check:**
- Run through complete user flow 3 times
- Test with different communications
- Verify all design system rules followed
- Check performance (API <200ms, AI <5s)
- Verify no memory leaks

Return complete E2E test results and performance metrics.
```

### Verification Steps After Step 6

```bash
# 1. Start full stack
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev

# 2. E2E Test
# Open http://localhost:5173
# Upload communication
# Expected: Full flow works

# 3. Performance Test
# Open DevTools → Network tab
# Upload communication
# Check timings:
# - GraphQL mutation: <2s (including AI processing)
# - WebSocket latency: <100ms
# - Page load: <2s

# 4. Verify data flow
# Check database:
docker-compose exec db psql -U nexl -d nexl_opportunities -c "SELECT COUNT(*) FROM opportunities;"
# Expected: Count increases after each upload

# 5. WebSocket stress test
# Open 3 browser tabs to http://localhost:5173
# Upload in one tab
# Expected: All tabs receive notification (if high confidence)

# 6. Final design system check
# Review all components in browser
# Expected: Consistent colors, spacing, typography
```

### Expected Output
- ✅ Complete working application
- ✅ End-to-end flow functional
- ✅ Real-time notifications working
- ✅ Performance within targets
- ✅ Error handling robust
- ✅ Professional UI/UX

---

## Summary of 6 Steps

| Step | Focus | Time | Testable Output |
|------|-------|------|----------------|
| 1 | Database & Models | 2-3h | Tables created, migrations work |
| 2 | GraphQL API | 2-3h | Queries work in playground |
| 3 | AI Integration | 3-4h | Opportunities extracted from text |
| 4 | WebSocket & Protobuf | 2-3h | Real-time notifications sent |
| 5 | Frontend Components | 3-4h | UI components with design system |
| 6 | Integration & Polish | 2-3h | Full E2E flow working |
| **Total** | **Full Stack** | **14-20h** | **Production-ready MVP** |

---

## Benefits of 6-Step Approach

### ✅ Advantages
1. **Testable Increments** - Verify each step before proceeding
2. **Early Issue Detection** - Catch problems before they compound
3. **Flexible Pacing** - Can pause between steps
4. **Clear Progress** - Know exactly what's done
5. **Parallel Work** - Different steps can be done by different people/agents
6. **Risk Mitigation** - Each step is independently verified

### ✅ Quality Gates
After each step, you can:
- Run tests
- Manual verification
- Code review
- Performance check
- Decide to refactor before continuing

### ✅ Rollback Strategy
If a step fails:
- Previous steps are still intact
- Can rollback database migrations
- Can restart from last successful step
- Git commits per step for version control

---

## Progress Tracking

### Checklist

- [ ] **Step 1 Complete:** Database & Models ✓
- [ ] **Step 2 Complete:** GraphQL API ✓
- [ ] **Step 3 Complete:** AI Integration ✓
- [ ] **Step 4 Complete:** WebSocket ✓
- [ ] **Step 5 Complete:** Frontend Components ✓
- [ ] **Step 6 Complete:** Integration & Polish ✓

### Git Commit Strategy

```bash
# After each step
git add .
git commit -m "Step X: [Description] - [Test Results]"

# Examples:
git commit -m "Step 1: Database models and migrations - All tables created successfully"
git commit -m "Step 2: GraphQL API foundation - Queries working, 5/5 tests passing"
git commit -m "Step 3: AI integration - OpenAI detecting 2-3 opportunities per sample"
# etc.
```

---

## Troubleshooting by Step

### Step 1 Issues
- **Database won't start:** Check Docker, verify port 5432 free
- **Migration fails:** Check alembic.ini DATABASE_URL
- **Import errors:** Verify virtual environment activated

### Step 2 Issues
- **GraphQL errors:** Check schema syntax, imports
- **CORS errors:** Verify CORS_ORIGINS in .env
- **Can't connect:** Check server running on port 8000

### Step 3 Issues
- **OpenAI API errors:** Verify API key, check credits
- **Validation fails:** Check response format from OpenAI
- **Opportunities not saving:** Check transaction commit

### Step 4 Issues
- **Protobuf generation fails:** Install grpcio-tools
- **WebSocket won't connect:** Check ws:// protocol (not http://)
- **No notifications:** Verify confidence >= 70%

### Step 5 Issues
- **shadcn install fails:** Check Node.js version (18+)
- **Import errors:** Verify @/ alias in tsconfig.json
- **Design system violations:** Review docs/DESIGN_SYSTEM.md

### Step 6 Issues
- **Apollo errors:** Check API URL in .env
- **Protobuf decode fails:** Verify messages.proto matches backend
- **WebSocket reconnect loop:** Check error handling

---

## Next Steps After All 6 Steps

1. **Documentation:**
   - Update README with setup instructions
   - Add API documentation
   - Create user guide

2. **Deployment:**
   - Create production Dockerfiles
   - Set up environment variables
   - Deploy to cloud (Railway, Vercel, etc.)

3. **Enhancements:**
   - Add authentication
   - Implement filtering UI
   - Add pagination
   - Improve AI prompts
   - Add caching layer

4. **Monitoring:**
   - Add logging
   - Set up error tracking (Sentry)
   - Add analytics
   - Performance monitoring

---

**Document Version:** 1.0
**Last Updated:** November 4, 2025
**Estimated Total Time:** 14-20 hours (over 3-4 days)

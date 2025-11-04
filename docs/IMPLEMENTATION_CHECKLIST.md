# Implementation Checklist
## Smart Matter Opportunity Detector - 3-Day Task List

**Version:** 1.0  
**Last Updated:** November 4, 2025  
**Total Estimated Time:** 24 hours (3 days × 8 hours)

---

## How to Use This Checklist

- [ ] Mark tasks as complete using checkboxes
- ⏱️ Time estimates are guidelines, adjust as needed
- 🔴 = Critical path item (must be done before other tasks)
- 🟡 = Important but can be adjusted
- 🟢 = Nice to have, can be skipped if time-constrained

---

## Pre-Implementation (Day 0) - 30 minutes

### Environment Setup
- [ ] ⏱️ 10 min - Install Docker Desktop
- [ ] ⏱️ 5 min - Install Python 3.11+
- [ ] ⏱️ 5 min - Install Node.js 18+
- [ ] ⏱️ 5 min - Get OpenAI API key from platform.openai.com
- [ ] ⏱️ 5 min - Install VS Code / Cursor with Python and TypeScript extensions

**Total: 30 minutes**

---

## DAY 1: Backend Foundation (8 hours)

### 🔴 Phase 1.1: Project Setup (30 min)

#### 1.1.1 Project Structure
- [ ] ⏱️ 5 min - Create root project directory
- [ ] ⏱️ 10 min - Create backend folder structure
  ```
  backend/
  ├── app/
  │   ├── api/graphql/
  │   ├── models/
  │   ├── services/
  │   ├── websocket/
  │   ├── protobuf/
  │   └── utils/
  ├── tests/
  └── alembic/
  ```
- [ ] ⏱️ 5 min - Create frontend folder structure
- [ ] ⏱️ 5 min - Initialize Git repository
- [ ] ⏱️ 5 min - Create .gitignore file

#### 1.1.2 Docker Setup
- [ ] ⏱️ 10 min - Create docker-compose.yml for PostgreSQL
- [ ] ⏱️ 5 min - Test PostgreSQL container starts
- [ ] ⏱️ 5 min - Create backend Dockerfile (if using Docker)

**Subtotal: 50 minutes** (includes buffer)

---

### 🔴 Phase 1.2: Database Layer (90 min)

#### 1.2.1 Python Environment
- [ ] ⏱️ 5 min - Create Python virtual environment
- [ ] ⏱️ 10 min - Create requirements.txt with all dependencies
- [ ] ⏱️ 10 min - Install dependencies via pip
- [ ] ⏱️ 5 min - Create .env file with DATABASE_URL and OPENAI_API_KEY

#### 1.2.2 SQLAlchemy Models
- [ ] ⏱️ 15 min - Create `models/base.py` with Base class
- [ ] ⏱️ 20 min - Create `models/communication.py` with Communication model
- [ ] ⏱️ 20 min - Create `models/opportunity.py` with Opportunity model
- [ ] ⏱️ 5 min - Create `models/__init__.py` to export models

#### 1.2.3 Database Connection
- [ ] ⏱️ 15 min - Create `utils/database.py` with async engine setup
- [ ] ⏱️ 10 min - Implement get_db dependency function
- [ ] ⏱️ 10 min - Test database connection works

**Subtotal: 110 minutes**

---

### 🔴 Phase 1.3: Alembic Migrations (30 min)

- [ ] ⏱️ 5 min - Initialize Alembic
- [ ] ⏱️ 10 min - Configure alembic.ini with DATABASE_URL
- [ ] ⏱️ 10 min - Update alembic/env.py to import models
- [ ] ⏱️ 10 min - Generate initial migration
- [ ] ⏱️ 5 min - Run migration and verify tables created
- [ ] ⏱️ 5 min - Test rollback works

**Subtotal: 45 minutes** (includes testing)

---

### 🔴 Phase 1.4: GraphQL API Setup (120 min)

#### 1.4.1 GraphQL Types
- [ ] ⏱️ 30 min - Create `api/graphql/types.py` with all Strawberry types:
  - [ ] Communication type
  - [ ] Opportunity type
  - [ ] Enums (CommunicationType, OpportunityType, OpportunityStatus)
  - [ ] Connection types (OpportunityConnection, OpportunityEdge, PageInfo)
  - [ ] Input types (CreateCommunicationInput)
  - [ ] Stats types (OpportunityStats, TypeCount)

#### 1.4.2 Query Resolvers
- [ ] ⏱️ 30 min - Create `api/graphql/queries.py`:
  - [ ] opportunities query with filters
  - [ ] opportunity query (single)
  - [ ] opportunityStats query
  - [ ] Helper function: convert_opportunity_to_gql

#### 1.4.3 Mutation Resolvers (Stub)
- [ ] ⏱️ 10 min - Create `api/graphql/mutations.py`:
  - [ ] createCommunication mutation (stub for now)
  - [ ] Return dummy data to test schema

#### 1.4.4 Schema & FastAPI Integration
- [ ] ⏱️ 20 min - Create `api/graphql/schema.py` with Strawberry schema
- [ ] ⏱️ 20 min - Create `main.py` with FastAPI app:
  - [ ] Add CORS middleware
  - [ ] Add GraphQL router
  - [ ] Add health check endpoint
  - [ ] Add get_context function for DB session
- [ ] ⏱️ 10 min - Test server starts without errors

**Subtotal: 120 minutes**

---

### 🟡 Phase 1.5: Basic Testing (60 min)

#### 1.5.1 Test Setup
- [ ] ⏱️ 20 min - Create `tests/conftest.py`:
  - [ ] Event loop fixture
  - [ ] Test database fixture
  - [ ] Test client fixture
- [ ] ⏱️ 10 min - Create pytest.ini configuration

#### 1.5.2 Write Tests
- [ ] ⏱️ 15 min - Create `tests/test_api/test_graphql.py`:
  - [ ] Test health endpoint
  - [ ] Test opportunityStats query returns 0
- [ ] ⏱️ 10 min - Create `tests/test_models/test_opportunity.py`:
  - [ ] Test Opportunity model creation
- [ ] ⏱️ 10 min - Run tests and fix any issues

**Subtotal: 65 minutes**

---

### Day 1 Wrap-up (15 min)

- [ ] ⏱️ 5 min - Manual test GraphQL playground at http://localhost:8000/graphql
- [ ] ⏱️ 5 min - Run all tests: `pytest -v`
- [ ] ⏱️ 5 min - Git commit: "Day 1: Database, GraphQL API, and testing"
- [ ] ⏱️ 5 min - Review Day 2 plan

**Day 1 Total: ~480 minutes (8 hours)**

---

## DAY 2: AI Integration & WebSocket (8 hours)

### 🔴 Phase 2.1: Protobuf Setup (45 min)

#### 2.1.1 Protobuf Definitions
- [ ] ⏱️ 20 min - Create `protobuf/messages.proto`:
  - [ ] OpportunityNotification message
  - [ ] OpportunityType enum
  - [ ] AnalysisRequest message
  - [ ] AnalysisResponse message
  - [ ] ExtractedOpportunity message

#### 2.1.2 Generate Python Code
- [ ] ⏱️ 5 min - Install grpcio-tools
- [ ] ⏱️ 5 min - Generate messages_pb2.py from .proto file
- [ ] ⏱️ 5 min - Verify generated file imports correctly

#### 2.1.3 Helper Functions
- [ ] ⏱️ 15 min - Create `protobuf/helpers.py`:
  - [ ] create_opportunity_notification function
  - [ ] parse_opportunity_notification function
  - [ ] Enum mapping dictionary
- [ ] ⏱️ 5 min - Test protobuf serialization/deserialization

**Subtotal: 55 minutes**

---

### 🔴 Phase 2.2: OpenAI Integration (120 min)

#### 2.2.1 AI Service Base
- [ ] ⏱️ 30 min - Create `services/ai_service.py`:
  - [ ] OpportunityDetector class
  - [ ] __init__ with OpenAI client
  - [ ] _get_system_prompt method
  - [ ] _build_prompt method

#### 2.2.2 Analysis Logic
- [ ] ⏱️ 40 min - Implement analyze_communication method:
  - [ ] OpenAI API call with structured output
  - [ ] JSON parsing
  - [ ] Validation logic
  - [ ] Error handling
- [ ] ⏱️ 10 min - Implement _validate_opportunities method:
  - [ ] Type validation
  - [ ] Confidence score validation
  - [ ] Required field checks

#### 2.2.3 Retry Logic
- [ ] ⏱️ 15 min - Add @retry decorator with tenacity
- [ ] ⏱️ 10 min - Create AIServiceError exception class
- [ ] ⏱️ 10 min - Add comprehensive logging

#### 2.2.4 Testing
- [ ] ⏱️ 15 min - Create manual_test.py script
- [ ] ⏱️ 10 min - Test with 3-5 sample communications
- [ ] ⏱️ 10 min - Verify opportunity extraction works

**Subtotal: 140 minutes**

---

### 🔴 Phase 2.3: Opportunity Service (60 min)

#### 2.3.1 Service Layer
- [ ] ⏱️ 30 min - Create `services/opportunity_service.py`:
  - [ ] OpportunityService class
  - [ ] create_communication_with_opportunities method
  - [ ] Type mapping from AI output to DB enum
  - [ ] Database transaction handling

#### 2.3.2 Notification Logic
- [ ] ⏱️ 15 min - Add should_notify method (confidence >= 70%)
- [ ] ⏱️ 10 min - Add create_notification_message method
- [ ] ⏱️ 10 min - Add logging throughout

**Subtotal: 65 minutes**

---

### 🔴 Phase 2.4: Update GraphQL Mutation (45 min)

- [ ] ⏱️ 25 min - Update `api/graphql/mutations.py`:
  - [ ] Import OpportunityDetector and OpportunityService
  - [ ] Implement createCommunication mutation logic
  - [ ] Add input validation
  - [ ] Call AI service
  - [ ] Send WebSocket notification (stub for now)
  - [ ] Return GraphQL types
- [ ] ⏱️ 10 min - Create helper functions:
  - [ ] convert_communication_to_gql
  - [ ] convert_opportunity_to_gql
- [ ] ⏱️ 10 min - Test mutation via GraphQL playground

**Subtotal: 45 minutes**

---

### 🔴 Phase 2.5: WebSocket Implementation (90 min)

#### 2.5.1 Connection Manager
- [ ] ⏱️ 30 min - Create `websocket/manager.py`:
  - [ ] ConnectionManager class
  - [ ] connect method
  - [ ] disconnect method
  - [ ] broadcast method
  - [ ] send_to_client method

#### 2.5.2 FastAPI Integration
- [ ] ⏱️ 20 min - Update `main.py`:
  - [ ] Import ConnectionManager
  - [ ] Create global manager instance
  - [ ] Add WebSocket endpoint /ws
  - [ ] Handle ping/pong
  - [ ] Add manager to GraphQL context

#### 2.5.3 Connect Notification Flow
- [ ] ⏱️ 20 min - Update mutation to actually send WebSocket messages
- [ ] ⏱️ 10 min - Add logging for WebSocket events

#### 2.5.4 Testing
- [ ] ⏱️ 15 min - Test WebSocket connection with websocat or browser
- [ ] ⏱️ 10 min - Verify notifications sent when opportunity created

**Subtotal: 105 minutes**

---

### 🟡 Phase 2.6: Integration Testing (60 min)

- [ ] ⏱️ 30 min - Create `tests/test_integration.py`:
  - [ ] test_create_communication_with_ai_analysis
  - [ ] test_query_opportunities_with_filters
  - [ ] Mock OpenAI for tests
- [ ] ⏱️ 15 min - Run integration tests
- [ ] ⏱️ 15 min - Fix any failing tests

**Subtotal: 60 minutes**

---

### Day 2 Wrap-up (15 min)

- [ ] ⏱️ 5 min - End-to-end manual test:
  - [ ] Start server
  - [ ] Create communication via GraphQL
  - [ ] Verify opportunities in database
  - [ ] Check WebSocket logs
- [ ] ⏱️ 5 min - Run all tests: `pytest -v`
- [ ] ⏱️ 5 min - Git commit: "Day 2: AI integration, Protobuf, WebSocket"
- [ ] ⏱️ 5 min - Review Day 3 plan

**Day 2 Total: ~480 minutes (8 hours)**

---

## DAY 3: Frontend & Polish (8 hours)

### 🔴 Phase 3.1: Frontend Project Setup (45 min)

#### 3.1.1 Vite + React
- [ ] ⏱️ 10 min - Initialize Vite project with React + TypeScript
- [ ] ⏱️ 5 min - Clean up boilerplate files
- [ ] ⏱️ 5 min - Create .env file with API URLs

#### 3.1.2 Install Dependencies
- [ ] ⏱️ 15 min - Install all npm packages:
  - [ ] @apollo/client, graphql
  - [ ] zustand
  - [ ] date-fns
  - [ ] protobufjs
- [ ] ⏱️ 10 min - Initialize shadcn/ui:
  - [ ] Run init command
  - [ ] Install components (button, card, dialog, input, textarea, badge, toast, select)

#### 3.1.3 Project Structure
- [ ] ⏱️ 5 min - Create folder structure:
  ```
  src/
  ├── components/
  ├── graphql/
  ├── hooks/
  ├── lib/
  ├── stores/
  └── types/
  ```

**Subtotal: 50 minutes**

---

### 🔴 Phase 3.2: Types & GraphQL Client (45 min)

#### 3.2.1 TypeScript Types
- [ ] ⏱️ 15 min - Create `types/index.ts`:
  - [ ] All enums (CommunicationType, OpportunityType, OpportunityStatus)
  - [ ] Opportunity interface
  - [ ] Communication interface

#### 3.2.2 Apollo Client
- [ ] ⏱️ 10 min - Create `graphql/client.ts` with Apollo setup
- [ ] ⏱️ 15 min - Create `graphql/queries.ts`:
  - [ ] GET_OPPORTUNITIES query
  - [ ] GET_OPPORTUNITY_STATS query
- [ ] ⏱️ 10 min - Create `graphql/mutations.ts`:
  - [ ] CREATE_COMMUNICATION mutation

**Subtotal: 50 minutes**

---

### 🔴 Phase 3.3: Protobuf Client Setup (60 min)

- [ ] ⏱️ 10 min - Copy messages.proto from backend to frontend
- [ ] ⏱️ 10 min - Generate JavaScript from .proto:
  - [ ] Install protobufjs-cli globally
  - [ ] Run pbjs command
  - [ ] Run pbts command
- [ ] ⏱️ 10 min - Test protobuf import works
- [ ] ⏱️ 30 min - Create `hooks/useWebSocket.ts`:
  - [ ] WebSocket connection logic
  - [ ] Protobuf decoding
  - [ ] Auto-reconnect on disconnect
  - [ ] Return isConnected and lastNotification

**Subtotal: 60 minutes**

---

### 🔴 Phase 3.4: UI Components (180 min)

#### 3.4.1 OpportunityCard Component
- [ ] ⏱️ 40 min - Create `components/OpportunityCard.tsx`:
  - [ ] Card layout with shadcn Card
  - [ ] Display all opportunity fields
  - [ ] Color-coded confidence badges
  - [ ] Type-specific badge colors
  - [ ] Relative time display (date-fns)
  - [ ] Truncated extracted text
  - [ ] Hover effects

#### 3.4.2 UploadModal Component
- [ ] ⏱️ 60 min - Create `components/UploadModal.tsx`:
  - [ ] Dialog wrapper
  - [ ] Form with controlled inputs
  - [ ] Client name input
  - [ ] Source type select
  - [ ] Content textarea with character count
  - [ ] Validation (min 50 chars)
  - [ ] Apollo useMutation hook
  - [ ] Loading state
  - [ ] Success/error toasts
  - [ ] Clear form on success

#### 3.4.3 Dashboard Layout
- [ ] ⏱️ 40 min - Update `App.tsx`:
  - [ ] Header with title and Upload button
  - [ ] WebSocket connection badge
  - [ ] Stats cards (total, high confidence, this week)
  - [ ] Opportunity grid layout
  - [ ] Loading state
  - [ ] Empty state
  - [ ] useQuery for opportunities and stats

#### 3.4.4 Real-time Integration
- [ ] ⏱️ 20 min - Integrate useWebSocket in App:
  - [ ] Call useWebSocket hook
  - [ ] useEffect to watch lastNotification
  - [ ] Show toast on new notification
  - [ ] Refetch opportunities on notification

#### 3.4.5 Main Entry Point
- [ ] ⏱️ 15 min - Update `main.tsx`:
  - [ ] Wrap app in ApolloProvider
  - [ ] Add Toaster component
  - [ ] Import global CSS

**Subtotal: 175 minutes**

---

### 🟡 Phase 3.5: Styling & UX Polish (60 min)

- [ ] ⏱️ 20 min - Add responsive design tweaks
- [ ] ⏱️ 15 min - Improve loading states and transitions
- [ ] ⏱️ 15 min - Add error boundaries (optional)
- [ ] ⏱️ 10 min - Test on different screen sizes
- [ ] ⏱️ 10 min - Fix any UI bugs

**Subtotal: 70 minutes**

---

### 🔴 Phase 3.6: Integration & Testing (60 min)

#### 3.6.1 End-to-End Testing
- [ ] ⏱️ 15 min - Test complete flow:
  1. Upload communication
  2. Wait for analysis
  3. See opportunities appear
  4. Verify WebSocket notification
  5. Check stats update
- [ ] ⏱️ 10 min - Test error cases:
  - [ ] Invalid input
  - [ ] Network errors
  - [ ] OpenAI API failure

#### 3.6.2 Performance Check
- [ ] ⏱️ 10 min - Check page load time
- [ ] ⏱️ 10 min - Verify WebSocket doesn't leak memory
- [ ] ⏱️ 5 min - Check console for errors

#### 3.6.3 Browser Testing
- [ ] ⏱️ 10 min - Test in Chrome
- [ ] ⏱️ 5 min - Test in Firefox (optional)

**Subtotal: 65 minutes**

---

### 🔴 Phase 3.7: Docker & Documentation (60 min)

#### 3.7.1 Docker Setup
- [ ] ⏱️ 15 min - Create backend Dockerfile
- [ ] ⏱️ 15 min - Create frontend Dockerfile
- [ ] ⏱️ 15 min - Update docker-compose.yml with all services
- [ ] ⏱️ 10 min - Test `docker-compose up` works

#### 3.7.2 Documentation
- [ ] ⏱️ 30 min - Create comprehensive README.md:
  - [ ] Project description
  - [ ] Features list
  - [ ] Tech stack
  - [ ] Setup instructions
  - [ ] Architecture diagram (text-based)
  - [ ] API documentation link
  - [ ] Development guide
  - [ ] Troubleshooting section
- [ ] ⏱️ 10 min - Create .env.example files for backend and frontend

**Subtotal: 85 minutes**

---

### Day 3 Wrap-up (30 min)

- [ ] ⏱️ 10 min - Final end-to-end test with Docker Compose
- [ ] ⏱️ 5 min - Create demo script (what to say during demo)
- [ ] ⏱️ 5 min - Test from fresh clone (if time permits)
- [ ] ⏱️ 5 min - Git commit: "Day 3: Frontend, integration, documentation"
- [ ] ⏱️ 5 min - Tag release: `git tag v1.0.0-mvp`
- [ ] ⏱️ 5 min - Prepare demo (test sample data)

**Day 3 Total: ~480 minutes (8 hours)**

---

## Post-Implementation Checklist

### 🟢 Optional Enhancements (if time permits)

- [ ] ⏱️ 30 min - Add opportunity filtering UI (by type, confidence)
- [ ] ⏱️ 20 min - Add sorting options (confidence, date)
- [ ] ⏱️ 30 min - Add opportunity detail modal/page
- [ ] ⏱️ 45 min - Deploy to Heroku/Railway/Vercel
- [ ] ⏱️ 20 min - Add basic authentication
- [ ] ⏱️ 30 min - Add Redis caching layer
- [ ] ⏱️ 60 min - Improve test coverage to 80%+

### Demo Preparation

- [ ] ⏱️ 15 min - Prepare 2-3 sample client communications
- [ ] ⏱️ 10 min - Practice demo flow (under 5 minutes)
- [ ] ⏱️ 10 min - Prepare talking points about architecture
- [ ] ⏱️ 5 min - Screenshot key features
- [ ] ⏱️ 10 min - Record demo video (optional)

---

## Quality Assurance Checklist

### Code Quality
- [ ] All files have clear, descriptive names
- [ ] Functions are small and single-purpose
- [ ] No code duplication (DRY principle)
- [ ] Proper error handling everywhere
- [ ] Meaningful variable names
- [ ] No commented-out code
- [ ] Type hints in Python
- [ ] TypeScript types for frontend

### Testing
- [ ] Unit tests for critical functions
- [ ] Integration tests for main flows
- [ ] Tests have clear names
- [ ] Tests actually test something meaningful
- [ ] All tests pass

### Documentation
- [ ] README is clear and complete
- [ ] Environment variables documented
- [ ] Setup steps work from scratch
- [ ] Code has comments where needed (not obvious code)
- [ ] API endpoints documented

### Performance
- [ ] No N+1 queries
- [ ] Database indexes on queried columns
- [ ] API responses under 200ms
- [ ] Frontend loads in under 2 seconds
- [ ] WebSocket doesn't drop connections

### Security
- [ ] No API keys committed to git
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (using ORM)
- [ ] CORS configured correctly
- [ ] No sensitive data in logs

---

## Time Tracking Summary

| Day | Phase | Estimated | Buffer | Total |
|-----|-------|-----------|--------|-------|
| Day 1 | Backend Setup | 360 min | 60 min | 420 min |
| Day 2 | AI & WebSocket | 410 min | 50 min | 460 min |
| Day 3 | Frontend & Polish | 430 min | 50 min | 480 min |
| **Total** | **All Phases** | **1200 min** | **160 min** | **1360 min** |

**Note:** Estimates include buffer time for debugging and unexpected issues.

---

## Risk Mitigation Checklist

### High-Risk Items (Address First)

- [ ] OpenAI API key valid and has credits
- [ ] PostgreSQL accessible and running
- [ ] Node.js and Python versions compatible
- [ ] Docker installed and working
- [ ] Network allows WebSocket connections
- [ ] CORS properly configured

### Common Failure Points

- [ ] Check: Database migrations applied
- [ ] Check: Environment variables loaded
- [ ] Check: All dependencies installed
- [ ] Check: Ports not in use (5432, 8000, 5173)
- [ ] Check: OpenAI rate limits not hit
- [ ] Check: WebSocket URL uses 'ws://' not 'http://'

---

## Daily Progress Tracking

### End of Day 1
**Expected Deliverables:**
- ✅ PostgreSQL database running
- ✅ SQLAlchemy models defined
- ✅ GraphQL API responding
- ✅ Basic tests passing
- ✅ Can query empty opportunities

**Checkpoint Questions:**
- [ ] Can I start the server without errors?
- [ ] Does GraphQL playground load?
- [ ] Do queries return data (even if empty)?
- [ ] Are tests passing?

---

### End of Day 2
**Expected Deliverables:**
- ✅ OpenAI integration working
- ✅ Can create communications
- ✅ Opportunities extracted and saved
- ✅ WebSocket server running
- ✅ Notifications sent to clients
- ✅ Protobuf messages working

**Checkpoint Questions:**
- [ ] Can I create a communication via GraphQL?
- [ ] Are opportunities detected correctly?
- [ ] Can I connect to WebSocket?
- [ ] Are notifications received?
- [ ] Are all integration tests passing?

---

### End of Day 3
**Expected Deliverables:**
- ✅ React frontend running
- ✅ Can upload communications via UI
- ✅ Opportunities display correctly
- ✅ Real-time notifications working
- ✅ Docker Compose starts all services
- ✅ README complete

**Checkpoint Questions:**
- [ ] Does the full stack run with docker-compose up?
- [ ] Can I upload a communication and see results?
- [ ] Do WebSocket notifications appear as toasts?
- [ ] Is the UI polished and professional?
- [ ] Can someone else run it using just the README?

---

## Success Criteria (Final Check)

### Functional
- [ ] ✅ Upload communication → AI analyzes → Opportunities appear
- [ ] ✅ Opportunities display with correct confidence and type
- [ ] ✅ GraphQL queries work (opportunities, stats)
- [ ] ✅ WebSocket pushes notifications
- [ ] ✅ Frontend shows real-time updates
- [ ] ✅ No critical bugs or crashes

### Technical
- [ ] ✅ Code follows SOLID principles
- [ ] ✅ DRY - no repeated code
- [ ] ✅ YAGNI - no over-engineering
- [ ] ✅ Clean architecture (layers separated)
- [ ] ✅ Proper error handling
- [ ] ✅ Tests cover critical paths

### Presentation
- [ ] ✅ Professional UI
- [ ] ✅ Clear documentation
- [ ] ✅ Easy to run (docker-compose up)
- [ ] ✅ Demo-ready
- [ ] ✅ Git history clean and organized

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Port already in use | `docker-compose down` or kill process |
| Database connection error | Check DATABASE_URL, ensure PostgreSQL running |
| OpenAI API error | Verify API key, check credits |
| WebSocket won't connect | Check ws:// protocol, ensure server running |
| Frontend 404 errors | Check VITE_API_URL in .env |
| CORS error | Add frontend URL to CORS_ORIGINS |
| Tests failing | Check test database exists, migrations applied |
| Docker build fails | Clear Docker cache: `docker system prune` |

---

## Notes Section (Use During Implementation)

### Day 1 Notes
```
[Space for notes, issues encountered, time adjustments]
```

### Day 2 Notes
```
[Space for notes, issues encountered, time adjustments]
```

### Day 3 Notes
```
[Space for notes, issues encountered, time adjustments]
```

---

## Final Checklist Before Demo

- [ ] All services start with `docker-compose up`
- [ ] Sample data prepared (2-3 test emails)
- [ ] Demo script rehearsed
- [ ] No errors in browser console
- [ ] No errors in backend logs
- [ ] Git repository clean and pushed
- [ ] README reviewed and accurate
- [ ] Screenshots taken (optional)

---

**You're ready to build! 🚀**

**Pro Tips:**
1. Commit early, commit often
2. Test as you go, don't wait until the end
3. If stuck >30 min, skip and come back
4. MVP first, polish later
5. Keep it simple - YAGNI principle

---

**Document Version:** 1.0  
**Last Updated:** November 4, 2025

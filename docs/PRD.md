# Product Requirements Document (PRD)
## Smart Matter Opportunity Detector

**Version:** 1.0 MVP  
**Date:** November 4, 2025  
**Target Completion:** 3 Days  
**Author:** Portfolio Project for Nexl Application

---

## 1. Executive Summary

### Problem Statement
Law firms lose millions in revenue because business opportunities are hidden in emails, meeting notes, and client communications. Lawyers don't have time to manually review all communications to spot cross-sell or upsell opportunities.

### Solution
A lightweight AI-powered system that automatically analyzes client communications, detects business opportunities, and alerts the right people in real-time.

### Success Metrics (MVP)
- System can process and analyze a document in <5 seconds
- Accurately extract at least 3 types of opportunities (real estate, employment, M&A)
- Send real-time WebSocket notifications
- Clean, working GraphQL API with <200ms response time

---

## 2. Target Users

### Primary User: Business Development Manager
- **Needs:** See all opportunities across the firm in one dashboard
- **Pain Points:** Currently relies on lawyers manually flagging opportunities
- **Goal:** Increase firm revenue by 15-20% through better opportunity capture

### Secondary User: Practice Area Lawyer
- **Needs:** Get alerted only to opportunities relevant to their expertise
- **Pain Points:** Misses opportunities because they don't see all client communications
- **Goal:** Spend less time on BD, more time on billable work

---

## 3. Core Features (MVP Scope)

### Must Have (P0)
1. **Document Upload**
   - Upload email text or meeting notes
   - Support plain text input
   - Store in database

2. **AI Opportunity Detection**
   - Extract client needs from text (using OpenAI)
   - Identify opportunity types: Real Estate, Employment Law, M&A, IP, Litigation
   - Calculate confidence score (0-100%)

3. **GraphQL API**
   - Query opportunities (with filters)
   - Query contacts and companies
   - Mutations for creating/updating records

4. **Real-time Notifications**
   - WebSocket connection for live updates
   - Push notification when high-value opportunity detected (>70% confidence)

5. **Simple Dashboard**
   - List view of opportunities (sorted by confidence/value)
   - Basic filtering (by type, confidence)
   - Upload new document form

### Nice to Have (P1 - Skip for MVP)
- Email integration (direct inbox sync)
- Advanced ML scoring models
- User authentication
- Opportunity assignment workflow
- Historical analytics

### Out of Scope (P2)
- Mobile apps
- Multi-tenancy
- Complex role-based permissions
- Calendar integration
- Document version control

---

## 4. User Stories

### Story 1: Upload Communication
**As a** BD Manager  
**I want to** upload a client email  
**So that** the system can analyze it for opportunities  

**Acceptance Criteria:**
- Can paste text into a form
- System confirms upload success
- Document appears in database within 2 seconds

### Story 2: View Opportunities
**As a** BD Manager  
**I want to** see all detected opportunities in a dashboard  
**So that** I can prioritize follow-ups  

**Acceptance Criteria:**
- See list of opportunities sorted by confidence
- Each opportunity shows: title, client, type, confidence score, extracted text
- Can filter by opportunity type

### Story 3: Real-time Alert
**As a** Practice Lawyer  
**I want to** receive instant notifications for high-value opportunities  
**So that** I can respond quickly to clients  

**Acceptance Criteria:**
- WebSocket connection established on page load
- Notification appears within 1 second of opportunity detection
- Notification shows opportunity title and confidence

---

## 5. Non-Functional Requirements

### Performance
- API response time: <200ms (p95)
- Document processing: <5 seconds
- WebSocket latency: <100ms
- Support 10 concurrent users (MVP)

### Scalability (Design Considerations)
- Architecture should allow horizontal scaling
- Use message queues for async processing (Protobuf messages)
- Stateless API design

### Security (MVP Level)
- No authentication required (demo project)
- Input validation on all endpoints
- SQL injection prevention (use ORMs)
- API rate limiting: 100 requests/minute

### Reliability
- Graceful error handling
- Database connection pooling
- Retry logic for OpenAI API calls

---

## 6. Technical Constraints

### Must Use (Per Job Requirements)
- Python backend
- GraphQL API
- WebSockets for real-time
- Protobuf for service communication
- PostgreSQL database
- OpenAI for text analysis

### Frontend
- React with Vite
- shadcn/ui components
- Tailwind CSS

### Development Timeline
- **Day 1:** Backend API + Database + GraphQL
- **Day 2:** AI Processing + WebSocket + Protobuf
- **Day 3:** Frontend Dashboard + Integration + Polish

---

## 7. Out of Scope (Explicitly)

❌ **NOT building:**
- User authentication/authorization
- Email server integration
- Complex workflow engine
- Multi-tenant architecture
- Advanced analytics dashboard
- Export to PDF/Excel
- Mobile responsive (desktop-first only)
- Internationalization

---

## 8. Success Criteria

### Demo Readiness
✅ Upload a sample client email  
✅ AI extracts 2-3 opportunities with confidence scores  
✅ GraphQL queries return structured data  
✅ WebSocket pushes notification to frontend  
✅ Dashboard displays opportunities clearly  
✅ Code is clean, documented, and follows best practices  
✅ README has setup instructions and architecture diagram  
✅ Can run entire stack with `docker-compose up`  

### Quality Bar
- 70%+ test coverage on critical paths
- No critical security vulnerabilities
- Clean code that follows SOLID principles
- Clear separation of concerns

---

## 9. Assumptions

1. Users will manually upload documents (no automated sync)
2. English language only
3. Desktop browser only (no mobile optimization)
4. Single user system (no concurrent editing conflicts)
5. OpenAI API key available and working
6. PostgreSQL sufficient (no need for vector DB in MVP)

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenAI API downtime | High | Implement retry logic + fallback to rule-based extraction |
| Complex WebSocket state management | Medium | Use simple pub/sub pattern, avoid complex state |
| Over-engineering | High | Strict MVP scope, review against YAGNI principle daily |
| Time overrun | High | Cut P1 features aggressively, focus on core demo flow |

---

## 11. Dependencies

### External Services
- OpenAI API (GPT-4 or GPT-3.5-turbo)

### Infrastructure
- PostgreSQL database
- Docker + Docker Compose

### Development Tools
- Python 3.11+
- Node.js 18+
- Claude Code for implementation

---

## Approval & Sign-off

This is an MVP scoped for 3 days of development work, focusing on demonstrating technical skills for the Nexl Senior Backend Engineer role.

**Approved for Development:** ✅

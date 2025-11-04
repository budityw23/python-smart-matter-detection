# Agent Implementation Prompts
## Smart Matter Opportunity Detector - MCP Context7 Integration

**Version:** 1.0
**Last Updated:** November 4, 2025
**MCP Server:** Context7 (Upstash)

---

## Overview

This document contains specialized prompts for using the Task agent with Context7 MCP integration to implement the Smart Matter Opportunity Detector project. Each prompt is designed to leverage real-time, version-specific documentation for maximum accuracy.

---

## Prerequisites

### MCP Setup
```bash
# Context7 MCP should already be configured in .mcp.json
claude mcp list  # Verify installation
```

### Required Documentation
- [TECHNICAL_IMPLEMENTATION_STRATEGY.md](TECHNICAL_IMPLEMENTATION_STRATEGY.md) - Step-by-step implementation guide
- [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) - Architecture and design patterns
- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) - Frontend design system rules
- [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) - Progress tracking

---

## Day 1: Backend Foundation Agent

### Agent Configuration
- **Agent Type:** `general-purpose`
- **Estimated Time:** 8 hours
- **Dependencies:** PostgreSQL, Python 3.11+, Docker

### Prompt Template

```
use context7

I need you to implement Day 1 of the Smart Matter Opportunity Detector backend
following the detailed specifications in docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md.

**Your Task:**
1. Read docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 1-932 cover Day 1)
2. Implement ALL Day 1 phases in order:
   - Phase 1.1: Database Setup (90 min)
   - Phase 1.2: GraphQL API Setup (120 min)
   - Phase 1.3: Basic Testing (60 min)

**Context7 Usage:**
Use Context7 to fetch the latest documentation for:
- FastAPI 0.104+ (async patterns, lifespan, middleware)
- Strawberry GraphQL 0.215+ (async resolvers, context, types)
- SQLAlchemy 2.0+ (async ORM, declarative base, relationships)
- Alembic 1.13+ (async migrations, autogenerate)
- PostgreSQL 15+ (UUID, ENUM types, indexes)
- Pydantic 2.5+ (validation, settings)

**Critical Requirements:**
- Follow SOLID principles from docs/TECHNICAL_DESIGN.md
- Use async/await throughout (SQLAlchemy async, FastAPI async)
- Implement proper error handling with try/except
- Add type hints everywhere
- Create comprehensive docstrings
- Follow the exact database schema from docs
- Run tests after implementation

**Deliverables:**
1. Complete backend/ folder structure
2. Working PostgreSQL database with migrations
3. Functional GraphQL API with queries
4. Passing tests (pytest)
5. Updated .gitignore and requirements.txt

**Commands to run:**
```bash
# Start PostgreSQL
docker-compose up -d db

# Run migrations
cd backend
alembic upgrade head

# Start server
uvicorn app.main:app --reload

# Test
pytest -v
```

**Success Criteria:**
- GraphQL playground accessible at http://localhost:8000/graphql
- Can query opportunityStats (returns 0 initially)
- All tests passing
- No errors in server logs

Return a summary of what was implemented and any issues encountered.
```

---

## Day 2: AI Integration & WebSocket Agent

### Agent Configuration
- **Agent Type:** `general-purpose`
- **Estimated Time:** 8 hours
- **Dependencies:** OpenAI API key, Day 1 complete

### Prompt Template

```
use context7

Implement Day 2 of the Smart Matter Opportunity Detector following
docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 933-1837).

**Your Task:**
1. Read the Day 2 section from docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md
2. Implement ALL Day 2 phases:
   - Phase 2.1: Protobuf Setup (45 min)
   - Phase 2.2: OpenAI Integration (120 min)
   - Phase 2.3: Opportunity Service (60 min)
   - Phase 2.4: Update GraphQL Mutation (45 min)
   - Phase 2.5: WebSocket Implementation (90 min)
   - Phase 2.6: Integration Testing (60 min)

**Context7 Usage:**
Fetch latest documentation for:
- OpenAI Python SDK 1.3+ (chat completions, structured outputs, async)
- Protobuf 4.25+ (message definitions, Python code generation)
- FastAPI WebSockets (connection management, async)
- Tenacity 8.2+ (retry decorators, exponential backoff)
- Python logging (structured logging, best practices)

**Critical Requirements:**
- Implement retry logic for OpenAI API calls (3 attempts max)
- Use structured output for OpenAI (JSON mode)
- Validate all AI responses before saving to database
- Implement comprehensive error handling
- Create Protobuf messages for WebSocket notifications
- Test WebSocket connection manually

**Environment Variables Needed:**
```bash
# Add to backend/.env
OPENAI_API_KEY=sk-...
```

**Deliverables:**
1. Working OpenAI integration with opportunity detection
2. Protobuf message definitions and generated code
3. WebSocket server with connection manager
4. Complete createCommunication mutation
5. Integration tests passing
6. Manual test script results

**Test Command:**
```bash
# Manual test
python backend/manual_test.py

# Integration tests
pytest backend/tests/test_integration.py -v
```

**Success Criteria:**
- Can create communication via GraphQL mutation
- AI extracts opportunities with confidence scores
- WebSocket sends notifications for high-value opportunities
- All integration tests passing

Return implementation summary and any API usage statistics.
```

---

## Day 3: Frontend Implementation Agent

### Agent Configuration
- **Agent Type:** `general-purpose`
- **Estimated Time:** 8 hours
- **Dependencies:** Node.js 18+, Day 2 complete

### Prompt Template

```
use context7

Implement Day 3 frontend for the Smart Matter Opportunity Detector.
This is CRITICAL: You MUST strictly follow docs/DESIGN_SYSTEM.md.

**Your Task:**
1. Read docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md (lines 1840-2709 - Day 3)
2. Read docs/DESIGN_SYSTEM.md (ENTIRE FILE - this is mandatory)
3. Implement ALL Day 3 phases:
   - Phase 3.1: Frontend Setup (45 min)
   - Phase 3.2: Apollo Client & GraphQL Setup (45 min)
   - Phase 3.3: WebSocket Integration (60 min)
   - Phase 3.4: Build UI Components (180 min)
   - Phase 3.5: Final Polish & Testing (60 min)

**Context7 Usage:**
Fetch latest documentation for:
- React 18 (hooks, effects, state management)
- Vite (configuration, build, env variables)
- shadcn/ui (ALL components: Button, Card, Dialog, Input, etc.)
- Tailwind CSS 3+ (utility classes, dark mode, theme configuration)
- Apollo Client 3+ (queries, mutations, cache)
- date-fns (date formatting)
- protobufjs (JavaScript protobuf)

**CRITICAL DESIGN SYSTEM RULES:**
You MUST follow these rules from docs/DESIGN_SYSTEM.md:

✅ Use ONLY shadcn/ui components
✅ Use ONLY Tailwind utility classes (NO custom CSS)
✅ Use ONLY theme color variables:
   - bg-background, bg-card, bg-muted (NOT bg-white, bg-gray-50)
   - text-foreground, text-muted-foreground (NOT text-black, text-gray-600)
   - border-border, border-input (NOT border-gray-200)
✅ Include dark mode variants (dark:bg-*, dark:text-*)
✅ Spacing: p-6, gap-4, space-y-4 (consistent)
✅ Typography: text-sm font-medium, text-lg font-semibold, text-3xl font-bold
✅ Responsive: Mobile-first with md:, lg:, xl: breakpoints
✅ Container: max-w-7xl mx-auto px-4

**Anti-Patterns to AVOID:**
❌ NO hardcoded colors (bg-white, text-black, bg-gray-50)
❌ NO custom CSS files
❌ NO non-shadcn components
❌ NO inline styles
❌ NO missing dark mode variants

**Component Requirements:**
1. OpportunityCard - Follow example in docs exactly
2. UploadModal - Form with validation
3. App.tsx - Main layout with stats and grid
4. All components must pass design system checklist

**Deliverables:**
1. Complete frontend/ folder with React + Vite
2. All shadcn/ui components installed
3. Apollo Client configured
4. WebSocket hook with Protobuf
5. Working UI matching design system
6. Dark mode support

**Test Commands:**
```bash
cd frontend
npm run dev
# Visit http://localhost:5173
```

**Success Criteria:**
- UI loads without errors
- Can upload communication via modal
- Opportunities display in grid layout
- WebSocket shows connection status
- All colors use theme variables (verify in DevTools)
- Dark mode toggle works
- Responsive on mobile/tablet/desktop

IMPORTANT: Before finalizing, verify EVERY component against the
design system checklist in docs/DESIGN_SYSTEM.md.

Return implementation summary and design system compliance report.
```

---

## Specialized Agent Prompts

### Database Migration Agent

```
use context7

Create a new Alembic migration for [describe change].

Use Context7 to fetch latest Alembic async migration patterns.
Follow the migration strategy from docs/TECHNICAL_DESIGN.md.

Generate migration with proper:
- Async upgrade/downgrade functions
- Foreign key constraints
- Index creation
- Enum type handling

Test both upgrade and downgrade paths.
```

### Component Development Agent

```
use context7

Create a new React component [ComponentName] following docs/DESIGN_SYSTEM.md.

Use Context7 for latest shadcn/ui and React patterns.

Requirements:
- Use only shadcn/ui primitives
- Theme color variables only
- Include dark mode support
- Add TypeScript types
- Implement loading/error states
- Follow spacing system (p-6, gap-4, space-y-4)
- Mobile-first responsive

Verify against design system checklist before returning.
```

### API Integration Agent

```
use context7

Add a new GraphQL [query/mutation] for [feature].

Use Context7 for latest Strawberry GraphQL and FastAPI patterns.

Requirements:
- Async resolver function
- Proper type hints
- Error handling
- Database session from context
- Input validation with Pydantic
- Comprehensive docstring

Include test case in tests/test_api/test_graphql.py.
```

### Testing Agent

```
use context7

Write comprehensive tests for [component/feature].

Use Context7 for pytest-asyncio and testing best practices.

Create:
- Unit tests for business logic
- Integration tests for API endpoints
- Mock external services (OpenAI, database)
- Test edge cases and error conditions

Aim for 70%+ code coverage.
Run tests and fix any failures.
```

---

## Multi-Agent Workflow

### Parallel Implementation Strategy

You can run multiple agents in parallel for faster development:

```bash
# Terminal 1: Backend Agent (Day 1)
# Use Backend Agent prompt above

# Terminal 2: Documentation Agent
# Review and update documentation as backend is implemented

# Terminal 3: Testing Agent
# Write tests for completed backend components
```

### Sequential Implementation Strategy

For quality-focused development:

```
Day 1 → Verify → Day 2 → Verify → Day 3 → Verify → Polish
```

Each verification step includes:
- Running all tests
- Manual testing in browser/GraphQL playground
- Code review against design docs
- Performance check

---

## Agent Communication Pattern

### Information to Provide to Agent

When launching a Task agent, provide:

1. **Context Documents:**
   - "Read docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md"
   - "Follow patterns from docs/TECHNICAL_DESIGN.md"
   - "Comply with docs/DESIGN_SYSTEM.md"

2. **Specific Requirements:**
   - Exact phase/task to implement
   - Success criteria
   - Testing requirements

3. **Context7 Instructions:**
   - List all libraries needing documentation
   - Specify version requirements if critical

### Expected Agent Output

Request the agent to return:

1. **Summary of Changes:**
   - Files created/modified
   - Key implementation decisions
   - Any deviations from specs (with justification)

2. **Test Results:**
   - Test command output
   - Coverage report (if applicable)
   - Manual testing results

3. **Issues Encountered:**
   - Blockers resolved
   - Known issues
   - Suggestions for improvement

---

## Troubleshooting Agent Issues

### Agent Can't Find Documentation

```
If agent reports missing docs:
1. Verify Context7 MCP is running: claude mcp list
2. Explicitly mention library version: "use context7 for FastAPI 0.104"
3. Provide alternative: "If Context7 unavailable, use best practices from official docs"
```

### Agent Deviates from Design System

```
If agent doesn't follow design system:
1. Re-emphasize: "You MUST follow docs/DESIGN_SYSTEM.md - this is critical"
2. Provide specific violations: "You used bg-white instead of bg-card"
3. Request fix: "Update all components to use theme variables"
```

### Agent Implementation Incomplete

```
If agent stops before completion:
1. Check for errors in logs
2. Restart with: "Continue implementing remaining tasks from [phase]"
3. Provide checkpoint: "You completed X, now do Y and Z"
```

---

## Quality Assurance Checklist

After each agent completes its task, verify:

### Backend QA
- [ ] All imports resolve correctly
- [ ] Type hints on all functions
- [ ] Async/await used properly
- [ ] Error handling implemented
- [ ] Tests passing
- [ ] GraphQL playground works
- [ ] Database migrations successful

### Frontend QA
- [ ] No console errors
- [ ] Design system compliance (use DevTools to verify colors)
- [ ] Dark mode works
- [ ] Responsive design (test on mobile view)
- [ ] All shadcn components used correctly
- [ ] No custom CSS files
- [ ] Theme variables used exclusively

### Integration QA
- [ ] End-to-end flow works
- [ ] WebSocket notifications appear
- [ ] AI integration functional
- [ ] No CORS errors
- [ ] Environment variables loaded

---

## Success Metrics

### Quantitative Metrics
- **Code Coverage:** >70%
- **API Response Time:** <200ms (p95)
- **AI Processing Time:** <5 seconds per communication
- **WebSocket Latency:** <100ms
- **Build Time:** <30 seconds (frontend)

### Qualitative Metrics
- **Code Quality:** Follows SOLID principles
- **Design Consistency:** 100% design system compliance
- **Documentation:** All major functions documented
- **Error Handling:** Graceful degradation
- **User Experience:** Smooth, responsive UI

---

## Next Steps After Implementation

1. **Code Review:**
   - Self-review all code against documentation
   - Check for security vulnerabilities
   - Verify SOLID principles applied

2. **Performance Testing:**
   - Load test API endpoints
   - Test with multiple WebSocket connections
   - Verify database query performance

3. **Documentation Update:**
   - Update README with actual setup steps
   - Document any deviations from original plan
   - Add troubleshooting section

4. **Deployment Preparation:**
   - Create production Dockerfile
   - Configure environment variables
   - Set up CI/CD pipeline (optional)

---

## Useful Context7 Commands in Prompts

```
# General usage
"use context7"

# Specific library
"use context7 to get FastAPI async patterns"

# Multiple libraries
"use context7 for React 18 hooks and shadcn/ui Card component"

# Version-specific
"use context7 for SQLAlchemy 2.0 async ORM examples"

# Best practices
"use context7 to show best practices for Strawberry GraphQL error handling"
```

---

## Additional Resources

- [Context7 Documentation](https://upstash.com/blog/context7-mcp)
- [Claude Code MCP Guide](https://docs.claude.com/en/docs/claude-code/mcp)
- [Model Context Protocol Spec](https://github.com/anthropics/anthropic-quickstarts/tree/main/model-context-protocol)

---

**Document Version:** 1.0
**Last Updated:** November 4, 2025
**Author:** Development Team

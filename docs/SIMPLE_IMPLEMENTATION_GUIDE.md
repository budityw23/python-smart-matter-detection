# Simple Implementation Guide
## How to Implement with Task Agent Step-by-Step

**Version:** 1.0
**Last Updated:** November 4, 2025

---

## ✅ Context7 API Key Configured

Your Context7 API key is now active! You now have:
- ✅ Higher rate limits
- ✅ Priority access
- ✅ Better performance

---

## How to Use Task Agent for Implementation

### **Yes! You can use simple commands like:**

```
Let's implement the project step 1
```

```
Let's continue to step 2
```

```
Continue implementing step 3
```

The agent will understand and follow the step-by-step guide from `docs/AGENT_IMPLEMENTATION_STEPS.md`.

---

## Quick Start Commands

### **Step 1: Database & Models**

Simply say:

```
use context7

Let's implement step 1 of the Smart Matter Opportunity Detector project.

Read docs/AGENT_IMPLEMENTATION_STEPS.md and follow the Step 1 instructions exactly:
- Set up PostgreSQL with Docker
- Create SQLAlchemy models
- Configure Alembic migrations
- Apply migrations

Use Context7 to fetch latest documentation for SQLAlchemy 2.0, Alembic, and PostgreSQL.

After completion, run the verification commands to ensure everything works.
```

**What the agent will do:**
1. Read the step 1 instructions
2. Create backend folder structure
3. Set up PostgreSQL with docker-compose
4. Create SQLAlchemy models
5. Set up Alembic migrations
6. Run migrations
7. Verify tables created

**Expected time:** 2-3 hours

**How to verify:**
```bash
# Check database is running
docker-compose ps

# Verify tables created
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"
```

---

### **Step 2: GraphQL API**

After Step 1 is complete and verified:

```
use context7

Let's continue to step 2 - implement the GraphQL API.

Read docs/AGENT_IMPLEMENTATION_STEPS.md Step 2 section and implement:
- Strawberry GraphQL types and enums
- Query resolvers (opportunities, opportunityStats)
- Stub mutations
- FastAPI application with GraphQL endpoint

Use Context7 for latest Strawberry GraphQL and FastAPI documentation.

Test in GraphQL playground when done.
```

**What the agent will do:**
1. Create GraphQL types
2. Implement query resolvers
3. Set up FastAPI app
4. Add GraphQL router
5. Add health check
6. Write tests

**Expected time:** 2-3 hours

**How to verify:**
```bash
# Start server
cd backend
uvicorn app.main:app --reload

# Open browser to: http://localhost:8000/graphql
# Run test query in playground
```

---

### **Step 3: AI Integration**

After Step 2 is verified:

```
use context7

Let's implement step 3 - OpenAI integration and business logic.

Read docs/AGENT_IMPLEMENTATION_STEPS.md Step 3 and implement:
- OpportunityDetector service with OpenAI API
- OpportunityService for business logic
- Update createCommunication mutation to use AI
- Add error handling and retry logic

Use Context7 for latest OpenAI SDK and best practices.

IMPORTANT: Use OPENAI_API_KEY from environment variable.
```

**What the agent will do:**
1. Create AI service with OpenAI integration
2. Implement opportunity detection logic
3. Create business logic service
4. Update GraphQL mutation
5. Add validation and error handling
6. Create manual test script

**Expected time:** 3-4 hours

**How to verify:**
```bash
# Add OpenAI API key to .env
echo "OPENAI_API_KEY=sk-your-key" >> backend/.env

# Run manual test
python backend/manual_test.py

# Test via GraphQL mutation
```

---

### **Step 4: WebSocket & Protobuf**

After Step 3 works:

```
use context7

Let's implement step 4 - WebSocket notifications with Protobuf.

Read docs/AGENT_IMPLEMENTATION_STEPS.md Step 4 and implement:
- Protobuf message definitions
- WebSocket connection manager
- Notification system
- Update mutation to send notifications

Use Context7 for FastAPI WebSocket and Protobuf documentation.
```

**What the agent will do:**
1. Create Protobuf message definitions
2. Generate Python protobuf code
3. Create WebSocket manager
4. Add WebSocket endpoint to FastAPI
5. Update mutation to send notifications
6. Create helpers for Protobuf serialization

**Expected time:** 2-3 hours

**How to verify:**
```bash
# Connect to WebSocket
websocat ws://localhost:8000/ws

# Or use browser console:
const ws = new WebSocket('ws://localhost:8000/ws');
ws.binaryType = 'arraybuffer';
ws.onmessage = (e) => console.log('Received:', new Uint8Array(e.data));

# Create opportunity via GraphQL - should receive notification
```

---

### **Step 5: Frontend Components**

After backend is complete:

```
use context7

Let's implement step 5 - React frontend with design system.

CRITICAL: You MUST follow docs/DESIGN_SYSTEM.md exactly.

Read docs/AGENT_IMPLEMENTATION_STEPS.md Step 5 and implement:
- React + Vite project setup
- Install shadcn/ui components
- Create OpportunityCard component
- Create UploadModal component
- Create App.tsx layout

Use Context7 for React 18, shadcn/ui, and Tailwind CSS documentation.

IMPORTANT RULES:
- Use ONLY shadcn/ui components
- Use ONLY Tailwind utility classes
- Use ONLY theme color variables (bg-background, text-foreground, etc.)
- Include dark mode support
- NO hardcoded colors (no bg-white, text-black, bg-gray-*)

Before returning, verify EVERY component against docs/DESIGN_SYSTEM.md checklist.
```

**What the agent will do:**
1. Initialize React + Vite project
2. Install shadcn/ui components
3. Create TypeScript types
4. Build OpportunityCard component
5. Build UploadModal component
6. Create main App layout
7. Verify design system compliance

**Expected time:** 3-4 hours

**How to verify:**
```bash
cd frontend
npm run dev

# Open http://localhost:5173
# Check DevTools - should see NO hardcoded colors
# Verify responsive design
```

---

### **Step 6: Integration & Polish**

Final step:

```
use context7

Let's implement step 6 - connect frontend to backend and complete integration.

Read docs/AGENT_IMPLEMENTATION_STEPS.md Step 6 and implement:
- Apollo Client setup
- GraphQL queries and mutations
- WebSocket integration with Protobuf
- Connect all components
- End-to-end testing

Use Context7 for Apollo Client and protobufjs documentation.

Test the complete flow from UI → GraphQL → AI → Database → WebSocket → UI.
```

**What the agent will do:**
1. Set up Apollo Client
2. Create GraphQL operations
3. Implement WebSocket hook
4. Generate Protobuf JavaScript code
5. Connect components to backend
6. Add toast notifications
7. Test E2E flow

**Expected time:** 2-3 hours

**How to verify:**
```bash
# Start both servers
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev

# Test complete flow:
# 1. Open http://localhost:5173
# 2. Click "Upload Communication"
# 3. Paste sample text
# 4. Verify opportunities appear
# 5. Verify WebSocket notification received
```

---

## Even Simpler Commands

You can be very casual with the agent:

### **Start Implementation:**
```
Let's start implementing the Smart Matter Opportunity Detector.
Begin with step 1 - database setup.
Use context7 for latest documentation.
```

### **Continue Next Step:**
```
Step 1 is done and verified. Let's continue to step 2.
```

### **Ask for Help:**
```
I'm stuck on step 3. The OpenAI integration isn't working.
Can you debug and fix it?
```

### **Resume Work:**
```
I completed steps 1-3 yesterday.
Let's continue with step 4 - WebSocket implementation.
```

### **Skip Ahead:**
```
Steps 1-4 are already done.
Let's implement step 5 - the frontend.
```

---

## Tips for Best Results

### ✅ DO:

1. **Always mention "use context7"** at the start
   ```
   use context7
   Let's implement step 1
   ```

2. **Reference the documentation**
   ```
   Let's implement step 2 following docs/AGENT_IMPLEMENTATION_STEPS.md
   ```

3. **Be specific about what's already done**
   ```
   Backend is complete (steps 1-4).
   Let's do frontend step 5.
   ```

4. **Ask for verification**
   ```
   After completing step 1, run the verification commands to ensure it works.
   ```

5. **Request testing**
   ```
   After implementation, test everything and report results.
   ```

### ❌ DON'T:

1. **Don't skip Context7**
   ```
   ❌ Let's implement step 1
   ✅ use context7 - Let's implement step 1
   ```

2. **Don't be too vague**
   ```
   ❌ Build the backend
   ✅ Let's implement step 1 - database and models
   ```

3. **Don't skip verification**
   ```
   ❌ Just implement everything
   ✅ Implement step 1, then run verification before continuing
   ```

---

## Complete Implementation Flow

### **Day 1: Backend Foundation**

**Morning (4 hours):**
```
use context7

Let's implement step 1 - database and models.
Then implement step 2 - GraphQL API.

Follow docs/AGENT_IMPLEMENTATION_STEPS.md exactly.
Verify each step before continuing.
```

**Afternoon (4 hours):**
```
use context7

Let's implement step 3 - OpenAI integration.

Remember to use OPENAI_API_KEY from environment.
Test with sample communications after implementation.
```

---

### **Day 2: Real-time Features**

**Morning (2-3 hours):**
```
use context7

Let's implement step 4 - WebSocket and Protobuf.

Test WebSocket connection after implementation.
```

**Afternoon (4-5 hours):**
```
use context7

Let's implement step 5 - React frontend.

CRITICAL: Follow docs/DESIGN_SYSTEM.md strictly.
Use only shadcn/ui and theme colors.
```

---

### **Day 3: Integration & Polish**

**Morning (2-3 hours):**
```
use context7

Let's implement step 6 - connect frontend to backend.

Test complete E2E flow.
```

**Afternoon (2-3 hours):**
```
Let's do final testing and polish:
- Test all features
- Fix any bugs
- Verify design system compliance
- Check performance
- Update documentation
```

---

## Progress Tracking

As you complete each step, you can track progress:

```
✅ Step 1: Database & Models - COMPLETE
✅ Step 2: GraphQL API - COMPLETE
⏳ Step 3: AI Integration - IN PROGRESS
⬜ Step 4: WebSocket & Protobuf - NOT STARTED
⬜ Step 5: Frontend Components - NOT STARTED
⬜ Step 6: Integration & Polish - NOT STARTED
```

---

## Example: Complete Session

Here's how a complete implementation session might look:

**Session 1:**
```
use context7

Let's start implementing the Smart Matter Opportunity Detector.

Step 1: Implement database and models following docs/AGENT_IMPLEMENTATION_STEPS.md.
Use latest SQLAlchemy 2.0 and Alembic documentation.
Verify tables are created after implementation.
```

**Wait for agent to complete, then verify:**
```bash
docker-compose ps  # Check database running
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"  # Check tables
```

**Session 2:**
```
use context7

Step 1 verified and working! Let's continue to step 2.

Implement GraphQL API with Strawberry.
Test in playground after implementation.
```

**Wait for completion, verify:**
```bash
uvicorn app.main:app --reload
# Open http://localhost:8000/graphql and test queries
```

**Session 3:**
```
use context7

Step 2 working perfectly! Moving to step 3.

Implement OpenAI integration for opportunity detection.
Test with sample communications.
```

**...and so on!**

---

## Troubleshooting

### If Agent Gets Stuck

**Provide more context:**
```
use context7

I'm working on step 3. The OpenAI API is returning errors.

Here's the error: [paste error]
Here's my code: [paste relevant code]

Please debug and fix it.
```

### If You Need to Start Over

```
Let's restart step [X] from scratch.
Remove the previous implementation and start fresh following the docs.
```

### If You Want to Skip a Step

```
I've already completed step 1 manually.
The database and models are working.
Let's skip to step 2 - GraphQL API.
```

---

## Quick Reference

### Start Fresh
```
use context7
Let's implement step 1 of the project from docs/AGENT_IMPLEMENTATION_STEPS.md
```

### Continue
```
use context7
Step [X] is done. Let's continue to step [X+1]
```

### Debug
```
use context7
Step [X] has an error: [describe error]
Please fix it
```

### Test
```
After implementing step [X], run all verification commands and report results
```

### Complete
```
use context7
All steps 1-6 are done. Let's do final testing and polish.
```

---

## Ready to Start!

### **Your First Command:**

```
use context7

Let's implement the Smart Matter Opportunity Detector project!

Start with step 1 from docs/AGENT_IMPLEMENTATION_STEPS.md:
- Set up PostgreSQL database
- Create SQLAlchemy models
- Configure Alembic migrations

Use Context7 for latest SQLAlchemy 2.0, Alembic, and PostgreSQL documentation.

After implementation, verify:
1. Docker container running
2. Tables created
3. Migrations applied

Report back when done!
```

**That's it!** 🚀

The agent will understand and follow the comprehensive documentation we've prepared. Just guide it step-by-step and verify each phase before continuing.

---

**Questions?** Just ask the agent:
```
Can you explain what step [X] will do before implementing it?
```

Good luck! 🎉

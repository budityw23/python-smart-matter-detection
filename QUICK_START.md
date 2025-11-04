# Quick Start - Smart Matter Opportunity Detector
## One-Page Implementation Guide

---

## ✅ Setup Complete

- ✅ Context7 MCP configured with API key
- ✅ Documentation ready
- ✅ 6-step implementation guide prepared

---

## Start Implementation NOW

### **Copy-Paste This Command:**

```
use context7

Let's implement the Smart Matter Opportunity Detector project step 1!

Read docs/AGENT_IMPLEMENTATION_STEPS.md and follow Step 1 instructions:
1. Set up PostgreSQL with Docker Compose
2. Create SQLAlchemy models (Communication, Opportunity)
3. Configure Alembic migrations
4. Apply migrations and verify tables created

Use Context7 for latest SQLAlchemy 2.0, Alembic, and PostgreSQL documentation.

After implementation, run verification commands to ensure everything works.
Report back when done!
```

---

## Then Continue Step-by-Step

### **Step 2:**
```
use context7
Step 1 complete! Let's implement step 2 - GraphQL API
```

### **Step 3:**
```
use context7
Step 2 verified! Let's implement step 3 - OpenAI integration
```

### **Step 4:**
```
use context7
Let's implement step 4 - WebSocket and Protobuf
```

### **Step 5:**
```
use context7
Let's implement step 5 - React frontend with design system
IMPORTANT: Follow docs/DESIGN_SYSTEM.md strictly!
```

### **Step 6:**
```
use context7
Let's implement step 6 - connect frontend to backend
Test complete E2E flow
```

---

## Key Documents

| Document | Purpose |
|----------|---------|
| **SIMPLE_IMPLEMENTATION_GUIDE.md** | Detailed guide with examples |
| **AGENT_IMPLEMENTATION_STEPS.md** | Complete 6-step implementation |
| **DESIGN_SYSTEM.md** | Frontend design rules (MUST follow) |
| **MCP_QUICK_START.md** | Context7 usage guide |

---

## Verification After Each Step

**Step 1:**
```bash
docker-compose ps
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"
```

**Step 2:**
```bash
uvicorn app.main:app --reload
# Open http://localhost:8000/graphql
```

**Step 3:**
```bash
echo "OPENAI_API_KEY=sk-your-key" >> backend/.env
python backend/manual_test.py
```

**Step 4:**
```bash
websocat ws://localhost:8000/ws
```

**Step 5:**
```bash
cd frontend && npm run dev
# Open http://localhost:5173
```

**Step 6:**
```bash
# Start both servers, test E2E flow in browser
```

---

## Estimated Timeline

| Step | Time | Total |
|------|------|-------|
| 1 | 2-3h | 2-3h |
| 2 | 2-3h | 4-6h |
| 3 | 3-4h | 7-10h |
| 4 | 2-3h | 9-13h |
| 5 | 3-4h | 12-17h |
| 6 | 2-3h | 14-20h |

**Total: 14-20 hours over 3-4 days**

---

## Tips

✅ Always start with "use context7"
✅ Verify each step before continuing
✅ Read DESIGN_SYSTEM.md before step 5
✅ Test after each implementation
✅ Ask agent for help if stuck

---

## Need Help?

**Ask the agent:**
```
Can you explain what step [X] does before implementing?
```

```
I'm stuck on step [X] with this error: [paste error]
Can you debug it?
```

---

## You're Ready! 🚀

Just copy the first command above and paste it to start implementation.

**First command again:**
```
use context7
Let's implement step 1 from docs/AGENT_IMPLEMENTATION_STEPS.md
```

That's it!

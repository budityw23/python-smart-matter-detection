# MCP Context7 Quick Start Guide
## Smart Matter Opportunity Detector

**Last Updated:** November 4, 2025

---

## What is Context7 MCP?

Context7 is an MCP (Model Context Protocol) server that provides **up-to-date, version-specific documentation** for libraries directly into your Claude Code prompts. It eliminates outdated code generation and hallucinated APIs.

### Benefits
- ✅ **Always current** - Fetches latest docs from official sources
- ✅ **Version-specific** - Shows examples for your exact library version
- ✅ **No hallucinations** - Real documentation, not AI-generated guesses
- ✅ **Instant context** - Just say "use context7" in your prompt

---

## Setup Status

Context7 MCP has been configured for this project:

```bash
# Verify installation
claude mcp list
# Expected: Shows context7 server

# Check configuration
cat .mcp.json
# Expected: Shows context7 with npx command
```

**Configuration File:** `.mcp.json`
```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {}
    }
  }
}
```

---

## How to Use Context7

### Basic Usage

Simply add `use context7` to any prompt:

```
use context7

Help me implement FastAPI async endpoints with proper error handling.
```

Context7 will automatically:
1. Detect mentioned libraries (FastAPI)
2. Fetch latest documentation
3. Inject relevant content into the prompt
4. Enable accurate code generation

### With Task Agent

When launching a Task agent, include Context7 in your prompt:

```
use context7

Use the general-purpose agent to implement Step 1 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Fetch latest documentation for SQLAlchemy 2.0, Alembic, and PostgreSQL.
```

---

## Supported Libraries (This Project)

Context7 can fetch documentation for all libraries used in this project:

### Backend
- ✅ FastAPI 0.104+
- ✅ Strawberry GraphQL 0.215+
- ✅ SQLAlchemy 2.0+
- ✅ Alembic 1.13+
- ✅ Pydantic 2.5+
- ✅ OpenAI Python SDK 1.3+
- ✅ Protobuf 4.25+
- ✅ pytest-asyncio
- ✅ Tenacity
- ✅ uvicorn

### Frontend
- ✅ React 18
- ✅ Vite
- ✅ TypeScript 5+
- ✅ shadcn/ui (all components)
- ✅ Tailwind CSS 3+
- ✅ Apollo Client 3+
- ✅ date-fns
- ✅ protobufjs

---

## Example Prompts

### General Development
```
use context7

Show me how to implement async SQLAlchemy 2.0 relationships with proper type hints.
```

### Specific Feature
```
use context7

How do I create a Strawberry GraphQL resolver that queries PostgreSQL using async SQLAlchemy?
Include error handling and pagination.
```

### Component Development
```
use context7

Help me build a React component using shadcn/ui Card and Badge components with Tailwind CSS.
Follow the design system from docs/DESIGN_SYSTEM.md.
```

### Debugging
```
use context7

I'm getting a CORS error in FastAPI when calling from React. Show me the correct CORS middleware setup.
```

---

## Context7 with Implementation Steps

### Step 1: Database & Models
```
use context7

Implement Step 1 from docs/AGENT_IMPLEMENTATION_STEPS.md.
I need SQLAlchemy 2.0 async models with proper relationships.
Fetch documentation for:
- SQLAlchemy async patterns
- Alembic async migrations
- PostgreSQL UUID types
```

### Step 2: GraphQL API
```
use context7

Implement Step 2 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Fetch latest Strawberry GraphQL documentation for:
- Async resolvers
- Context management
- Connection types (pagination)
- Error handling
```

### Step 3: AI Integration
```
use context7

Implement Step 3 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Need OpenAI API documentation for:
- Async chat completions
- Structured JSON output
- Error handling and retries
```

### Step 4: WebSocket
```
use context7

Implement Step 4 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Fetch documentation for:
- FastAPI WebSocket handling
- Protobuf message definitions in Python
- Connection management patterns
```

### Step 5: Frontend Components
```
use context7

Implement Step 5 from docs/AGENT_IMPLEMENTATION_STEPS.md.
MUST follow docs/DESIGN_SYSTEM.md strictly.
Fetch latest documentation for:
- shadcn/ui components (Card, Dialog, Button, Badge)
- Tailwind CSS utility classes
- React 18 hooks
```

### Step 6: Integration
```
use context7

Implement Step 6 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Fetch documentation for:
- Apollo Client 3 setup and hooks
- WebSocket API in browser
- protobufjs decoding
```

---

## Best Practices

### DO ✅
- Always mention library versions when specific version matters
- Ask for complete examples, not just snippets
- Request error handling patterns
- Ask for TypeScript types when using TypeScript
- Mention async/await when using async code

### DON'T ❌
- Don't assume Context7 knows your project structure (reference docs/)
- Don't skip "use context7" - it won't activate otherwise
- Don't rely on old cached responses - Context7 fetches fresh
- Don't forget to mention framework (React, FastAPI, etc.)

---

## Troubleshooting

### Context7 Not Responding
```bash
# Check if MCP server is running
claude mcp list

# Restart Claude Code if needed
# Context7 will auto-start on next prompt with "use context7"
```

### Getting Generic Responses
If responses seem generic (not using Context7):
- Verify you included "use context7" in prompt
- Check MCP server is configured: `cat .mcp.json`
- Try being more specific about library and version

### Library Not Found
If Context7 can't find a library:
- Verify library name is correct (e.g., "FastAPI" not "fast-api")
- Check if library has official documentation online
- Try alternative: "show me best practices for [library]"

---

## Common Patterns

### Pattern 1: Feature Implementation
```
use context7

I need to implement [feature] using [library].
Follow the patterns from docs/[file].md.
Show me:
1. Latest [library] patterns
2. Error handling
3. Type hints
4. Tests
```

### Pattern 2: Bug Fixing
```
use context7

I'm getting [error] when using [library].
Current code: [paste code]
Expected: [describe expected behavior]
Show me the correct way to [do thing] in [library version].
```

### Pattern 3: Optimization
```
use context7

How can I optimize [code/feature] using [library]?
Current performance: [describe issue]
Fetch latest best practices for [specific optimization].
```

---

## Integration with Task Agent

When using the Task tool with Context7:

```
Launch task agent with:

Prompt: "use context7 to implement Step X from docs/AGENT_IMPLEMENTATION_STEPS.md.
Follow all specifications exactly.
Fetch latest documentation for [libraries].
Return implementation summary and test results."

Expected: Agent will use Context7 to get accurate, up-to-date code examples.
```

---

## Verification

To verify Context7 is working:

1. **Test basic functionality:**
   ```
   use context7

   Show me a simple FastAPI async endpoint example.
   ```

   Expected: Returns code with async/await, proper imports, current FastAPI syntax.

2. **Test version-specific:**
   ```
   use context7

   Show me SQLAlchemy 2.0 style declarative base (not 1.x legacy).
   ```

   Expected: Returns code using `DeclarativeBase`, not old `declarative_base()`.

3. **Test multiple libraries:**
   ```
   use context7

   Show me how to use Strawberry GraphQL with FastAPI async endpoints.
   ```

   Expected: Returns integrated example with both libraries.

---

## Advanced Usage

### Combining Context7 with Project Docs

```
use context7

Read docs/TECHNICAL_DESIGN.md section 6 (AI Integration Design).
Implement the OpportunityDetector class using latest OpenAI SDK patterns.
Fetch OpenAI documentation for:
- Async chat completions
- Structured output mode
- Error handling
```

### Context7 for Code Review

```
use context7

Review this code against latest [library] best practices:
[paste code]

Check for:
- Outdated patterns
- Better alternatives
- Performance issues
- Type safety
```

---

## Resources

- **Context7 GitHub:** https://github.com/upstash/context7
- **MCP Documentation:** https://docs.claude.com/en/docs/claude-code/mcp
- **Project Docs:** `docs/AGENT_IMPLEMENTATION_STEPS.md`

---

## Quick Command Reference

```bash
# Check MCP status
claude mcp list

# View Context7 config
cat .mcp.json

# Test Context7 (in Claude Code)
# Just send: "use context7 - test FastAPI example"

# Start implementation with Context7
# Use prompts from docs/AGENT_IMPLEMENTATION_STEPS.md
# Each prompt includes "use context7" already
```

---

**Ready to start?** Open `docs/AGENT_IMPLEMENTATION_STEPS.md` and begin with Step 1!

Every step includes a pre-written prompt with Context7 integration for accurate implementation.

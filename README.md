# Smart Matter Opportunity Detector
## AI-Powered Opportunity Detection for Law Firms

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)

---

## Overview

An intelligent system that automatically analyzes client communications (emails, meeting notes) using AI to detect business opportunities in real-time. Built for law firms to capture hidden revenue opportunities.

### Key Features

- 🤖 **AI-Powered Detection** - Uses OpenAI GPT-4 to extract opportunities from text
- ⚡ **Real-Time Notifications** - WebSocket alerts for high-value opportunities
- 🎯 **Smart Categorization** - Identifies 5 practice areas (Real Estate, Employment, M&A, IP, Litigation)
- 📊 **Confidence Scoring** - AI assigns confidence scores (40-100%) to each opportunity
- 🎨 **Modern UI** - Beautiful, responsive interface with shadcn/ui components
- 🌙 **Dark Mode** - Full theme support with design system
- 📈 **GraphQL API** - Flexible, type-safe API with Strawberry

---

## Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **Strawberry GraphQL** - Type-safe GraphQL for Python
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **OpenAI API** - GPT-4 for text analysis
- **Protobuf** - Efficient message serialization
- **WebSockets** - Real-time communication
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI framework with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **shadcn/ui** - Beautiful, accessible components
- **Tailwind CSS** - Utility-first styling
- **Apollo Client** - GraphQL client
- **WebSocket API** - Real-time updates

### Infrastructure
- **PostgreSQL 15** - Relational database
- **Docker** - Containerization
- **docker-compose** - Multi-service orchestration

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-smart-matter-detection
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Add your OpenAI API key to backend/.env

   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. **Start with Docker Compose** (easiest)
   ```bash
   docker-compose up
   ```

   **OR Manual Setup:**

   ```bash
   # Start PostgreSQL
   docker-compose up -d db

   # Backend setup
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload

   # Frontend setup (new terminal)
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - GraphQL Playground: http://localhost:8000/graphql
   - Backend API: http://localhost:8000

---

## ✅ MCP Context7 Integration - READY TO USE

This project is **fully configured** with **Context7 MCP + API key** for enhanced development experience.

### ✅ Context7 Status
- ✅ MCP server configured
- ✅ API key applied (higher rate limits & priority access)
- ✅ All documentation ready
- ✅ Ready for immediate use

### 🚀 Start Implementation NOW

**Copy-paste this command to begin:**
```
use context7

Let's implement the Smart Matter Opportunity Detector step 1!
Read docs/AGENT_IMPLEMENTATION_STEPS.md and follow Step 1 instructions.
Use Context7 for latest SQLAlchemy 2.0, Alembic, PostgreSQL documentation.
```

### 📚 Implementation Guides

| Guide | Purpose | When to Use |
|-------|---------|-------------|
| **[QUICK_START.md](QUICK_START.md)** 🚀 | One-page cheat sheet | **START HERE** |
| **[SIMPLE_IMPLEMENTATION_GUIDE.md](docs/SIMPLE_IMPLEMENTATION_GUIDE.md)** 📖 | Detailed step-by-step with examples | Detailed instructions |
| **[AGENT_IMPLEMENTATION_STEPS.md](docs/AGENT_IMPLEMENTATION_STEPS.md)** 📋 | Complete 6-step technical guide | Full implementation specs |
| **[MCP_QUICK_START.md](docs/MCP_QUICK_START.md)** 🔧 | Context7 usage reference | Context7 help |

### How to Use with Agent

**Yes! You can use simple commands like:**

```
Let's implement step 1
```

```
Step 1 is done, let's continue to step 2
```

```
Continue implementing step 3
```

The agent understands and will follow the documentation automatically!

📖 **Full guide:** [docs/SIMPLE_IMPLEMENTATION_GUIDE.md](docs/SIMPLE_IMPLEMENTATION_GUIDE.md)

---

## Implementation Guide

### For Developers

This project includes comprehensive documentation for implementation:

1. **🚀 [QUICK_START.md](QUICK_START.md)** ⭐ **START HERE**
   - One-page implementation guide
   - Copy-paste commands ready
   - Quick verification steps
   - **Fastest way to begin!**

2. **📖 [SIMPLE_IMPLEMENTATION_GUIDE.md](docs/SIMPLE_IMPLEMENTATION_GUIDE.md)**
   - Detailed step-by-step instructions
   - Example commands for each step
   - Casual language guide
   - Troubleshooting tips

3. **📋 [AGENT_IMPLEMENTATION_STEPS.md](docs/AGENT_IMPLEMENTATION_STEPS.md)**
   - Complete 6-step technical guide
   - Each step: 2-4 hours
   - Testable deliverables
   - Pre-written agent prompts
   - Verification commands

2. **🎨 [DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)**
   - Complete frontend design system
   - shadcn/ui component patterns
   - Tailwind CSS guidelines
   - Dark mode support
   - Accessibility standards

3. **🏗️ [TECHNICAL_DESIGN.md](docs/TECHNICAL_DESIGN.md)**
   - System architecture
   - Database design
   - API specifications
   - Best practices

4. **📝 [TECHNICAL_IMPLEMENTATION_STRATEGY.md](docs/TECHNICAL_IMPLEMENTATION_STRATEGY.md)**
   - Detailed 3-day implementation plan
   - Code examples for every component
   - Testing strategies

5. **✅ [IMPLEMENTATION_CHECKLIST.md](docs/IMPLEMENTATION_CHECKLIST.md)**
   - Task breakdown with time estimates
   - Progress tracking
   - Quality assurance checklist

### 6-Step Implementation Plan

| Step | Focus | Time | Status |
|------|-------|------|--------|
| 1 | Database & Models | 2-3h | ⬜ Not Started |
| 2 | GraphQL API | 2-3h | ⬜ Not Started |
| 3 | AI Integration | 3-4h | ⬜ Not Started |
| 4 | WebSocket & Protobuf | 2-3h | ⬜ Not Started |
| 5 | Frontend Components | 3-4h | ⬜ Not Started |
| 6 | Integration & Polish | 2-3h | ⬜ Not Started |

📖 **Get Started:** [docs/AGENT_IMPLEMENTATION_STEPS.md](docs/AGENT_IMPLEMENTATION_STEPS.md)

---

## Using Task Agents

### Launch Implementation Agent

Use Claude Code's Task agent with Context7 for autonomous implementation:

```
use context7

Implement Step 1 from docs/AGENT_IMPLEMENTATION_STEPS.md.
Follow all specifications exactly.
Use Context7 for latest SQLAlchemy 2.0, Alembic, and PostgreSQL documentation.
```

📚 **Agent Prompts:** [docs/AGENT_PROMPTS.md](docs/AGENT_PROMPTS.md)

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (React + Vite)         │
│    shadcn/ui + Tailwind + Apollo        │
└────────────┬────────────────────────────┘
             │
             │ GraphQL (HTTP)
             │ WebSocket
             ▼
┌─────────────────────────────────────────┐
│      API Gateway (FastAPI)              │
│    Strawberry GraphQL + WebSocket       │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌─────────┐ ┌──────────────┐
│Business│ │AI Service│ │Notification  │
│Logic   │ │(OpenAI) │ │(WebSocket)   │
└────┬───┘ └────┬────┘ └──────┬───────┘
     │          │              │
     └──────────┴──────────────┘
                │
                ▼
        ┌───────────────┐
        │  PostgreSQL   │
        └───────────────┘
```

---

## API Documentation

### GraphQL Queries

**Get Opportunities**
```graphql
query {
  opportunities(minConfidence: 70, limit: 20) {
    edges {
      node {
        id
        title
        opportunityType
        confidence
        description
      }
    }
    totalCount
  }
}
```

**Get Dashboard Stats**
```graphql
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

### GraphQL Mutations

**Create Communication**
```graphql
mutation {
  createCommunication(input: {
    content: "We're opening a Chicago office and need lease help."
    clientName: "Acme Corp"
    sourceType: EMAIL
  }) {
    communication {
      id
      clientName
    }
    opportunities {
      id
      title
      opportunityType
      confidence
    }
  }
}
```

### WebSocket

**Connect to WebSocket**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.binaryType = 'arraybuffer';

ws.onmessage = (event) => {
  // Decode Protobuf message
  const notification = OpportunityNotification.decode(
    new Uint8Array(event.data)
  );
  console.log('New opportunity:', notification);
};
```

---

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest -v

# Run with coverage
pytest --cov=app tests/

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### Frontend Development

```bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check
```

### Database

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U nexl -d nexl_opportunities

# View tables
\dt

# View table structure
\d communications

# Query opportunities
SELECT title, confidence, opportunity_type FROM opportunities LIMIT 10;
```

---

## Testing

### Backend Tests

```bash
cd backend
pytest -v                          # Run all tests
pytest tests/test_api/ -v          # API tests only
pytest tests/test_services/ -v     # Service tests only
pytest --cov=app tests/            # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test                           # Run tests
npm run test:coverage              # With coverage
```

### End-to-End Testing

1. Start full stack: `docker-compose up`
2. Visit http://localhost:5173
3. Upload a sample communication
4. Verify:
   - AI extracts opportunities
   - Opportunities appear in UI
   - WebSocket notification received
   - Stats update

---

## Design System

### Component Standards
- ✅ Use **only** shadcn/ui components
- ✅ Use **only** Tailwind utility classes (no custom CSS)
- ✅ Use **only** theme color variables (no hardcoded colors)
- ✅ Support dark mode with `dark:` variants
- ✅ Mobile-first responsive design

### Example
```tsx
// ✅ CORRECT - Design System Compliant
<Card className="p-6">
  <CardHeader className="space-y-2">
    <CardTitle className="text-lg font-semibold text-foreground">
      Title
    </CardTitle>
    <CardDescription className="text-muted-foreground">
      Description
    </CardDescription>
  </CardHeader>
</Card>

// ❌ WRONG - Violates Design System
<div className="bg-white p-5">
  <h2 className="text-black">Title</h2>
</div>
```

📚 **Full Design System:** [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)

---

## Project Structure

```
python-smart-matter-detection/
├── backend/
│   ├── app/
│   │   ├── api/graphql/         # GraphQL schema and resolvers
│   │   ├── models/              # SQLAlchemy models
│   │   ├── services/            # Business logic
│   │   ├── websocket/           # WebSocket manager
│   │   ├── protobuf/            # Protobuf messages
│   │   └── utils/               # Database, logging
│   ├── tests/                   # Backend tests
│   ├── alembic/                 # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── graphql/             # GraphQL queries/mutations
│   │   ├── hooks/               # Custom hooks
│   │   ├── lib/                 # Utilities, protobuf
│   │   └── types/               # TypeScript types
│   └── package.json
├── docs/
│   ├── AGENT_IMPLEMENTATION_STEPS.md   # 6-step guide
│   ├── AGENT_PROMPTS.md               # Agent prompt templates
│   ├── DESIGN_SYSTEM.md               # Frontend design system
│   ├── TECHNICAL_DESIGN.md            # Architecture
│   ├── TECHNICAL_IMPLEMENTATION_STRATEGY.md
│   ├── IMPLEMENTATION_CHECKLIST.md
│   ├── MCP_QUICK_START.md             # Context7 MCP guide
│   ├── PRD.md                         # Product requirements
│   └── PRODUCT_REQUIREMENTS.md
├── docker-compose.yml
├── .mcp.json                    # MCP Context7 config
└── README.md
```

---

## Contributing

This is a portfolio project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Follow the design system and coding standards
4. Add tests for new features
5. Submit a pull request

---

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### OpenAI API Errors
```bash
# Verify API key in .env
cat backend/.env | grep OPENAI_API_KEY

# Check API credits at platform.openai.com
```

### CORS Errors
```bash
# Verify CORS_ORIGINS in backend/.env
# Should include: http://localhost:5173
```

### WebSocket Won't Connect
```bash
# Check protocol (ws:// not http://)
# Verify backend is running
# Check browser console for errors
```

---

## Performance

### Target Metrics
- API Response Time: <200ms (p95)
- AI Processing Time: <5 seconds per communication
- WebSocket Latency: <100ms
- Frontend Load Time: <2 seconds

### Monitoring
- Health check: `GET /health`
- Database query performance: Check SQLAlchemy logs
- OpenAI API usage: Check OpenAI dashboard

---

## Security

### Best Practices Implemented
- ✅ SQL injection prevention (ORM parameterized queries)
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Environment variables for secrets
- ✅ No API keys in code/git

### For Production
- [ ] Add authentication (JWT)
- [ ] Add rate limiting
- [ ] Add HTTPS
- [ ] Add API key rotation
- [ ] Add security headers
- [ ] Add input sanitization

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

- Built for **Nexl Senior Backend Engineer** application
- Designed with **SOLID principles** and **clean architecture**
- Implements **MCP (Model Context Protocol)** for enhanced development
- Uses **Context7** for up-to-date documentation

---

## Support

- 📚 **Documentation:** See `docs/` folder
- 🐛 **Issues:** GitHub Issues
- 💬 **Questions:** Create a discussion
- 🚀 **MCP Guide:** [docs/MCP_QUICK_START.md](docs/MCP_QUICK_START.md)

---

## Roadmap

### Phase 1 - MVP (Current)
- [x] Design documentation
- [x] MCP Context7 integration
- [x] 6-step implementation guide
- [ ] Complete backend implementation
- [ ] Complete frontend implementation
- [ ] End-to-end testing

### Phase 2 - Enhancements
- [ ] Authentication system
- [ ] Advanced filtering UI
- [ ] Email integration
- [ ] Export to PDF/CSV
- [ ] Analytics dashboard

### Phase 3 - Scale
- [ ] Multi-tenancy
- [ ] Team collaboration
- [ ] Mobile app
- [ ] Advanced ML models
- [ ] Performance optimization

---

**Ready to start?** 🚀

1. Open [docs/AGENT_IMPLEMENTATION_STEPS.md](docs/AGENT_IMPLEMENTATION_STEPS.md)
2. Follow Step 1 with Context7 MCP
3. Build incrementally, test at each step
4. Deploy and demo!

**Questions?** Check the [docs/](docs/) folder or the MCP guide.

# Backend - Smart Matter Opportunity Detector

## Step 1: Database Foundation - COMPLETED

This directory contains the database foundation for the Smart Matter Opportunity Detector.

## What's Implemented

### Database Models
- **Communication Model** (`app/models/communication.py`)
  - UUID primary key
  - Content, client_name, source_type fields
  - CommunicationType enum (EMAIL, MEETING, NOTE)
  - Indexed on created_at and client_name
  - One-to-many relationship with Opportunities

- **Opportunity Model** (`app/models/opportunity.py`)
  - UUID primary key
  - Foreign key to Communication (CASCADE delete)
  - Fields: title, description, opportunity_type, confidence, estimated_value, extracted_text, status, detected_at
  - OpportunityType enum (REAL_ESTATE, EMPLOYMENT_LAW, MERGERS_AND_ACQUISITIONS, INTELLECTUAL_PROPERTY, LITIGATION)
  - OpportunityStatus enum (NEW, REVIEWING, CONTACTED, CLOSED, ARCHIVED)
  - Indexed on confidence, type, detected_at, and communication_id

- **Base Model** (`app/models/base.py`)
  - Shared created_at and updated_at timestamps
  - AsyncAttrs for async SQLAlchemy support

### Database Connection
- Async SQLAlchemy 2.0 engine (`app/utils/database.py`)
- Connection pooling configured
- get_db() dependency function for FastAPI

### Migration System
- Alembic configured for async migrations
- Initial migration applied: `9dd6863490de_initial_schema.py`
- Migrations support auto-detection of model changes

### Database
- PostgreSQL 15-alpine running in Docker
- Database: nexl_opportunities
- User: nexl
- Port: 5432 (exposed on host)

## Quick Start

### 1. Start the Database
```bash
# From project root
docker-compose up -d db

# Check database is healthy
docker-compose ps
```

### 2. Setup Python Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
# Ensure database is running first
alembic upgrade head
```

### 4. Verify Tables
```bash
docker-compose exec db psql -U nexl -d nexl_opportunities -c "\dt"
```

Expected output:
```
            List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | alembic_version | table | nexl
 public | communications  | table | nexl
 public | opportunities   | table | nexl
```

## Database Schema

### Communications Table
```sql
Table "public.communications"
   Column    |            Type             | Nullable | Default
-------------+-----------------------------+----------+---------
 id          | uuid                        | not null |
 content     | text                        | not null |
 client_name | character varying(200)      | not null |
 source_type | communicationtype           | not null |
 created_at  | timestamp without time zone | not null | now()
 updated_at  | timestamp without time zone | not null | now()

Indexes:
    communications_pkey PRIMARY KEY (id)
    idx_communications_client_name (client_name)
    idx_communications_created_at (created_at)
```

### Opportunities Table
```sql
Table "public.opportunities"
      Column      |            Type             | Nullable | Default
------------------+-----------------------------+----------+---------
 id               | uuid                        | not null |
 communication_id | uuid                        | not null |
 title            | character varying(200)      | not null |
 description      | text                        | not null |
 opportunity_type | opportunitytype             | not null |
 confidence       | numeric(5,2)                | not null |
 estimated_value  | character varying(50)       |          |
 extracted_text   | text                        | not null |
 status           | opportunitystatus           | not null |
 detected_at      | timestamp without time zone | not null |
 created_at       | timestamp without time zone | not null | now()
 updated_at       | timestamp without time zone | not null | now()

Indexes:
    opportunities_pkey PRIMARY KEY (id)
    idx_opportunities_communication_id (communication_id)
    idx_opportunities_confidence (confidence)
    idx_opportunities_detected_at (detected_at)
    idx_opportunities_type (opportunity_type)

Foreign Keys:
    opportunities_communication_id_fkey
    FOREIGN KEY (communication_id)
    REFERENCES communications(id) ON DELETE CASCADE
```

## Working with Migrations

### Create a New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

## Database Management

### Connect to Database
```bash
docker-compose exec db psql -U nexl -d nexl_opportunities
```

### View Table Structure
```sql
\dt                    -- List tables
\d communications      -- Describe communications table
\d opportunities       -- Describe opportunities table
\dT+                   -- List custom types (enums)
```

### Query Data
```sql
SELECT COUNT(*) FROM communications;
SELECT COUNT(*) FROM opportunities;
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://nexl:nexl123@localhost:5432/nexl_opportunities
OPENAI_API_KEY=your_openai_key_here
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
```

## Dependencies

Key packages installed:
- **FastAPI**: Web framework
- **SQLAlchemy 2.0**: Async ORM
- **asyncpg**: PostgreSQL async driver
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **python-dotenv**: Environment variable management

See `requirements.txt` for complete list.

## Next Steps

- [ ] Implement GraphQL API (Day 1, Phase 1.2)
- [ ] Add AI service for opportunity detection (Day 1, Phase 1.3)
- [ ] Implement WebSocket notifications (Day 1, Phase 1.4)
- [ ] Add CRUD operations and queries (Day 1, Phase 1.5)
- [ ] Add unit tests for models

## Troubleshooting

### Database Connection Issues
```bash
# Check database is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Migration Issues
```bash
# Check current migration version
alembic current

# View pending migrations
alembic heads
```

### Clean Slate (CAUTION: Deletes all data)
```bash
# Stop and remove database
docker-compose down -v

# Restart
docker-compose up -d db

# Rerun migrations
alembic upgrade head
```

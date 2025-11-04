# Product Requirements
## Smart Matter Opportunity Detector - Detailed Specifications

**Version:** 1.0 MVP  
**Last Updated:** November 4, 2025

---

## 1. Feature Specifications

### 1.1 Document Upload & Storage

#### Description
Allow users to submit client communications (emails, notes) for AI analysis.

#### User Flow
1. User navigates to dashboard
2. User clicks "Upload Communication" button
3. User pastes text into textarea
4. User adds metadata: Client Name, Source Type (Email/Meeting/Note)
5. User clicks "Analyze"
6. System shows loading state
7. System displays success message + extracted opportunities

#### API Specification
```graphql
mutation CreateCommunication {
  createCommunication(input: {
    content: String!
    clientName: String!
    sourceType: CommunicationType!
  }) {
    communication {
      id
      content
      clientName
      createdAt
    }
    opportunities {
      id
      title
      confidence
    }
  }
}
```

#### Validation Rules
- Content: Required, min 50 characters, max 10,000 characters
- Client Name: Required, max 200 characters
- Source Type: Enum [EMAIL, MEETING, NOTE]

#### Error Handling
- Empty content → "Communication content is required"
- Too short → "Content must be at least 50 characters"
- API failure → "Failed to process. Please try again."

---

### 1.2 AI Opportunity Detection

#### Description
Analyze text using OpenAI to extract business opportunities with confidence scores.

#### Detection Logic

**Step 1: Text Analysis**
```python
# Use OpenAI GPT-4 with structured output
# Extract: opportunity_type, description, confidence, keywords
```

**Step 2: Opportunity Types**
1. **Real Estate** - Keywords: office, lease, property, space, location, relocate
2. **Employment Law** - Keywords: hiring, employees, HR, termination, contracts
3. **M&A** - Keywords: acquisition, merger, buy, sell, due diligence
4. **Intellectual Property** - Keywords: trademark, patent, copyright, IP
5. **Litigation** - Keywords: lawsuit, dispute, court, arbitration

**Step 3: Confidence Scoring**
- **High (80-100%)**: Explicit mention of need + timeline
- **Medium (60-79%)**: Clear need mentioned, no timeline
- **Low (40-59%)**: Implied need, vague language

#### Processing Time
- Target: <5 seconds per document
- Implement async processing with Celery/background tasks

#### API Specification
```graphql
type Opportunity {
  id: ID!
  title: String!
  description: String!
  opportunityType: OpportunityType!
  confidence: Float!
  estimatedValue: String
  extractedText: String!
  detectedAt: DateTime!
  communication: Communication!
  contact: Contact
}

enum OpportunityType {
  REAL_ESTATE
  EMPLOYMENT_LAW
  MERGERS_AND_ACQUISITIONS
  INTELLECTUAL_PROPERTY
  LITIGATION
}
```

#### OpenAI Prompt Template
```
You are analyzing a law firm client communication to identify business opportunities.

Communication:
{content}

Extract any legal service opportunities mentioned. For each opportunity:
1. Type (real_estate, employment_law, m&a, ip, litigation)
2. Brief title (max 60 chars)
3. Description (what client needs)
4. Confidence score (0-100%)
5. Quote the relevant text

Return JSON array of opportunities.
```

---

### 1.3 GraphQL API

#### Description
Provide flexible query interface for frontend to fetch data.

#### Core Queries

**Query 1: List Opportunities**
```graphql
query GetOpportunities(
  $minConfidence: Float
  $type: OpportunityType
  $limit: Int = 20
  $offset: Int = 0
) {
  opportunities(
    minConfidence: $minConfidence
    type: $type
    limit: $limit
    offset: $offset
  ) {
    edges {
      node {
        id
        title
        description
        confidence
        opportunityType
        detectedAt
        communication {
          clientName
          sourceType
        }
      }
    }
    totalCount
  }
}
```

**Query 2: Opportunity Details**
```graphql
query GetOpportunity($id: ID!) {
  opportunity(id: $id) {
    id
    title
    description
    confidence
    opportunityType
    estimatedValue
    extractedText
    detectedAt
    communication {
      id
      content
      clientName
      sourceType
      createdAt
    }
    contact {
      name
      company
      email
    }
  }
}
```

**Query 3: Dashboard Statistics**
```graphql
query GetDashboardStats {
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

#### Core Mutations

**Mutation 1: Create Communication**
(Defined in section 1.1)

**Mutation 2: Update Opportunity Status**
```graphql
mutation UpdateOpportunity($id: ID!, $status: String) {
  updateOpportunity(id: $id, status: $status) {
    opportunity {
      id
      status
    }
  }
}
```

#### Response Standards
- Always include `id` field
- Use ISO 8601 for dates
- Include `__typename` for type identification
- Paginate lists with `limit` and `offset`

---

### 1.4 Real-time Notifications (WebSocket)

#### Description
Push instant notifications to connected clients when high-value opportunities are detected.

#### WebSocket Protocol

**Connection**
```javascript
ws://localhost:8000/ws
```

**Message Format (Protobuf)**
```protobuf
message OpportunityNotification {
  string opportunity_id = 1;
  string title = 2;
  OpportunityType type = 3;
  float confidence = 4;
  string client_name = 5;
  int64 timestamp = 6;
}
```

**Notification Triggers**
- New opportunity detected with confidence ≥ 70%
- Estimated value ≥ $20,000 (if calculated)

#### Client Implementation
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  // Show toast notification
  toast.success(`New opportunity: ${notification.title}`);
};
```

---

### 1.5 Dashboard UI

#### Description
Single-page application showing opportunities with filters and upload capability.

#### Page Layout

**Header**
- Logo/Title: "Smart Matter Opportunity Detector"
- "Upload Communication" button (primary CTA)

**Main Content**
- **Filters** (left sidebar):
  - Opportunity Type (multi-select)
  - Confidence Range (slider: 0-100%)
  - Date Range (last 7/30/90 days)
  
- **Opportunity List** (main area):
  - Card-based layout
  - Each card shows:
    - Title (bold)
    - Client Name
    - Opportunity Type badge
    - Confidence score with color coding:
      - Green: 80-100%
      - Yellow: 60-79%
      - Orange: 40-59%
    - Timestamp (relative: "2 hours ago")
    - Excerpt of extracted text (truncated)
  - Click card → Expand to show full details

**Upload Modal**
- Textarea for content
- Input for client name
- Dropdown for source type
- Submit button

#### Responsive Behavior
- Desktop-first (no mobile optimization for MVP)
- Min width: 1024px

#### Empty States
- No opportunities: "Upload your first communication to get started"
- No results after filter: "No opportunities match your filters"

---

## 2. Data Models

### 2.1 Database Schema

**Communications Table**
```sql
CREATE TABLE communications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  client_name VARCHAR(200) NOT NULL,
  source_type VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Opportunities Table**
```sql
CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  communication_id UUID REFERENCES communications(id),
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  opportunity_type VARCHAR(50) NOT NULL,
  confidence DECIMAL(5,2) NOT NULL,
  estimated_value VARCHAR(50),
  extracted_text TEXT NOT NULL,
  status VARCHAR(20) DEFAULT 'NEW',
  detected_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Contacts Table** (Optional for MVP)
```sql
CREATE TABLE contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(200) NOT NULL,
  company VARCHAR(200),
  email VARCHAR(200),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Indexes
```sql
CREATE INDEX idx_opportunities_confidence ON opportunities(confidence DESC);
CREATE INDEX idx_opportunities_type ON opportunities(opportunity_type);
CREATE INDEX idx_opportunities_detected_at ON opportunities(detected_at DESC);
CREATE INDEX idx_communications_created_at ON communications(created_at DESC);
```

---

## 3. Business Rules

### 3.1 Opportunity Creation Rules
- One communication can generate 0-5 opportunities
- Minimum confidence to save: 40%
- Duplicate detection: If similar opportunity exists (same type + client + within 7 days), increase confidence instead of creating new

### 3.2 Notification Rules
- Only send WebSocket notification if:
  - Confidence ≥ 70% AND
  - Opportunity type is HIGH_VALUE (M&A, Real Estate >$50k)
  
### 3.3 Data Retention
- Keep all communications indefinitely (for MVP)
- Archive opportunities older than 90 days (status = ARCHIVED)

---

## 4. API Rate Limits

### GraphQL API
- 100 requests per minute per client
- Queries: Count as 1 request
- Mutations: Count as 2 requests

### OpenAI API
- Max 10 concurrent requests
- Implement retry with exponential backoff
- Cache results to avoid duplicate analysis

---

## 5. Error Messages

### User-Facing Errors
```json
{
  "errors": [
    {
      "message": "Failed to analyze communication",
      "code": "ANALYSIS_FAILED",
      "extensions": {
        "suggestion": "Please try again or contact support"
      }
    }
  ]
}
```

### Common Error Codes
- `VALIDATION_ERROR` - Input validation failed
- `ANALYSIS_FAILED` - OpenAI processing error
- `NOT_FOUND` - Resource doesn't exist
- `RATE_LIMITED` - Too many requests
- `INTERNAL_ERROR` - Unexpected server error

---

## 6. Testing Requirements

### Unit Tests (70% Coverage)
- All GraphQL resolvers
- Opportunity detection logic
- Database models and queries

### Integration Tests
- Complete flow: Upload → Analysis → Query → Notification
- WebSocket connection and message delivery
- Error handling scenarios

### Test Data
- Sample emails with known opportunities
- Edge cases: very short text, no opportunities, multiple opportunities

---

## 7. Acceptance Criteria

### Feature 1.1: Document Upload ✅
- [ ] Can submit communication via GraphQL mutation
- [ ] Input validation works correctly
- [ ] Success/error messages display
- [ ] Communication saved to database

### Feature 1.2: AI Detection ✅
- [ ] OpenAI integration working
- [ ] Extracts at least 3 different opportunity types
- [ ] Confidence scores are reasonable (40-100%)
- [ ] Processing completes in <5 seconds

### Feature 1.3: GraphQL API ✅
- [ ] All queries return correct data
- [ ] Mutations update database
- [ ] Filtering and pagination work
- [ ] Error handling is graceful

### Feature 1.4: WebSocket ✅
- [ ] Client can connect to WebSocket
- [ ] Notifications sent when opportunity detected
- [ ] Messages use Protobuf format
- [ ] Connection resilient to brief disconnects

### Feature 1.5: Dashboard ✅
- [ ] Displays opportunity list
- [ ] Filters work correctly
- [ ] Upload modal functional
- [ ] Toast notifications appear
- [ ] UI is clean and professional

---

## 8. Definition of Done

A feature is "Done" when:
1. ✅ Code written and follows style guide
2. ✅ Unit tests pass (70%+ coverage)
3. ✅ Integration test passes
4. ✅ Manual QA completed
5. ✅ Documentation updated
6. ✅ Code reviewed (self-review counts for solo project)
7. ✅ No critical bugs

---

## 9. Prioritization

### Day 1 (Must Have)
- Database setup
- GraphQL API basic structure
- Communication upload mutation
- Basic opportunity query

### Day 2 (Must Have)
- OpenAI integration
- Opportunity detection logic
- WebSocket server setup
- Protobuf message definitions

### Day 3 (Must Have)
- Frontend dashboard
- Upload form
- Opportunity list view
- Real-time notifications

### Post-MVP (Nice to Have)
- Advanced filtering
- Export functionality
- Analytics dashboard
- Email integration

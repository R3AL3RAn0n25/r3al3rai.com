# R3ÆLƎR Droid Integration Guide

## 🤖 What is the R3ÆLƎR Droid?

The **R3ÆLƎR Droid** is an adaptive AI system that learns from user interactions and provides personalized, context-aware responses. It's the "personality layer" of R3alerAI that:

- **Adapts** to individual users (adaptability level 0-100)
- **Tracks** user preferences, habits, and goals
- **Analyzes** intent from messages (greeting, help, crypto, technical, investigation)
- **Generates** contextual suggestions based on conversation
- **Stores** interaction history in PostgreSQL (same database as main backend)
- **Personalizes** responses over time

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│             Frontend (React Terminal)                   │
│  • User sends message                                   │
│  • Receives AI response with suggestions               │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│          Node.js Backend (Express - Port 3000)          │
│  • /api/thebrain receives message                       │
│  • Orchestrates 3 AI systems:                           │
│    1. Droid API (adaptive personality)                  │
│    2. Knowledge Base (domain expertise)                 │
│    3. HuggingFace (expert personas)                     │
│  • Combines context → sends to Gemini                   │
└──┬────────────────┬─────────────────┬───────────────────┘
   │                │                 │
   │ Droid API      │ KB API          │ HF API
   │                │                 │
   ▼                ▼                 ▼
┌──────────────┐  ┌────────────┐  ┌───────────────┐
│ droid_api.py │  │knowledge   │  │ HuggingFace   │
│ Port 5002    │  │_api.py     │  │ External API  │
│              │  │Port 5001   │  │ 100 personas  │
│ • Adaptive   │  │            │  └───────────────┘
│   learning   │  │• 7 topics  │
│ • Intent     │  │• 4 prompts │
│   analysis   │  │• 13 sources│
│ • User       │  └────────────┘
│   profiles   │
│ • MongoDB    │
│   storage    │
└──────────────┘
```

---

## 🔄 Request Flow Example

**User Message:** "How do I extract Bitcoin private keys?"

### Step 1: Droid Analysis
```json
POST http://localhost:5002/api/droid/chat
{
  "user_id": "user123",
  "message": "How do I extract Bitcoin private keys?",
  "context": {}
}

Response:
{
  "success": true,
  "response": "Investigation mode activated...",
  "suggestions": [
    "Mobile device forensics",
    "Wallet extraction",
    "Blockchain analysis"
  ],
  "metadata": {
    "intent": "investigation",
    "adaptability_level": 45,
    "interaction_count": 127
  }
}
```

### Step 2: Knowledge Base Search
```json
POST http://localhost:5001/api/kb/search
{
  "query": "extract Bitcoin private keys"
}

Response:
{
  "results": [
    {
      "topic": "wallet",
      "content": "Cryptocurrency Wallet Analysis: ...",
      "relevance": 95
    },
    {
      "topic": "bitcoin",
      "content": "Bitcoin blockchain private keys...",
      "relevance": 88
    }
  ]
}
```

### Step 3: Combined Context
```
--- R3ÆLƎR Droid Context ---
Intent: investigation
Adaptability: 45/100
Interactions: 127
Suggestions: Mobile device forensics, Wallet extraction, Blockchain analysis

--- R3ÆLƎR Knowledge Base Context ---
[WALLET]: Cryptocurrency Wallet Analysis: Methods for extracting...
[BITCOIN]: Bitcoin blockchain private keys are stored in...

User request: How do I extract Bitcoin private keys?
```

### Step 4: Gemini Response
Enhanced prompt sent to Gemini with full context → returns expert-level response

---

## 🚀 Setup & Installation

### 1. Install Droid API Dependencies
```powershell
cd application\Backend
pip install Flask flask-cors pymongo
```

### 2. Configure Database
The Droid uses the same PostgreSQL database as the main backend.

Database configuration in `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=r3aler_user_2025
DB_PASSWORD=R3@l3r_dfe8q9wpxn3m
DB_NAME=r3al3rai_2025
```

**Note:** Tables are created automatically on first run. The Droid will work without database (degraded mode - no persistence)

### 3. Start Droid API
```powershell
# Start individually
.\application\Backend\start-droid-api.ps1

# Or start complete system (KB + Droid + Backend)
.\start-complete-system.ps1
```

### 4. Configure Backend .env
Add to `application/Backend/.env`:
```env
DROID_API_URL=http://localhost:5002
KNOWLEDGE_API_URL=http://localhost:5001

# Database already configured (shared with main backend)
DB_HOST=localhost
DB_PORT=5432
DB_USER=r3aler_user_2025
DB_PASSWORD=R3@l3r_dfe8q9wpxn3m
DB_NAME=r3al3rai_2025
```

---

## 📡 API Endpoints

### Droid API (Port 5002)

#### `POST /api/droid/chat`
Process user message through adaptive Droid
```json
Request:
{
  "user_id": "user123",
  "message": "Hello",
  "context": {
    "role": "Blockchain Expert",
    "timestamp": "2025-10-30T12:00:00Z"
  }
}

Response:
{
  "success": true,
  "response": "Hello. I am R3ÆLƎR AI Droid...",
  "suggestions": ["Ask about cryptocurrency", "Request technical help"],
  "metadata": {
    "user_id": "user123",
    "intent": "greeting",
    "adaptability_level": 45,
    "interaction_count": 128,
    "timestamp": "2025-10-30T12:00:00Z"
  },
  "profile_summary": {
    "likes_count": 5,
    "dislikes_count": 2,
    "habits_count": 3,
    "goals_count": 1
  }
}
```

#### `GET /api/droid/profile/<user_id>`
Get user's Droid profile
```json
Response:
{
  "success": true,
  "profile": {
    "user_id": "user123",
    "adaptability": 45,
    "profile": {
      "likes": ["Python", "Bitcoin", "AI"],
      "dislikes": ["spam", "ads"],
      "habits": ["morning coding"],
      "financial_goals": ["save $10k"],
      "interaction_count": 128,
      "last_interaction": "2025-10-30T12:00:00Z"
    },
    "metadata": {
      "database_connected": true,
      "database_type": "PostgreSQL",
      "last_interaction": "2025-10-30T12:00:00Z"
    }
  }
}
```

#### `POST /api/droid/adapt`
Manually trigger Droid adaptation
```json
Request:
{
  "user_id": "user123",
  "user_data": {
    "intent": "set_goal",
    "goal": "Learn blockchain development"
  }
}

Response:
{
  "success": true,
  "adaptability": 46,
  "message": "Droid adapted successfully"
}
```

#### `GET /health`
Health check
```json
Response:
{
  "status": "healthy",
  "service": "R3ÆLƎR Droid API",
  "active_droids": 5,
  "database_type": "PostgreSQL",
  "database_configured": true
}
```

### Backend Proxy Endpoints (Port 3000)

#### `GET /api/droid/profile`
Get current user's Droid profile (JWT protected)
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://192.168.1.59:3000/api/droid/profile
```

#### `POST /api/droid/adapt`
Adapt current user's Droid (JWT protected)
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"intent":"set_goal","goal":"Master crypto forensics"}' \
  http://192.168.1.59:3000/api/droid/adapt
```

---

## 🎯 Droid Intent System

The Droid automatically analyzes user messages and categorizes intent:

| Intent | Trigger Keywords | Response Behavior |
|--------|------------------|-------------------|
| **greeting** | hello, hi, hey | Welcome message with stats |
| **help_request** | help, support, assist | Offer assistance menu |
| **crypto_inquiry** | bitcoin, crypto, wallet, blockchain | Activate crypto analysis mode |
| **technical_support** | code, programming, debug, function | Engage technical support mode |
| **investigation** | analyze, investigate, forensics | Investigation mode with tools |
| **general_inquiry** | (default) | Adaptive response based on history |

---

## 📊 Adaptability System

The Droid's adaptability level increases with each interaction (max 100):

| Level | Behavior |
|-------|----------|
| **0-20** | Basic responses, learning user patterns |
| **21-50** | Contextual suggestions, preference tracking |
| **51-80** | Proactive recommendations, habit recognition |
| **81-100** | Fully personalized, predictive assistance |

**Example:**
- Interaction 1 (Level 1): "Hello. I am R3ÆLƎR AI Droid."
- Interaction 50 (Level 50): "Hello again! Based on your interest in Bitcoin forensics, I recommend..."
- Interaction 100 (Level 100): "Welcome back! Ready to continue your blockchain investigation from yesterday?"

---

## 🧠 Integration with Other Systems

### Combined Intelligence
When a user sends a message, R3alerAI combines:

1. **Droid Context** - User's adaptability, intent, suggestions, interaction history
2. **Knowledge Base** - Domain expertise (7 topics, 13 sources)
3. **HuggingFace Roles** - Expert persona prompts (100 roles)
4. **Gemini AI** - Language generation and reasoning

**Result:** Highly personalized, expert-level responses with contextual awareness

### Example Enhancement
```javascript
// Without Droid:
User: "Bitcoin mining"
Response: "Bitcoin mining is the process of..."

// With Droid (45 interactions, crypto interest):
User: "Bitcoin mining"
Droid Context: Intent=crypto_inquiry, Interactions=45, Interest=high
Knowledge Context: [BITCOIN] mining algorithms, [WALLET] extraction
Response: "Based on your previous blockchain forensics work, 
          Bitcoin mining involves... [detailed technical explanation]
          Suggestions: Analyze mining pool, Extract miner rewards"
```

---

## 🔧 Testing

### Test Droid API
```powershell
# Health check
curl http://localhost:5002/health

# Chat test
curl -X POST http://localhost:5002/api/droid/chat `
  -H "Content-Type: application/json" `
  -d '{"user_id":"test","message":"Hello"}'

# Get profile
curl http://localhost:5002/api/droid/profile/test
```

### Test Backend Integration
```powershell
# Login first
$token = (curl -X POST http://192.168.1.59:3000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"test","password":"test123"}' | ConvertFrom-Json).token

# Test Droid profile
curl -H "Authorization: Bearer $token" `
  http://192.168.1.59:3000/api/droid/profile

# Test enhanced chat
curl -X POST http://192.168.1.59:3000/api/thebrain `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{"userInput":"How does Bitcoin work?"}'
```

---

## 📝 User Profile Structure

```json
{
  "user_id": "user123",
  "likes": ["Python", "Bitcoin", "AI", "forensics"],
  "dislikes": ["spam", "ads", "trackers"],
  "habits": ["morning coding", "evening research"],
  "financial_goals": ["save $10k", "invest in crypto"],
  "interaction_count": 127,
  "last_interaction": "2025-10-30T12:00:00Z",
  "adaptability_level": 45
}
```

Stored in MongoDB collection: `r3al3r_db.user_profiles`

---

## 🎓 Advanced Features

### 1. **Personalized Suggestions**
Droid generates contextual suggestions based on:
- Current intent
- Past interactions
- User preferences
- Conversation history

### 2. **Intent-Based Routing**
Different intents trigger specialized response modes:
- Crypto → Blockchain expertise
- Technical → Code generation
- Investigation → Forensics tools

### 3. **Adaptive Learning**
Droid learns from every interaction:
- Tracks likes/dislikes
- Identifies habits
- Remembers goals
- Builds user context

### 4. **PostgreSQL Persistence**
All interactions and profiles stored in same database as main backend:
- `droid_profiles` table - User profiles with JSONB columns
- `droid_interactions` table - Interaction history
- Historical analysis available
- Automatic table creation on first run

---

## 🔐 Security Considerations

1. **JWT Protection** - All backend endpoints require valid JWT
2. **User Isolation** - Each user has separate Droid instance
3. **PostgreSQL Security** - Uses same secured database as main backend
4. **Data Privacy** - User profiles contain sensitive preference data
5. **Prepared Statements** - All queries use parameterized statements (SQL injection protection)
5. **Kill Switch** - Emergency disable via `innovations.KillSwitch`

---

## 📚 Summary

**R3ÆLƎR Droid System:**
- ✅ Adaptive AI personality layer
- ✅ User-specific learning (0-100 adaptability)
- ✅ Intent analysis (6 categories)
- ✅ MongoDB persistence (optional)
- ✅ Contextual suggestions
- ✅ Integrated with Knowledge Base + HuggingFace
- ✅ Full backend bridge to Node.js
- ✅ JWT-protected endpoints

**Access Methods:**
1. **Automatic** - Every `/api/thebrain` call uses Droid
2. **Profile** - View user's Droid stats via `/api/droid/profile`
3. **Adapt** - Manual learning via `/api/droid/adapt`
4. **Direct** - Python API at `http://localhost:5002`

**Result:** R3alerAI now has a complete adaptive personality system that learns from users and provides increasingly personalized responses over time!

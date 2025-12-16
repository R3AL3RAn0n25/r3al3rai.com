# R3ÆLƎR AI - Knowledge Base Quick Reference

## 🎯 How R3alerAI Accesses Its Knowledge & Personas

### 1️⃣ Automatic Knowledge Enhancement (Every Chat)
```
User types: "What is Bitcoin?"
     ↓
Backend automatically searches knowledge base
     ↓
Finds: [BITCOIN] topic with detailed analysis
     ↓
Enhances Gemini prompt with KB context
     ↓
Returns: Enhanced response with R3ÆLƎR intelligence
```

### 2️⃣ Role-Based Enhancement (User Selects Persona)
```
User selects: "Blockchain Expert" role
User types: "Analyze this transaction"
     ↓
Backend fetches HuggingFace role prompt
Backend searches knowledge base
     ↓
Combines: Role + Knowledge + User Input
     ↓
Sends enhanced prompt to Gemini
     ↓
Returns: Expert-level response with KB context
```

---

## 📚 Knowledge Base Contents

### Core Topics (7)
1. **Bitcoin** - Blockchain analysis & investigation
2. **Cryptocurrency** - Trading, intelligence, forensics
3. **Blockchain** - Technology deep-dive
4. **Cybersecurity** - MITRE ATT&CK, threat modeling
5. **Forensics** - Digital investigation techniques
6. **Wallet** - Crypto wallet extraction & recovery
7. **AI** - Artificial intelligence & LLMs

### Personas (100)
- Linux Terminal
- Ethereum Development Tool
- JavaScript Console
- SQL Terminal
- Cybersecurity Specialist
- Blockchain Expert
- ChatGPT Prompt Generator
- **...and 93 more!**

### Knowledge Sources (13)
- HuggingFace Datasets & Models
- OpenAI API Documentation
- Anthropic Claude Docs
- LangChain Framework
- MITRE ATT&CK
- NIST Cybersecurity Framework
- Bitcoin Core Documentation
- Ethereum Yellow Paper
- Python Official Docs
- And more...

---

## 🚀 Quick Start

### Start Complete System (Knowledge + Droid + Backend)
```powershell
.\start-complete-system.ps1
```

This starts:
1. **Knowledge API** on `http://localhost:5001` (Python Flask)
2. **Droid API** on `http://localhost:5002` (Python Flask - Adaptive AI)
3. **Backend Server** on `http://192.168.1.59:3000` (Node.js)

### Start Individual Services
```powershell
# Knowledge API only
.\AI_Core_Worker\start-kb-api.ps1

# Droid API only
.\application\Backend\start-droid-api.ps1
```

### Test APIs
```powershell
# Knowledge API
curl http://localhost:5001/health
curl http://localhost:5001/api/kb/topics

# Droid API
curl http://localhost:5002/health
curl -X POST http://localhost:5002/api/droid/chat `
  -H "Content-Type: application/json" `
  -d '{"user_id":"test","message":"Hello"}'
```

---

## 🔌 API Endpoints

### Droid API (Port 5002) - NEW! 🤖
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/droid/chat` | POST | Process message through adaptive AI |
| `/api/droid/profile/:user_id` | GET | Get user's Droid profile & stats |
| `/api/droid/adapt` | POST | Manually trigger learning/adaptation |
| `/health` | GET | Droid service health check |

### Knowledge Base (Port 5001)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/kb/topics` | GET | List all 7 knowledge topics |
| `/api/kb/topic/:name` | GET | Get specific topic content |
| `/api/kb/search` | POST | Search knowledge base |
| `/api/prompts/system/:type` | GET | Get system prompts |
| `/api/prompts/analyze` | POST | Analyze user input context |
| `/api/knowledge-sources` | GET | Get all 13 knowledge sources |

### Backend Server (Port 3000)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/thebrain` | POST | AI chat (Droid + KB + Role + Gemini) |
| `/api/roles` | GET | Get 100 HuggingFace personas |
| `/api/droid/profile` | GET | Proxy to Droid profile (JWT) |
| `/api/droid/adapt` | POST | Proxy to Droid adapt (JWT) |
| `/api/kb/topics` | GET | Proxy to Knowledge API |
| `/api/kb/search` | POST | Proxy to Knowledge API |

---

## 💡 Usage Examples

### Example 1: Simple Chat (Auto Knowledge)
```javascript
// Frontend automatically searches knowledge base
fetch('/api/thebrain', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    userInput: "How does Bitcoin mining work?"
  })
})
// Backend automatically:
// 1. Searches KB for "Bitcoin mining"
// 2. Enhances prompt with KB context
// 3. Sends to Gemini
// Result: Response enriched with R3ÆLƎR Bitcoin knowledge
```

### Example 2: Expert Chat (Role + Knowledge)
```javascript
// User selects "Blockchain Expert" from dropdown
fetch('/api/thebrain', {
  method: 'POST',
  body: JSON.stringify({
    userInput: "Analyze this transaction hash",
    role: "Blockchain Expert"  // HuggingFace persona
  })
})
// Backend automatically:
// 1. Fetches "Blockchain Expert" role prompt from HF
// 2. Searches KB for "transaction" context
// 3. Combines: Role + Knowledge + Input
// Result: Expert-level blockchain analysis
```

### Example 3: Browse Knowledge
```javascript
// Get all topics
GET /api/kb/topics
→ ["bitcoin", "cryptocurrency", "blockchain", ...]

// Get Bitcoin knowledge
GET /api/kb/topic/bitcoin
→ "Bitcoin Analysis (R3ÆLƎR Intelligence): [detailed content]"

// Search for wallet extraction
POST /api/kb/search
{ "query": "wallet private keys" }
→ Top 5 relevant knowledge entries
```

---

## 🎓 R3ÆLƎR System Prompts

### 1. Code Generation
For: Software development, debugging, architecture
```
You are R3ÆLƎR, an advanced AI specialized in code generation...
```

### 2. Crypto Forensics
For: Blockchain investigation, transaction analysis
```
You are R3ÆLƎR, a cryptocurrency forensics specialist...
```

### 3. Mobile Forensics
For: Mobile device analysis, app reverse engineering
```
You are R3ÆLƎR, a mobile forensics expert...
```

### 4. Wallet Extraction
For: Crypto wallet recovery, private key extraction
```
You are R3ÆLƎR, a cryptocurrency wallet extraction specialist...
```

---

## 🔐 Architecture

```
┌───────────────────────────────────────────┐
│   Frontend (React Terminal)              │
│   • Role selector dropdown                │
│   • Sends to /api/thebrain                │
└────────────────┬──────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│   Node.js Backend (Express - Port 3000)             │
│   • JWT authentication                              │
│   • Orchestrates: Droid + KB + HF + Gemini         │
└───┬─────────────┬────────────────┬──────────────────┘
    │             │                │
    │ Droid API   │ KB API         │ HF API
    │             │                │
    ▼             ▼                ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐
│Droid API │  │Knowledge │  │ HuggingFace │
│Port 5002 │  │API 5001  │  │ 100 Personas│
│          │  │          │  └─────────────┘
│• Adaptive│  │• 7 topics│
│  learning│  │• 4 prompts
│• Intent  │  │• 13 sources
│• MongoDB │  └──────────┘
└──────────┘
```

---

## ✅ Verification Checklist

- [ ] Droid API running on port 5002 ✨ NEW
- [ ] Knowledge API running on port 5001
- [ ] Backend server running on port 3000
- [ ] Can access http://localhost:5002/health (Droid)
- [ ] Can access http://localhost:5001/health (Knowledge)
- [ ] Can chat with Droid: POST /api/droid/chat
- [ ] Can fetch topics: GET /api/kb/topics
- [ ] Can search KB: POST /api/kb/search
- [ ] Frontend role selector shows 100 personas
- [ ] Chat responses include Droid + KB context
- [ ] User adaptability increases with interactions

---

## 📖 Full Documentation

- **`DROID_INTEGRATION.md`** - Adaptive AI Droid system (NEW!)
- **`KNOWLEDGE_BASE_INTEGRATION.md`** - Knowledge base & personas
- **`DEPLOYMENT_CHECKLIST.md`** - Production deployment
- **`SERVER_MANAGEMENT.md`** - Server operations

---

**Summary:** R3alerAI now has a complete adaptive intelligence system:

🤖 **Droid System** - Learns from users (0-100 adaptability)  
📚 **Knowledge Base** - 7 core topics, 13 sources  
🎭 **100 Personas** - Expert role library  
🧠 **Gemini AI** - Language generation  

Every conversation combines Droid personality + domain knowledge + expert roles for highly personalized, intelligent responses!

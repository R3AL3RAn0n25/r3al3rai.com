# Adding New Knowledge to R3ÆLƎR AI Storage Facility

## ✅ Automatic Ingestion Now Available!

New knowledge is **automatically stored** in the PostgreSQL Storage Facility using the `/api/kb/ingest` endpoint.

---

## 🚀 How It Works

```
User/Script → Knowledge API (/api/kb/ingest) → Storage Facility (/api/unit/*/store) → PostgreSQL
```

1. **Send knowledge** to Knowledge API endpoint
2. **Knowledge API validates** and forwards to Storage Facility
3. **Storage Facility stores** in PostgreSQL with full-text search indexing
4. **Immediately available** for AI queries

---

## 📝 Adding Knowledge via API

### **Endpoint**
```
POST http://localhost:5001/api/kb/ingest
Content-Type: application/json
```

### **Request Format**
```json
{
  "unit": "crypto",
  "entries": [
    {
      "entry_id": "unique_identifier",
      "topic": "Topic Name",
      "category": "Category",
      "subcategory": "Subcategory (optional)",
      "level": "Beginner|Intermediate|Advanced|Expert",
      "content": "Knowledge content here...",
      "source": "Source name"
    }
  ]
}
```

### **Supported Units**
- `crypto` - Cryptocurrency & blockchain knowledge
- `physics` - Classical physics knowledge
- `quantum` - Quantum physics knowledge
- `space` - Astronomy & aerospace knowledge

---

## 💻 Example: Python Script

```python
import requests

new_knowledge = {
    "unit": "crypto",
    "entries": [
        {
            "entry_id": "ethereum_erc20",
            "topic": "ERC-20 Token Standard",
            "category": "Cryptocurrency",
            "subcategory": "Token Standards",
            "level": "Intermediate",
            "content": """ERC-20 is the technical standard for fungible tokens on Ethereum.

Required Functions:
- totalSupply(): Returns total token supply
- balanceOf(address): Returns balance of an address
- transfer(to, amount): Transfer tokens
- approve(spender, amount): Approve spending
- transferFrom(from, to, amount): Transfer on behalf
- allowance(owner, spender): Check allowance

Events:
- Transfer(from, to, value)
- Approval(owner, spender, value)

Security:
- Beware of approve/transferFrom race condition
- Check for return values
- Use SafeERC20 wrapper (OpenZeppelin)""",
            "source": "R3ÆLƎR Knowledge Base"
        }
    ]
}

response = requests.post(
    'http://localhost:5001/api/kb/ingest',
    json=new_knowledge,
    timeout=30
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Added {result['entries_added']} entries to {result['unit']} unit")
else:
    print(f"❌ Error: {response.text}")
```

---

## 💻 Example: PowerShell

```powershell
$newKnowledge = @{
    unit = "crypto"
    entries = @(
        @{
            entry_id = "ethereum_erc20"
            topic = "ERC-20 Token Standard"
            category = "Cryptocurrency"
            subcategory = "Token Standards"
            level = "Intermediate"
            content = @"
ERC-20 is the technical standard for fungible tokens on Ethereum...
"@
            source = "R3ÆLƎR Knowledge Base"
        }
    )
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:5001/api/kb/ingest" `
    -Method Post `
    -Body $newKnowledge `
    -ContentType "application/json"
```

---

## 💻 Example: cURL

```bash
curl -X POST http://localhost:5001/api/kb/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "unit": "crypto",
    "entries": [{
      "entry_id": "ethereum_erc20",
      "topic": "ERC-20 Token Standard",
      "category": "Cryptocurrency",
      "subcategory": "Token Standards",
      "level": "Intermediate",
      "content": "ERC-20 is the technical standard...",
      "source": "R3ÆLƎR Knowledge Base"
    }]
  }'
```

---

## 📊 Response Format

### **Success Response**
```json
{
  "success": true,
  "message": "Successfully ingested 1 entries to crypto unit",
  "unit": "crypto",
  "entries_added": 1,
  "storage_facility_response": {
    "success": true,
    "unit": "crypto",
    "unit_name": "Cryptocurrency Unit",
    "total_processed": 1,
    "stored": 1,
    "updated": 0,
    "errors": 0
  }
}
```

### **Error Response**
```json
{
  "success": false,
  "error": "Error description"
}
```

---

## 🔄 Update Existing Knowledge

If you POST an entry with an `entry_id` that already exists:
- **Existing entry is UPDATED** with new content
- No duplicates created
- `updated` count incremented in response

```json
{
  "total_processed": 1,
  "stored": 0,
  "updated": 1
}
```

---

## 🧪 Test the Ingestion

Run the test script:
```bash
python test_add_knowledge.py
```

This will:
1. Add 2 new crypto knowledge entries (Ethereum & Monero)
2. Verify storage with a search query
3. Display results showing new knowledge is accessible

---

## 📋 Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `entry_id` | ✅ Yes | Unique identifier (e.g., "ethereum_erc20") |
| `topic` | No | Title/topic of the knowledge entry |
| `content` | No | Main knowledge content (supports markdown) |
| `category` | No | Primary category (default: "General") |
| `subcategory` | No | More specific classification |
| `level` | No | Difficulty level (Beginner/Intermediate/Advanced/Expert) |
| `source` | No | Source attribution (default: "R3ÆLƎR AI") |

---

## ⚡ Best Practices

### **1. Use Descriptive entry_id**
```json
// Good
"entry_id": "ethereum_erc721_nft_standard"

// Not ideal
"entry_id": "entry123"
```

### **2. Structure Content Clearly**
```json
"content": """Brief overview paragraph.

Key Points:
• Point 1
• Point 2
• Point 3

Technical Details:
- Detail 1
- Detail 2

Examples:
[code or examples here]"""
```

### **3. Choose Appropriate Level**
- `Beginner`: Basic concepts, no prior knowledge needed
- `Intermediate`: Requires some background understanding
- `Advanced`: Deep technical knowledge
- `Expert`: Specialized, cutting-edge topics

### **4. Batch Entries**
Send multiple entries in one request for efficiency:
```json
{
  "unit": "crypto",
  "entries": [
    {...entry1...},
    {...entry2...},
    {...entry3...}
  ]
}
```

---

## 🔍 Verify Knowledge Was Added

### **Search Query**
```bash
curl -X POST http://localhost:5001/api/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query":"ERC-20 token","maxPassages":3}'
```

### **Check Storage Facility Directly**
```bash
# Get total entries
curl http://localhost:5003/api/facility/status

# Search crypto unit
curl -X POST http://localhost:5003/api/unit/crypto/search \
  -H "Content-Type: application/json" \
  -d '{"query":"ERC-20","limit":5}'
```

---

## 🛠️ Alternative: Direct Storage Facility Access

You can also POST directly to the Storage Facility (bypasses Knowledge API):

```bash
curl -X POST http://localhost:5003/api/unit/crypto/store \
  -H "Content-Type: application/json" \
  -d '{
    "entries": [{
      "entry_id": "example_entry",
      "topic": "Example Topic",
      "content": "Content here...",
      "category": "Category",
      "level": "Intermediate",
      "source": "Source"
    }]
  }'
```

**Recommended**: Use Knowledge API (`/api/kb/ingest`) for consistency and validation.

---

## 🔧 Troubleshooting

### **Error: "Cannot connect to Storage Facility"**
- Ensure Storage Facility is running on port 5003
- Start with: `cd AI_Core_Worker && python self_hosted_storage_facility_windows.py`

### **Error: "Invalid unit"**
- Check unit name spelling (crypto, physics, quantum, space)
- Unit names are case-sensitive and lowercase

### **Error: "No entries provided"**
- Ensure `entries` array is not empty
- Verify JSON format is correct

### **Knowledge not appearing in search**
- Wait a few seconds for indexing
- Try more specific search terms
- Check if entry was actually stored (check response)

---

## 📚 Example Use Cases

### **1. Adding Forensic Tool Documentation**
```json
{
  "unit": "crypto",
  "entries": [{
    "entry_id": "chainanalysis_reactor",
    "topic": "Chainalysis Reactor - Blockchain Investigation Tool",
    "category": "Cryptocurrency",
    "subcategory": "Forensic Tools",
    "level": "Advanced",
    "content": "Chainalysis Reactor is enterprise blockchain investigation software...",
    "source": "Forensic Tools Documentation"
  }]
}
```

### **2. Adding New Cryptocurrency**
```json
{
  "unit": "crypto",
  "entries": [{
    "entry_id": "cardano_ada",
    "topic": "Cardano (ADA) Overview",
    "category": "Cryptocurrency",
    "subcategory": "Altcoins",
    "level": "Intermediate",
    "content": "Cardano is a proof-of-stake blockchain platform...",
    "source": "Cryptocurrency Knowledge Base"
  }]
}
```

### **3. Adding Malware Analysis Info**
```json
{
  "unit": "crypto",
  "entries": [{
    "entry_id": "cryptojacking_malware",
    "topic": "Cryptojacking Malware Detection",
    "category": "Cryptocurrency",
    "subcategory": "Security",
    "level": "Expert",
    "content": "Cryptojacking is unauthorized use of computing resources...",
    "source": "Cybersecurity Research"
  }]
}
```

---

## ✅ Summary

**Before**: Had to manually edit Python dictionaries or run migration scripts

**Now**: 
- ✅ POST to `/api/kb/ingest` endpoint
- ✅ Knowledge automatically stored in PostgreSQL
- ✅ Immediately searchable by R3ÆLƎR AI
- ✅ Full-text search indexing automatic
- ✅ Update existing entries by re-POSTing with same entry_id

**Storage**: All knowledge persists in PostgreSQL database, no code changes needed!

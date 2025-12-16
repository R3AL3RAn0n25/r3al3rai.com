# 🚀 R3ÆLƎR AI Quick Start Guide

## Start the Complete AI System

### **Prerequisites**
- PostgreSQL running on localhost:5432
- Database: `r3aler_ai` (with all schemas)
- Python 3.8+ with dependencies installed

---

## **Option 1: Start All Services (Recommended)**

### **Windows PowerShell:**
```powershell
# Terminal 1: Storage Facility (Port 5003)
python AI_Core_Worker/self_hosted_storage_facility_windows.py

# Terminal 2: Knowledge API with AI (Port 5001)
python AI_Core_Worker/knowledge_api.py

# Terminal 3: User Authentication API (Port 5004)
python AI_Core_Worker/user_auth_api.py

# Terminal 4: Run Tests
python test_user_system.py
```

### **WSL/Linux:**
```bash
# Terminal 1: Storage Facility
python3 AI_Core_Worker/self_hosted_storage_facility_windows.py &

# Terminal 2: Knowledge API
python3 AI_Core_Worker/knowledge_api.py &

# Terminal 3: User Auth API
python3 AI_Core_Worker/user_auth_api.py &

# Wait for services to start
sleep 5

# Run tests
python3 test_user_system.py
```

---

## **Option 2: Test Individual Components**

### **1. Test User Registration**
```bash
curl -X POST http://localhost:5004/api/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@r3aler.ai",
    "password": "SecurePassword123!",
    "subscription_tier": "paid"
  }'
```

**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "username": "alice",
  "api_key": "abc123xyz..."
}
```

### **2. Test Login**
```bash
curl -X POST http://localhost:5004/api/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@r3aler.ai",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "success": true,
  "session_token": "session_abc123...",
  "user_id": 1,
  "expires_at": "2025-01-17T12:00:00"
}
```

### **3. Test Personalized Knowledge Search**
```bash
curl -X POST http://localhost:5001/api/kb/search \
  -H "Content-Type: application/json" \
  -H "X-User-ID: 1" \
  -d '{
    "query": "cryptography",
    "maxPassages": 5
  }'
```

**Response:**
```json
{
  "success": true,
  "personalized": true,
  "personalized_greeting": "Welcome back! Ready to explore cryptography?",
  "local_results": [...],
  "suggested_topics": [...],
  "recommended_tools": [...]
}
```

### **4. Test AI Dashboard**
```bash
curl -X GET "http://localhost:5001/api/ai/dashboard" \
  -H "X-User-ID: 1"
```

**Response:**
```json
{
  "success": true,
  "dashboard": {
    "greeting": "Welcome back!",
    "profile_summary": {
      "skill_level": "beginner",
      "top_interests": [],
      "learning_style": "balanced"
    },
    "recommended_tools": [],
    "learning_path": {...},
    "suggested_topics": [],
    "trending_now": []
  }
}
```

### **5. Test Self-Learning Insights**
```bash
curl -X GET "http://localhost:5001/api/ai/self-learning/gaps?days=30"
```

### **6. Test Evolution Report**
```bash
curl -X GET "http://localhost:5001/api/ai/evolution/report?days=7"
```

---

## **Testing Workflow**

### **Simulate Real User Activity:**

```python
import requests
import time

# 1. Register user
user = requests.post('http://localhost:5004/api/user/register', json={
    "username": "test_user",
    "email": "test@r3aler.ai",
    "password": "password123",
    "subscription_tier": "paid"
}).json()

user_id = user['user_id']
headers = {"X-User-ID": str(user_id)}

# 2. Perform searches
queries = ["network security", "cryptography", "penetration testing", "wifi hacking"]

for query in queries:
    # Search
    result = requests.post('http://localhost:5001/api/kb/search',
                          json={"query": query},
                          headers=headers).json()
    
    # Click first result
    if result['local_results']:
        entry = result['local_results'][0]
        requests.post('http://localhost:5001/api/ai/activity/log',
                     json={
                         "type": "knowledge_click",
                         "entry_id": entry['key'],
                         "topic": entry['topic'],
                         "relevance_score": entry['relevance'],
                         "position": 1
                     },
                     headers=headers)
    
    time.sleep(2)  # Simulate reading time

# 3. Check personalized dashboard
dashboard = requests.get('http://localhost:5001/api/ai/dashboard',
                        headers=headers).json()

print("User Profile:", dashboard['dashboard']['profile_summary'])
print("Recommended Tools:", dashboard['dashboard']['recommended_tools'][:3])
print("Suggested Topics:", dashboard['dashboard']['suggested_topics'][:5])
```

---

## **Verify System Status**

### **Check All Services:**
```bash
# Storage Facility
curl http://localhost:5003/api/facility/status

# Knowledge API
curl http://localhost:5001/health

# User Auth API
curl http://localhost:5004/api/user/stats
```

**Expected Output:**
```json
{
  "total_entries": 30657,
  "units": ["physics", "quantum", "space", "crypto", "blackarch", "users"],
  "status": "healthy"
}
```

---

## **Common Issues**

### **Issue 1: "Cannot connect to Storage Facility"**
**Solution:**
```bash
# Start Storage Facility first
python AI_Core_Worker/self_hosted_storage_facility_windows.py
```

### **Issue 2: "AI modules not loaded"**
**Solution:**
```bash
# Install dependencies
pip install psycopg2 flask flask-cors bcrypt

# Verify all files exist:
ls AI_Core_Worker/activity_tracker.py
ls AI_Core_Worker/personalization_engine.py
ls AI_Core_Worker/recommendation_engine.py
ls AI_Core_Worker/self_learning_engine.py
ls AI_Core_Worker/evolution_engine.py
```

### **Issue 3: "PostgreSQL connection failed"**
**Solution:**
```bash
# Verify PostgreSQL is running
psql -U r3aler_user_2025 -d r3aler_ai -c "SELECT COUNT(*) FROM physics_unit.knowledge;"

# Should return: 25875
```

### **Issue 4: "User not found"**
**Solution:**
```bash
# Register new user first
curl -X POST http://localhost:5004/api/user/register -H "Content-Type: application/json" -d '{"username":"test","email":"test@r3aler.ai","password":"pass123"}'
```

---

## **Monitor AI Learning**

### **Watch Activity Log:**
```sql
-- Connect to PostgreSQL
psql -U r3aler_user_2025 -d r3aler_ai

-- Check recent activity
SELECT 
    activity_type,
    activity_data->>'query' as query,
    timestamp
FROM user_unit.activity_log
ORDER BY timestamp DESC
LIMIT 10;
```

### **Check User Profiles:**
```sql
SELECT 
    user_id,
    username,
    email,
    subscription_tier,
    created_at,
    last_login
FROM user_unit.profiles;
```

### **Monitor Self-Learning:**
```bash
# Get knowledge gaps
curl "http://localhost:5001/api/ai/self-learning/gaps?days=7"

# Get evolution insights
curl "http://localhost:5001/api/ai/evolution/report?days=7"
```

---

## **Production Deployment**

### **Environment Variables:**
```bash
export KNOWLEDGE_API_PORT=5001
export STORAGE_FACILITY_URL=http://localhost:5003
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=r3aler_ai
export DATABASE_USER=r3aler_user_2025
export DATABASE_PASSWORD=postgres
```

### **Systemd Service (Linux):**
```ini
[Unit]
Description=R3ÆLƎR AI Knowledge API
After=network.target postgresql.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/path/to/R3aler-ai
ExecStart=/usr/bin/python3 AI_Core_Worker/knowledge_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## **Next Steps**

1. ✅ Start all services
2. ✅ Run `test_user_system.py`
3. ✅ Create test users
4. ✅ Perform searches
5. ✅ Monitor AI learning
6. ✅ Check personalization improvements
7. ✅ Review self-learning reports
8. ✅ Analyze evolution metrics

---

## **Support**

- **Documentation:** `AI_ADAPTABILITY_COMPLETE.md`
- **Architecture:** `USER_PROFILE_SYSTEM_EXPLAINED.md`
- **Testing:** `test_user_system.py`

---

**🎉 R3ÆLƎR AI is ready to learn, adapt, and evolve!** 🚀

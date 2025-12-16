# AI Core Worker Upgrades - HuggingFace Integration

## Overview
Enhanced `ai_core_worker.py` with HuggingFace Awesome ChatGPT Prompts dataset integration for dynamic persona/role-based AI responses.

## New Features

### 1. **HuggingFace Prompts Integration**
- **Dataset**: `fka/awesome-chatgpt-prompts` - 100+ curated ChatGPT prompts and personas
- **API Endpoints**:
  - Rows: `https://datasets-server.huggingface.co/rows`
  - Splits: `https://datasets-server.huggingface.co/splits`
  - Parquet: `https://huggingface.co/api/datasets/fka/awesome-chatgpt-prompts/parquet/default/train`

### 2. **Prompt Caching System**
- In-memory cache with 1-hour TTL (configurable)
- Reduces API calls and improves response time
- Force refresh option available

### 3. **New Methods in RealerAI Class**

#### `load_hf_prompts(force_refresh=False)`
Fetches and caches prompts from HuggingFace dataset.
```python
prompts = ai.load_hf_prompts()  # Returns list of {"act": "...", "prompt": "..."}
```

#### `get_prompt_by_role(role_name)`
Retrieves a specific prompt template by role name (case-insensitive).
```python
linux_prompt = ai.get_prompt_by_role("Linux Terminal")
```

#### `list_available_roles()`
Lists all available AI roles/personas from the dataset.
```python
roles = ai.list_available_roles()  # Returns: ["An Ethereum Developer", "SEO Prompt", ...]
```

#### `enhance_system_prompt_with_role(base_prompt, role_name)`
Combines R3ÆLƎR base personality with HuggingFace role for hybrid personas.
```python
enhanced = ai.enhance_system_prompt_with_role(
    R3AELERPrompts.CODE_GENERATION_SYSTEM_PROMPT, 
    "Python Developer"
)
```

#### `process_chat_with_role(user_message, role_name=None, ...)`
Processes chat with optional role/persona enhancement.
```python
response = ai.process_chat_with_role(
    "Explain async/await", 
    role_name="Python Developer",
    user_id=123
)
```

### 4. **Enhanced Prompts System**

#### New Knowledge Sources in `prompts.py`:
- **HuggingFace Prompts Dataset**: AI persona library
- **HuggingFace Models Hub**: Pre-trained model repository
- **OpenAI API Docs**: GPT model documentation
- **Anthropic Claude Docs**: Claude AI reference
- **LangChain Docs**: LLM application framework

#### New Static Method: `analyze_context(user_message, conversation_history)`
Advanced context analysis for intelligent prompt selection.

**Returns**:
```python
{
    "domain": "technology|cryptocurrency|forensics|mobile|ai|general",
    "intent": "creation|analysis|explanation|guidance|question",
    "complexity": "simple|moderate|advanced",
    "has_context": bool,
    "keywords": [...]
}
```

## Usage Examples

### Example 1: Basic Role Usage
```python
from ai_core_worker import RealerAI

ai = RealerAI(config, db, openai_key)

# List available roles
roles = ai.list_available_roles()
print(f"Available roles: {len(roles)}")

# Use specific role
response = ai.process_chat_with_role(
    "Write a regex for email validation",
    role_name="Regex Generator",
    user_id=456
)
```

### Example 2: Hybrid Persona (R3ÆLƎR + HuggingFace)
```python
# Combine R3ÆLƎR forensics expertise with specific role
response = ai.process_chat_with_role(
    "Analyze this Bitcoin transaction",
    role_name="Blockchain Developer",
    user_id=789
)
# Result: R3ÆLƎR forensics knowledge + blockchain dev persona
```

### Example 3: Dynamic Context-Aware Processing
```python
# AI automatically selects appropriate base prompt
response = ai.process_chat(
    "How do I extract keys from a wallet.dat file?",
    user_id=101
)
# Automatically uses CRYPTO_FORENSICS_SYSTEM_PROMPT based on keywords
```

## Backend Integration (Express.js)

Update `/api/thebrain` endpoint to support role parameter:

```javascript
app.post('/api/thebrain', verifyJWT, async (req, res) => {
  const { userInput, role } = req.body;
  
  // Forward to AI Core Worker with optional role
  const response = await aiCore.process_chat_with_role(
    userInput,
    role,
    req.user.uid
  );
  
  res.json({ success: true, response });
});
```

## Frontend Integration (React)

Add role selector to Terminal component:

```tsx
const [selectedRole, setSelectedRole] = useState<string | null>(null);
const [availableRoles, setAvailableRoles] = useState<string[]>([]);

// Fetch roles on mount
useEffect(() => {
  fetch('/api/roles')
    .then(r => r.json())
    .then(data => setAvailableRoles(data.roles));
}, []);

// Send with role
const onSend = async () => {
  const res = await fetch('/api/thebrain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ 
      userInput: input,
      role: selectedRole  // Optional role parameter
    })
  });
};
```

## API Endpoints to Add

### GET `/api/roles`
List available AI roles from HuggingFace.
```json
{
  "success": true,
  "roles": ["An Ethereum Developer", "SEO Prompt", "Linux Terminal", ...]
}
```

### POST `/api/thebrain`
Enhanced with optional `role` parameter.
```json
{
  "userInput": "Write a smart contract",
  "role": "An Ethereum Developer"  // Optional
}
```

## Performance Considerations

- **Cache**: 100 prompts cached in memory (~50KB)
- **Cache TTL**: 1 hour (3600 seconds)
- **API Calls**: Only on cache miss or force refresh
- **Fallback**: System works without HuggingFace if API fails

## Testing

Run the test script:
```bash
python AI_Core_Worker/test_hf_prompts.py
```

Or use PowerShell:
```powershell
irm "https://datasets-server.huggingface.co/rows?dataset=fka%2Fawesome-chatgpt-prompts&config=default&split=train&offset=0&length=5"
```

## Security & Best Practices

1. **Rate Limiting**: HuggingFace API has rate limits; cache aggressively
2. **Error Handling**: System gracefully degrades if HuggingFace is unavailable
3. **Validation**: Role names are sanitized and matched case-insensitively
4. **Logging**: All HuggingFace interactions are logged for debugging

## Future Enhancements

- [ ] User-selectable roles in UI
- [ ] Custom prompt templates saved per user
- [ ] Role history and favorites
- [ ] Integration with other prompt libraries (PromptHero, PromptBase)
- [ ] Fine-tuning prompts based on user feedback
- [ ] Multi-language prompt support

## Dependencies

```python
requests>=2.31.0  # For HuggingFace API calls
```

Add to `requirements.txt`:
```
requests>=2.31.0
```

---

**Created**: 2025-10-30  
**Version**: 1.0  
**Author**: R3ÆLƎR AI Development Team

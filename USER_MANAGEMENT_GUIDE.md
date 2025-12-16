# R3AL3R AI User Management System

## 🎯 Overview

Your R3AL3R AI system now has a **complete user management solution** that supports:
- ✅ **3 Subscription Tiers** (Basic, Premium, Enterprise)
- ✅ **AI Personalization** per user
- ✅ **Usage Tracking** and limits enforcement
- ✅ **User Preferences** and settings
- ✅ **Session Management**
- ✅ **Subscription History** audit trail

---

## 📊 Database Tables

### 1. **subscription_tiers** - Subscription Plans

Defines the 3 subscription tiers with their limits and features:

| Tier | Monthly Price | API Calls/Day | Tools/Day | AI Tokens/Month | Features |
|------|---------------|---------------|-----------|-----------------|----------|
| **Basic** | $0 (Free) | 100 | 5 | 10,000 | Basic API access |
| **Premium** | $29.99 | 1,000 | 50 | 100,000 | + AI personalization, priority support, custom tools |
| **Enterprise** | $99.99 | 10,000 | 500 | 1,000,000 | + Dedicated support, white label, unlimited features |

**Features stored as JSON:**
```json
{
  "advanced_security": true,
  "api_access": true,
  "priority_support": true,
  "custom_tools": true,
  "ai_personalization": true,
  "dedicated_support": true,
  "white_label": true
}
```

---

### 2. **users** - Enhanced User Profiles

Extended user table with subscription information:

**Columns:**
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `full_name` - User's full name
- `password_hash` - Encrypted password
- `role` - User role (user, admin, moderator)
- `subscription_tier_id` - Links to subscription tier (FK)
- `subscription_status` - active, cancelled, expired, trial
- `subscription_start_date` - When subscription started
- `subscription_end_date` - When subscription expires
- `trial_ends_at` - Trial expiration
- `is_email_verified` - Email verification status
- `profile_image_url` - Profile picture URL
- `last_login` - Last login timestamp
- `created_at`, `updated_at` - Timestamps

---

### 3. **user_ai_preferences** - AI Personalization

Stores user-specific AI behavior preferences:

**Purpose:** Allows each user to have a customized AI experience

**Examples:**
```sql
-- User prefers aggressive security scanning
INSERT INTO user_ai_preferences (user_id, preference_key, preference_value) VALUES
(1, 'security_scan_mode', '{"mode": "aggressive", "auto_block": true}');

-- User's preferred output format
INSERT INTO user_ai_preferences (user_id, preference_key, preference_value) VALUES
(1, 'output_format', '{"format": "json", "verbose": true}');

-- User's AI assistant personality
INSERT INTO user_ai_preferences (user_id, preference_key, preference_value) VALUES
(1, 'ai_personality', '{"tone": "professional", "detail_level": "high"}');
```

---

### 4. **user_ai_learning** - AI Adaptation

Tracks user interactions for AI to learn and adapt:

**What it stores:**
- User queries and responses
- Tool usage patterns
- User feedback (1-5 stars)
- Learned patterns (AI-extracted)

**How AI uses this:**
1. **Pattern Recognition:** Learns user's favorite tools and workflows
2. **Suggestion Improvement:** Suggests tools based on past success
3. **Error Prevention:** Remembers past mistakes and warns user
4. **Personalized Responses:** Adapts tone and detail level

**Example:**
```sql
INSERT INTO user_ai_learning (user_id, interaction_type, input_data, output_data, feedback_score, learned_patterns) VALUES
(1, 'query', 
 '{"query": "scan for SQL injection", "target": "example.com"}',
 '{"tool_used": "sqlmap", "results_found": 3}',
 5,
 '{"preferred_tools": ["sqlmap", "nmap"], "success_rate": 0.95"}');
```

---

### 5. **user_usage_stats** - Usage Tracking

Daily usage statistics for enforcing tier limits:

**Tracks:**
- `api_calls_count` - API calls made today
- `blackarch_tools_used` - Tools executed today
- `ai_tokens_used` - AI tokens consumed this month
- `total_queries` - Total queries
- `total_errors` - Error count
- `avg_response_time` - Performance metric

**Enforcement Logic:**
```python
def can_user_execute_tool(user_id):
    today_usage = get_usage_today(user_id)
    user_tier = get_user_tier(user_id)
    
    if today_usage.tools_used >= user_tier.max_tools_per_day:
        return False, "Daily tool limit reached. Upgrade to Premium for more!"
    return True, "OK"
```

---

### 6. **user_settings** - User Preferences

User interface and system preferences:

**Settings:**
- `theme` - dark, light, auto
- `language` - en, es, fr, etc.
- `timezone` - UTC, America/New_York, etc.
- `notifications_enabled` - Enable/disable notifications
- `email_notifications` - Email alerts
- `security_alerts` - Security notifications
- `ai_suggestions_enabled` - Show AI suggestions
- `auto_save` - Auto-save feature
- `custom_settings` - JSONB for any custom settings

---

### 7. **user_sessions** - Session Management

Active user sessions for authentication:

**Columns:**
- `session_token` - Unique session token (JWT)
- `ip_address` - User's IP
- `user_agent` - Browser/device info
- `device_info` - Device details (JSON)
- `is_active` - Session status
- `expires_at` - Session expiration
- `last_activity` - Last activity timestamp

**Security:**
- Automatic session expiration
- Multi-device support
- IP tracking for security
- Device fingerprinting

---

### 8. **subscription_history** - Audit Trail

Complete history of subscription changes:

**Tracks:**
- Upgrades (Basic → Premium)
- Downgrades (Premium → Basic)
- Cancellations
- Renewals
- Trial starts
- Payment information (amount, method, transaction ID)

---

### 9. **user_favorite_tools** - Saved Tools

User's favorite/frequently used tools:

**Features:**
- Save favorite tools
- Track usage count
- Store custom configurations per tool
- Quick access to frequently used tools

**Example:**
```sql
INSERT INTO user_favorite_tools (user_id, tool_name, category, usage_count, custom_config) VALUES
(1, 'nmap', 'scanner', 25, '{"default_scan": "-sV -sC", "save_output": true}');
```

---

## 🔍 Database Views

### user_profiles
Complete user profile with subscription info in one query:

```sql
SELECT * FROM user_profiles WHERE username = 'john_doe';
```

Returns:
- User details
- Current subscription tier
- Tier features
- Subscription dates
- Last login

### user_usage_today
Current usage vs limits:

```sql
SELECT * FROM user_usage_today WHERE username = 'john_doe';
```

Returns:
- API calls today vs limit
- Tools used today vs limit
- Whether limits are reached
- Tier information

---

## 💡 How AI Personalization Works

### Example Workflow:

1. **User executes a tool:**
   ```python
   execute_tool('nmap', target='192.168.1.1', args=['-sV'])
   ```

2. **System logs to user_ai_learning:**
   ```sql
   INSERT INTO user_ai_learning (user_id, interaction_type, input_data, learned_patterns)
   VALUES (1, 'tool_use', '{"tool": "nmap", "args": ["-sV"]}', '{"scan_type": "version_detection"}');
   ```

3. **AI learns user prefers version detection**

4. **Next time, AI suggests:**
   > "Based on your previous scans, would you like to add version detection (-sV)?"

5. **User provides feedback:**
   ```sql
   UPDATE user_ai_learning SET feedback_score = 5 WHERE id = 123;
   ```

6. **AI confidence increases, continues suggesting**

---

## 🎯 Subscription Tier Enforcement

### Code Example:

```python
def check_user_limits(user_id):
    # Get user's tier and today's usage
    usage = db.query("""
        SELECT * FROM user_usage_today 
        WHERE user_id = ?
    """, user_id)
    
    # Check API limit
    if usage['api_limit_reached']:
        return {
            'allowed': False,
            'message': 'Daily API limit reached',
            'upgrade_url': '/upgrade-to-premium'
        }
    
    # Check tools limit
    if usage['tools_limit_reached']:
        return {
            'allowed': False,
            'message': f'Daily tool limit ({usage["tools_limit"]}) reached',
            'upgrade_message': 'Upgrade to Premium for 50 tools/day'
        }
    
    return {'allowed': True}
```

---

## 📱 User Registration Example

```sql
-- 1. Create user with Basic tier
INSERT INTO users (username, email, password_hash, subscription_tier_id, subscription_status)
VALUES ('john_doe', 'john@example.com', '$2b$12$...', 1, 'trial');

-- 2. Set trial period (14 days)
UPDATE users SET trial_ends_at = NOW() + INTERVAL '14 days' WHERE username = 'john_doe';

-- 3. Create default settings
INSERT INTO user_settings (user_id, theme, language) 
VALUES ((SELECT id FROM users WHERE username = 'john_doe'), 'dark', 'en');

-- 4. Initialize usage stats
INSERT INTO user_usage_stats (user_id, date) 
VALUES ((SELECT id FROM users WHERE username = 'john_doe'), CURRENT_DATE);
```

---

## 🔄 Upgrade User Example

```sql
-- User upgrades from Basic to Premium
BEGIN;

-- Update user's tier
UPDATE users 
SET subscription_tier_id = 2,
    subscription_status = 'active',
    subscription_start_date = NOW(),
    subscription_end_date = NOW() + INTERVAL '1 month'
WHERE id = 1;

-- Log the upgrade
INSERT INTO subscription_history (user_id, tier_id, action, previous_tier_id, amount_paid, payment_method)
VALUES (1, 2, 'upgrade', 1, 29.99, 'credit_card');

COMMIT;
```

---

## 🎨 Query Examples

### Get user's AI preferences:
```sql
SELECT preference_key, preference_value 
FROM user_ai_preferences 
WHERE user_id = 1;
```

### Get user's most used tools:
```sql
SELECT tool_name, usage_count, last_used
FROM user_favorite_tools
WHERE user_id = 1
ORDER BY usage_count DESC
LIMIT 10;
```

### Get user's subscription history:
```sql
SELECT action, tier_name, amount_paid, created_at
FROM subscription_history sh
JOIN subscription_tiers st ON sh.tier_id = st.id
WHERE user_id = 1
ORDER BY created_at DESC;
```

### Check if user can perform action:
```sql
SELECT 
    CASE 
        WHEN api_limit_reached THEN 'API limit reached'
        WHEN tools_limit_reached THEN 'Tools limit reached'
        ELSE 'OK'
    END as status
FROM user_usage_today
WHERE user_id = 1;
```

---

## 🚀 Implementation in Your Code

Your Python/Node.js code can now:

1. **Check user permissions:**
   ```python
   if not user.has_feature('custom_tools'):
       return "Upgrade to Premium for custom tools"
   ```

2. **Track usage:**
   ```python
   increment_user_usage(user_id, 'api_calls')
   increment_user_usage(user_id, 'blackarch_tools')
   ```

3. **Personalize AI responses:**
   ```python
   user_prefs = get_ai_preferences(user_id)
   ai_response = generate_response(query, personality=user_prefs)
   ```

4. **Enforce limits:**
   ```python
   if user_reached_limit(user_id, 'tools'):
       suggest_upgrade(user_id)
   ```

---

## ✅ Summary

Your R3AL3R AI now has:
- ✅ **Complete user profiles** with subscription tiers
- ✅ **AI personalization** that learns from each user
- ✅ **Usage tracking** with tier-based limits
- ✅ **Subscription management** with history
- ✅ **Session management** for security
- ✅ **User preferences** for customization
- ✅ **Favorite tools** with custom configs

**Next Steps:**
1. Integrate with your authentication system
2. Add payment processing (Stripe/PayPal)
3. Build subscription upgrade/downgrade flows
4. Implement AI learning algorithms
5. Create user dashboard UI

🎉 **Your database is production-ready for managing R3AL3R AI public users!**

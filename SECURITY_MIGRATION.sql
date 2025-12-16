# R3ÆLƎR AI - Database Migration Guide for user_auth_api.py
# 
# This guide shows you how to migrate the authentication database
# to support the new security features (hashed API keys, etc.)

# MIGRATION STEPS:
# 1. Back up your current database
# 2. Run the ALTER TABLE statements below
# 3. Update your .env file with proper credentials
# 4. Restart the application

-- ============================================
-- PostgreSQL Migration Script
-- ============================================

-- Add new columns for hashed API keys if not exists
ALTER TABLE user_unit.profiles
ADD COLUMN IF NOT EXISTS api_key_hash VARCHAR(64);

-- Migrate existing API keys to hashed format
-- First, hash all existing plaintext API keys
UPDATE user_unit.profiles
SET api_key_hash = encode(digest(api_key, 'sha256'), 'hex')
WHERE api_key IS NOT NULL AND api_key_hash IS NULL;

-- Drop the old api_key column after migration is complete
-- ALTER TABLE user_unit.profiles DROP COLUMN api_key;

-- Create index on api_key_hash for faster lookups
CREATE INDEX IF NOT EXISTS idx_profiles_api_key_hash 
ON user_unit.profiles(api_key_hash);

-- Add created_at timestamp if not exists
ALTER TABLE user_unit.profiles
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- Add session activity tracking
ALTER TABLE user_unit.sessions
ADD COLUMN IF NOT EXISTS ip_address INET;

ALTER TABLE user_unit.sessions
ADD COLUMN IF NOT EXISTS user_agent VARCHAR(500);

-- Create index on session expiration for faster queries
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at 
ON user_unit.sessions(expires_at);

-- Enable logging for security events
ALTER TABLE user_unit.profiles
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;

-- ============================================
-- Security Best Practices
-- ============================================

-- 1. Enable row-level security (RLS)
ALTER TABLE user_unit.profiles ENABLE ROW LEVEL SECURITY;

-- 2. Create a policy so users can only see their own profile
CREATE POLICY user_profile_policy 
ON user_unit.profiles 
FOR SELECT 
USING (user_id = current_user_id);

-- 3. Add audit logging for password changes
CREATE TABLE IF NOT EXISTS user_unit.audit_log (
    audit_id SERIAL PRIMARY KEY,
    user_id UUID,
    action VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    details JSONB
);

-- ============================================
-- Backup Strategy
-- ============================================

-- Create a backup table before making changes:
-- CREATE TABLE user_unit.profiles_backup AS SELECT * FROM user_unit.profiles;

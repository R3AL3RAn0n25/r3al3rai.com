#!/bin/bash
# R3ÆLƎR AI - Security Setup Script
# Applies security hardening to user_auth_api.py

echo "=================================="
echo "R3ÆLƎR AI - Security Setup"
echo "=================================="

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found!"
    echo "Creating .env.local from .env.example..."
    cp .env.example .env.local
    echo "✅ Created .env.local"
    echo ""
    echo "⚠️  Please edit .env.local with your database credentials:"
    echo "   nano .env.local"
    exit 1
fi

# Install required packages
echo "📦 Installing required dependencies..."
pip install python-dotenv flask-limiter --quiet
echo "✅ Dependencies installed"

# Check database connection
echo ""
echo "🔍 Checking database configuration in .env.local..."
source .env.local

if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo "❌ Missing database credentials in .env.local"
    exit 1
fi

echo "✅ Configuration looks good"

# Show migration reminder
echo ""
echo "=================================="
echo "⚠️  DATABASE MIGRATION REQUIRED"
echo "=================================="
echo ""
echo "Run this SQL migration on your PostgreSQL database:"
echo ""
echo "  psql -U $DB_USER -d $DB_NAME < SECURITY_MIGRATION.sql"
echo ""
echo "Or manually run:"
echo ""
echo "  ALTER TABLE user_unit.profiles ADD COLUMN api_key_hash VARCHAR(64);"
echo "  CREATE INDEX idx_profiles_api_key_hash ON user_unit.profiles(api_key_hash);"
echo "  ALTER TABLE user_unit.sessions ADD COLUMN ip_address INET;"
echo "  ALTER TABLE user_unit.sessions ADD COLUMN user_agent VARCHAR(500);"
echo ""

# Verify files
echo "=================================="
echo "📋 Verification"
echo "=================================="

if [ -f "src/apis/user_auth_api.py" ]; then
    echo "✅ user_auth_api.py found"
else
    echo "❌ user_auth_api.py not found"
    exit 1
fi

if [ -f ".env.local" ]; then
    echo "✅ .env.local configured"
else
    echo "❌ .env.local not found"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ SETUP COMPLETE!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run database migrations"
echo "2. Start the API:"
echo "   python src/apis/user_auth_api.py"
echo ""
echo "Test with:"
echo "   curl http://localhost:5004/health"
echo ""

#!/bin/bash
# Start R3ÆLƎR Knowledge Base API

echo "🧠 Starting R3ÆLƎR AI Knowledge Base API..."
echo "================================================"

cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-kb-api.txt

# Start API
echo "🚀 Starting Knowledge API on http://localhost:5001"
echo "================================================"
python3 knowledge_api.py

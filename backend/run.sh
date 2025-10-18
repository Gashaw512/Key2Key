#!/bin/bash
# ========================================
# 🚀 Key2Key Backend Run Script
# ========================================

# Exit on any error
set -e

# Go to backend directory (if not already)
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated."
else
    echo "❌ Virtual environment not found. Run:"
    echo "   python -m venv .venv && source .venv/bin/activate"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file missing! Copying from example..."
    cp .env.example .env
fi

# Run Uvicorn with reload
echo "🚀 Starting Key2Key API..."
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

#!/usr/bin/env bash
# ========================================
# 🚀 Key2Key Backend Run Script
# ========================================
# Purpose: Activate environment, check prerequisites, and start FastAPI with Uvicorn.
# Usage: ./run.sh
# ========================================

set -euo pipefail  # Exit on error, unset vars are errors, fail on pipe errors

# --- Functions ---
info()  { echo -e "\033[1;32m[INFO]\033[0m $1"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m $1"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# --- Go to script directory ---
cd "$(dirname "$0")" || { error "Cannot change to script directory"; exit 1; }

# --- Check virtual environment ---
if [ -d ".venv" ]; then
    source .venv/bin/activate
    info "Virtual environment activated."
else
    warn ".venv not found. Creating..."
    python3 -m venv .venv
    source .venv/bin/activate
    info "Virtual environment created and activated."
fi

# --- Check .env file ---
if [ ! -f ".env" ]; then
    warn ".env file missing. Copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        info ".env file created from .env.example"
    else
        error ".env.example missing. Cannot continue!"
        exit 1
    fi
fi

# --- Install dependencies if missing ---
if ! python -c "import fastapi, uvicorn" &>/dev/null; then
    warn "Dependencies missing. Installing..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# --- Start the API ---
info "🚀 Starting Key2Key API on http://127.0.0.1:8000"
uvicorn app.main:app \
    --reload \
    --host 127.0.0.1 \
    --port 8000 \
    --log-level info

# Optional: for production, replace --reload with a proper ASGI server manager like Gunicorn or systemd

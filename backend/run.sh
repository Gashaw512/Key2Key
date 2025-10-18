#!/usr/bin/env bash
# =======================================================
# 🚀 Key2Key Backend Run Script
# =======================================================
# Purpose: Manages virtual environment, ensures dependencies,
#          and starts the FastAPI application with optional reloading.
# Usage: ./run.sh --dev  (for development with hot-reloading)
#        ./run.sh --prod (for production, no reloading)
# =======================================================

set -euo pipefail

# --- Configuration Variables ---
VENV_DIR=".venv"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate" # Define the path to the activation script
APP_MODULE="app.main:app"
HOST="127.0.0.1"
PORT="8000"
RELOAD_FLAG="" # Default to empty (production mode)

# --- Logging Functions ---
info()  { echo -e "\033[1;32m[INFO]\033[0m $1"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m $1"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# --- Set Environment Mode ---
# Check for --dev argument
if [ "$#" -gt 0 ] && [ "$1" == "--dev" ]; then
    RELOAD_FLAG="--reload"
    info "Operating in DEVELOPMENT mode (Uvicorn reloading enabled)."
else
    info "Operating in PRODUCTION mode (Uvicorn reloading disabled)."
fi

# --- 1. Go to script directory ---
cd "$(dirname "$0")" || { error "Failed to change to script directory."; exit 1; }

# --- 2. Virtual Environment Setup ---
# Check if the VENV directory *or* the crucial activate script is missing.
if [ ! -d "$VENV_DIR" ] || [ ! -f "$ACTIVATE_SCRIPT" ]; then
    # If the directory exists but is incomplete, remove it first to ensure a clean start
    if [ -d "$VENV_DIR" ]; then
        warn "Virtual environment '$VENV_DIR' is incomplete (missing activate script). Removing and recreating..."
        rm -rf "$VENV_DIR"
    else
        warn "Virtual environment '$VENV_DIR' not found. Creating..."
    fi
    
    # Attempt to create the environment
    python3 -m venv "$VENV_DIR" || { error "Failed to create virtual environment. Check python3-venv package or permissions."; exit 1; }
    
    # After creation, perform a final check
    if [ ! -f "$ACTIVATE_SCRIPT" ]; then
        error "Creation succeeded but activation script '$ACTIVATE_SCRIPT' is still missing. Aborting."
        exit 1
    fi

    info "Virtual environment created successfully."
    NEEDS_INSTALL=true
fi

# Activate the virtual environment
source "$ACTIVATE_SCRIPT"
info "Virtual environment activated."


# --- 3. Dependency Check and Install ---
# Check if the environment looks fresh/uninitialized by testing for a core package.
# Use a more robust check: if the SQLAlchemy core library is missing, assume installation is needed.
if ! python -c "import sqlalchemy.orm" &>/dev/null; then
    NEEDS_INSTALL=true
fi

if [ "${NEEDS_INSTALL:-false}" = true ] || [ ! -f "requirements.txt" ]; then
    if [ -f "requirements.txt" ]; then
        warn "Dependencies missing or Venv is new. Installing packages from requirements.txt..."
        pip install --upgrade pip > /dev/null 2>&1
        pip install -r requirements.txt || { error "Failed to install dependencies."; exit 1; }
        info "Dependencies installed successfully."
    else
        error "requirements.txt not found. Cannot install dependencies."
        exit 1
    fi
fi

# --- 4. .env File Check ---
if [ ! -f ".env" ]; then
    warn ".env file missing. Copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        info ".env file created. Please customize .env for your database settings."
    else
        error ".env.example missing. Cannot continue without configuration!"
        exit 1
    fi
fi


# --- 5. Start the API ---
info "🚀 Starting Key2Key API on http://$HOST:$PORT (Module: $APP_MODULE)"
# Execute Uvicorn with conditional reload flag
uvicorn "$APP_MODULE" \
    $RELOAD_FLAG \
    --host "$HOST" \
    --port "$PORT" \
    --log-level info

# --- Final Cleanup ---
deactivate
info "Script finished."

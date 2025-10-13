@echo off
:: ========================================
:: 🚀 Key2Key Backend Run Script
:: ========================================
cd %~dp0

if not exist .venv (
    echo ❌ Virtual environment not found. Run:
    echo     python -m venv .venv && .venv\Scripts\activate
    exit /b 1
)

call .venv\Scripts\activate
echo ✅ Virtual environment activated.

if not exist .env (
    echo ⚠️  .env file missing! Copying from example...
    copy .env.example .env
)

echo 🚀 Starting Key2Key API...
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

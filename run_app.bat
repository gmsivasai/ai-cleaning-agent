@echo off
echo ===============================
echo Starting AI Data Cleaning App
echo ===============================

REM Move to project root (this file’s location)
cd /d "%~dp0"

echo Current directory:
cd

REM Activate virtual environment
call venv\Scripts\activate

REM Start FastAPI backend
start "FastAPI Backend" python -m uvicorn app.main:app --reload

REM Wait a bit
timeout /t 3 >nul

REM Start Streamlit frontend (EXPLICIT FILE PATH)
start "Streamlit Frontend" streamlit run frontend_streamlit.py

echo.
echo App started successfully.
exit

@echo off
echo ===============================
echo Stopping AI Data Cleaning App
echo ===============================

REM Move to project directory
cd /d "%~dp0"

REM Stop backend
taskkill /F /IM uvicorn.exe >nul 2>&1

REM Stop frontend
taskkill /F /IM streamlit.exe >nul 2>&1

echo.
echo App stopped successfully.

exit

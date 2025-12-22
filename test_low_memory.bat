@echo off
REM Test LOW_MEMORY mode locally before deploying to Render

echo ================================================================================
echo TESTING LOW MEMORY MODE LOCALLY
echo ================================================================================
echo.

REM Set environment variable for low memory mode
set LOW_MEMORY=true

echo ✅ LOW_MEMORY environment variable set to: %LOW_MEMORY%
echo.
echo Starting backend in LOW MEMORY mode...
echo You should see messages about skipping semantic embeddings.
echo.
echo ================================================================================
echo.

REM Start the backend
cd /d "%~dp0"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause

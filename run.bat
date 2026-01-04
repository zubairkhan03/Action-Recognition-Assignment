@echo off
echo ========================================
echo Video Action Recognition App
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo Starting Flask application...
echo.
echo The app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause

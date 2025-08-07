@echo off
REM Company Knowledge Base Assistant - Run Script (Windows)

echo Company Knowledge Base Assistant
echo ================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if requirements are installed
if not exist "venv\installed" (
    echo Installing requirements...
    pip install -r requirements.txt
    type nul > venv\installed
)

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create a .env file with your OpenAI API key:
    echo OPENAI_API_KEY=your_openai_api_key_here
    exit /b 1
)

REM Check if API key is set
findstr /C:"your_openai_api_key_here" .env >nul
if %errorlevel% == 0 (
    echo WARNING: Please update .env with your actual OpenAI API key
    echo Current content:
    type .env
    echo.
    set /p REPLY="Continue anyway? (y/N): "
    if /i not "%REPLY%"=="y" (
        exit /b 1
    )
)

REM Run the application
echo Starting the application...
echo API will be available at http://localhost:8000
echo Press Ctrl+C to stop
python app.py
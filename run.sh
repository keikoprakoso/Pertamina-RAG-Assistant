#!/bin/bash

# Company Knowledge Base Assistant - Run Script

echo "Company Knowledge Base Assistant"
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch venv/installed
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create a .env file with your OpenAI API key:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    exit 1
fi

# Check if API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "WARNING: Please update .env with your actual OpenAI API key"
    echo "Current content:"
    cat .env
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the application
echo "Starting the application..."
echo "API will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"
python3 app.py
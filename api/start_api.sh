#!/bin/bash
# Start API Server

echo "🚀 Starting Face Recognition API Server..."
echo "📍 Working directory: $(pwd)"

# Check if in API directory
if [[ ! -f "app.py" ]]; then
    echo "❌ Error: app.py not found. Please run from the api/ directory"
    exit 1
fi

# Activate virtual environment
if [[ -f "../.venv/bin/activate" ]]; then
    echo "🔧 Activating virtual environment..."
    source ../.venv/bin/activate
else
    echo "❌ Error: Virtual environment not found at ../.venv/"
    echo "   Please create it: cd .. && python -m venv .venv"
    exit 1
fi

# Start the server
echo "🌐 Starting Flask server on http://127.0.0.1:5000"
python app.py

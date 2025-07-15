#!/bin/bash

# Start the MCP Server for UI Automation

echo "🚀 Starting MCP Server..."
echo "📍 Make sure you have activated the virtual environment first:"
echo "   source venv/bin/activate"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate
fi

echo "🔧 Starting server on http://localhost:5000"
echo "📝 Server logs will appear below. Press Ctrl+C to stop."
echo "---"

python mcpserver.py
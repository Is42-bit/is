#!/bin/bash

# Start the Streamlit App for UI Automation

echo "🎯 Starting Streamlit App..."
echo "📍 Make sure the MCP server is running first!"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate
fi

echo "🌐 Starting Streamlit on http://localhost:8501"
echo "📱 Your browser should open automatically"
echo "---"

streamlit run streamlit_app.py
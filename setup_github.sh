#!/bin/bash

# GitHub Setup Script for Natural Language UI Automation Project
echo "🚀 Setting up project for GitHub upload..."

# Create project directory structure
echo "📁 Creating project structure..."
mkdir -p proj
cd proj

echo "📝 Project structure created!"
echo "Now copy your files into the 'proj' directory:"
echo ""
echo "Required files to copy:"
echo "- streamlit_app.py"
echo "- mcpserver_final.py (rename to mcpserver.py)"
echo "- requirements_download.txt (rename to requirements.txt)"
echo "- start_server_download.sh (rename to start_server.sh)"
echo "- start_app_download.sh (rename to start_app.sh)" 
echo "- README_download.md (rename to README.md)"
echo ""
echo "After copying files, run the GitHub commands below:"
echo ""
echo "🔧 GitHub Commands:"
echo "cd proj"
echo "git init"
echo "git add ."
echo "git commit -m 'Initial commit: Natural Language UI Automation System'"
echo "git branch -M main"
echo "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "git push -u origin main"
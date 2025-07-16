#!/usr/bin/env python3
"""
Start script for the Sauce Demo UI Automation System
This script will start both the MCP server and Streamlit app
"""

import subprocess
import sys
import time
import os
import webbrowser
from threading import Thread

# Virtual environment paths
VENV_PYTHON = "venv/bin/python"
VENV_STREAMLIT = "venv/bin/streamlit"

def check_venv():
    """Check if virtual environment exists and is set up"""
    if not os.path.exists(VENV_PYTHON):
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv")
        return False
    
    if not os.path.exists(VENV_STREAMLIT):
        print("❌ Streamlit not found in virtual environment!")
        print("Please run: source venv/bin/activate && pip install -r requirements.txt")
        return False
    
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        result = subprocess.run([VENV_PYTHON, "-c", "import streamlit, flask, playwright, requests"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All dependencies are installed!")
            return True
        else:
            print("❌ Some dependencies are missing!")
            print("Please run: source venv/bin/activate && pip install -r requirements.txt")
            return False
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False

def install_playwright():
    """Install Playwright browsers"""
    print("🎭 Installing Playwright browsers...")
    try:
        result = subprocess.run([VENV_PYTHON, "-m", "playwright", "install", "chromium"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Playwright browsers installed successfully!")
        else:
            print(f"❌ Failed to install Playwright browsers: {result.stderr}")
    except Exception as e:
        print(f"❌ Error installing Playwright: {e}")

def start_mcp_server():
    """Start the MCP server"""
    print("🚀 Starting MCP Server...")
    try:
        subprocess.run([VENV_PYTHON, "mcpse.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 MCP Server stopped")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")

def start_streamlit():
    """Start the Streamlit app"""
    print("🌟 Starting Streamlit App...")
    try:
        subprocess.run([VENV_STREAMLIT, "run", "streamlit_app.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Streamlit App stopped")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

def main():
    print("🤖 Sauce Demo UI Automation System")
    print("=" * 40)
    
    # Check virtual environment
    if not check_venv():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install Playwright browsers
    install_playwright()
    
    print("\n🎯 Starting the system...")
    print("- MCP Server will start first")
    print("- Streamlit app will start after")
    print("- Press Ctrl+C to stop both services")
    
    # Start MCP server in a separate thread
    mcp_thread = Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()
    
    # Wait a bit for MCP server to start
    time.sleep(3)
    
    # Open browser automatically
    print("\n🌐 Opening browser...")
    webbrowser.open("http://localhost:8501")
    
    # Start Streamlit (this will block)
    start_streamlit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 System stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        print("👋 Goodbye!")
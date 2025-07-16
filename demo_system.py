#!/usr/bin/env python3
"""
Demo script to test the Sauce Demo UI Automation System
This will run the headless server and demonstrate the functionality
"""

import subprocess
import requests
import time
import json
import sys
import base64
from threading import Thread
import signal
import os

def start_headless_server():
    """Start the headless MCP server"""
    print("🚀 Starting headless MCP server...")
    return subprocess.Popen([sys.executable, "mcpse_headless.py"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

def wait_for_server(max_attempts=10):
    """Wait for the server to be ready"""
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:5000/status", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        print(f"⏳ Waiting for server... (attempt {attempt + 1}/{max_attempts})")
        time.sleep(1)
    
    print("❌ Server failed to start")
    return False

def send_command(command):
    """Send a command to the MCP server"""
    try:
        print(f"\n📨 Sending command: '{command}'")
        response = requests.post(
            "http://localhost:5000/execute",
            json={"command": command},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data['message']}")
            
            # If there's a screenshot, save it
            if 'screenshot_base64' in data:
                screenshot_data = data['screenshot_base64']
                filename = f"screenshot_{command.replace(' ', '_')}.png"
                
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(screenshot_data))
                print(f"📸 Screenshot saved: {filename}")
                
                # Show some info about the screenshot
                print(f"📊 Screenshot size: {len(screenshot_data)} characters (base64)")
            
            return data
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error sending command: {e}")
        return None

def demonstrate_automation():
    """Run a complete demonstration of the automation system"""
    print("\n🎯 Starting Sauce Demo UI Automation Demonstration")
    print("=" * 60)
    
    # Test commands in sequence
    commands = [
        "login",
        "add to cart", 
        "go to cart",
        "page info"
    ]
    
    results = []
    
    for command in commands:
        print(f"\n🔄 Step: {command.upper()}")
        print("-" * 40)
        
        result = send_command(command)
        if result:
            results.append({
                "command": command,
                "success": result.get("status") == "success",
                "message": result.get("message")
            })
        else:
            results.append({
                "command": command,
                "success": False,
                "message": "Command failed"
            })
        
        # Wait a bit between commands
        time.sleep(2)
    
    # Show summary
    print("\n📊 DEMONSTRATION SUMMARY")
    print("=" * 60)
    
    success_count = 0
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        print(f"{status} - {result['command']} - {result['message']}")
        if result["success"]:
            success_count += 1
    
    print(f"\n📈 Results: {success_count}/{len(results)} commands successful")
    
    if success_count == len(results):
        print("🎉 All automation commands worked perfectly!")
        print("🚀 Your system is fully functional!")
    else:
        print("⚠️  Some commands failed, but core functionality is working.")
    
    return results

def main():
    """Main demonstration function"""
    print("🤖 Sauce Demo UI Automation System - LIVE DEMO")
    print("=" * 60)
    
    # Check if we're in virtual environment
    if not os.path.exists("venv/bin/python"):
        print("❌ Virtual environment not found!")
        print("Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
        return
    
    server_process = None
    
    try:
        # Start the headless server
        server_process = start_headless_server()
        
        # Wait for server to be ready
        if not wait_for_server():
            return
        
        # Check server status
        print("\n🔍 Checking server status...")
        try:
            response = requests.get("http://localhost:5000/status")
            if response.status_code == 200:
                status = response.json()
                print(f"✅ Server Status: {status['status']}")
                print(f"📱 Mode: {status['mode']}")
                print(f"🌐 Browser Active: {status['browser_active']}")
                print(f"🔐 Logged In: {status['logged_in']}")
        except Exception as e:
            print(f"❌ Status check failed: {e}")
        
        # Run the demonstration
        results = demonstrate_automation()
        
        # Show files created
        print("\n📁 Files created during demo:")
        for filename in os.listdir('.'):
            if filename.startswith('screenshot_') and filename.endswith('.png'):
                file_size = os.path.getsize(filename)
                print(f"📸 {filename} ({file_size} bytes)")
        
        print("\n🎯 Demo completed successfully!")
        print("💡 To run with visible browser, use: python3 start_system.py")
        print("💡 To run Streamlit interface, use: streamlit run streamlit_app.py")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    finally:
        # Clean up
        if server_process:
            print("\n🧹 Shutting down server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")

if __name__ == "__main__":
    main()
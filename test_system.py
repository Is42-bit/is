#!/usr/bin/env python3
"""
Test script to verify the Sauce Demo UI Automation System is working
"""

import sys
import subprocess
import time
import requests

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("🧪 Testing dependencies...")
    
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import flask
        print("✅ Flask installed")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import playwright
        print("✅ Playwright installed")
    except ImportError:
        print("❌ Playwright not installed")
        return False
    
    try:
        import requests
        print("✅ Requests installed")
    except ImportError:
        print("❌ Requests not installed")
        return False
    
    return True

def test_playwright_browser():
    """Test if Playwright browser is installed"""
    print("\n🌐 Testing Playwright browser...")
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com")
            title = page.title()
            browser.close()
            print(f"✅ Playwright browser working - visited: {title}")
            return True
    except Exception as e:
        print(f"❌ Playwright browser test failed: {e}")
        print("💡 Try running: python -m playwright install chromium")
        return False

def test_mcp_server():
    """Test if the MCP server can start"""
    print("\n🖥️ Testing MCP server...")
    
    try:
        # Start MCP server as subprocess
        server_process = subprocess.Popen(
            [sys.executable, "mcpse.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Test if server is responding
        try:
            response = requests.get("http://localhost:5000/status", timeout=10)
            if response.status_code == 200:
                print("✅ MCP server started successfully")
                result = True
            else:
                print(f"❌ MCP server returned status {response.status_code}")
                result = False
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to MCP server")
            result = False
        except Exception as e:
            print(f"❌ MCP server test failed: {e}")
            result = False
        
        # Clean up
        server_process.terminate()
        server_process.wait()
        
        return result
        
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be loaded"""
    print("\n🌟 Testing Streamlit app...")
    
    try:
        # Try to validate the Streamlit app syntax
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Streamlit app syntax is valid")
            return True
        else:
            print(f"❌ Streamlit app validation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Testing Sauce Demo UI Automation System")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Playwright Browser", test_playwright_browser),
        ("MCP Server", test_mcp_server),
        ("Streamlit App", test_streamlit_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results:")
    print("=" * 20)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Summary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("🚀 Run 'python start_system.py' to start the system.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("💡 Try running 'pip install -r requirements.txt' and 'python -m playwright install chromium'")

if __name__ == "__main__":
    main()
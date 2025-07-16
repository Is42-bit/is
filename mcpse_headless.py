#!/usr/bin/env python3
"""
Headless version of MCP server for testing in environments without display
"""

import asyncio
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright
import base64
import os
from threading import Lock
import json

app = Flask(__name__)

# Global state with proper session management
class BrowserSession:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.is_logged_in = False
        self.lock = Lock()
    
    async def ensure_browser(self):
        """Ensure browser is running and page is available"""
        if not self.playwright:
            print("🚀 Starting Playwright...")
            self.playwright = await async_playwright().start()
        
        if not self.browser:
            print("🌐 Launching browser (headless mode)...")
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # HEADLESS for testing
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
        
        if not self.context:
            print("📄 Creating browser context...")
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
        
        if not self.page or self.page.is_closed():
            print("🔄 Creating new page...")
            self.page = await self.context.new_page()
        
        return self.page

    async def take_screenshot(self):
        """Take a screenshot and return base64 encoded image"""
        if self.page:
            screenshot_bytes = await self.page.screenshot(full_page=True)
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        return None

    async def cleanup(self):
        """Clean up browser resources"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

# Global session instance
session = BrowserSession()

# Constants
SAUCE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

async def login():
    """Login to saucedemo.com"""
    page = await session.ensure_browser()
    
    try:
        print("🔐 Navigating to login page...")
        await page.goto(SAUCE_URL, wait_until='networkidle')
        
        print("🔐 Filling login credentials...")
        await page.fill('input[data-test="username"]', USERNAME)
        await page.fill('input[data-test="password"]', PASSWORD)
        
        print("🔐 Clicking login button...")
        await page.click('input[data-test="login-button"]')
        
        print("🔐 Waiting for inventory page...")
        await page.wait_for_selector('.inventory_list', timeout=10000)
        
        session.is_logged_in = True
        print("✅ Login successful!")
        
        # Take screenshot after login
        screenshot = await session.take_screenshot()
        
        return {
            "message": "🔐 Successfully logged in to Sauce Demo!",
            "screenshot_base64": screenshot,
            "status": "success"
        }
    
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return {"message": f"❌ Login failed: {str(e)}", "status": "error"}

async def add_to_cart():
    """Add item to cart"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!", "status": "error"}
    
    page = await session.ensure_browser()
    
    try:
        print("🛒 Looking for product to add to cart...")
        
        # Make sure we're on the inventory page
        current_url = page.url
        if "inventory.html" not in current_url:
            print("🔄 Navigating to inventory page...")
            await page.goto(f"{SAUCE_URL}inventory.html", wait_until='networkidle')
        
        # Wait for inventory items to load
        await page.wait_for_selector('.inventory_item', timeout=10000)
        
        # Find and click the "Add to cart" button for Sauce Labs Backpack
        print("🎒 Adding Sauce Labs Backpack to cart...")
        await page.click('button[data-test="add-to-cart-sauce-labs-backpack"]')
        
        # Wait a moment for the action to complete
        await page.wait_for_timeout(1000)
        
        # Verify the button changed to "Remove"
        remove_button = await page.query_selector('button[data-test="remove-sauce-labs-backpack"]')
        if remove_button:
            print("✅ Item successfully added to cart!")
            
            # Take screenshot
            screenshot = await session.take_screenshot()
            
            return {
                "message": "🛒 Successfully added Sauce Labs Backpack to cart!",
                "screenshot_base64": screenshot,
                "status": "success"
            }
        else:
            return {"message": "❌ Failed to add item to cart - button didn't change", "status": "error"}
    
    except Exception as e:
        print(f"❌ Add to cart failed: {str(e)}")
        return {"message": f"❌ Failed to add to cart: {str(e)}", "status": "error"}

async def go_to_cart():
    """Navigate to shopping cart"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!", "status": "error"}
    
    page = await session.ensure_browser()
    
    try:
        print("🛒 Going to shopping cart...")
        await page.click('.shopping_cart_link')
        await page.wait_for_selector('.cart_list', timeout=10000)
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": "🛒 Successfully navigated to shopping cart!",
            "screenshot_base64": screenshot,
            "status": "success"
        }
    
    except Exception as e:
        print(f"❌ Go to cart failed: {str(e)}")
        return {"message": f"❌ Failed to go to cart: {str(e)}", "status": "error"}

async def get_page_info():
    """Get current page information"""
    if not session.page:
        return {"message": "❌ No page loaded", "status": "error"}
    
    try:
        page = await session.ensure_browser()
        
        # Get page info
        url = page.url
        title = await page.title()
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": f"📄 Current page: {title} ({url})",
            "screenshot_base64": screenshot,
            "status": "success"
        }
    
    except Exception as e:
        print(f"❌ Get page info failed: {str(e)}")
        return {"message": f"❌ Failed to get page info: {str(e)}", "status": "error"}

def run_async_command(command):
    """Run async command in Flask context"""
    def run_in_thread():
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(execute_command(command))
            return result
        finally:
            loop.close()
    
    return run_in_thread()

async def execute_command(command):
    """Execute the appropriate command based on user input"""
    command = command.lower().strip()
    
    if "login" in command:
        return await login()
    elif "add to cart" in command:
        return await add_to_cart()
    elif "go to cart" in command or "cart" in command:
        return await go_to_cart()
    elif "page info" in command or "info" in command:
        return await get_page_info()
    else:
        return {
            "message": "🤖 Available commands: login, add to cart, go to cart, page info",
            "status": "help"
        }

@app.route("/execute", methods=["POST"])
def execute():
    """Main execution endpoint"""
    data = request.get_json()
    command = data.get("command", "")
    
    print(f"📨 Received command: {command}")
    
    try:
        # Use thread lock to ensure thread safety
        with session.lock:
            result = run_async_command(command)
        
        print(f"✅ Command executed successfully")
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Command execution failed: {str(e)}")
        return jsonify({"message": f"❌ Error: {str(e)}", "status": "error"})

@app.route("/status", methods=["GET"])
def status():
    """Get system status"""
    return jsonify({
        "status": "running",
        "logged_in": session.is_logged_in,
        "browser_active": session.browser is not None,
        "mode": "headless"
    })

if __name__ == "__main__":
    print("🚀 Starting MCP Server (Headless Mode)...")
    print("📡 Server running on http://localhost:5000")
    print("🔧 Mode: Headless (for testing)")
    
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)
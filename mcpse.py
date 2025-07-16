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
            print("🌐 Launching browser...")
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Keep headless=False as requested
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
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return {"message": f"❌ Login failed: {str(e)}"}

async def add_to_cart():
    """Add item to cart"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!"}
    
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
                "screenshot_base64": screenshot
            }
        else:
            return {"message": "❌ Failed to add item to cart - button didn't change"}
    
    except Exception as e:
        print(f"❌ Add to cart failed: {str(e)}")
        return {"message": f"❌ Failed to add to cart: {str(e)}"}

async def go_to_cart():
    """Navigate to shopping cart"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!"}
    
    page = await session.ensure_browser()
    
    try:
        print("🛒 Going to shopping cart...")
        await page.click('.shopping_cart_link')
        await page.wait_for_selector('.cart_list', timeout=10000)
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": "🛒 Successfully navigated to shopping cart!",
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Go to cart failed: {str(e)}")
        return {"message": f"❌ Failed to go to cart: {str(e)}"}

async def remove_from_cart():
    """Remove item from cart"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!"}
    
    page = await session.ensure_browser()
    
    try:
        print("🗑️ Removing item from cart...")
        
        # Make sure we're on the cart page
        if "cart.html" not in page.url:
            await page.click('.shopping_cart_link')
            await page.wait_for_selector('.cart_list', timeout=10000)
        
        # Find and click remove button
        await page.click('button[data-test="remove-sauce-labs-backpack"]')
        await page.wait_for_timeout(1000)
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": "🗑️ Successfully removed item from cart!",
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Remove from cart failed: {str(e)}")
        return {"message": f"❌ Failed to remove from cart: {str(e)}"}

async def checkout():
    """Start checkout process"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!"}
    
    page = await session.ensure_browser()
    
    try:
        print("💳 Starting checkout process...")
        
        # Make sure we're on the cart page
        if "cart.html" not in page.url:
            await page.click('.shopping_cart_link')
            await page.wait_for_selector('.cart_list', timeout=10000)
        
        # Click checkout button
        await page.click('button[data-test="checkout"]')
        await page.wait_for_selector('.checkout_info', timeout=10000)
        
        # Fill out checkout form with dummy data
        print("📝 Filling checkout form...")
        await page.fill('input[data-test="firstName"]', 'John')
        await page.fill('input[data-test="lastName"]', 'Doe')
        await page.fill('input[data-test="postalCode"]', '12345')
        
        # Click continue
        await page.click('input[data-test="continue"]')
        await page.wait_for_selector('.checkout_summary_container', timeout=10000)
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": "💳 Successfully filled checkout form! Ready to finish order.",
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Checkout failed: {str(e)}")
        return {"message": f"❌ Checkout failed: {str(e)}"}

async def finish_order():
    """Complete the order"""
    if not session.is_logged_in:
        return {"message": "❌ Please login first!"}
    
    page = await session.ensure_browser()
    
    try:
        print("✅ Finishing order...")
        
        # Click finish button
        await page.click('button[data-test="finish"]')
        await page.wait_for_selector('.complete-header', timeout=10000)
        
        # Take screenshot
        screenshot = await session.take_screenshot()
        
        return {
            "message": "🎉 Order completed successfully! Thank you for your purchase.",
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Finish order failed: {str(e)}")
        return {"message": f"❌ Failed to finish order: {str(e)}"}

async def take_screenshot_command():
    """Take a screenshot of current page"""
    page = await session.ensure_browser()
    
    try:
        screenshot = await session.take_screenshot()
        return {
            "message": "📸 Screenshot taken!",
            "screenshot_base64": screenshot
        }
    
    except Exception as e:
        print(f"❌ Screenshot failed: {str(e)}")
        return {"message": f"❌ Failed to take screenshot: {str(e)}"}

async def get_help():
    """Show available commands"""
    help_text = """
🤖 **Available Commands:**

• `login` - Login to Sauce Demo
• `add to cart` - Add Sauce Labs Backpack to cart
• `go to cart` - Navigate to shopping cart
• `remove from cart` - Remove item from cart
• `checkout` - Fill checkout form
• `finish order` - Complete the purchase
• `screenshot` - Take a screenshot
• `help` - Show this help message

**Example Usage:**
- "login"
- "add to cart" 
- "go to cart and take screenshot"
- "checkout with dummy data"
"""
    return {"message": help_text}

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
    elif "remove" in command:
        return await remove_from_cart()
    elif "checkout" in command:
        return await checkout()
    elif "finish" in command or "complete" in command:
        return await finish_order()
    elif "screenshot" in command:
        return await take_screenshot_command()
    elif "help" in command:
        return await get_help()
    else:
        return {
            "message": "🤖 Command not recognized. Try 'help' to see available commands."
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
        return jsonify({"message": f"❌ Error: {str(e)}"})

@app.route("/status", methods=["GET"])
def status():
    """Get system status"""
    return jsonify({
        "status": "running",
        "logged_in": session.is_logged_in,
        "browser_active": session.browser is not None
    })

if __name__ == "__main__":
    import atexit
    
    # Register cleanup function
    def cleanup():
        print("🧹 Cleaning up browser resources...")
        asyncio.run(session.cleanup())
    
    atexit.register(cleanup)
    
    # Set Flask environment
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    
    print("🚀 Starting MCP Server...")
    print("🌐 Browser will launch in non-headless mode")
    print("📡 Server running on http://localhost:5000")
    
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
import asyncio
import base64
from quart import Quart, request, jsonify
from playwright.async_api import async_playwright
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Quart(__name__)

# Global state for browser session
class BrowserSession:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.lock = asyncio.Lock()
        self.is_logged_in = False

browser_session = BrowserSession()

SAUCE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

async def ensure_browser():
    """Ensure browser is running and page is available"""
    async with browser_session.lock:
        if not browser_session.playwright:
            logger.info("Starting Playwright...")
            browser_session.playwright = await async_playwright().start()
        
        if not browser_session.browser:
            logger.info("Launching browser...")
            browser_session.browser = await browser_session.playwright.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )
            browser_session.context = await browser_session.browser.new_context()
            
        if not browser_session.page or browser_session.page.is_closed():
            logger.info("Creating new page...")
            browser_session.page = await browser_session.context.new_page()
            browser_session.is_logged_in = False
        
        logger.info(f"Page is ready. Current URL: {browser_session.page.url}")

async def login():
    """Login to saucedemo.com"""
    try:
        await ensure_browser()
        logger.info("🔐 Logging in...")
        
        # Navigate to the site
        await browser_session.page.goto(SAUCE_URL, wait_until='networkidle')
        
        # Fill login form
        await browser_session.page.fill('input[data-test="username"]', USERNAME)
        await browser_session.page.fill('input[data-test="password"]', PASSWORD)
        
        # Click login button
        await browser_session.page.click('input[data-test="login-button"]')
        
        # Wait for inventory page to load
        await browser_session.page.wait_for_selector('.inventory_list', timeout=10000)
        
        browser_session.is_logged_in = True
        logger.info("✅ Login successful")
        
        return {
            "message": "🔐 Logged in successfully to SauceDemo!",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"❌ Login failed: {str(e)}")
        return {
            "message": f"❌ Login failed: {str(e)}",
            "success": False
        }

async def add_to_cart():
    """Add item to cart"""
    try:
        await ensure_browser()
        
        # Check if logged in
        if not browser_session.is_logged_in:
            login_result = await login()
            if not login_result["success"]:
                return login_result
        
        logger.info("🛒 Attempting to add item to cart...")
        logger.info(f"Current URL: {browser_session.page.url}")
        
        # Make sure we're on the inventory page
        if 'inventory.html' not in browser_session.page.url:
            await browser_session.page.goto(f"{SAUCE_URL}inventory.html", wait_until='networkidle')
        
        # Wait for inventory to load
        await browser_session.page.wait_for_selector('.inventory_list', timeout=5000)
        
        # Try to add backpack to cart directly from inventory page
        backpack_selector = 'button[data-test="add-to-cart-sauce-labs-backpack"]'
        
        # Check if button exists
        button_exists = await browser_session.page.locator(backpack_selector).count()
        if button_exists == 0:
            logger.error("❌ Add to cart button not found")
            return {
                "message": "❌ Could not find 'Add to cart' button for Sauce Labs Backpack",
                "success": False
            }
        
        # Click the add to cart button
        await browser_session.page.click(backpack_selector)
        
        # Wait a moment for the action to complete
        await browser_session.page.wait_for_timeout(1000)
        
        # Check if item was added (button should change to "Remove")
        remove_button = await browser_session.page.locator('button[data-test="remove-sauce-labs-backpack"]').count()
        
        if remove_button > 0:
            logger.info("✅ Item successfully added to cart")
            return {
                "message": "🛒 Successfully added 'Sauce Labs Backpack' to cart!",
                "success": True
            }
        else:
            return {
                "message": "⚠️ Add to cart clicked, but couldn't verify if item was added",
                "success": False
            }
            
    except Exception as e:
        logger.error(f"❌ Add to cart failed: {str(e)}")
        return {
            "message": f"❌ Failed to add to cart: {str(e)}",
            "success": False
        }

async def remove_from_cart():
    """Remove item from cart"""
    try:
        await ensure_browser()
        
        logger.info("🗑️ Removing item from cart...")
        
        # Try to remove backpack from cart
        remove_selector = 'button[data-test="remove-sauce-labs-backpack"]'
        
        # Check if remove button exists
        button_exists = await browser_session.page.locator(remove_selector).count()
        if button_exists == 0:
            return {
                "message": "❌ Could not find 'Remove' button for Sauce Labs Backpack",
                "success": False
            }
        
        # Click the remove button
        await browser_session.page.click(remove_selector)
        
        # Wait a moment for the action to complete
        await browser_session.page.wait_for_timeout(1000)
        
        # Check if item was removed (button should change back to "Add to cart")
        add_button = await browser_session.page.locator('button[data-test="add-to-cart-sauce-labs-backpack"]').count()
        
        if add_button > 0:
            logger.info("✅ Item successfully removed from cart")
            return {
                "message": "🗑️ Successfully removed 'Sauce Labs Backpack' from cart!",
                "success": True
            }
        else:
            return {
                "message": "⚠️ Remove clicked, but couldn't verify if item was removed",
                "success": False
            }
            
    except Exception as e:
        logger.error(f"❌ Remove from cart failed: {str(e)}")
        return {
            "message": f"❌ Failed to remove from cart: {str(e)}",
            "success": False
        }

async def go_to_cart():
    """Navigate to shopping cart"""
    try:
        await ensure_browser()
        
        logger.info("🛒 Going to cart...")
        
        # Click the cart icon
        await browser_session.page.click('.shopping_cart_link')
        
        # Wait for cart page to load
        await browser_session.page.wait_for_selector('.cart_list', timeout=5000)
        
        return {
            "message": "🛒 Navigated to shopping cart",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to go to cart: {str(e)}")
        return {
            "message": f"❌ Failed to go to cart: {str(e)}",
            "success": False
        }

async def checkout():
    """Navigate to checkout"""
    try:
        await ensure_browser()
        
        logger.info("💳 Starting checkout...")
        
        # Click checkout button
        await browser_session.page.click('button[data-test="checkout"]')
        
        # Wait for checkout page to load
        await browser_session.page.wait_for_selector('.checkout_info', timeout=5000)
        
        return {
            "message": "💳 Navigated to checkout page",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to checkout: {str(e)}")
        return {
            "message": f"❌ Failed to checkout: {str(e)}",
            "success": False
        }

async def take_screenshot():
    """Take a screenshot of current page"""
    try:
        await ensure_browser()
        
        logger.info("📸 Taking screenshot...")
        
        # Take screenshot
        screenshot_bytes = await browser_session.page.screenshot(full_page=True)
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
        
        return {
            "message": "📸 Screenshot taken successfully",
            "success": True,
            "screenshot_base64": screenshot_base64
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to take screenshot: {str(e)}")
        return {
            "message": f"❌ Failed to take screenshot: {str(e)}",
            "success": False
        }

@app.route("/execute", methods=["POST"])
async def execute():
    """Main endpoint to execute commands"""
    data = await request.get_json()
    command = data.get("command", "").lower().strip()
    logger.info(f"Received command: '{command}'")
    
    try:
        if "login" in command:
            result = await login()
        elif "add to cart" in command or "add item" in command:
            result = await add_to_cart()
        elif "remove" in command and "cart" in command:
            result = await remove_from_cart()
        elif "go to cart" in command or ("cart" in command and "go" in command):
            result = await go_to_cart()
        elif "checkout" in command:
            result = await checkout()
        elif "screenshot" in command or "take screenshot" in command:
            result = await take_screenshot()
        else:
            result = {
                "message": "🤖 Command not recognized. Try: 'login', 'add to cart', 'remove from cart', 'go to cart', 'checkout', or 'take screenshot'",
                "success": False
            }
            
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        result = {
            "message": f"❌ Unexpected error: {str(e)}",
            "success": False
        }
    
    return jsonify(result)

@app.route("/status", methods=["GET"])
async def status():
    """Get current browser status"""
    return jsonify({
        "browser_running": browser_session.browser is not None,
        "page_ready": browser_session.page is not None and not browser_session.page.is_closed(),
        "logged_in": browser_session.is_logged_in,
        "current_url": browser_session.page.url if browser_session.page and not browser_session.page.is_closed() else None
    })

async def cleanup():
    """Cleanup browser resources"""
    if browser_session.browser:
        await browser_session.browser.close()
    if browser_session.playwright:
        await browser_session.playwright.stop()

if __name__ == "__main__":
    import atexit
    atexit.register(lambda: asyncio.run(cleanup()))
    
    logger.info("🚀 Starting MCP Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
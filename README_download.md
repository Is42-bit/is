# 🛍️ Natural Language UI Automation for SauceDemo

A powerful natural language-driven UI automation system that allows users to control a browser using simple text commands via a chatbot interface.

## 🎯 Features

- **Natural Language Commands**: Control browser automation with simple text
- **Real-time Screenshots**: Get visual feedback of current page state
- **Session Management**: Persistent browser sessions across commands
- **Multi-command Support**: Login, shopping, cart management, checkout
- **Beautiful UI**: Modern Streamlit chatbot interface

## 🧱 Architecture

| Component | Role | Port |
|-----------|------|------|
| **Streamlit App** | Frontend chatbot UI | 8501 |
| **MCP Server (Quart)** | Backend automation controller | 5000 |
| **Playwright** | Browser automation engine | - |
| **Target Website** | https://www.saucedemo.com | - |

## 🚀 Quick Setup

### 1. **Download Files**
Download all these files to your project directory:
- `streamlit_app.py`
- `mcpserver_final.py` (rename to `mcpserver.py`)
- `requirements_download.txt` (rename to `requirements.txt`)
- `start_server_download.sh` (rename to `start_server.sh`)
- `start_app_download.sh` (rename to `start_app.sh`)

### 2. **Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### 3. **Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 4. **Run the System**

**Option A: Use Scripts**
```bash
# Terminal 1 - Start MCP Server
chmod +x start_server.sh
./start_server.sh

# Terminal 2 - Start Streamlit App
chmod +x start_app.sh
./start_app.sh
```

**Option B: Manual Start**
```bash
# Terminal 1 - Start MCP Server
python mcpserver.py

# Terminal 2 - Start Streamlit App
streamlit run streamlit_app.py
```

### 5. **Access the Application**
Open your browser to: **http://localhost:8501**

## 🎮 Available Commands

| Command | Action | Example |
|---------|--------|---------|
| `login` | Login to SauceDemo | "login" |
| `add to cart` | Add backpack to cart | "add to cart" |
| `remove from cart` | Remove item from cart | "remove from cart" |
| `go to cart` | Navigate to shopping cart | "go to cart" |
| `checkout` | Start checkout process | "checkout" |
| `take screenshot` | Capture current page | "take screenshot" |

## 📝 Example Usage

1. **Start with login:**
   ```
   You: login
   Bot: 🔐 Logged in successfully to SauceDemo!
   ```

2. **Add item to cart:**
   ```
   You: add to cart
   Bot: 🛒 Successfully added 'Sauce Labs Backpack' to cart!
   ```

3. **Take a screenshot:**
   ```
   You: take screenshot
   Bot: 📸 Screenshot taken successfully
   [Screenshot appears in chat]
   ```

## 🔧 Troubleshooting

### Common Issues:

**Port Already in Use:**
```bash
# Kill processes on port 5000 or 8501
lsof -ti:5000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

**Playwright Browser Issues:**
```bash
# Reinstall browsers
playwright install
```

**Virtual Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Future Enhancements

### Easy Additions:
- **More Products**: Support for other SauceDemo items
- **Checkout Flow**: Complete purchase simulation  
- **Natural Language Parsing**: Better command understanding
- **Command History**: Save and replay sequences

### Advanced Features:
- **Multiple Websites**: Extend beyond SauceDemo
- **AI Integration**: Use LLMs for better command parsing
- **Visual Recognition**: Element detection with computer vision
- **Test Recording**: Save automation sequences as tests

## 📁 Project Structure

```
your_project/
├── streamlit_app.py      # Frontend chatbot interface
├── mcpserver.py         # Backend automation server
├── requirements.txt     # Python dependencies
├── start_server.sh      # Server startup script
├── start_app.sh        # App startup script
└── README.md           # This file
```

## 🛠️ Development

### Adding New Commands:

1. **Add function in mcpserver.py:**
```python
async def new_command():
    # Your automation logic
    return {"message": "Success!", "success": True}
```

2. **Update the execute route:**
```python
elif "new command" in command:
    result = await new_command()
```

### Browser Settings:
- **Headless Mode**: Change `headless=True` to `headless=False` for visual debugging
- **Slow Motion**: Add `slow_mo=1000` to see actions in slow motion
- **Different Browser**: Use `firefox` or `webkit` instead of `chromium`

## 📊 System Requirements

- **Python**: 3.8+
- **Memory**: 2GB+ RAM
- **Browser**: Chromium (auto-installed by Playwright)
- **OS**: Windows, macOS, Linux

## 🎯 Credits

Built with:
- **Streamlit**: Beautiful web app framework
- **Quart**: Async Python web framework  
- **Playwright**: Modern browser automation
- **SauceDemo**: Demo e-commerce site for testing

---

## 🎉 You're Ready!

Your Natural Language UI Automation system is now ready to use. Start with simple commands and expand from there!

**Happy Automating!** 🚀
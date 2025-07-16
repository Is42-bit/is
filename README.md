# 🤖 Sauce Demo UI Automation System

A natural language-driven UI automation system that allows users to control a browser using simple text commands via a chatbot interface.

## 🎯 Project Overview

This system uses:
- **Streamlit** - Frontend chatbot UI where users type commands
- **Flask** - Backend MCP server for command processing
- **Playwright** - Browser automation engine
- **Target Website** - https://www.saucedemo.com

## 🚀 Quick Start

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browser
```bash
python -m playwright install chromium
```

### 4. Start the System (Easy Method)
```bash
python3 start_system.py
```

**OR** start manually:

Terminal 1 (MCP Server):
```bash
source venv/bin/activate
python mcpse.py
```

Terminal 2 (Streamlit App):
```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

### 5. Open Browser
- The system will automatically open http://localhost:8501
- If not, manually navigate to this URL

## 🧪 Testing the System

Run the test script to verify everything is working:
```bash
source venv/bin/activate
python test_system.py
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `login` | Login to Sauce Demo |
| `add to cart` | Add Sauce Labs Backpack to cart |
| `go to cart` | Navigate to shopping cart |
| `remove from cart` | Remove item from cart |
| `checkout` | Fill checkout form with dummy data |
| `finish order` | Complete the purchase |
| `screenshot` | Take a screenshot of current page |
| `help` | Show available commands |

## 🎮 Usage Examples

1. **Start by logging in:**
   ```
   login
   ```

2. **Add items to cart:**
   ```
   add to cart
   ```

3. **Check your cart:**
   ```
   go to cart
   ```

4. **Complete checkout:**
   ```
   checkout
   finish order
   ```

5. **Take screenshots anytime:**
   ```
   screenshot
   ```

## 🏗️ Architecture

```
┌─────────────────┐    HTTP POST     ┌─────────────────┐
│   Streamlit     │ ──────────────► │   Flask MCP     │
│   Frontend      │                 │   Server        │
│                 │ ◄────────────── │                 │
│ • Chat UI       │   JSON Response │ • Command Parser│
│ • Screenshots   │                 │ • Session Mgmt  │
│ • Status        │                 │ • Async Handler │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │   Playwright    │
                                    │   Browser       │
                                    │                 │
                                    │ • Chromium      │
                                    │ • Automation    │
                                    │ • Screenshots   │
                                    └─────────────────┘
```

## 🔧 Features

### ✅ Working Features
- **Login automation** - Automatically logs into saucedemo.com
- **Add to cart** - Adds items to shopping cart
- **Navigation** - Cart, checkout, product pages
- **Form filling** - Automatic checkout form completion
- **Screenshots** - Visual feedback with screenshots
- **Session persistence** - Maintains login state between commands
- **Error handling** - Graceful error messages
- **Status monitoring** - Real-time server and login status

### 🎨 UI Features
- **Modern interface** - Clean, responsive design
- **Real-time status** - Server and login status indicators
- **Command examples** - Built-in help and suggestions
- **Chat history** - Timestamped conversation log
- **Loading indicators** - Visual feedback during processing
- **Screenshot display** - Inline image viewing

## 🛠️ Technical Details

### Browser Configuration
- **Headless mode**: Disabled (you can see the browser)
- **Viewport**: 1280x720
- **Browser**: Chromium
- **Session**: Persistent context maintained

### Session Management
- **Thread-safe**: Uses threading locks for concurrent requests
- **Persistent context**: Browser state maintained between commands
- **Login tracking**: Tracks authentication state
- **Error recovery**: Handles page context loss

### Key Improvements Made
- **Fixed Flask async issues** - Proper async handling with Flask
- **Session persistence** - Browser context maintained between requests
- **Thread safety** - Concurrent request handling
- **Better error handling** - Graceful error recovery
- **Virtual environment** - Isolated Python environment
- **Comprehensive testing** - Test scripts for validation

## 🐛 Troubleshooting

### Common Issues

1. **"Virtual environment not found" Error**
   - Create virtual environment: `python3 -m venv venv`
   - Activate it: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

2. **"Server Offline" Error**
   - Make sure MCP server is running: `python mcpse.py`
   - Check if port 5000 is available

3. **"Browser not found" Error**
   - Install Playwright browsers: `python -m playwright install chromium`

4. **"Add to cart" fails**
   - Make sure you're logged in first
   - Try taking a screenshot to see current page state

5. **Timeout errors**
   - Check your internet connection
   - The site might be slow - try again

### Debug Mode
To enable debug output, set debug=True in the Flask app:
```python
app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
```

### Environment Issues
If you encounter permission errors or package conflicts:
```bash
# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## 📊 System Status

Check system health:
- Click "🔄 Check Server Status" in the Streamlit sidebar
- Green indicators mean everything is working
- Red indicators show connection issues

## 🔮 Future Enhancements

- [ ] Multi-product support
- [ ] Natural language parsing (NLP)
- [ ] Order history tracking
- [ ] Multiple user sessions
- [ ] Advanced error recovery
- [ ] Performance monitoring
- [ ] Docker containerization

## 📝 Files Structure

```
├── streamlit_app.py    # Frontend Streamlit application
├── mcpse.py           # Backend Flask MCP server
├── requirements.txt   # Python dependencies
├── start_system.py    # Easy startup script
├── test_system.py     # System testing script
├── README.md         # This file
└── venv/             # Virtual environment (created by you)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes and demonstration of UI automation concepts.

## 🎉 Acknowledgments

- Built with Streamlit, Flask, and Playwright
- Uses Sauce Demo (https://www.saucedemo.com) for testing
- Inspired by natural language UI automation concepts

---

**Happy automating!** 🤖✨

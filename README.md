# 🛍️ Natural Language UI Automation for SauceDemo

A natural language-driven UI automation system that allows users to control a browser using simple text commands via a Streamlit chatbot interface.

## 🎯 Project Overview

This system enables you to automate browser interactions on [SauceDemo](https://www.saucedemo.com) using natural language commands. Simply type what you want to do, and the system will execute the browser actions for you!

### Architecture

- **Frontend**: Streamlit chatbot interface for user interaction
- **Backend**: Quart (async Flask) server for command processing
- **Automation**: Playwright for browser automation
- **Target**: SauceDemo.com e-commerce demo site

## ✨ Features

- 🔐 **Login automation** - Automatic login to SauceDemo
- 🛒 **Add to cart** - Add products to shopping cart
- 🛍️ **Cart navigation** - Navigate to shopping cart
- 📸 **Screenshots** - Take screenshots of current page
- 🔄 **Session persistence** - Maintains browser context between commands
- 📝 **Natural language** - Type commands in plain English

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Start the MCP Server
In one terminal window:
```bash
python mcpserver.py
```

### 3. Start the Streamlit App
In another terminal window:
```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

### 4. Open Your Browser
Navigate to `http://localhost:8501` to access the chatbot interface.

## 🎮 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `login` | Login to SauceDemo | "login" |
| `add to cart` | Add Sauce Labs Backpack to cart | "add to cart" |
| `go to cart` | Navigate to shopping cart | "go to cart" |
| `take screenshot` | Capture current page | "take screenshot" |

## 💬 Example Usage

1. Type "login" to log into SauceDemo
2. Type "add to cart" to add an item
3. Type "go to cart" to view your cart
4. Type "take screenshot" to capture the current page

## 🔧 System Requirements

- Python 3.13+
- Chromium browser (installed via Playwright)
- Linux/Ubuntu environment

## 📂 Project Structure

```
workspace/
├── streamlit_app.py      # Frontend chatbot interface
├── mcpserver.py          # Backend automation server
├── requirements.txt      # Python dependencies
├── venv/                 # Virtual environment
└── README.md            # This file
```

## 🐛 Troubleshooting

### Server Connection Issues
- Ensure the MCP server is running on port 5000
- Check that both terminals are using the virtual environment

### Browser Issues
- Run `playwright install` if browsers are missing
- Ensure the system has sufficient memory for browser automation

### Command Not Working
- Check the server logs for detailed error messages
- Verify you're on the correct page (login required for most actions)

## 🔮 Future Enhancements

- [ ] More e-commerce actions (checkout, remove items)
- [ ] Advanced natural language parsing
- [ ] Multiple product selection
- [ ] Order history tracking
- [ ] Support for other demo sites

## 🤝 Contributing

This is a development project. Feel free to extend the commands or improve the natural language processing!

## 📄 License

Educational/Development use only.

---

**Happy Automating! 🚀**

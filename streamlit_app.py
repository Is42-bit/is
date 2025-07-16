import streamlit as st
import requests
import base64
import time

st.set_page_config(
    page_title="Sauce Demo UI Bot", 
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .status-indicator {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-weight: bold;
    }
    .status-online {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .command-examples {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🤖 Sauce Demo UI Automation Bot</h1>', unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "server_status" not in st.session_state:
    st.session_state.server_status = "unknown"
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Sidebar with controls and info
with st.sidebar:
    st.header("🎛️ Controls")
    
    # Server status check
    if st.button("🔄 Check Server Status"):
        try:
            response = requests.get("http://localhost:5000/status", timeout=5)
            if response.status_code == 200:
                status_data = response.json()
                st.session_state.server_status = "online"
                st.session_state.is_logged_in = status_data.get("logged_in", False)
            else:
                st.session_state.server_status = "error"
        except:
            st.session_state.server_status = "offline"
    
    # Display server status
    if st.session_state.server_status == "online":
        st.markdown('<div class="status-indicator status-online">🟢 Server Online</div>', unsafe_allow_html=True)
        if st.session_state.is_logged_in:
            st.markdown('<div class="status-indicator status-online">🔐 Logged In</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-offline">🔒 Not Logged In</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-offline">🔴 Server Offline</div>', unsafe_allow_html=True)
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Command examples
    st.markdown("""
    <div class="command-examples">
        <h4>💡 Example Commands:</h4>
        <ul>
            <li><code>login</code></li>
            <li><code>add to cart</code></li>
            <li><code>go to cart</code></li>
            <li><code>checkout</code></li>
            <li><code>finish order</code></li>
            <li><code>screenshot</code></li>
            <li><code>help</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input("💬 Enter your command:", "", key="user_input", placeholder="Type 'help' to see available commands...")

with col2:
    send_button = st.button("🚀 Send", use_container_width=True)

# Process user input
if (send_button or st.session_state.get("user_input_submitted", False)) and user_input.strip():
    st.session_state.chat_history.append(("user", user_input, time.time()))
    
    # Show loading spinner
    with st.spinner("🔄 Processing your request..."):
        try:
            # Call MCP server
            mcp_response = requests.post(
                "http://localhost:5000/execute",
                json={"command": user_input},
                timeout=60
            )
            mcp_response.raise_for_status()
            mcp_data = mcp_response.json()
            
            # Store response
            timestamp = time.time()
            st.session_state.chat_history.append(("mcp", mcp_data.get("message", "[No message]"), timestamp))
            
            # Store screenshot if included
            if "screenshot_base64" in mcp_data:
                st.session_state.chat_history.append(("screenshot", mcp_data["screenshot_base64"], timestamp))
            
            # Update login status if it was a login command
            if "login" in user_input.lower() and "successfully" in mcp_data.get("message", "").lower():
                st.session_state.is_logged_in = True
                
        except requests.exceptions.Timeout:
            st.session_state.chat_history.append(("error", "⏱️ Request timed out. The server might be busy processing your request.", time.time()))
        except requests.exceptions.ConnectionError:
            st.session_state.chat_history.append(("error", "🔌 Cannot connect to MCP server. Make sure it's running on localhost:5000", time.time()))
        except Exception as e:
            st.session_state.chat_history.append(("error", f"❌ Error: {str(e)}", time.time()))
    
    # Clear input and rerun
    st.session_state.user_input = ""
    st.rerun()

# Display chat history
st.markdown("---")
st.subheader("💬 Chat History")

if not st.session_state.chat_history:
    st.info("👋 Welcome! Start by typing a command or 'help' to see available options.")
else:
    # Display messages in reverse order (newest first)
    for i, (sender, msg, timestamp) in enumerate(reversed(st.session_state.chat_history)):
        message_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
        
        if sender == "user":
            st.markdown(f"**🧑 You** ({message_time}): {msg}")
        elif sender == "mcp":
            with st.expander(f"🤖 Bot Response ({message_time})", expanded=True):
                st.markdown(msg)
        elif sender == "error":
            st.error(f"❌ Error ({message_time}): {msg}")
        elif sender == "screenshot":
            st.image(
                base64.b64decode(msg), 
                caption=f"📸 Screenshot taken at {message_time}", 
                use_column_width=True
            )
        
        # Add separator between messages
        if i < len(st.session_state.chat_history) - 1:
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🤖 Sauce Demo UI Automation Bot | Built with Streamlit + Flask + Playwright</p>
    <p>Make sure your MCP server is running on <code>localhost:5000</code></p>
</div>
""", unsafe_allow_html=True)

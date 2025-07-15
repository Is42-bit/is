import streamlit as st
import requests
import base64

st.set_page_config(page_title="SauceDemo UI Bot", page_icon="🛒")
st.title("🛍️ Natural Language UI Automation Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", "", key="user_input")

if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))

    # Call MCP server
    try:
        mcp_response = requests.post(
            "http://localhost:5000/execute",
            json={"command": user_input},
            timeout=60
        )
        mcp_response.raise_for_status()
        mcp_data = mcp_response.json()

        # Check if screenshot is included
        if "screenshot_base64" in mcp_data:
            st.session_state.chat_history.append(("mcp", mcp_data["message"]))
            st.session_state.chat_history.append(("screenshot", mcp_data["screenshot_base64"]))
        else:
            st.session_state.chat_history.append(("mcp", mcp_data.get("message", "[No message]")))

    except Exception as e:
        st.session_state.chat_history.append(("mcp", f"[Error contacting MCP server: {e}]"))

    st.rerun()

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    elif sender == "mcp":
        with st.expander("🛠️ MCP Response"):
            st.markdown(msg)
    elif sender == "screenshot":
        st.image(base64.b64decode(msg), caption="📸 Screenshot", use_column_width=True)
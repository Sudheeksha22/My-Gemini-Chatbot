import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖"
)

st.title("🤖 My Gemini Chatbot")
st.write("Have a conversation with Gemini!")

# API KEY BOX
api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password"
)

if not api_key:
    st.info("Enter your Gemini API key in the box on the left.")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat box
user_input = st.chat_input("Type your message...")

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        # Create Gemini chat
        if "gemini_chat" not in st.session_state:
            st.session_state.gemini_chat = client.chats.create(
                model="gemini-3.8-flash"
            )

        response = st.session_state.gemini_chat.send_message(
            message=user_input
        )

        answer = response.text

    except Exception as e:
        answer = f"❌ Error: {e}"

    # Show Gemini response
    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# Clear chat
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    if "gemini_chat" in st.session_state:
        del st.session_state.gemini_chat

    st.rerun()
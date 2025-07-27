import streamlit as st
import google.generativeai as genai
import os

# --- Streamlit Page Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(page_title="Sahaayika AI Companion", page_icon="🌸", layout="centered")

# --- Configuration ---
gemini_api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyBxKCFSAzzncIGG98jiGqZV1fnt2LFSfQU"

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("Gemini API Key not found. Please set the GOOGLE_API_KEY environment variable or provide it directly in the code.")
    model = None

# Custom CSS for a touch of styling (similar to your React app's feel)
st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to bottom right, #e0f2fe, #fce4ec); /* Light blue to light pink gradient */
    }
    .main .block-container {
        max-width: 700px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stApp {
        background-color: #f8fafc; /* Light gray background for the app content area */
        border-radius: 1.5rem; /* Rounded corners for the app container */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* Shadow */
        overflow: hidden;
    }
    .stButton>button {
        background-color: #8b5cf6; /* Purple button */
        color: white;
        border-radius: 0.75rem; /* Rounded corners */
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        background-color: #7c3aed; /* Darker purple on hover */
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .stTextInput>div>div>input {
        border-radius: 0.75rem;
        border: 1px solid #d1d5db;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        color: #374151;
    }
    .chat-message-user {
        background-color: #d8b4fe; /* Light purple for user message */
        border-radius: 0.75rem;
        border-bottom-right-radius: 0;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        align-self: flex-end;
        text-align: right;
    }
    .chat-message-ai {
        background-color: #e5e7eb; /* Light gray for AI message */
        border-radius: 0.75rem;
        border-bottom-left-radius: 0;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        align-self: flex-start;
        text-align: left;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Header with Logo
st.markdown(
    """
    <div style="background: linear-gradient(to right, #8b5cf6, #ec4899); padding: 1.5rem; border-top-left-radius: 1.5rem; border-top-right-radius: 1.5rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <img src="http://googleusercontent.com/file_content/2" alt="Sahaayika Logo" style="height: 40px; border-radius: 0.5rem;"/>
        <h1 style="color: white; font-size: 2.25rem; font-weight: bold; margin: 0;">Sahaayika</h1>
        <span style="background-color: rgba(255, 255, 255, 0.2); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; color: white;">User ID: local-user-id</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---") # Separator

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align: center; color: #6b7280; margin-top: 2.5rem;">
            <p style="font-size: 1.125rem;">Speak your mind...</p>
            <p style="font-size: 0.875rem;">Type your feelings or thoughts below.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message-user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-ai">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input("Type your message here...", key="user_input")

# Send button
if st.button("Send", key="send_button"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Sahaayika is thinking..."):
            if model:
                try:
                    response = model.generate_content(user_input)
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"An error occurred: {e}. Please check your API key or try again."
            else:
                ai_response = "AI model not initialized due to missing API key."

            st.session_state.messages.append({"role": "ai", "content": ai_response})
        st.rerun()
    else:
        st.warning("Please type a message before sending.")

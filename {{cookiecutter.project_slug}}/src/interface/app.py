import streamlit as st
import httpx
import os
from dotenv import load_dotenv
from src.backend.core.config import settings

# Load environment variables for the API Key
load_dotenv()
st.set_page_config(page_title="{{cookiecutter.project_name}}", page_icon="🤖")

# FIX: Define the function BEFORE calling it
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True

    def password_entered():
        if st.session_state["password"] == settings.ADMIN_PASSWORD.get_secret_value():
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    st.sidebar.title("Access Required")
    st.sidebar.text_input("Enter Password", type="password", key="password", on_change=password_entered)
    return st.session_state.password_correct

# FIX: Now call it safely
if not check_password():
    st.info("Please enter the password in the sidebar to continue.")
    st.stop()

st.title("🤖 {{cookiecutter.project_name}}")
st.markdown("Interact with your Google ADK-powered agent.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your task today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Agent is thinking..."):
        try:
            # Call your FastAPI backend
            # Note: Ensure your backend is running on localhost:8000
            API_URL = "http://localhost:8000/api/v1/task" # Example endpoint
            HEADERS = {"X-API-Key": os.getenv("API_KEY", "")}
            
            response = httpx.post(
                API_URL, 
                json={"task": prompt}, 
                headers=HEADERS,
                timeout=30.0
            )
            
            if response.status_code == 200:
                answer = response.json().get("result", "No result returned.")
            else:
                answer = f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            answer = f"Connection Error: {str(e)}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
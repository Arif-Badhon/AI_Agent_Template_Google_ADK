import streamlit as st
import pandas as pd
import os
from src.backend.core.config import settings
from src.backend.services.agent_service import AgentOrchestrator

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Basic Auth using .env credentials
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    with st.form("admin_login"):
        password = st.text_input("Admin Password", type="password")
        if st.form_submit_button("Login"):
            if password == settings.ADMIN_PASSWORD.get_secret_value():
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

st.title("🛡️ System Administration")

# Tab 1: Agent Registry
st.header("🤖 Active Agents")
orch = AgentOrchestrator()
agent_data = [{"Name": k, "Description": v.description} for k, v in orch.agents.items()]
st.table(pd.DataFrame(agent_data))

# Tab 2: Logs
st.header("📋 Logs & Issues")
if os.path.exists(settings.LOG_FILE_PATH):
    with open(settings.LOG_FILE_PATH, "r") as f:
        st.text_area("Live Logs", f.read(), height=400)
else:
    st.warning("Log file not found. Check LOG_FILE_PATH in .env")
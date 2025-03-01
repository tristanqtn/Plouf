import streamlit as st  # type: ignore
import requests
from config import PLOUF_BACKEND_URL

def show():
    st.title("🩺 System Health")
    api_response = requests.get(f"{PLOUF_BACKEND_URL}/health/api/uptime")
    mongo_response = requests.get(f"{PLOUF_BACKEND_URL}/health/mongo/full_health")

    if api_response.status_code == 200:
        st.subheader("API Health")
        st.json(api_response.json())
    else:
        st.error("Failed to fetch API health.")

    if mongo_response.status_code == 200:
        st.subheader("MongoDB Health")
        st.json(mongo_response.json())
    else:
        st.error("Failed to fetch MongoDB health.")

    st.markdown("---")

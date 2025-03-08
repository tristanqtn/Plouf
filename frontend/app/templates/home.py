import streamlit as st  # type: ignore
import requests
from config import PLOUF_BACKEND_URL


def show():
    st.title("🏊 Plouf Dashboard")
    st.write("Welcome to Plouf! Use the navigation on the left to explore.")

    # Fetch backend statistics
    total_pools_response = requests.get(f"{PLOUF_BACKEND_URL}/stats/total_pools")
    total_logs_response = requests.get(f"{PLOUF_BACKEND_URL}/stats/total_logs")
    api_response = requests.get(f"{PLOUF_BACKEND_URL}/health/api/uptime")
    mongo_response = requests.get(f"{PLOUF_BACKEND_URL}/health/mongo/full_health")

    # ------------------- DISPLAY BIG STATS -------------------
    st.subheader("📊 System Overview", divider="red")
    col1, col2 = st.columns(2)

    with col1:
        if total_pools_response.status_code == 200:
            total_pools = total_pools_response.json()["total_pools"]
            st.metric("🏊 Total Pools", total_pools, delta=None, delta_color="normal")
        else:
            st.error("Failed to fetch total pools data.")

    with col2:
        if total_logs_response.status_code == 200:
            total_logs = total_logs_response.json()["total_logs"]
            st.metric("📋 Total Logs", total_logs, delta=None, delta_color="normal")
        else:
            st.error("Failed to fetch total logs data.")

    # ------------------- API Health Stats -------------------
    st.subheader("🩺 System Health Overview", divider="red")

    col1, col2 = st.columns(2)

    with col1:
        if api_response.status_code == 200:
            api_data = api_response.json()
            uptime_seconds = api_data.get("uptime_seconds", 0)
            st.metric(
                "API Uptime (s)",
                round(uptime_seconds),
                delta=None,
                delta_color="normal",
            )
            st.metric("API Status", "🟢 OK", delta=None, delta_color="normal")
        else:
            st.metric("API Status", "🔴 ERROR", delta=None, delta_color="normal")
            st.error("Failed to fetch API health data.")

    with col2:
        if mongo_response.status_code == 200:
            mongo_data = mongo_response.json()
            mongo_uptime = mongo_data["uptime"]["uptime_seconds"]
            st.metric(
                "MongoDB Uptime (s)",
                round(mongo_uptime),
                delta=None,
                delta_color="normal",
            )
            st.metric("Mongo Status", "🟢 OK", delta=None, delta_color="normal")

            # MongoDB Storage Stats
            memory_stats = mongo_data["storage_stats"]["memory"]
            memory_usage = f"Resident: {memory_stats['resident_MB']} MB, Virtual: {memory_stats['virtual_MB']} MB"
            st.write(f"💾 **Memory Usage**: {memory_usage}")
        else:
            st.metric("Mongo Status", "🔴 ERROR", delta=None, delta_color="normal")
            st.error("Failed to fetch MongoDB health data.")

    st.markdown("---")

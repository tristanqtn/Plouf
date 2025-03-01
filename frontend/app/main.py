import streamlit as st  # type: ignore
from templates import home, pools, pool_details, health

st.set_page_config(page_title="Pool Dashboard", layout="wide")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Sidebar Navigation (Sync with session state)
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Pools", "Pool Details", "Health Check"],
    index=["Home", "Pools", "Pool Details", "Health Check"].index(
        st.session_state["page"]
    ),
    key="navigation_radio",  # 👈 Ensures state updates properly
)

# Update session state when user changes the page manually
if page != st.session_state["page"]:
    st.session_state["page"] = page
    st.rerun()  # 🔄 Force rerun so the UI updates instantly

# Page Routing
if st.session_state["page"] == "Home":
    home.show()
elif st.session_state["page"] == "Pools":
    pools.show()
elif st.session_state["page"] == "Pool Details":
    pool_details.show()
elif st.session_state["page"] == "Health Check":
    health.show()

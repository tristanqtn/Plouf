import streamlit as st  # type: ignore
import requests
from config import PLOUF_BACKEND_URL


def show():
    st.title("📋 All Pools")
    st.write(
        "Here you can view all the pools in the system, and add new pools to Plouf."
    )
    st.markdown("---")
    response = requests.get(f"{PLOUF_BACKEND_URL}/pool/all")
    if response.status_code == 200:
        data = response.json()

        for pool in data["pools"]:
            st.subheader(f"Pool ID: {pool['id']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Owner Name:** {pool['owner_name']}")
                st.write(
                    f"**Dimensions:** {pool['length']}m x {pool['width']}m x {pool['depth']}m"
                )
                st.write(f"**Water Volume:** {pool['water_volume']} cubic meters")

            with col2:
                st.write(f"**Type:** {pool['type']}")
                st.write(f"**Next Maintenance:** {pool['next_maintenance']}")
                if pool["notes"]:
                    st.write(f"**Notes:** {pool['notes']}")

            with col3:
                if st.button("View Details ➡️", key=f"details_{pool['id']}"):
                    st.session_state["selected_pool"] = pool["id"]
                    st.session_state["page"] = "Pool Details"
                    st.rerun()

                sender = False

                if f"delete_{pool['id']}" not in st.session_state:
                    st.session_state[f"delete_{pool['id']}"] = False

                # Display the delete button
                if st.button("❌ Delete", key=f"del_{pool['id']}"):
                    st.session_state[f"delete_{pool['id']}"] = not st.session_state[
                        f"delete_{pool['id']}"
                    ]

                if st.session_state[f"delete_{pool['id']}"]:
                    if st.button("❌ Confirm", key=f"confirm_{pool['id']}"):
                        sender = True

                if sender:
                    delete_response = requests.delete(
                        f"{PLOUF_BACKEND_URL}/pool/{pool['id']}"
                    )
                    if (
                        delete_response.status_code == 200
                        and delete_response.json()["status"] == "ok"
                    ):
                        st.success("Pool deleted successfully!")
                    else:
                        st.error("Failed to delete pool.")
                    sender = False
                    st.session_state[f"delete_{pool['id']}"] = False
                    st.rerun()

            st.markdown("---")
    else:
        st.error("Failed to fetch pools data.")

    # -------------------- ADD NEW POOL FORM --------------------
    st.subheader("➕ Add a New Pool")
    with st.form("add_pool_form", clear_on_submit=True):
        owner_name = st.text_input("Owner Name", placeholder="John Doe")
        length = st.number_input("Length (m)", min_value=1.0, step=0.1)
        width = st.number_input("Width (m)", min_value=1.0, step=0.1)
        depth = st.number_input("Depth (m)", min_value=0.5, step=0.1)
        pool_type = st.text_input("Type", placeholder="Indoor, Heated, etc.")
        notes = st.text_area("Notes", placeholder="Additional pool details (optional)")
        next_maintenance = st.date_input("Next Maintenance Date")

        submit_button = st.form_submit_button("✅ Add Pool")

        if submit_button:
            water_volume = length * width * depth
            pool_data = {
                "owner_name": owner_name,
                "length": length,
                "width": width,
                "depth": depth,
                "type": pool_type,
                "notes": notes,
                "water_volume": water_volume,
                "next_maintenance": str(next_maintenance),
            }

            add_response = requests.post(f"{PLOUF_BACKEND_URL}/pool", json=pool_data)

            if (
                add_response.status_code == 200
                and add_response.json()["status"] == "ok"
            ):
                st.success("Pool added successfully!")
                st.rerun()
            else:
                st.error("Failed to add pool.")
    st.markdown("---")

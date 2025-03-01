import streamlit as st  # type: ignore
import requests

import numpy as np
import plotly.graph_objs as go  # type: ignore

from config import PLOUF_BACKEND_URL

def show():
    if "selected_pool" not in st.session_state:
        st.warning("No pool selected. Please go to 'Pools' and choose one.")
    else:
        pool_id = st.session_state["selected_pool"]
        response = requests.get(f"{PLOUF_BACKEND_URL}/pool/{pool_id}")

        if response.status_code == 200:
            pool_data = response.json()["pool"]
            # -------------------- POOL DETAILS --------------------
            st.title(f"🏊 Pool {pool_data['id']} - Details")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Owner Name:** {pool_data['owner_name']}")
                st.write(
                    f"**Dimensions:** {pool_data['length']}m x {pool_data['width']}m x {pool_data['depth']}m"
                )
                st.write(f"**Water Volume:** {pool_data['water_volume']} cubic meters")

            with col2:
                st.write(f"**Type:** {pool_data['type']}")
                st.write(f"**Next Maintenance:** {pool_data['next_maintenance']}")
            if pool_data["notes"]:
                st.write(f"**Notes:** {pool_data['notes']}")

            st.markdown("---")

            # -------------------- SAMPLES GRAPH --------------------
            logbook = sorted(pool_data["logbook"], key=lambda x: x["date"])
            chlorine_data = [log["chlorine_level"] for log in logbook]
            ph_data = [log["pH_level"] for log in logbook]
            dates = [log["date"] for log in logbook]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=np.arange(len(chlorine_data)),
                    y=chlorine_data,
                    mode="lines",
                    name="Chlorine Level",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=np.arange(len(ph_data)), y=ph_data, mode="lines", name="pH Level"
                )
            )
            fig.update_xaxes(tickvals=np.arange(len(dates)), ticktext=dates)
            fig.update_layout(
                title="Pool Logbook", xaxis_title="Time", yaxis_title="Value"
            )

            st.plotly_chart(fig)

            # -------------------- POOL LOGS SECTION --------------------
            st.subheader("Recent Logs")

            if len(logbook) == 0:
                st.write("No logs available.")
            else:
                for log in logbook:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if log["notes"]:
                            st.write(
                                f"- **Date:** {log['date']}, **pH Level:** {log['pH_level']}, **Chlorine Level:** {log['chlorine_level']}\n- **Notes:** {log['notes']}"
                            )
                        else:
                            st.write(
                                f"- **Date:** {log['date']}, **pH Level:** {log['pH_level']}, **Chlorine Level:** {log['chlorine_level']}"
                            )

                    with col2:
                        sender = False
                        if f"edit_panel{log['id']}" not in st.session_state:
                            st.session_state[f"edit_panel{log['id']}"] = False

                        if st.button("✏️ Update Log", key=f"update_{log['id']}"):
                            st.session_state[
                                f"edit_panel{log['id']}"
                            ] = not st.session_state[f"edit_panel{log['id']}"]

                        if st.session_state[f"edit_panel{log['id']}"]:
                            with st.form("update_log_form"):
                                pH_level = st.number_input(
                                    "pH Level",
                                    min_value=0.0,
                                    max_value=14.0,
                                    step=0.1,
                                    value=log["pH_level"],
                                )
                                chlorine_level = st.number_input(
                                    "Chlorine Level",
                                    min_value=0.0,
                                    max_value=10.0,
                                    step=0.1,
                                    value=log["chlorine_level"],
                                )
                                notes = st.text_area(
                                    "Notes",
                                    placeholder="Additional notes for the log (optional)",
                                    value=log["notes"],
                                )
                                date = st.date_input("Log Date", value=log["date"])

                                submit_button = st.form_submit_button(
                                    "✅ Update Log Entry"
                                )

                                if submit_button:
                                    sender = True

                        if sender:
                            # Create the log data dictionary
                            log_data = {
                                "pH_level": pH_level,
                                "chlorine_level": chlorine_level,
                                "notes": notes,
                                "date": str(date),
                            }

                            # Send a POST request to add the new log entry
                            log_response = requests.put(
                                f"{PLOUF_BACKEND_URL}/pool/{pool_data['id']}/log/{log['id']}",
                                json=log_data,
                            )
                            if log_response.status_code == 200:
                                st.success("Log entry added successfully!")
                            else:
                                st.error("Failed to add log entry. Please try again.")
                            sender = False
                            st.session_state[f"edit_panel{log['id']}"] = False
                            st.rerun()

                    with col3:
                        # Display the delete button

                        sender = False

                        subcol1, subcol2 = st.columns(2)

                        if f"delete_{log['id']}" not in st.session_state:
                            st.session_state[f"delete_{log['id']}"] = False

                        with subcol1:
                            # Display the delete button
                            if st.button("❌ Delete", key=f"del_{log['id']}"):
                                st.session_state[
                                    f"delete_{log['id']}"
                                ] = not st.session_state[f"delete_{log['id']}"]
                        with subcol2:
                            if st.session_state[f"delete_{log['id']}"]:
                                if st.button("❌ Confirm", key=f"confirm_{log['id']}"):
                                    sender = True

                        if sender:
                            delete_response = requests.delete(
                                f"{PLOUF_BACKEND_URL}/pool/{pool_data['id']}/log/{log['id']}"
                            )
                            if (
                                delete_response.status_code == 200
                                and delete_response.json()["status"] == "ok"
                            ):
                                st.success("Pool log deleted successfully!")
                            else:
                                st.error("Failed to delete pool log.")
                            sender = False
                            st.session_state[f"delete_{log['id']}"] = False
                            st.rerun()

            st.markdown("---")

            # -------------------- NEW POOL LOG --------------------
            st.subheader("➕ Add Logbook Entry")

            with st.form("add_logbook_form", clear_on_submit=True):
                pH_level = st.number_input(
                    "pH Level", min_value=0.0, max_value=14.0, step=0.1
                )
                chlorine_level = st.number_input(
                    "Chlorine Level", min_value=0.0, max_value=10.0, step=0.1
                )
                notes = st.text_area(
                    "Notes", placeholder="Additional notes for the log (optional)"
                )
                date = st.date_input("Log Date")

                submit_button = st.form_submit_button("✅ Add Log Entry")

                if submit_button:
                    # Create the log data dictionary
                    log_data = {
                        "pH_level": pH_level,
                        "chlorine_level": chlorine_level,
                        "notes": notes,
                        "date": str(date),
                    }

                    # Send a POST request to add the new log entry
                    log_response = requests.post(
                        f"{PLOUF_BACKEND_URL}/pool/{pool_id}/log", json=log_data
                    )

                    if log_response.status_code == 200:
                        st.success("Log entry added successfully!")
                        st.rerun()  # Refresh the page to show the new log entry
                    else:
                        st.error("Failed to add log entry. Please try again.")

            st.markdown("---")

            # -------------------- UPDATE POOL FORM --------------------
            st.subheader("✏️ Update Pool Information")
            with st.form("update_pool_form"):
                owner_name = st.text_input("Owner Name", value=pool_data["owner_name"])
                length = st.number_input(
                    "Length (m)", min_value=1.0, step=0.1, value=pool_data["length"]
                )
                width = st.number_input(
                    "Width (m)", min_value=1.0, step=0.1, value=pool_data["width"]
                )
                depth = st.number_input(
                    "Depth (m)", min_value=0.5, step=0.1, value=pool_data["depth"]
                )
                pool_type = st.text_input("Type", value=pool_data["type"])
                notes = st.text_area("Notes", value=pool_data["notes"])
                next_maintenance = st.date_input(
                    "Next Maintenance Date", value=pool_data["next_maintenance"]
                )

                update_button = st.form_submit_button("✅ Update Pool")

                if update_button:
                    updated_pool = {
                        "owner_name": owner_name,
                        "length": length,
                        "width": width,
                        "depth": depth,
                        "type": pool_type,
                        "notes": notes,
                        "water_volume": length * width * depth,
                        "next_maintenance": str(next_maintenance),
                    }

                    update_response = requests.put(
                        f"{PLOUF_BACKEND_URL}/pool/{pool_id}", json=updated_pool
                    )

                    if (
                        update_response.status_code == 200
                        and update_response.json()["status"] == "ok"
                    ):
                        st.success("Pool updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update pool.")

            # Back to Pools Button
            if st.button("⬅️ Back to Pools"):
                del st.session_state["selected_pool"]
                st.session_state["page"] = "Pools"
                st.rerun()

        else:
            st.error("Failed to load pool details.")
        st.markdown("---")

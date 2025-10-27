"""
Meetings Management Page

This module contains the UI for creating and managing den meetings.
"""

import streamlit as st
import pandas as pd
from scout_tracker.data import load_requirement_key, load_meetings, save_meetings


def page_manage_meetings():
    """Page for creating and managing den meetings."""
    st.title("📅 Manage Meetings")
    st.write("Define each meeting by its date, title, and requirements covered.")

    # Load data
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()

    # Show helpful tips if no meetings exist yet
    if meetings_df.empty:
        st.info("""
        **👋 Welcome to Meeting Management!**

        This is where you plan your den meetings. For each meeting, you'll:
        1. **Set a date** - When the meeting will occur
        2. **Give it a title** - Something descriptive like "Nature Hike" or "First Aid Skills"
        3. **Select requirements** - Choose which advancement requirements you'll cover

        **Why this matters:**
        When you log attendance later, scouts who attended will automatically get credit for all requirements covered at that meeting. This makes tracking advancement super easy!

        **Getting started:** Fill out the form below to add your first meeting.
        """)

    # Create formatted options for multiselect
    requirement_options = [
        f"{row['Req_ID']} - {row['Requirement_Description']}"
        for _, row in requirement_key.iterrows()
    ]

    # Add meeting form
    st.subheader("Add a New Meeting")
    with st.form("add_meeting_form"):
        meeting_date = st.date_input("Meeting Date", key="meeting_date")
        meeting_title = st.text_input("Meeting Title", key="meeting_title")
        selected_requirements = st.multiselect(
            "Requirements Covered",
            options=requirement_options,
            key="selected_requirements"
        )

        submit_meeting = st.form_submit_button("Add Meeting")

        if submit_meeting:
            if not meeting_title.strip():
                st.error("❌ Please enter a meeting title.")
            elif not selected_requirements:
                st.error("❌ Please select at least one requirement.")
            elif not meetings_df.empty and meeting_date in pd.to_datetime(meetings_df["Meeting_Date"]).dt.date.values:
                st.error(f"❌ A meeting already exists for {meeting_date}. Please choose a different date.")
            else:
                # Extract Req_IDs from selected options
                req_ids = [req.split(" - ")[0] for req in selected_requirements]
                req_ids_str = ",".join(req_ids)

                # Add new meeting
                new_meeting = pd.DataFrame({
                    "Meeting_Date": [pd.to_datetime(meeting_date)],
                    "Meeting_Title": [meeting_title],
                    "Req_IDs_Covered": [req_ids_str]
                })
                meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
                save_meetings(meetings_df)
                st.success(f"✅ Added meeting '{meeting_title}' for {meeting_date}!")
                st.rerun()

    # Display existing meetings
    st.write("---")
    st.subheader("Existing Meetings")
    if not meetings_df.empty:
        # Sort by date descending
        display_df = meetings_df.sort_values("Meeting_Date", ascending=False).copy()
        display_df["Meeting_Date"] = pd.to_datetime(display_df["Meeting_Date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, width='stretch', hide_index=True)
    else:
        st.info("No meetings scheduled yet. Add a meeting above to get started!")

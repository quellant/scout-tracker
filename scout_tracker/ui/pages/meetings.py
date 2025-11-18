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
        optional_meeting = st.checkbox(
            "Optional Meeting",
            value=False,
            help="Optional meetings (like camps or special events) don't count toward attendance requirements. "
                 "Scouts who don't attend won't need to make up these requirements.",
            key="optional_meeting"
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
                    "Req_IDs_Covered": [req_ids_str],
                    "Optional": [optional_meeting]
                })
                meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
                save_meetings(meetings_df)
                optional_text = " (Optional)" if optional_meeting else ""
                st.success(f"✅ Added meeting '{meeting_title}'{optional_text} for {meeting_date}!")
                st.rerun()

    # Edit meeting section
    st.write("---")
    st.subheader("Edit an Existing Meeting")

    if not meetings_df.empty:
        # Create meeting selection options
        meetings_df_sorted = meetings_df.sort_values("Meeting_Date", ascending=False)
        meeting_options = [
            f"{pd.to_datetime(row['Meeting_Date']).strftime('%Y-%m-%d')} - {row['Meeting_Title']}"
            for _, row in meetings_df_sorted.iterrows()
        ]

        selected_meeting_str = st.selectbox(
            "Select a meeting to edit:",
            options=meeting_options,
            key="edit_meeting_selector"
        )

        if selected_meeting_str:
            # Extract the date from the selection
            selected_date_str = selected_meeting_str.split(" - ")[0]
            selected_date = pd.to_datetime(selected_date_str)

            # Get the meeting data
            meeting_data = meetings_df[meetings_df["Meeting_Date"] == selected_date].iloc[0]

            # Get current requirements
            current_req_ids = meeting_data["Req_IDs_Covered"].split(",") if pd.notna(meeting_data["Req_IDs_Covered"]) and meeting_data["Req_IDs_Covered"] else []
            current_req_selections = [
                opt for opt in requirement_options
                if opt.split(" - ")[0] in current_req_ids
            ]

            # Edit form - use unique key based on selected date so form resets when selection changes
            with st.form(f"edit_meeting_form_{selected_date_str}"):
                st.info(f"**Editing meeting from {selected_date_str}**")

                edit_date = st.date_input(
                    "Meeting Date",
                    value=pd.to_datetime(meeting_data["Meeting_Date"]).date(),
                    key=f"edit_meeting_date_{selected_date_str}"
                )
                edit_title = st.text_input(
                    "Meeting Title",
                    value=meeting_data["Meeting_Title"],
                    key=f"edit_meeting_title_{selected_date_str}"
                )
                edit_requirements = st.multiselect(
                    "Requirements Covered",
                    options=requirement_options,
                    default=current_req_selections,
                    key=f"edit_selected_requirements_{selected_date_str}"
                )
                edit_optional = st.checkbox(
                    "Optional Meeting",
                    value=bool(meeting_data.get("Optional", False)),
                    help="Optional meetings (like camps or special events) don't count toward attendance requirements.",
                    key=f"edit_optional_meeting_{selected_date_str}"
                )

                col1, col2 = st.columns([1, 1])
                with col1:
                    update_meeting = st.form_submit_button("💾 Update Meeting")
                with col2:
                    delete_meeting = st.form_submit_button("🗑️ Delete Meeting", type="secondary")

                if update_meeting:
                    if not edit_title.strip():
                        st.error("❌ Please enter a meeting title.")
                    elif not edit_requirements:
                        st.error("❌ Please select at least one requirement.")
                    elif edit_date != pd.to_datetime(meeting_data["Meeting_Date"]).date():
                        # Check if new date conflicts with another meeting
                        if edit_date in pd.to_datetime(meetings_df["Meeting_Date"]).dt.date.values:
                            st.error(f"❌ A meeting already exists for {edit_date}. Please choose a different date.")
                        else:
                            # Extract Req_IDs from selected options
                            req_ids = [req.split(" - ")[0] for req in edit_requirements]
                            req_ids_str = ",".join(req_ids)

                            # Update the meeting
                            meetings_df.loc[meetings_df["Meeting_Date"] == selected_date, "Meeting_Date"] = pd.to_datetime(edit_date)
                            meetings_df.loc[meetings_df["Meeting_Date"] == pd.to_datetime(edit_date), "Meeting_Title"] = edit_title
                            meetings_df.loc[meetings_df["Meeting_Date"] == pd.to_datetime(edit_date), "Req_IDs_Covered"] = req_ids_str
                            meetings_df.loc[meetings_df["Meeting_Date"] == pd.to_datetime(edit_date), "Optional"] = edit_optional

                            save_meetings(meetings_df)
                            optional_text = " (Optional)" if edit_optional else ""
                            st.success(f"✅ Updated meeting '{edit_title}'{optional_text} for {edit_date}!")
                            st.rerun()
                    else:
                        # Same date, just update other fields
                        req_ids = [req.split(" - ")[0] for req in edit_requirements]
                        req_ids_str = ",".join(req_ids)

                        meetings_df.loc[meetings_df["Meeting_Date"] == selected_date, "Meeting_Title"] = edit_title
                        meetings_df.loc[meetings_df["Meeting_Date"] == selected_date, "Req_IDs_Covered"] = req_ids_str
                        meetings_df.loc[meetings_df["Meeting_Date"] == selected_date, "Optional"] = edit_optional

                        save_meetings(meetings_df)
                        optional_text = " (Optional)" if edit_optional else ""
                        st.success(f"✅ Updated meeting '{edit_title}'{optional_text}!")
                        st.rerun()

                if delete_meeting:
                    # Confirm deletion using session state
                    if "confirm_delete" not in st.session_state:
                        st.session_state.confirm_delete = selected_date_str
                        st.warning(f"⚠️ Are you sure you want to delete the meeting on {selected_date_str}? Click 'Delete Meeting' again to confirm.")
                        st.rerun()
                    elif st.session_state.confirm_delete == selected_date_str:
                        # Delete the meeting
                        meetings_df = meetings_df[meetings_df["Meeting_Date"] != selected_date]
                        save_meetings(meetings_df)
                        st.session_state.pop("confirm_delete")
                        st.success(f"✅ Deleted meeting from {selected_date_str}!")
                        st.rerun()
    else:
        st.info("No meetings to edit yet. Add a meeting above first!")

    # Display existing meetings
    st.write("---")
    st.subheader("All Meetings")
    if not meetings_df.empty:
        # Sort by date descending
        display_df = meetings_df.sort_values("Meeting_Date", ascending=False).copy()
        display_df["Meeting_Date"] = pd.to_datetime(display_df["Meeting_Date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, width='stretch', hide_index=True)
    else:
        st.info("No meetings scheduled yet. Add a meeting above to get started!")

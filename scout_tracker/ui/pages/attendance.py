"""
Attendance Logging Page

This module contains the UI for logging which scouts attended each meeting.
"""

import streamlit as st
import pandas as pd
from scout_tracker.data import load_roster, load_meetings, load_attendance, save_attendance


def page_log_attendance():
    """Page for logging which scouts attended each meeting."""
    st.title("✅ Log Meeting Attendance")
    st.write("Select a meeting to record or edit attendance.")

    # Load data
    roster_df = load_roster()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    # Show helpful tips if no meetings exist
    if meetings_df.empty:
        st.warning("⚠️ No meetings have been created yet.")
        st.info("""
        **Getting Started with Attendance Logging:**

        Before you can log attendance, you need to:
        1. **Create meetings** - Go to "Manage Meetings" to add meetings
        2. **Specify requirements** - When creating a meeting, select which requirements you'll cover
        3. **Log attendance** - Come back here after each meeting to mark who attended

        **How it works:**
        - When you mark a scout as "attended," they automatically get credit for all requirements covered at that meeting
        - This makes progress tracking automatic - no need to manually check off requirements for each scout!
        """)
        return

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet.")
        st.info("""
        **Need to add scouts first:**

        Go to "Manage Roster" to add the scouts in your den. Once you have scouts in your roster, you can log their meeting attendance here.
        """)
        return

    # Create meeting selection options
    meeting_options = [
        f"{row['Meeting_Date'].strftime('%Y-%m-%d')} - {row['Meeting_Title']}"
        for _, row in meetings_df.iterrows()
    ]
    meeting_dates = meetings_df["Meeting_Date"].tolist()

    selected_meeting_str = st.selectbox(
        "Select a Meeting",
        options=meeting_options,
        key="selected_meeting"
    )

    # Get the selected meeting date
    selected_idx = meeting_options.index(selected_meeting_str)
    selected_date = meeting_dates[selected_idx]

    # Get current attendance for this meeting
    current_attendees = attendance_df[
        attendance_df["Meeting_Date"] == selected_date
    ]["Scout_Name"].tolist()

    # Show attendance status
    total_scouts = len(roster_df)
    attendance_count = len(current_attendees)

    st.write("---")

    # Show current attendance first
    st.subheader("📊 Current Attendance")

    if current_attendees:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Present ({len(current_attendees)}):**")
            for scout in sorted(current_attendees):
                st.write(f"✅ {scout}")

        with col2:
            # Show who was absent
            absent_scouts = [scout for scout in roster_df["Scout Name"] if scout not in current_attendees]
            if absent_scouts:
                st.write(f"**Absent ({len(absent_scouts)}):**")
                for scout in sorted(absent_scouts):
                    st.write(f"❌ {scout}")
            else:
                st.success("🎉 Perfect attendance!")

        st.info(f"**Summary:** {attendance_count} of {total_scouts} scouts attended ({(attendance_count/total_scouts*100):.0f}%)")
    else:
        st.warning("⚠️ No attendance recorded yet for this meeting")

    st.write("---")

    # Attendance form for editing
    st.subheader("✏️ Edit Attendance")
    st.write("Modify the selections below and click Save to update attendance.")

    # Use the meeting date as part of the form key to force re-render when meeting changes
    form_key = f"attendance_form_{selected_date.strftime('%Y%m%d')}"

    with st.form(form_key):
        selected_scouts = st.multiselect(
            "Scouts who were Present",
            options=roster_df["Scout Name"].tolist(),
            default=current_attendees,
            help="Select all scouts who attended this meeting"
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            submit_attendance = st.form_submit_button("💾 Save Attendance", width='stretch')
        with col2:
            st.write(f"*Selected: {len(selected_scouts)} of {total_scouts} scouts*")

        if submit_attendance:
            # Remove all existing attendance records for this date
            attendance_df = attendance_df[attendance_df["Meeting_Date"] != selected_date]

            # Add new attendance records
            if selected_scouts:
                new_attendance = pd.DataFrame({
                    "Meeting_Date": [selected_date] * len(selected_scouts),
                    "Scout_Name": selected_scouts
                })
                attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)

            save_attendance(attendance_df)

            if current_attendees:
                st.success(f"✅ Attendance updated for {selected_date.strftime('%Y-%m-%d')}! ({len(selected_scouts)} scouts)")
            else:
                st.success(f"✅ Attendance recorded for {selected_date.strftime('%Y-%m-%d')}! ({len(selected_scouts)} scouts)")
            st.rerun()

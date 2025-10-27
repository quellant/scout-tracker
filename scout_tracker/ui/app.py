"""
Scout Tracker Main Application

This module contains the main application entry point and navigation logic.
"""

import streamlit as st
from scout_tracker.data import initialize_data_files
from scout_tracker.ui.pages import (
    page_manage_roster,
    page_manage_requirements,
    page_manage_meetings,
    page_log_attendance,
    page_tracker_dashboard,
    page_plan_meetings,
    page_individual_scout_reports,
    page_meeting_reports,
    is_first_run,
    page_onboarding,
)


def main():
    """Main application entry point."""

    # Initialize data files on first run
    initialize_data_files()

    # Configure page
    st.set_page_config(
        page_title="Scout Tracker",
        page_icon="🏕️",
        layout="wide"
    )

    # Check if onboarding is needed
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = not is_first_run()

    # Show onboarding if not complete
    if not st.session_state.onboarding_complete:
        page_onboarding()
        return

    # Sidebar navigation
    st.sidebar.title("🏕️ Scout Tracker")
    st.sidebar.write("---")

    page = st.sidebar.radio(
        "Navigation",
        ["Manage Roster", "Manage Requirements", "Plan Meetings", "Manage Meetings", "Log Attendance", "Tracker Dashboard", "Individual Reports", "Meeting Reports"],
        key="navigation"
    )

    st.sidebar.write("---")
    st.sidebar.info(
        "**Workflow:**\n"
        "1. Add scouts to roster\n"
        "2. Configure requirements\n"
        "3. Plan & create meetings\n"
        "4. Log attendance\n"
        "5. View progress"
    )

    # Route to selected page
    if page == "Manage Roster":
        page_manage_roster()
    elif page == "Manage Requirements":
        page_manage_requirements()
    elif page == "Plan Meetings":
        page_plan_meetings()
    elif page == "Manage Meetings":
        page_manage_meetings()
    elif page == "Log Attendance":
        page_log_attendance()
    elif page == "Tracker Dashboard":
        page_tracker_dashboard()
    elif page == "Individual Reports":
        page_individual_scout_reports()
    elif page == "Meeting Reports":
        page_meeting_reports()

"""
Tracker Dashboard Page

This module contains the UI for the advancement tracking dashboard.
Shows progress for all scouts in the den.
"""

import streamlit as st
import pandas as pd
from scout_tracker.data import load_roster, load_requirement_key, load_meetings, load_attendance


def page_tracker_dashboard():
    """Dashboard showing advancement progress for all scouts."""
    st.title("📊 Tracker Dashboard")
    st.write("View progress for all scouts in your den.")

    # Load all data
    roster_df = load_roster()
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet. Please add scouts to get started!")
        return

    # Build master tracker DataFrame
    scouts = roster_df["Scout Name"].tolist()
    req_ids = requirement_key["Req_ID"].tolist()

    # Initialize with all False
    master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered
    meeting_req_lookup = {}
    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered

    # Process attendance to mark completed requirements
    for _, attendance_row in attendance_df.iterrows():
        scout_name = attendance_row["Scout_Name"]
        meeting_date = attendance_row["Meeting_Date"]

        if scout_name in master_tracker.index and meeting_date in meeting_req_lookup:
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in master_tracker.columns:
                    master_tracker.at[scout_name, req_id] = True

    # ========================================================================
    # SUMMARY VIEW
    # ========================================================================

    st.subheader("📈 Adventure Completion Summary")

    # Separate required and elective adventures
    required_adventures = requirement_key[requirement_key["Required"] == True]["Adventure"].unique()
    elective_adventures = requirement_key[requirement_key["Required"] == False]["Adventure"].unique()

    # Calculate completion data for all scouts
    required_summary_data = []
    elective_summary_data = []
    rank_completion_data = []

    for scout in scouts:
        # Required adventures
        required_summary = {"Scout Name": scout}
        all_required_complete = True

        for adventure in required_adventures:
            adventure_reqs = requirement_key[requirement_key["Adventure"] == adventure]["Req_ID"].tolist()
            completed = master_tracker.loc[scout, adventure_reqs].sum()
            total = len(adventure_reqs)
            percentage = (completed / total * 100) if total > 0 else 0  # Convert to 0-100 scale
            required_summary[adventure] = percentage
            if percentage < 100.0:
                all_required_complete = False

        required_summary_data.append(required_summary)

        # Elective adventures
        elective_summary = {"Scout Name": scout}
        completed_electives = 0

        for adventure in elective_adventures:
            adventure_reqs = requirement_key[requirement_key["Adventure"] == adventure]["Req_ID"].tolist()
            completed = master_tracker.loc[scout, adventure_reqs].sum()
            total = len(adventure_reqs)
            percentage = (completed / total * 100) if total > 0 else 0  # Convert to 0-100 scale
            elective_summary[adventure] = percentage
            if percentage == 100.0:
                completed_electives += 1

        elective_summary_data.append(elective_summary)

        # Lion Rank completion: All required + at least 2 electives
        lion_rank_earned = all_required_complete and completed_electives >= 2
        rank_completion_data.append({
            "Scout Name": scout,
            "Required Complete": "✅ Yes" if all_required_complete else "❌ No",
            "Electives Complete": f"{completed_electives} / 2",
            "Lion Rank Earned": "✅ Yes" if lion_rank_earned else "❌ No"
        })

    # Display Required Adventures Table
    st.write("### Required Adventures (Must complete all 6)")
    required_summary_df = pd.DataFrame(required_summary_data)

    required_column_config = {"Scout Name": st.column_config.TextColumn("Scout Name")}
    for adventure in required_adventures:
        required_column_config[adventure] = st.column_config.ProgressColumn(
            adventure,
            format="%.0f%%",
            min_value=0,
            max_value=100,
        )

    st.dataframe(
        required_summary_df,
        column_config=required_column_config,
        width='stretch',
        hide_index=True
    )

    st.write("---")

    # Display Elective Adventures Table
    st.write("### Elective Adventures (Must complete any 2)")
    elective_summary_df = pd.DataFrame(elective_summary_data)

    elective_column_config = {"Scout Name": st.column_config.TextColumn("Scout Name")}
    for adventure in elective_adventures:
        elective_column_config[adventure] = st.column_config.ProgressColumn(
            adventure,
            format="%.0f%%",
            min_value=0,
            max_value=100,
        )

    st.dataframe(
        elective_summary_df,
        column_config=elective_column_config,
        width='stretch',
        hide_index=True
    )

    st.write("---")

    # Display Lion Rank Completion Status
    st.write("### Lion Rank Completion Status")
    rank_completion_df = pd.DataFrame(rank_completion_data)
    st.dataframe(
        rank_completion_df,
        width='stretch',
        hide_index=True
    )

    # ========================================================================
    # DETAILED VIEW
    # ========================================================================

    with st.expander("🔍 Show Detailed Requirement Tracker"):
        st.write("Detailed view showing each requirement completion status.")

        # Create display version with checkmarks
        display_tracker = master_tracker.copy()
        display_tracker = display_tracker.replace({True: "✅", False: "❌"})

        st.dataframe(
            display_tracker,
            width='stretch'
        )

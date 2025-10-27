"""
Plan Meetings Page

This module contains the UI for planning future meetings based on requirement completion.
"""

import streamlit as st
import pandas as pd
from scout_tracker.data import load_roster, load_requirement_key, load_meetings, load_attendance


def page_plan_meetings():
    """Page for planning future meetings based on requirement completion."""
    st.title("📅 Plan Meetings")
    st.write("See which required requirements need the most attention to help plan your next meetings.")

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

    # Get only required requirements
    required_reqs = requirement_key[requirement_key["Required"] == True].copy()

    # Calculate completion statistics for each requirement
    planning_data = []

    for _, req_row in required_reqs.iterrows():
        req_id = req_row["Req_ID"]
        adventure = req_row["Adventure"]
        description = req_row["Requirement_Description"]

        # Count how many scouts have completed this requirement
        completed_count = master_tracker[req_id].sum()
        total_scouts = len(scouts)
        completion_percentage = (completed_count / total_scouts * 100) if total_scouts > 0 else 0

        # Get list of scouts who haven't completed it
        scouts_missing = [scout for scout in scouts if not master_tracker.loc[scout, req_id]]

        planning_data.append({
            "Req_ID": req_id,
            "Adventure": adventure,
            "Requirement": description,
            "Completed": completed_count,
            "Total Scouts": total_scouts,
            "% Complete": completion_percentage,
            "Scouts Missing": ", ".join(scouts_missing) if scouts_missing else "All complete!"
        })

    planning_df = pd.DataFrame(planning_data)

    # Sort by completion percentage (lowest first) to show most needed requirements at top
    planning_df = planning_df.sort_values("% Complete", ascending=True)

    # Display options
    st.subheader("View Options")
    col1, col2 = st.columns(2)

    with col1:
        view_mode = st.radio(
            "Show:",
            ["All Required Requirements", "Incomplete Only (< 100%)", "Most Needed (< 50%)"],
            key="view_mode"
        )

    with col2:
        group_by_adventure = st.checkbox("Group by Adventure", value=True)

    # Filter based on view mode
    if view_mode == "Incomplete Only (< 100%)":
        filtered_df = planning_df[planning_df["% Complete"] < 100]
    elif view_mode == "Most Needed (< 50%)":
        filtered_df = planning_df[planning_df["% Complete"] < 50]
    else:
        filtered_df = planning_df

    if filtered_df.empty:
        st.success("🎉 All scouts have completed all required requirements!")
        return

    st.write("---")

    # Display the data
    if group_by_adventure:
        st.subheader("Required Requirements by Adventure")
        adventures = filtered_df["Adventure"].unique()

        for adventure in adventures:
            adventure_reqs = filtered_df[filtered_df["Adventure"] == adventure]

            # Calculate adventure-level stats
            avg_completion = adventure_reqs["% Complete"].mean()

            with st.expander(f"**{adventure}** ({len(adventure_reqs)} requirements, {avg_completion:.0f}% average completion)", expanded=True):
                for _, req_row in adventure_reqs.iterrows():
                    completion = req_row["% Complete"]

                    # Color-code based on completion
                    if completion == 100:
                        status_color = "🟢"
                    elif completion >= 50:
                        status_color = "🟡"
                    else:
                        status_color = "🔴"

                    st.write(f"{status_color} **{req_row['Req_ID']}** ({completion:.0f}% complete)")
                    st.write(f"   *{req_row['Requirement']}*")
                    st.write(f"   **Completed by:** {req_row['Completed']} of {req_row['Total Scouts']} scouts")

                    if req_row['Scouts Missing'] != "All complete!":
                        st.write(f"   **Still need:** {req_row['Scouts Missing']}")
                    st.write("")
    else:
        st.subheader("All Required Requirements")

        # Configure column display
        column_config = {
            "Req_ID": st.column_config.TextColumn("Requirement ID", width="small"),
            "Adventure": st.column_config.TextColumn("Adventure", width="medium"),
            "Requirement": st.column_config.TextColumn("Requirement", width="large"),
            "Completed": st.column_config.NumberColumn("Completed", width="small"),
            "Total Scouts": st.column_config.NumberColumn("Total", width="small"),
            "% Complete": st.column_config.ProgressColumn(
                "% Complete",
                format="%.0f%%",
                min_value=0,
                max_value=100,
                width="small"
            ),
            "Scouts Missing": st.column_config.TextColumn("Scouts Missing", width="large")
        }

        st.dataframe(
            filtered_df,
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )

    # Summary statistics
    st.write("---")
    st.subheader("📊 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_reqs = len(required_reqs)
        completed_reqs = len(planning_df[planning_df["% Complete"] == 100])
        st.metric("Required Requirements", f"{completed_reqs} / {total_reqs} at 100%")

    with col2:
        avg_completion = planning_df["% Complete"].mean()
        st.metric("Average Completion", f"{avg_completion:.0f}%")

    with col3:
        needs_attention = len(planning_df[planning_df["% Complete"] < 50])
        st.metric("Needs Most Attention", f"{needs_attention} requirements")

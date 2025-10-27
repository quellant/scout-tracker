"""
Individual Scout Reports Page

This module contains the UI for viewing detailed individual scout progress reports.
"""

import streamlit as st
import pandas as pd
from scout_tracker.data import load_roster, load_requirement_key, load_meetings, load_attendance


def page_individual_scout_reports():
    """Page for viewing detailed individual scout progress reports."""
    st.title("👤 Individual Scout Reports")
    st.write("View comprehensive progress reports for individual scouts, including meeting attendance details.")

    # Load all data
    roster_df = load_roster()
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if roster_df.empty:
        st.warning("⚠️ No scouts in the roster yet. Please add scouts to get started!")
        return

    # Scout selection
    scouts = roster_df["Scout Name"].tolist()
    selected_scout = st.selectbox("Select a scout:", scouts, key="scout_selector")

    if not selected_scout:
        return

    st.write("---")

    # Build master tracker for this scout
    req_ids = requirement_key["Req_ID"].tolist()
    scout_progress = {req_id: False for req_id in req_ids}

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered
    meeting_req_lookup = {}
    meeting_details = {}  # Store meeting details for display
    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered
        meeting_details[meeting["Meeting_Date"]] = {
            "title": meeting["Meeting_Title"],
            "req_ids": req_ids_covered
        }

    # Track which requirements were completed at which meetings
    req_completion_meetings = {req_id: [] for req_id in req_ids}

    # Get meetings attended by this scout
    scout_attendance = attendance_df[attendance_df["Scout_Name"] == selected_scout]
    meetings_attended = []

    for _, attendance_row in scout_attendance.iterrows():
        meeting_date = attendance_row["Meeting_Date"]

        if meeting_date in meeting_req_lookup:
            # Convert meeting_date to datetime if it's a string
            meeting_date_dt = pd.to_datetime(meeting_date) if isinstance(meeting_date, str) else meeting_date

            # Record meeting attendance
            meeting_info = meeting_details.get(meeting_date, {"title": "Untitled Meeting", "req_ids": []})
            meetings_attended.append({
                "date": meeting_date_dt,
                "title": meeting_info["title"],
                "req_ids": meeting_info["req_ids"]
            })

            # Mark requirements as completed
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in scout_progress:
                    scout_progress[req_id] = True
                    req_completion_meetings[req_id].append({
                        "date": meeting_date_dt,
                        "title": meeting_info["title"]
                    })

    # Sort meetings by date (most recent first)
    meetings_attended = sorted(meetings_attended, key=lambda x: x["date"], reverse=True)

    # ========================================================================
    # OVERALL PROGRESS SUMMARY
    # ========================================================================

    st.header(f"📊 Progress Summary for {selected_scout}")

    # Separate required and elective
    required_reqs = requirement_key[requirement_key["Required"] == True]
    elective_reqs = requirement_key[requirement_key["Required"] == False]

    # Calculate required progress
    required_completed = sum(1 for req_id in required_reqs["Req_ID"] if scout_progress.get(req_id, False))
    required_total = len(required_reqs)
    required_percentage = (required_completed / required_total * 100) if required_total > 0 else 0

    # Calculate elective progress
    elective_adventures = elective_reqs["Adventure"].unique()
    completed_electives = 0
    for adventure in elective_adventures:
        adventure_reqs = elective_reqs[elective_reqs["Adventure"] == adventure]["Req_ID"].tolist()
        if all(scout_progress.get(req_id, False) for req_id in adventure_reqs):
            completed_electives += 1

    # Check rank completion (all required + 2 electives)
    all_required_complete = required_completed == required_total
    rank_earned = all_required_complete and completed_electives >= 2

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Required Complete", f"{required_completed} / {required_total}",
                 f"{required_percentage:.0f}%")

    with col2:
        st.metric("Electives Complete", f"{completed_electives} / 2",
                 "✅ Ready" if completed_electives >= 2 else f"Need {2 - completed_electives}")

    with col3:
        st.metric("Meetings Attended", len(meetings_attended))

    with col4:
        rank_status = "✅ EARNED!" if rank_earned else "In Progress"
        st.metric("Rank Status", rank_status)

    if rank_earned:
        st.success(f"🎉 **Congratulations!** {selected_scout} has earned their rank!")

    st.write("---")

    # ========================================================================
    # MEETING ATTENDANCE HISTORY
    # ========================================================================

    st.header("📅 Meeting Attendance History")

    if not meetings_attended:
        st.info("No meetings attended yet.")
    else:
        st.write(f"**Total meetings attended:** {len(meetings_attended)}")
        st.write("")

        for i, meeting in enumerate(meetings_attended, 1):
            meeting_date_str = meeting["date"].strftime("%B %d, %Y")

            with st.expander(f"**Meeting #{i}** - {meeting_date_str}: {meeting['title']}", expanded=(i <= 3)):
                st.write(f"**Date:** {meeting_date_str}")
                st.write(f"**Title:** {meeting['title']}")
                st.write("")

                if meeting["req_ids"]:
                    st.write("**Requirements covered at this meeting:**")
                    for req_id in meeting["req_ids"]:
                        req_info = requirement_key[requirement_key["Req_ID"] == req_id]
                        if not req_info.empty:
                            adventure = req_info.iloc[0]["Adventure"]
                            description = req_info.iloc[0]["Requirement_Description"]
                            st.write(f"- **{req_id}** ({adventure}): {description}")
                else:
                    st.write("*No requirements recorded for this meeting*")

    st.write("---")

    # ========================================================================
    # REQUIRED ADVENTURES PROGRESS
    # ========================================================================

    st.header("✅ Required Adventures Progress")

    required_adventures = required_reqs["Adventure"].unique()

    for adventure in required_adventures:
        adventure_reqs = required_reqs[required_reqs["Adventure"] == adventure]
        completed = sum(1 for _, req in adventure_reqs.iterrows() if scout_progress.get(req["Req_ID"], False))
        total = len(adventure_reqs)
        percentage = (completed / total * 100) if total > 0 else 0

        status_icon = "✅" if completed == total else "⏳"

        with st.expander(f"{status_icon} **{adventure}** - {completed}/{total} complete ({percentage:.0f}%)",
                        expanded=(completed < total)):
            for _, req in adventure_reqs.iterrows():
                req_id = req["Req_ID"]
                is_complete = scout_progress.get(req_id, False)
                icon = "✅" if is_complete else "⬜"

                st.write(f"{icon} **{req_id}**: {req['Requirement_Description']}")

                # Show which meetings this was completed at
                if is_complete and req_id in req_completion_meetings:
                    meetings = req_completion_meetings[req_id]
                    if meetings:
                        meeting_list = ", ".join([f"{m['date'].strftime('%m/%d/%Y')}" for m in meetings])
                        st.caption(f"   Completed at: {meeting_list}")

                st.write("")

    st.write("---")

    # ========================================================================
    # ELECTIVE ADVENTURES PROGRESS
    # ========================================================================

    st.header("🌟 Elective Adventures Progress")
    st.write(f"**Need to complete:** 2 elective adventures | **Completed:** {completed_electives}")
    st.write("")

    for adventure in elective_adventures:
        adventure_reqs = elective_reqs[elective_reqs["Adventure"] == adventure]
        completed = sum(1 for _, req in adventure_reqs.iterrows() if scout_progress.get(req["Req_ID"], False))
        total = len(adventure_reqs)
        percentage = (completed / total * 100) if total > 0 else 0
        is_complete = (completed == total)

        status_icon = "✅" if is_complete else "⏳"

        with st.expander(f"{status_icon} **{adventure}** - {completed}/{total} complete ({percentage:.0f}%)",
                        expanded=False):
            for _, req in adventure_reqs.iterrows():
                req_id = req["Req_ID"]
                is_req_complete = scout_progress.get(req_id, False)
                icon = "✅" if is_req_complete else "⬜"

                st.write(f"{icon} **{req_id}**: {req['Requirement_Description']}")

                # Show which meetings this was completed at
                if is_req_complete and req_id in req_completion_meetings:
                    meetings = req_completion_meetings[req_id]
                    if meetings:
                        meeting_list = ", ".join([f"{m['date'].strftime('%m/%d/%Y')}" for m in meetings])
                        st.caption(f"   Completed at: {meeting_list}")

                st.write("")

    # ========================================================================
    # PRINT INSTRUCTIONS
    # ========================================================================

    st.write("---")
    st.info("""
    **💡 To print or save this report:**
    - Use your browser's Print function (Ctrl+P or Cmd+P)
    - Choose "Save as PDF" as the printer destination
    - Expand sections you want to include before printing
    """)

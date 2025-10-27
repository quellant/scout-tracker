"""
Meeting Reports Page

This module contains the UI for viewing detailed meeting reports,
including attendance and requirements covered.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from scout_tracker.data import load_roster, load_requirement_key, load_meetings, load_attendance
from scout_tracker.services import generate_meeting_list_pdf


def page_meeting_reports():
    """Page for viewing detailed meeting reports."""
    st.title("📋 Meeting Reports")
    st.write("View comprehensive reports for each meeting, including attendance and requirements covered.")

    # Load all data
    roster_df = load_roster()
    requirement_key = load_requirement_key()
    meetings_df = load_meetings()
    attendance_df = load_attendance()

    if meetings_df.empty:
        st.warning("⚠️ No meetings scheduled yet. Please create meetings to get started!")
        return

    # Export button at the top
    st.write("---")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📄 Export Meeting List", type="primary", use_container_width=True):
            try:
                # Generate PDF
                pdf_buffer = generate_meeting_list_pdf(
                    meetings_df=meetings_df,
                    roster_df=roster_df,
                    attendance_df=attendance_df,
                    requirement_key=requirement_key
                )

                # Generate filename with current date
                filename = f"Meeting_List_{datetime.now().strftime('%Y%m%d')}.pdf"

                # Download button
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success(f"✅ PDF generated successfully! Click the button above to download.")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")

    with col2:
        st.info("💡 Export all meetings to a PDF with one page per meeting showing attendance and requirements covered.")

    st.write("---")

    # Meeting selection
    meetings_df = meetings_df.sort_values("Meeting_Date", ascending=False).reset_index(drop=True)
    meeting_options = []
    meeting_lookup = {}

    for _, meeting in meetings_df.iterrows():
        meeting_date = pd.to_datetime(meeting["Meeting_Date"])
        option_str = f"{meeting_date.strftime('%Y-%m-%d')} - {meeting['Meeting_Title']}"
        meeting_options.append(option_str)
        meeting_lookup[option_str] = meeting

    selected_meeting_option = st.selectbox("Select a meeting:", meeting_options, key="meeting_selector")

    if not selected_meeting_option:
        return

    selected_meeting = meeting_lookup[selected_meeting_option]
    meeting_date = pd.to_datetime(selected_meeting["Meeting_Date"])
    meeting_title = selected_meeting["Meeting_Title"]

    # Get requirements covered at this meeting
    req_ids_covered = selected_meeting["Req_IDs_Covered"].split(",") if pd.notna(selected_meeting["Req_IDs_Covered"]) else []

    st.write("---")

    # ========================================================================
    # MEETING DETAILS
    # ========================================================================

    st.header(f"📅 {meeting_title}")
    st.subheader(f"Date: {meeting_date.strftime('%B %d, %Y')}")

    # ========================================================================
    # ATTENDANCE SUMMARY
    # ========================================================================

    st.write("---")
    st.header("👥 Attendance Summary")

    # Get attendance for this meeting
    meeting_attendance = attendance_df[attendance_df["Meeting_Date"] == selected_meeting["Meeting_Date"]]
    scouts_attended = meeting_attendance["Scout_Name"].tolist() if not meeting_attendance.empty else []

    # Get all scouts from roster
    all_scouts = roster_df["Scout Name"].tolist() if not roster_df.empty else []
    scouts_absent = [scout for scout in all_scouts if scout not in scouts_attended]

    # Calculate attendance percentage
    total_scouts = len(all_scouts)
    present_count = len(scouts_attended)
    absent_count = len(scouts_absent)
    attendance_percentage = (present_count / total_scouts * 100) if total_scouts > 0 else 0

    # Display attendance metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Scouts", total_scouts)

    with col2:
        st.metric("Present", present_count, f"{attendance_percentage:.0f}%")

    with col3:
        st.metric("Absent", absent_count)

    st.write("")

    # Display attendance details
    col_present, col_absent = st.columns(2)

    with col_present:
        st.subheader(f"✅ Present ({present_count})")
        if scouts_attended:
            for scout in sorted(scouts_attended):
                st.write(f"- {scout}")
        else:
            st.info("No scouts attended this meeting")

    with col_absent:
        st.subheader(f"❌ Absent ({absent_count})")
        if scouts_absent:
            for scout in sorted(scouts_absent):
                st.write(f"- {scout}")
        else:
            st.success("Perfect attendance!")

    # ========================================================================
    # REQUIREMENTS COVERED
    # ========================================================================

    st.write("---")
    st.header("📚 Requirements Covered")

    if not req_ids_covered or req_ids_covered == ['']:
        st.info("No requirements were covered at this meeting.")
    else:
        st.write(f"**Total requirements covered:** {len(req_ids_covered)}")
        st.write("")

        # Group requirements by adventure
        requirements_by_adventure = {}
        for req_id in req_ids_covered:
            req_info = requirement_key[requirement_key["Req_ID"] == req_id]
            if not req_info.empty:
                adventure = req_info.iloc[0]["Adventure"]
                description = req_info.iloc[0]["Requirement_Description"]
                required = req_info.iloc[0]["Required"]

                if adventure not in requirements_by_adventure:
                    requirements_by_adventure[adventure] = {
                        "required": required,
                        "requirements": []
                    }

                requirements_by_adventure[adventure]["requirements"].append({
                    "req_id": req_id,
                    "description": description
                })

        # Display requirements grouped by adventure
        for adventure, data in sorted(requirements_by_adventure.items()):
            adventure_type = "Required" if data["required"] else "Elective"
            badge = "🎯" if data["required"] else "⭐"

            with st.expander(f"{badge} **{adventure}** ({adventure_type}) - {len(data['requirements'])} requirement(s)", expanded=True):
                for req in data["requirements"]:
                    st.write(f"**{req['req_id']}:** {req['description']}")
                    st.write("")

    # ========================================================================
    # PROGRESS IMPACT
    # ========================================================================

    st.write("---")
    st.header("📈 Progress Impact")

    if scouts_attended and req_ids_covered and req_ids_covered != ['']:
        st.write(f"**{len(scouts_attended)} scout(s)** earned **{len(req_ids_covered)} requirement(s)** at this meeting:")
        st.write("")

        # Show which scouts earned which requirements
        for scout in sorted(scouts_attended):
            with st.expander(f"**{scout}** - {len(req_ids_covered)} requirement(s) earned"):
                for req_id in req_ids_covered:
                    req_info = requirement_key[requirement_key["Req_ID"] == req_id]
                    if not req_info.empty:
                        adventure = req_info.iloc[0]["Adventure"]
                        description = req_info.iloc[0]["Requirement_Description"]
                        st.write(f"✅ **{req_id}** ({adventure}): {description}")
                        st.write("")
    else:
        st.info("No progress was recorded at this meeting (either no attendees or no requirements covered).")

    # ========================================================================
    # PRINT INSTRUCTIONS
    # ========================================================================

    st.write("---")
    st.info("""
    **💡 To print or save this report:**
    - Use your browser's Print function (Ctrl+P or Cmd+P)
    - Choose "Save as PDF" as the printer destination
    - This will create a permanent record of the meeting
    """)

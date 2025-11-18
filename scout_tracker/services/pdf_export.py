"""
PDF Export Service

This module handles generating PDF reports for Scout Tracker data,
including meeting lists with attendance and requirements covered.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
import pandas as pd


def generate_meeting_list_pdf(meetings_df, roster_df, attendance_df, requirement_key):
    """
    Generate a PDF report with one page per meeting.

    Args:
        meetings_df: DataFrame of all meetings
        roster_df: DataFrame of all scouts
        attendance_df: DataFrame of attendance records
        requirement_key: DataFrame of all requirements

    Returns:
        BytesIO object containing the PDF data
    """
    # Create a buffer to hold the PDF
    buffer = io.BytesIO()

    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Get all scouts
    all_scouts = roster_df["Scout Name"].tolist() if not roster_df.empty else []

    # Container for all elements
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=8,
        spaceBefore=12
    )

    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=6
    )

    body_style = styles['BodyText']

    # Sort meetings by date
    meetings_df = meetings_df.sort_values("Meeting_Date", ascending=True).reset_index(drop=True)

    # Generate a page for each meeting
    for idx, meeting in meetings_df.iterrows():
        # Add title page if this is the first meeting
        if idx == 0:
            # Cover page
            elements.append(Spacer(1, 2*inch))
            cover_title = Paragraph("Scout Tracker", title_style)
            elements.append(cover_title)
            elements.append(Spacer(1, 0.3*inch))

            subtitle = Paragraph("Meeting List Report", heading_style)
            elements.append(subtitle)
            elements.append(Spacer(1, 0.2*inch))

            date_generated = Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                body_style
            )
            elements.append(date_generated)
            elements.append(Spacer(1, 0.2*inch))

            total_meetings = Paragraph(f"Total Meetings: {len(meetings_df)}", body_style)
            elements.append(total_meetings)

            elements.append(PageBreak())

        # Meeting details
        meeting_date = pd.to_datetime(meeting["Meeting_Date"])
        meeting_title = meeting["Meeting_Title"]

        # Title
        title = Paragraph(f"{meeting_title}", title_style)
        elements.append(title)

        # Date
        date_text = Paragraph(
            f"<b>Date:</b> {meeting_date.strftime('%B %d, %Y')}",
            body_style
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.2*inch))

        # ========================================================================
        # ATTENDANCE SUMMARY
        # ========================================================================

        elements.append(Paragraph("Attendance Summary", heading_style))

        # Get attendance for this meeting
        meeting_attendance = attendance_df[attendance_df["Meeting_Date"] == meeting["Meeting_Date"]]
        scouts_attended = meeting_attendance["Scout_Name"].tolist() if not meeting_attendance.empty else []
        scouts_absent = [scout for scout in all_scouts if scout not in scouts_attended]

        # Calculate attendance
        total_scouts = len(all_scouts)
        present_count = len(scouts_attended)
        absent_count = len(scouts_absent)
        attendance_percentage = (present_count / total_scouts * 100) if total_scouts > 0 else 0

        # Attendance metrics
        attendance_data = [
            ['Total Scouts', 'Present', 'Absent', 'Attendance Rate'],
            [str(total_scouts), str(present_count), str(absent_count), f'{attendance_percentage:.0f}%']
        ]

        attendance_table = Table(attendance_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))

        elements.append(attendance_table)
        elements.append(Spacer(1, 0.2*inch))

        # Present and Absent scouts
        if scouts_attended or scouts_absent:
            attendance_details = []

            # Present scouts
            present_list = "<b>Present:</b> " + ", ".join(sorted(scouts_attended)) if scouts_attended else "<b>Present:</b> None"
            attendance_details.append([Paragraph(present_list, body_style)])

            # Absent scouts
            absent_list = "<b>Absent:</b> " + ", ".join(sorted(scouts_absent)) if scouts_absent else "<b>Absent:</b> None"
            attendance_details.append([Paragraph(absent_list, body_style)])

            details_table = Table(attendance_details, colWidths=[6.5*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(details_table)
            elements.append(Spacer(1, 0.2*inch))

        # ========================================================================
        # REQUIREMENTS COVERED
        # ========================================================================

        elements.append(Paragraph("Requirements Covered", heading_style))

        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []

        if not req_ids_covered or req_ids_covered == ['']:
            no_reqs = Paragraph("<i>No requirements were covered at this meeting.</i>", body_style)
            elements.append(no_reqs)
        else:
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
                badge = "●" if data["required"] else "○"

                adventure_header = Paragraph(
                    f"{badge} <b>{adventure}</b> ({adventure_type}) - {len(data['requirements'])} requirement(s)",
                    subheading_style
                )
                elements.append(adventure_header)

                # Create table for requirements
                req_data = []
                for req in data["requirements"]:
                    req_text = f"<b>{req['req_id']}:</b> {req['description']}"
                    req_data.append([Paragraph(req_text, body_style)])

                req_table = Table(req_data, colWidths=[6.5*inch])
                req_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ]))

                elements.append(req_table)
                elements.append(Spacer(1, 0.1*inch))

        # Add page break after each meeting (except the last one)
        if idx < len(meetings_df) - 1:
            elements.append(PageBreak())

    # Build the PDF
    doc.build(elements)

    # Reset buffer position to beginning
    buffer.seek(0)

    return buffer


def generate_scout_progress_report(scout_name, roster_df, requirement_key, meetings_df, attendance_df):
    """
    Generate a PDF report focused on missed meetings and requirements to make up.

    This report helps parents understand what their scout needs to catch up on due to absences.

    Args:
        scout_name: Name of the scout
        roster_df: DataFrame of all scouts
        requirement_key: DataFrame of all requirements
        meetings_df: DataFrame of all meetings
        attendance_df: DataFrame of attendance records

    Returns:
        BytesIO object containing the PDF data
    """
    # Create a buffer to hold the PDF
    buffer = io.BytesIO()

    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for all elements
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=8,
        spaceBefore=16,
        leading=18
    )

    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=6,
        spaceBefore=10
    )

    body_style = styles['BodyText']
    body_style.leading = 14

    # ========================================================================
    # CALCULATE SCOUT PROGRESS
    # ========================================================================

    # Build master tracker for this scout
    req_ids = requirement_key["Req_ID"].tolist()
    scout_progress = {req_id: False for req_id in req_ids}

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered and meeting details
    # Separate required (non-optional) meetings for attendance tracking
    meeting_req_lookup = {}
    meeting_details = {}
    required_meeting_dates = set()

    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        is_optional = meeting.get("Optional", False)

        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered
        meeting_details[meeting["Meeting_Date"]] = {
            "title": meeting["Meeting_Title"],
            "date": pd.to_datetime(meeting["Meeting_Date"]),
            "req_ids": req_ids_covered,
            "optional": is_optional
        }

        # Track non-optional meetings for attendance calculations
        if not is_optional:
            required_meeting_dates.add(meeting["Meeting_Date"])

    # Track which requirements were completed at which meetings
    req_completion_meetings = {req_id: [] for req_id in req_ids}

    # Get meetings attended by this scout
    scout_attendance = attendance_df[attendance_df["Scout_Name"] == scout_name]
    meetings_attended_dates = set(scout_attendance["Meeting_Date"].tolist())

    # Mark requirements as completed based on attendance
    for meeting_date in meetings_attended_dates:
        if meeting_date in meeting_req_lookup:
            meeting_date_dt = pd.to_datetime(meeting_date)
            meeting_info = meeting_details.get(meeting_date, {"title": "Untitled Meeting", "req_ids": []})

            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in scout_progress:
                    scout_progress[req_id] = True
                    req_completion_meetings[req_id].append({
                        "date": meeting_date_dt,
                        "title": meeting_info["title"]
                    })

    # Calculate progress metrics
    required_reqs = requirement_key[requirement_key["Required"] == True]
    elective_reqs = requirement_key[requirement_key["Required"] == False]

    required_completed = sum(1 for req_id in required_reqs["Req_ID"] if scout_progress.get(req_id, False))
    required_total = len(required_reqs)
    required_percentage = (required_completed / required_total * 100) if required_total > 0 else 0

    # Calculate elective adventures completed
    elective_adventures = elective_reqs["Adventure"].unique()
    completed_electives = 0
    elective_progress = {}
    for adventure in elective_adventures:
        adventure_reqs = elective_reqs[elective_reqs["Adventure"] == adventure]["Req_ID"].tolist()
        completed_count = sum(1 for req_id in adventure_reqs if scout_progress.get(req_id, False))
        total_count = len(adventure_reqs)
        is_complete = all(scout_progress.get(req_id, False) for req_id in adventure_reqs)
        if is_complete:
            completed_electives += 1
        elective_progress[adventure] = {
            "completed": completed_count,
            "total": total_count,
            "is_complete": is_complete
        }

    # Check rank completion
    all_required_complete = required_completed == required_total
    rank_earned = all_required_complete and completed_electives >= 2

    # Calculate attendance (only for required/non-optional meetings)
    total_required_meetings = len(required_meeting_dates)
    required_meetings_attended = meetings_attended_dates & required_meeting_dates
    meetings_attended_count = len(required_meetings_attended)
    meetings_missed_count = total_required_meetings - meetings_attended_count
    attendance_percentage = (meetings_attended_count / total_required_meetings * 100) if total_required_meetings > 0 else 0

    # Identify missed REQUIRED meetings and their requirements
    # Optional meetings that weren't attended are NOT included as absences
    missed_meeting_dates = required_meeting_dates - meetings_attended_dates
    missed_meetings_data = []

    for meeting_date in sorted(missed_meeting_dates):
        if meeting_date in meeting_details:
            meeting_info = meeting_details[meeting_date]
            req_ids = meeting_info["req_ids"]

            # Check which requirements from this meeting are still incomplete
            incomplete_reqs = []
            for req_id in req_ids:
                if req_id and not scout_progress.get(req_id, False):
                    req_info = requirement_key[requirement_key["Req_ID"] == req_id]
                    if not req_info.empty:
                        incomplete_reqs.append({
                            "req_id": req_id,
                            "adventure": req_info.iloc[0]["Adventure"],
                            "description": req_info.iloc[0]["Requirement_Description"],
                            "required": req_info.iloc[0]["Required"]
                        })

            if incomplete_reqs:  # Only include missed meetings with incomplete requirements
                missed_meetings_data.append({
                    "date": meeting_info["date"],
                    "title": meeting_info["title"],
                    "requirements": incomplete_reqs
                })

    # ========================================================================
    # HEADER SECTION
    # ========================================================================

    elements.append(Spacer(1, 0.5*inch))

    title = Paragraph(f"Make-Up Work Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))

    scout_name_para = Paragraph(f"<b>{scout_name}</b>", heading_style)
    elements.append(scout_name_para)
    elements.append(Spacer(1, 0.05*inch))

    date_generated = Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        body_style
    )
    elements.append(date_generated)
    elements.append(Spacer(1, 0.2*inch))

    intro_text = Paragraph(
        "This report shows requirements covered at meetings your scout missed, "
        "and identifies what needs to be completed at home to stay caught up with the den.",
        body_style
    )
    elements.append(intro_text)
    elements.append(Spacer(1, 0.3*inch))

    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================

    elements.append(Paragraph("Attendance Summary", heading_style))

    attendance_note = Paragraph(
        "<i>Note: Optional meetings (special events, camps) are not included in attendance calculations.</i>",
        body_style
    )
    elements.append(attendance_note)
    elements.append(Spacer(1, 0.1*inch))

    attendance_data = [
        ['Required Meetings', 'Attended', 'Missed', 'Attendance Rate'],
        [str(total_required_meetings), str(meetings_attended_count), str(meetings_missed_count), f'{attendance_percentage:.0f}%']
    ]

    attendance_table = Table(attendance_data, colWidths=[1.625*inch, 1.625*inch, 1.625*inch, 1.625*inch])
    attendance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(attendance_table)
    elements.append(Spacer(1, 0.3*inch))

    # ========================================================================
    # MEETINGS MISSED
    # ========================================================================

    elements.append(Paragraph("Meetings Missed", heading_style))

    if not missed_meeting_dates:
        no_absences = Paragraph("<b>Perfect attendance!</b> No meetings missed.", body_style)
        no_table = Table([[no_absences]], colWidths=[6.5*inch])
        no_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d1fae5')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(no_table)
    else:
        # List each missed meeting
        for meeting_date in sorted(missed_meeting_dates):
            if meeting_date in meeting_details:
                meeting_info = meeting_details[meeting_date]
                meeting_date_str = meeting_info["date"].strftime("%B %d, %Y")
                meeting_text = f"<b>{meeting_date_str}</b> - {meeting_info['title']}"

                # Count requirements covered
                req_count = len([r for r in meeting_info["req_ids"] if r])

                if req_count > 0:
                    meeting_text += f" ({req_count} requirement{'s' if req_count != 1 else ''} covered)"

                meeting_para = Paragraph(f"• {meeting_text}", body_style)
                meeting_table = Table([[meeting_para]], colWidths=[6.5*inch])
                meeting_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
                    ('PADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ]))
                elements.append(meeting_table)
                elements.append(Spacer(1, 0.05*inch))

    elements.append(Spacer(1, 0.2*inch))

    # ========================================================================
    # OPTIONAL MEETINGS ATTENDED
    # ========================================================================

    # Show optional meetings the scout attended (special achievements)
    optional_meetings = [
        (date, meeting_details[date])
        for date in meetings_attended_dates
        if date in meeting_details and meeting_details[date].get("optional", False)
    ]

    if optional_meetings:
        elements.append(Paragraph("Optional Events Attended", heading_style))

        optional_intro = Paragraph(
            f"{scout_name} attended these special optional events:",
            body_style
        )
        elements.append(optional_intro)
        elements.append(Spacer(1, 0.1*inch))

        for meeting_date, meeting_info in sorted(optional_meetings, key=lambda x: x[0]):
            meeting_date_str = meeting_info["date"].strftime("%B %d, %Y")
            meeting_text = f"<b>{meeting_date_str}</b> - {meeting_info['title']}"

            # Show requirements earned
            req_count = len([r for r in meeting_info["req_ids"] if r])
            if req_count > 0:
                meeting_text += f" ({req_count} requirement{'s' if req_count != 1 else ''} earned)"

            meeting_para = Paragraph(f"• {meeting_text}", body_style)
            meeting_table = Table([[meeting_para]], colWidths=[6.5*inch])
            meeting_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d1fae5')),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ]))
            elements.append(meeting_table)
            elements.append(Spacer(1, 0.05*inch))

        elements.append(Spacer(1, 0.2*inch))

    # ========================================================================
    # MAKE-UP OPPORTUNITIES - REQUIREMENTS MISSED
    # ========================================================================

    elements.append(PageBreak())
    elements.append(Paragraph("Requirements to Make Up", heading_style))

    if not missed_meetings_data:
        no_makeups = Paragraph(
            "<b>Great news!</b> There are no incomplete requirements from missed meetings. "
            "Either all meetings were attended, or requirements from missed meetings were completed at other meetings.",
            body_style
        )
        elements.append(no_makeups)
    else:
        intro_text = Paragraph(
            f"<b>{scout_name}</b> missed <b>{len(missed_meetings_data)}</b> meeting(s) that covered requirements "
            "not yet completed. These can be made up at home or at future den meetings.",
            body_style
        )
        elements.append(intro_text)
        elements.append(Spacer(1, 0.15*inch))

        # Group missed requirements by adventure
        missed_by_adventure = {}
        for meeting in missed_meetings_data:
            for req in meeting["requirements"]:
                adventure = req["adventure"]
                if adventure not in missed_by_adventure:
                    missed_by_adventure[adventure] = {
                        "required": req["required"],
                        "requirements": []
                    }
                missed_by_adventure[adventure]["requirements"].append({
                    "req_id": req["req_id"],
                    "description": req["description"],
                    "meeting_date": meeting["date"],
                    "meeting_title": meeting["title"]
                })

        # Display by adventure
        for adventure, data in sorted(missed_by_adventure.items()):
            adventure_type = "Required" if data["required"] else "Elective"
            badge = "●" if data["required"] else "○"
            color = colors.HexColor('#fee2e2') if data["required"] else colors.HexColor('#fef3c7')

            adventure_header = Paragraph(
                f"{badge} <b>{adventure}</b> ({adventure_type}) - {len(data['requirements'])} requirement(s) to make up",
                subheading_style
            )
            elements.append(adventure_header)

            # Create table for requirements
            req_data = []
            for req in data["requirements"]:
                meeting_date_str = req["meeting_date"].strftime("%m/%d/%Y")
                req_text = (f"<b>{req['req_id']}:</b> {req['description']}<br/>"
                           f"<i>Missed at: {meeting_date_str} - {req['meeting_title']}</i>")
                req_data.append([Paragraph(req_text, body_style)])

            req_table = Table(req_data, colWidths=[6.5*inch])
            req_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), color),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ]))

            elements.append(req_table)
            elements.append(Spacer(1, 0.15*inch))

    # ========================================================================
    # SUMMARY
    # ========================================================================

    elements.append(Spacer(1, 0.3*inch))

    if missed_meetings_data:
        # Count requirements by type
        missed_required_reqs = []
        missed_elective_reqs = []

        for adventure, data in missed_by_adventure.items():
            if data["required"]:
                missed_required_reqs.extend(data["requirements"])
            else:
                missed_elective_reqs.extend(data["requirements"])

        summary_text = f"<b>Summary:</b> {scout_name} needs to make up "
        parts = []
        if missed_required_reqs:
            parts.append(f"{len(missed_required_reqs)} required requirement{'s' if len(missed_required_reqs) != 1 else ''}")
        if missed_elective_reqs:
            parts.append(f"{len(missed_elective_reqs)} elective requirement{'s' if len(missed_elective_reqs) != 1 else ''}")

        if parts:
            summary_text += " and ".join(parts) + " from missed meetings."
        else:
            summary_text = f"<b>Summary:</b> {scout_name} is fully caught up!"

        summary_para = Paragraph(summary_text, body_style)
        summary_table = Table([[summary_para]], colWidths=[6.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e0f2fe')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(summary_table)
    else:
        summary_text = f"<b>Excellent!</b> {scout_name} has perfect attendance and is fully caught up with the den."
        summary_para = Paragraph(summary_text, body_style)
        summary_table = Table([[summary_para]], colWidths=[6.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d1fae5')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(summary_table)

    # Build the PDF
    doc.build(elements)

    # Reset buffer position to beginning
    buffer.seek(0)

    return buffer

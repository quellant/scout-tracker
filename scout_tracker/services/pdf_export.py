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
    Generate a PDF report for the entire den showing meeting history and den progress.

    This report is designed to be sent to all den families, showing what the den
    has accomplished together without calling out individual absences.

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
    den_size = len(all_scouts)

    # Container for all elements
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
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

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        leading=14
    )

    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['BodyText'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#666666')
    )

    # Sort meetings by date
    meetings_df = meetings_df.sort_values("Meeting_Date", ascending=True).reset_index(drop=True)

    # ========================================================================
    # CALCULATE DEN-WIDE STATISTICS
    # ========================================================================

    # Get date range
    if not meetings_df.empty:
        first_meeting_date = pd.to_datetime(meetings_df.iloc[0]["Meeting_Date"])
        last_meeting_date = pd.to_datetime(meetings_df.iloc[-1]["Meeting_Date"])
        date_range_str = f"{first_meeting_date.strftime('%B %d, %Y')} - {last_meeting_date.strftime('%B %d, %Y')}"
    else:
        date_range_str = "No meetings yet"

    # Count total unique requirements covered across all meetings
    all_req_ids_covered = set()
    for _, meeting in meetings_df.iterrows():
        req_ids = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        all_req_ids_covered.update([r for r in req_ids if r])

    total_reqs_covered = len(all_req_ids_covered)
    total_reqs = len(requirement_key)

    # Count adventures worked on
    adventures_worked_on = set()
    for req_id in all_req_ids_covered:
        req_info = requirement_key[requirement_key["Req_ID"] == req_id]
        if not req_info.empty:
            adventures_worked_on.add(req_info.iloc[0]["Adventure"])

    # Get required vs elective adventures
    required_reqs = requirement_key[requirement_key["Required"] == True]
    elective_reqs = requirement_key[requirement_key["Required"] == False]
    required_adventures = set(required_reqs["Adventure"].unique())
    elective_adventures = set(elective_reqs["Adventure"].unique())

    required_adventures_worked = adventures_worked_on & required_adventures
    elective_adventures_worked = adventures_worked_on & elective_adventures

    # Calculate average scout progress
    scout_progress_list = []
    scouts_on_track = 0

    for scout in all_scouts:
        scout_reqs_completed = set()
        scout_attendance = attendance_df[attendance_df["Scout_Name"] == scout]
        scout_meetings = set(scout_attendance["Meeting_Date"].tolist())

        for meeting_date in scout_meetings:
            meeting_info = meetings_df[meetings_df["Meeting_Date"] == meeting_date]
            if not meeting_info.empty:
                req_ids = meeting_info.iloc[0]["Req_IDs_Covered"]
                if pd.notna(req_ids):
                    scout_reqs_completed.update([r for r in req_ids.split(",") if r])

        scout_progress_list.append(len(scout_reqs_completed))

        # Check if scout is on track (completed at least 50% of covered requirements)
        if len(scout_reqs_completed) >= total_reqs_covered * 0.5:
            scouts_on_track += 1

    avg_reqs_completed = sum(scout_progress_list) / den_size if den_size > 0 else 0

    # ========================================================================
    # SECTION 1: COVER PAGE
    # ========================================================================

    elements.append(Spacer(1, 1.5*inch))

    cover_title = Paragraph("Den Progress Report", title_style)
    elements.append(cover_title)

    if not meetings_df.empty:
        cover_subtitle = Paragraph(date_range_str, subtitle_style)
        elements.append(cover_subtitle)

    elements.append(Spacer(1, 0.3*inch))

    generated_text = Paragraph(
        f"Generated {datetime.now().strftime('%B %d, %Y')}",
        small_style
    )
    generated_text.alignment = TA_CENTER
    elements.append(generated_text)

    elements.append(Spacer(1, 0.5*inch))

    # Summary statistics box
    summary_data = [
        ['Den Size', 'Meetings Held', 'Requirements Covered', 'Adventures Started'],
        [str(den_size), str(len(meetings_df)), str(total_reqs_covered), str(len(adventures_worked_on))]
    ]

    summary_table = Table(summary_data, colWidths=[1.625*inch, 1.625*inch, 1.625*inch, 1.625*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f9ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 1), (-1, -1), 14),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
    ]))
    elements.append(summary_table)

    elements.append(Spacer(1, 0.5*inch))

    # Note about individual reports
    note_text = Paragraph(
        "<i>This report shows what our den has accomplished together. "
        "Individual Scout Progress Reports with personalized details are available for each family.</i>",
        body_style
    )
    note_table = Table([[note_text]], colWidths=[6.5*inch])
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e0f2fe')),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(note_table)

    elements.append(PageBreak())

    # ========================================================================
    # SECTION 2: DEN PROGRESS OVERVIEW
    # ========================================================================

    elements.append(Paragraph("Den Progress Overview", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Section description
    overview_desc = Paragraph(
        "<i>This section shows what our den has covered together at meetings. "
        "If you see an adventure marked as complete that your scout hasn't finished, don't worry! "
        "This means the den covered it at a meeting. Your scout's individual progress is tracked "
        "separately in their personalized Scout Progress Report.</i>",
        small_style
    )
    overview_desc_table = Table([[overview_desc]], colWidths=[6.5*inch])
    overview_desc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(overview_desc_table)
    elements.append(Spacer(1, 0.15*inch))

    # Progress message
    if scouts_on_track == den_size:
        progress_msg = f"<b>Excellent!</b> All {den_size} scouts are keeping pace with den activities."
        progress_color = colors.HexColor('#d1fae5')
    elif scouts_on_track >= den_size * 0.75:
        progress_msg = f"<b>Great progress!</b> {scouts_on_track} of {den_size} scouts are on track with den activities."
        progress_color = colors.HexColor('#d1fae5')
    else:
        progress_msg = f"Our den is making progress! {scouts_on_track} of {den_size} scouts have completed most covered requirements."
        progress_color = colors.HexColor('#e0f2fe')

    progress_para = Paragraph(progress_msg, body_style)
    progress_table = Table([[progress_para]], colWidths=[6.5*inch])
    progress_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), progress_color),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(progress_table)
    elements.append(Spacer(1, 0.2*inch))

    # Adventures progress
    elements.append(Paragraph("Adventures We've Worked On", heading_style))

    adventures_desc = Paragraph(
        "<i><b>COMPLETE</b> = The den covered all requirements for this adventure at meetings. "
        "<b>X/Y covered</b> = The den has worked on some requirements. "
        "<b>Not started</b> = We haven't covered this adventure yet at den meetings.</i>",
        small_style
    )
    elements.append(adventures_desc)
    elements.append(Spacer(1, 0.1*inch))

    # Required adventures
    elements.append(Paragraph("<b>Required Adventures</b> (must complete all 6 for Lion rank)", subheading_style))

    for adventure in sorted(required_adventures):
        # Count requirements completed in this adventure
        adventure_reqs = required_reqs[required_reqs["Adventure"] == adventure]["Req_ID"].tolist()
        completed_in_adventure = len(set(adventure_reqs) & all_req_ids_covered)
        total_in_adventure = len(adventure_reqs)

        if completed_in_adventure == total_in_adventure:
            status = "COMPLETE"
            bg_color = colors.HexColor('#d1fae5')
            status_color = colors.HexColor('#166534')
        elif completed_in_adventure > 0:
            status = f"{completed_in_adventure}/{total_in_adventure} covered"
            bg_color = colors.HexColor('#fef3c7')
            status_color = colors.HexColor('#92400e')
        else:
            status = "Not started"
            bg_color = colors.HexColor('#f5f5f4')
            status_color = colors.HexColor('#525252')

        adventure_text = Paragraph(f"<b>{adventure}</b>", body_style)
        status_text = Paragraph(f"<font color='{status_color.hexval()}'><b>{status}</b></font>", body_style)

        row_table = Table([[adventure_text, status_text]], colWidths=[5*inch, 1.5*inch])
        row_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(row_table)
        elements.append(Spacer(1, 0.03*inch))

    elements.append(Spacer(1, 0.15*inch))

    # Elective adventures
    elements.append(Paragraph("<b>Elective Adventures</b> (must complete any 2 for Lion rank)", subheading_style))

    for adventure in sorted(elective_adventures):
        adventure_reqs = elective_reqs[elective_reqs["Adventure"] == adventure]["Req_ID"].tolist()
        completed_in_adventure = len(set(adventure_reqs) & all_req_ids_covered)
        total_in_adventure = len(adventure_reqs)

        if completed_in_adventure == total_in_adventure:
            status = "COMPLETE"
            bg_color = colors.HexColor('#d1fae5')
            status_color = colors.HexColor('#166534')
        elif completed_in_adventure > 0:
            status = f"{completed_in_adventure}/{total_in_adventure} covered"
            bg_color = colors.HexColor('#fef3c7')
            status_color = colors.HexColor('#92400e')
        else:
            status = "Not started"
            bg_color = colors.HexColor('#f5f5f4')
            status_color = colors.HexColor('#525252')

        adventure_text = Paragraph(f"<b>{adventure}</b>", body_style)
        status_text = Paragraph(f"<font color='{status_color.hexval()}'><b>{status}</b></font>", body_style)

        row_table = Table([[adventure_text, status_text]], colWidths=[5*inch, 1.5*inch])
        row_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(row_table)
        elements.append(Spacer(1, 0.03*inch))

    elements.append(PageBreak())

    # ========================================================================
    # SECTION 3: MEETING PAGES
    # ========================================================================

    elements.append(Paragraph("Meeting History", title_style))
    elements.append(Spacer(1, 0.1*inch))

    # Section description
    meeting_history_desc = Paragraph(
        "<i>This section lists each den meeting, who attended, and what requirements were covered. "
        "Use this to verify your scout's attendance was recorded correctly. If your scout attended "
        "a meeting but isn't listed, please let your den leader know so we can update the records.</i>",
        small_style
    )
    meeting_desc_table = Table([[meeting_history_desc]], colWidths=[6.5*inch])
    meeting_desc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(meeting_desc_table)
    elements.append(Spacer(1, 0.2*inch))

    for idx, meeting in meetings_df.iterrows():
        meeting_date = pd.to_datetime(meeting["Meeting_Date"])
        meeting_title = meeting["Meeting_Title"]
        is_optional = meeting.get("Optional", False)

        # Meeting header
        optional_tag = " (Optional Event)" if is_optional else ""
        meeting_header = Paragraph(
            f"<b>{meeting_title}</b>{optional_tag}",
            heading_style
        )
        elements.append(meeting_header)

        date_text = Paragraph(
            f"{meeting_date.strftime('%B %d, %Y')}",
            body_style
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.1*inch))

        # Get attendance for this meeting
        meeting_attendance = attendance_df[attendance_df["Meeting_Date"] == meeting["Meeting_Date"]]
        scouts_attended = meeting_attendance["Scout_Name"].tolist() if not meeting_attendance.empty else []

        # Attendance - show who attended (no absent list)
        present_count = len(scouts_attended)

        attendance_text = f"<b>Attended ({present_count} of {den_size}):</b> "
        if scouts_attended:
            attendance_text += ", ".join(sorted(scouts_attended))
        else:
            attendance_text += "None recorded"

        attendance_para = Paragraph(attendance_text, body_style)
        attendance_table = Table([[attendance_para]], colWidths=[6.5*inch])
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(attendance_table)
        elements.append(Spacer(1, 0.1*inch))

        # Requirements covered
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        req_ids_covered = [r for r in req_ids_covered if r]  # Filter empty strings

        if not req_ids_covered:
            reqs_text = Paragraph("<i>No requirements covered at this meeting.</i>", body_style)
            elements.append(reqs_text)
        else:
            # Group by adventure and include URL
            requirements_by_adventure = {}
            for req_id in req_ids_covered:
                req_info = requirement_key[requirement_key["Req_ID"] == req_id]
                if not req_info.empty:
                    adventure = req_info.iloc[0]["Adventure"]
                    description = req_info.iloc[0]["Requirement_Description"]
                    required = req_info.iloc[0]["Required"]
                    url = req_info.iloc[0].get("URL", "")

                    if adventure not in requirements_by_adventure:
                        requirements_by_adventure[adventure] = {
                            "required": required,
                            "url": url,
                            "requirements": []
                        }

                    requirements_by_adventure[adventure]["requirements"].append({
                        "req_id": req_id,
                        "description": description
                    })

            reqs_label = Paragraph(f"<b>Requirements Covered ({len(req_ids_covered)}):</b>", body_style)
            elements.append(reqs_label)

            for adventure, data in sorted(requirements_by_adventure.items()):
                adventure_type = "Required" if data["required"] else "Elective"
                url = data.get("url", "")

                if url:
                    adventure_header = Paragraph(
                        f"• <b>{adventure}</b> ({adventure_type}) - "
                        f"<a href='{url}' color='blue'>View on BSA Website</a>",
                        body_style
                    )
                else:
                    adventure_header = Paragraph(
                        f"• <b>{adventure}</b> ({adventure_type})",
                        body_style
                    )

                req_rows = [[adventure_header]]
                for req in data["requirements"]:
                    req_text = f"    ○ {req['req_id']}: {req['description']}"
                    req_rows.append([Paragraph(req_text, small_style)])

                req_table = Table(req_rows, colWidths=[6.5*inch])
                req_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
                    ('PADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (0, 0), 6),
                ]))
                elements.append(req_table)

        elements.append(Spacer(1, 0.2*inch))

        # Add a subtle separator between meetings (not a page break)
        if idx < len(meetings_df) - 1:
            separator = Table([['']], colWidths=[6.5*inch])
            separator.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#e5e7eb')),
            ]))
            elements.append(separator)
            elements.append(Spacer(1, 0.1*inch))

    elements.append(PageBreak())

    # ========================================================================
    # SECTION 4: CUMULATIVE SUMMARY
    # ========================================================================

    elements.append(Paragraph("Cumulative Progress", title_style))
    elements.append(Spacer(1, 0.1*inch))

    # Section description
    cumulative_desc = Paragraph(
        "<i>This summary shows all requirements our den has covered across all meetings to date. "
        "This represents the den's collective progress - your scout earns credit for requirements "
        "covered at meetings they attended. See your individual Scout Progress Report for your "
        "scout's personal completion status.</i>",
        small_style
    )
    cumulative_desc_table = Table([[cumulative_desc]], colWidths=[6.5*inch])
    cumulative_desc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(cumulative_desc_table)
    elements.append(Spacer(1, 0.15*inch))

    # All requirements covered
    elements.append(Paragraph("All Requirements Covered to Date", heading_style))

    if all_req_ids_covered:
        # Group by adventure
        cumulative_by_adventure = {}
        for req_id in sorted(all_req_ids_covered):
            req_info = requirement_key[requirement_key["Req_ID"] == req_id]
            if not req_info.empty:
                adventure = req_info.iloc[0]["Adventure"]
                if adventure not in cumulative_by_adventure:
                    cumulative_by_adventure[adventure] = []
                cumulative_by_adventure[adventure].append(req_id)

        cumulative_text = f"Our den has covered <b>{total_reqs_covered} of {total_reqs}</b> total requirements across <b>{len(cumulative_by_adventure)}</b> adventures."
        cumulative_para = Paragraph(cumulative_text, body_style)
        elements.append(cumulative_para)
        elements.append(Spacer(1, 0.1*inch))

        # List adventures and requirement counts
        for adventure in sorted(cumulative_by_adventure.keys()):
            req_ids = cumulative_by_adventure[adventure]
            adventure_total = len(requirement_key[requirement_key["Adventure"] == adventure])
            adv_text = f"• <b>{adventure}</b>: {len(req_ids)} of {adventure_total} requirements"
            elements.append(Paragraph(adv_text, body_style))

    else:
        no_reqs = Paragraph("<i>No requirements have been covered yet.</i>", body_style)
        elements.append(no_reqs)

    elements.append(Spacer(1, 0.3*inch))

    # ========================================================================
    # SECTION 5: CLOSING MESSAGE
    # ========================================================================

    closing_text = (
        "<b>Thank you for being part of our den!</b><br/><br/>"
        "This report shows what we've accomplished together as a group. "
        "For detailed information about your scout's individual progress, including any activities "
        "that can be completed at home, please see your personalized <b>Scout Progress Report</b>.<br/><br/>"
        "If you have any questions about your scout's progress or upcoming den activities, "
        "please don't hesitate to reach out to your den leader."
    )

    closing_para = Paragraph(closing_text, body_style)
    closing_table = Table([[closing_para]], colWidths=[6.5*inch])
    closing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e0f2fe')),
        ('PADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(closing_table)

    elements.append(Spacer(1, 0.3*inch))

    # Footer
    footer_text = Paragraph(
        f"<i>Report generated {datetime.now().strftime('%B %d, %Y')}</i>",
        small_style
    )
    footer_text.alignment = TA_CENTER
    elements.append(footer_text)

    # Build the PDF
    doc.build(elements)

    # Reset buffer position to beginning
    buffer.seek(0)

    return buffer


def generate_scout_progress_report(scout_name, roster_df, requirement_key, meetings_df, attendance_df):
    """
    Generate a PDF progress report for a scout to send to parents.

    This report shows the scout's progress toward their Lion rank, how they compare
    to the den average, and what activities they can complete at home to catch up.
    The report is framed positively to inform parents without making them feel bad.

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
        fontSize=22,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        alignment=TA_CENTER
    )

    scout_name_style = ParagraphStyle(
        'ScoutName',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c5aa0'),
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

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        leading=14
    )

    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['BodyText'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#666666')
    )

    # ========================================================================
    # CALCULATE SCOUT PROGRESS
    # ========================================================================

    # Build master tracker for this scout
    req_ids = requirement_key["Req_ID"].tolist()
    scout_progress = {req_id: False for req_id in req_ids}

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered and meeting details
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

        if not is_optional:
            required_meeting_dates.add(meeting["Meeting_Date"])

    # Get meetings attended by this scout
    scout_attendance = attendance_df[attendance_df["Scout_Name"] == scout_name]
    meetings_attended_dates = set(scout_attendance["Meeting_Date"].tolist())

    # Mark requirements as completed based on attendance
    for meeting_date in meetings_attended_dates:
        if meeting_date in meeting_req_lookup:
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in scout_progress:
                    scout_progress[req_id] = True

    # Calculate progress metrics
    required_reqs = requirement_key[requirement_key["Required"] == True]
    elective_reqs = requirement_key[requirement_key["Required"] == False]

    # Get unique adventures
    required_adventures = required_reqs["Adventure"].unique()
    elective_adventures = elective_reqs["Adventure"].unique()

    # Calculate adventure completion for this scout
    def calc_adventure_progress(adventure, reqs_df, progress_dict):
        adventure_reqs = reqs_df[reqs_df["Adventure"] == adventure]["Req_ID"].tolist()
        completed = sum(1 for req_id in adventure_reqs if progress_dict.get(req_id, False))
        total = len(adventure_reqs)
        return completed, total, completed == total

    scout_required_adventures_complete = 0
    scout_adventure_progress = {}
    for adventure in required_adventures:
        completed, total, is_complete = calc_adventure_progress(adventure, required_reqs, scout_progress)
        scout_adventure_progress[adventure] = {"completed": completed, "total": total, "is_complete": is_complete, "required": True}
        if is_complete:
            scout_required_adventures_complete += 1

    scout_elective_adventures_complete = 0
    for adventure in elective_adventures:
        completed, total, is_complete = calc_adventure_progress(adventure, elective_reqs, scout_progress)
        scout_adventure_progress[adventure] = {"completed": completed, "total": total, "is_complete": is_complete, "required": False}
        if is_complete:
            scout_elective_adventures_complete += 1

    # Total requirements completed
    scout_total_reqs_completed = sum(1 for v in scout_progress.values() if v)
    total_reqs = len(req_ids)

    # Check rank completion
    rank_earned = scout_required_adventures_complete == len(required_adventures) and scout_elective_adventures_complete >= 2

    # ========================================================================
    # CALCULATE DEN AVERAGES FOR COMPARISON
    # ========================================================================

    all_scouts = roster_df["Scout Name"].tolist()
    den_size = len(all_scouts)

    # Calculate progress for each scout in den
    den_required_adventures_complete = []
    den_elective_adventures_complete = []
    den_total_reqs_completed = []

    for other_scout in all_scouts:
        other_progress = {req_id: False for req_id in req_ids}
        other_attendance = attendance_df[attendance_df["Scout_Name"] == other_scout]
        other_meetings = set(other_attendance["Meeting_Date"].tolist())

        for meeting_date in other_meetings:
            if meeting_date in meeting_req_lookup:
                for req_id in meeting_req_lookup[meeting_date]:
                    if req_id in other_progress:
                        other_progress[req_id] = True

        # Count completed adventures
        required_complete = 0
        for adventure in required_adventures:
            _, _, is_complete = calc_adventure_progress(adventure, required_reqs, other_progress)
            if is_complete:
                required_complete += 1

        elective_complete = 0
        for adventure in elective_adventures:
            _, _, is_complete = calc_adventure_progress(adventure, elective_reqs, other_progress)
            if is_complete:
                elective_complete += 1

        den_required_adventures_complete.append(required_complete)
        den_elective_adventures_complete.append(elective_complete)
        den_total_reqs_completed.append(sum(1 for v in other_progress.values() if v))

    # Calculate den averages
    den_avg_required = sum(den_required_adventures_complete) / den_size if den_size > 0 else 0
    den_avg_elective = sum(den_elective_adventures_complete) / den_size if den_size > 0 else 0
    den_avg_reqs = sum(den_total_reqs_completed) / den_size if den_size > 0 else 0

    # ========================================================================
    # IDENTIFY MISSED MEETINGS AND WHAT WAS COVERED
    # ========================================================================

    missed_meeting_dates = required_meeting_dates - meetings_attended_dates
    missed_meetings_info = []

    for meeting_date in sorted(missed_meeting_dates):
        if meeting_date in meeting_details:
            meeting_info = meeting_details[meeting_date]
            req_ids_at_meeting = meeting_info["req_ids"]

            # Get all requirements covered at this meeting (not just incomplete ones)
            reqs_covered = []
            for req_id in req_ids_at_meeting:
                if req_id:
                    req_info = requirement_key[requirement_key["Req_ID"] == req_id]
                    if not req_info.empty:
                        reqs_covered.append({
                            "req_id": req_id,
                            "adventure": req_info.iloc[0]["Adventure"],
                            "description": req_info.iloc[0]["Requirement_Description"],
                            "required": req_info.iloc[0]["Required"],
                            "completed_elsewhere": scout_progress.get(req_id, False),
                            "url": req_info.iloc[0].get("URL", "")
                        })

            if reqs_covered:
                missed_meetings_info.append({
                    "date": meeting_info["date"],
                    "title": meeting_info["title"],
                    "requirements": reqs_covered
                })

    # Build list of incomplete requirements for "Opportunities" section
    incomplete_reqs_by_adventure = {}
    for meeting in missed_meetings_info:
        for req in meeting["requirements"]:
            if not req["completed_elsewhere"]:
                adventure = req["adventure"]
                if adventure not in incomplete_reqs_by_adventure:
                    incomplete_reqs_by_adventure[adventure] = {
                        "required": req["required"],
                        "requirements": []
                    }
                # Avoid duplicates
                if not any(r["req_id"] == req["req_id"] for r in incomplete_reqs_by_adventure[adventure]["requirements"]):
                    incomplete_reqs_by_adventure[adventure]["requirements"].append(req)

    # ========================================================================
    # SECTION 1: HEADER
    # ========================================================================

    elements.append(Spacer(1, 0.3*inch))

    title = Paragraph("Scout Progress Report", title_style)
    elements.append(title)

    scout_name_para = Paragraph(f"{scout_name}", scout_name_style)
    elements.append(scout_name_para)

    date_generated = Paragraph(
        f"Generated {datetime.now().strftime('%B %d, %Y')}",
        small_style
    )
    date_generated.alignment = TA_CENTER
    elements.append(date_generated)
    elements.append(Spacer(1, 0.3*inch))

    # ========================================================================
    # SECTION 2: PROGRESS SUMMARY
    # ========================================================================

    elements.append(Paragraph("Progress Summary", heading_style))

    # Rank status message
    if rank_earned:
        rank_message = f"<b>Congratulations!</b> {scout_name} has earned their Lion rank!"
        rank_color = colors.HexColor('#d1fae5')
    else:
        remaining_required = len(required_adventures) - scout_required_adventures_complete
        remaining_elective = max(0, 2 - scout_elective_adventures_complete)

        if remaining_required == 0 and remaining_elective == 0:
            rank_message = f"<b>Almost there!</b> {scout_name} has completed all requirements for their Lion rank!"
            rank_color = colors.HexColor('#d1fae5')
        else:
            parts = []
            if remaining_required > 0:
                parts.append(f"{remaining_required} required adventure{'s' if remaining_required != 1 else ''}")
            if remaining_elective > 0:
                parts.append(f"{remaining_elective} elective adventure{'s' if remaining_elective != 1 else ''}")
            rank_message = f"{scout_name} needs to complete {' and '.join(parts)} to earn their Lion rank."
            rank_color = colors.HexColor('#e0f2fe')

    rank_para = Paragraph(rank_message, body_style)
    rank_table = Table([[rank_para]], colWidths=[6.5*inch])
    rank_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), rank_color),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(rank_table)
    elements.append(Spacer(1, 0.2*inch))

    # Progress metrics table
    progress_data = [
        ['', 'Completed', 'Total'],
        ['Required Adventures', str(scout_required_adventures_complete), str(len(required_adventures))],
        ['Elective Adventures', str(scout_elective_adventures_complete), '2 needed'],
        ['Total Requirements', str(scout_total_reqs_completed), str(total_reqs)],
    ]

    progress_table = Table(progress_data, colWidths=[3.25*inch, 1.625*inch, 1.625*inch])
    progress_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f9ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 1), (0, -1), 10),
    ]))
    elements.append(progress_table)
    elements.append(Spacer(1, 0.15*inch))

    # ========================================================================
    # SECTION 3: DEN COMPARISON
    # ========================================================================

    elements.append(Paragraph("How Your Scout Compares to the Den", heading_style))

    comparison_intro = Paragraph(
        f"Your den has {den_size} scouts. Here's how {scout_name} compares to the den average:",
        body_style
    )
    elements.append(comparison_intro)
    elements.append(Spacer(1, 0.1*inch))

    # Comparison table
    comparison_data = [
        ['', f'{scout_name}', 'Den Average'],
        ['Required Adventures Complete', str(scout_required_adventures_complete), f'{den_avg_required:.1f}'],
        ['Elective Adventures Complete', str(scout_elective_adventures_complete), f'{den_avg_elective:.1f}'],
        ['Total Requirements Complete', str(scout_total_reqs_completed), f'{den_avg_reqs:.0f}'],
    ]

    comparison_table = Table(comparison_data, colWidths=[3.25*inch, 1.625*inch, 1.625*inch])
    comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 1), (0, -1), 10),
    ]))
    elements.append(comparison_table)
    elements.append(Spacer(1, 0.1*inch))

    # Contextual message based on comparison
    if scout_total_reqs_completed >= den_avg_reqs:
        context_msg = f"{scout_name} is keeping pace with or ahead of the den. Great work!"
        context_color = colors.HexColor('#d1fae5')
    else:
        diff = den_avg_reqs - scout_total_reqs_completed
        context_msg = f"{scout_name} is about {diff:.0f} requirement{'s' if diff != 1 else ''} behind the den average. The activities below can help catch up."
        context_color = colors.HexColor('#fef3c7')

    context_para = Paragraph(context_msg, body_style)
    context_table = Table([[context_para]], colWidths=[6.5*inch])
    context_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), context_color),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(context_table)

    # ========================================================================
    # SECTION 4: ADVENTURE PROGRESS (Page 2)
    # ========================================================================

    elements.append(PageBreak())
    elements.append(Paragraph("Adventure Progress", heading_style))

    # Required Adventures
    elements.append(Paragraph("<b>Required Adventures</b> (must complete all 6)", subheading_style))

    for adventure in sorted(required_adventures):
        progress = scout_adventure_progress[adventure]
        completed = progress["completed"]
        total = progress["total"]
        is_complete = progress["is_complete"]

        if is_complete:
            status = "COMPLETE"
            bg_color = colors.HexColor('#d1fae5')
            status_color = colors.HexColor('#166534')
        elif completed > 0:
            status = f"{completed}/{total}"
            bg_color = colors.HexColor('#fef3c7')
            status_color = colors.HexColor('#92400e')
        else:
            status = "Not Started"
            bg_color = colors.HexColor('#f5f5f4')
            status_color = colors.HexColor('#525252')

        adventure_text = Paragraph(f"<b>{adventure}</b>", body_style)
        status_text = Paragraph(f"<font color='{status_color.hexval()}'><b>{status}</b></font>", body_style)

        row_table = Table([[adventure_text, status_text]], colWidths=[5*inch, 1.5*inch])
        row_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(row_table)
        elements.append(Spacer(1, 0.03*inch))

    elements.append(Spacer(1, 0.15*inch))

    # Elective Adventures
    elements.append(Paragraph("<b>Elective Adventures</b> (must complete any 2)", subheading_style))

    for adventure in sorted(elective_adventures):
        progress = scout_adventure_progress[adventure]
        completed = progress["completed"]
        total = progress["total"]
        is_complete = progress["is_complete"]

        if is_complete:
            status = "COMPLETE"
            bg_color = colors.HexColor('#d1fae5')
            status_color = colors.HexColor('#166534')
        elif completed > 0:
            status = f"{completed}/{total}"
            bg_color = colors.HexColor('#fef3c7')
            status_color = colors.HexColor('#92400e')
        else:
            status = "Not Started"
            bg_color = colors.HexColor('#f5f5f4')
            status_color = colors.HexColor('#525252')

        adventure_text = Paragraph(f"<b>{adventure}</b>", body_style)
        status_text = Paragraph(f"<font color='{status_color.hexval()}'><b>{status}</b></font>", body_style)

        row_table = Table([[adventure_text, status_text]], colWidths=[5*inch, 1.5*inch])
        row_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(row_table)
        elements.append(Spacer(1, 0.03*inch))

    # ========================================================================
    # SECTION 5: WHAT THE DEN COVERED
    # ========================================================================

    if missed_meetings_info:
        elements.append(PageBreak())
        elements.append(Paragraph("What the Den Covered", heading_style))

        intro_text = Paragraph(
            f"The following requirements were covered at den meetings while {scout_name} was away. "
            "Requirements marked with a checkmark were completed at other meetings.",
            body_style
        )
        elements.append(intro_text)
        elements.append(Spacer(1, 0.15*inch))

        for meeting in missed_meetings_info:
            meeting_date_str = meeting["date"].strftime("%B %d, %Y")
            meeting_header = Paragraph(
                f"<b>{meeting_date_str}</b> - {meeting['title']}",
                subheading_style
            )
            elements.append(meeting_header)

            # List requirements covered
            req_rows = []
            for req in meeting["requirements"]:
                if req["completed_elsewhere"]:
                    check = "✓"
                    note = " (completed at another meeting)"
                    text_color = colors.HexColor('#166534')
                else:
                    check = "○"
                    note = ""
                    text_color = colors.HexColor('#525252')

                req_text = f"<font color='{text_color.hexval()}'>{check} <b>{req['req_id']}</b>: {req['description']}{note}</font>"
                req_rows.append([Paragraph(req_text, body_style)])

            req_table = Table(req_rows, colWidths=[6.5*inch])
            req_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(req_table)
            elements.append(Spacer(1, 0.15*inch))

    # ========================================================================
    # SECTION 6: OPPORTUNITIES TO COMPLETE AT HOME
    # ========================================================================

    if incomplete_reqs_by_adventure:
        elements.append(Paragraph("Activities to Complete at Home", heading_style))

        intro_text = Paragraph(
            "These requirements can be completed at home with a parent or adult partner. "
            "Click the links to view detailed instructions on the BSA website.",
            body_style
        )
        elements.append(intro_text)
        elements.append(Spacer(1, 0.15*inch))

        # Group by required vs elective
        required_incomplete = {k: v for k, v in incomplete_reqs_by_adventure.items() if v["required"]}
        elective_incomplete = {k: v for k, v in incomplete_reqs_by_adventure.items() if not v["required"]}

        if required_incomplete:
            elements.append(Paragraph("<b>From Required Adventures:</b>", subheading_style))

            for adventure, data in sorted(required_incomplete.items()):
                # Get URL for adventure
                adventure_url = data["requirements"][0].get("url", "") if data["requirements"] else ""

                if adventure_url:
                    adventure_header = Paragraph(
                        f"<b>{adventure}</b> - <a href='{adventure_url}' color='blue'>View on BSA Website</a>",
                        body_style
                    )
                else:
                    adventure_header = Paragraph(f"<b>{adventure}</b>", body_style)

                elements.append(adventure_header)

                req_rows = []
                for req in data["requirements"]:
                    req_text = f"• <b>{req['req_id']}</b>: {req['description']}"
                    req_rows.append([Paragraph(req_text, body_style)])

                req_table = Table(req_rows, colWidths=[6.5*inch])
                req_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef2f2')),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ]))
                elements.append(req_table)
                elements.append(Spacer(1, 0.1*inch))

        if elective_incomplete:
            elements.append(Paragraph("<b>From Elective Adventures:</b>", subheading_style))

            for adventure, data in sorted(elective_incomplete.items()):
                adventure_url = data["requirements"][0].get("url", "") if data["requirements"] else ""

                if adventure_url:
                    adventure_header = Paragraph(
                        f"<b>{adventure}</b> - <a href='{adventure_url}' color='blue'>View on BSA Website</a>",
                        body_style
                    )
                else:
                    adventure_header = Paragraph(f"<b>{adventure}</b>", body_style)

                elements.append(adventure_header)

                req_rows = []
                for req in data["requirements"]:
                    req_text = f"• <b>{req['req_id']}</b>: {req['description']}"
                    req_rows.append([Paragraph(req_text, body_style)])

                req_table = Table(req_rows, colWidths=[6.5*inch])
                req_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffbeb')),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ]))
                elements.append(req_table)
                elements.append(Spacer(1, 0.1*inch))

    # ========================================================================
    # SECTION 7: POSITIVE CLOSING
    # ========================================================================

    elements.append(Spacer(1, 0.3*inch))

    # Encouraging closing message
    if rank_earned:
        closing_text = (
            f"<b>Congratulations!</b> {scout_name} has earned their Lion rank! "
            "Thank you for your support in helping your scout achieve this milestone. "
            "Keep up the great work!"
        )
        closing_color = colors.HexColor('#d1fae5')
    elif scout_total_reqs_completed >= den_avg_reqs:
        closing_text = (
            f"<b>Great progress!</b> {scout_name} is doing well and keeping up with the den. "
            "Thank you for supporting your scout's Cub Scout journey. "
            "We look forward to seeing you at our next den meeting!"
        )
        closing_color = colors.HexColor('#d1fae5')
    else:
        closing_text = (
            f"<b>Thank you</b> for being part of our den! Every scout progresses at their own pace, "
            f"and {scout_name} is making great strides. The activities listed above can be completed "
            "at home whenever it's convenient for your family. We're here to help!"
        )
        closing_color = colors.HexColor('#e0f2fe')

    closing_para = Paragraph(closing_text, body_style)
    closing_table = Table([[closing_para]], colWidths=[6.5*inch])
    closing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), closing_color),
        ('PADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(closing_table)

    elements.append(Spacer(1, 0.2*inch))

    # Footer with contact info placeholder
    footer_text = Paragraph(
        "<i>Questions? Contact your den leader for more information.</i>",
        small_style
    )
    footer_text.alignment = TA_CENTER
    elements.append(footer_text)

    # Build the PDF
    doc.build(elements)

    # Reset buffer position to beginning
    buffer.seek(0)

    return buffer

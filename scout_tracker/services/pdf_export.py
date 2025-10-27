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

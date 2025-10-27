"""
Scout Tracker Services Package

This package contains business logic for advancement tracking including:
- Advancement calculations and progress tracking
- Report generation (PDF exports)
- Requirement completion validation
- Statistical analysis

Modules:
    pdf_export: PDF report generation services
    advancement: Core advancement tracking logic (to be implemented)
    analytics: Statistical analysis and insights (to be implemented)

Exports:
    generate_meeting_list_pdf(): Generate PDF report of all meetings
"""

from scout_tracker.services.pdf_export import generate_meeting_list_pdf

__all__ = ['generate_meeting_list_pdf']

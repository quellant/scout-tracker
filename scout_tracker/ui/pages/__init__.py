"""
Scout Tracker UI Pages Subpackage

This subpackage contains individual page components for the Scout Tracker application.

Available pages:
    roster: Roster management
    requirements: Requirements management (CRUD)
    meetings: Meeting creation and management
    attendance: Meeting attendance logging
    dashboard: Main tracking dashboard
    plan_meetings: Meeting planning based on requirement completion
    individual_reports: Individual scout progress reports
    onboarding: First-time user onboarding flow

Each page module exports page functions that create the Streamlit UI for that page.
"""

from scout_tracker.ui.pages.roster import page_manage_roster
from scout_tracker.ui.pages.requirements import page_manage_requirements
from scout_tracker.ui.pages.meetings import page_manage_meetings
from scout_tracker.ui.pages.attendance import page_log_attendance
from scout_tracker.ui.pages.dashboard import page_tracker_dashboard
from scout_tracker.ui.pages.plan_meetings import page_plan_meetings
from scout_tracker.ui.pages.individual_reports import page_individual_scout_reports
from scout_tracker.ui.pages.meeting_reports import page_meeting_reports
from scout_tracker.ui.pages.onboarding import is_first_run, page_onboarding

__all__ = [
    'page_manage_roster',
    'page_manage_requirements',
    'page_manage_meetings',
    'page_log_attendance',
    'page_tracker_dashboard',
    'page_plan_meetings',
    'page_individual_scout_reports',
    'page_meeting_reports',
    'is_first_run',
    'page_onboarding',
]

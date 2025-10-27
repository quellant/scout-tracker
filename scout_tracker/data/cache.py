"""
Cache Management Module

This module handles Streamlit cache invalidation for the Scout Tracker application.
Provides utilities to clear cached data after modifications to ensure fresh data is loaded.
"""


def clear_cache():
    """Clear all cached data after modifications."""
    # Import at runtime to avoid circular import
    from .io import load_roster, load_requirement_key, load_meetings, load_attendance

    load_roster.clear()
    load_requirement_key.clear()
    load_meetings.clear()
    load_attendance.clear()

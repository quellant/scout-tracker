"""
Data Layer Module

This module provides the data access layer for the Scout Tracker application.
Exports all data I/O and cache management functions.
"""

from .io import (
    initialize_data_files,
    load_roster,
    load_requirement_key,
    load_meetings,
    load_attendance,
    save_roster,
    save_requirements,
    save_meetings,
    save_attendance,
)
from .cache import clear_cache

__all__ = [
    "initialize_data_files",
    "load_roster",
    "load_requirement_key",
    "load_meetings",
    "load_attendance",
    "save_roster",
    "save_requirements",
    "save_meetings",
    "save_attendance",
    "clear_cache",
]

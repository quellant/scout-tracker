"""
Data I/O Module

This module handles all file input/output operations for the Scout Tracker application.
Includes functions for loading and saving roster, requirements, meetings, and attendance data.
All load functions use Streamlit's caching mechanism for performance optimization.
"""

import streamlit as st
import pandas as pd
from scout_tracker import config


def initialize_data_files():
    """Create the data directory and initialize all CSV files if they don't exist."""

    # Create data directory
    config.DATA_DIR.mkdir(exist_ok=True)

    # Initialize Roster.csv
    if not config.ROSTER_FILE.exists():
        df = pd.DataFrame(columns=["Scout Name"])
        df.to_csv(config.ROSTER_FILE, index=False)

    # Initialize Requirement_Key.csv with default BSA requirements
    # This file can be edited by users through the "Manage Requirements" page
    if not config.REQUIREMENT_KEY_FILE.exists():
        df = pd.DataFrame(config.LION_REQUIREMENTS)
        df.to_csv(config.REQUIREMENT_KEY_FILE, index=False)

    # Initialize Meetings.csv
    if not config.MEETINGS_FILE.exists():
        df = pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered", "Optional"])
        df.to_csv(config.MEETINGS_FILE, index=False)

    # Initialize Meeting_Attendance.csv
    if not config.ATTENDANCE_FILE.exists():
        df = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])
        df.to_csv(config.ATTENDANCE_FILE, index=False)


@st.cache_data
def load_roster():
    """Load the roster CSV file, sorted alphabetically by Scout Name (case-insensitive)."""
    if config.ROSTER_FILE.exists():
        df = pd.read_csv(config.ROSTER_FILE)
        if not df.empty and "Scout Name" in df.columns:
            df = df.sort_values("Scout Name", key=lambda x: x.str.lower()).reset_index(drop=True)
        return df
    return pd.DataFrame(columns=["Scout Name"])


@st.cache_data
def load_requirement_key():
    """Load the requirement key CSV file."""
    if config.REQUIREMENT_KEY_FILE.exists():
        df = pd.read_csv(config.REQUIREMENT_KEY_FILE)
        return df
    return pd.DataFrame(columns=["Req_ID", "Adventure", "Requirement_Description", "Required"])


@st.cache_data
def load_meetings():
    """Load the meetings CSV file."""
    if config.MEETINGS_FILE.exists():
        df = pd.read_csv(config.MEETINGS_FILE)
        if not df.empty:
            df["Meeting_Date"] = pd.to_datetime(df["Meeting_Date"])
            # Add Optional column if it doesn't exist (backwards compatibility)
            if "Optional" not in df.columns:
                df["Optional"] = False
        return df
    return pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered", "Optional"])


@st.cache_data
def load_attendance():
    """Load the attendance CSV file."""
    if config.ATTENDANCE_FILE.exists():
        df = pd.read_csv(config.ATTENDANCE_FILE)
        if not df.empty:
            df["Meeting_Date"] = pd.to_datetime(df["Meeting_Date"])
        return df
    return pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])


def save_roster(df):
    """Save the roster dataframe to CSV, sorted alphabetically by Scout Name (case-insensitive)."""
    # Import at runtime to avoid circular import
    from .cache import clear_cache

    # Sort by Scout Name before saving (case-insensitive)
    df_to_save = df.copy()
    if not df_to_save.empty and "Scout Name" in df_to_save.columns:
        df_to_save = df_to_save.sort_values("Scout Name", key=lambda x: x.str.lower()).reset_index(drop=True)

    df_to_save.to_csv(config.ROSTER_FILE, index=False)
    clear_cache()


def save_requirements(df):
    """Save the requirements dataframe to CSV."""
    # Import at runtime to avoid circular import
    from .cache import clear_cache

    df.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    clear_cache()


def save_meetings(df):
    """Save the meetings dataframe to CSV."""
    # Import at runtime to avoid circular import
    from .cache import clear_cache

    df_to_save = df.copy()
    if not df_to_save.empty:
        # Convert to datetime first, then format as string
        df_to_save["Meeting_Date"] = pd.to_datetime(df_to_save["Meeting_Date"]).dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(config.MEETINGS_FILE, index=False)
    clear_cache()


def save_attendance(df):
    """Save the attendance dataframe to CSV."""
    # Import at runtime to avoid circular import
    from .cache import clear_cache

    df_to_save = df.copy()
    if not df_to_save.empty:
        # Convert to datetime first, then format as string
        df_to_save["Meeting_Date"] = pd.to_datetime(df_to_save["Meeting_Date"]).dt.strftime("%Y-%m-%d")
    df_to_save.to_csv(config.ATTENDANCE_FILE, index=False)
    clear_cache()

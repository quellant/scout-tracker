"""
Pytest configuration and fixtures for Scout Tracker tests.

This file ensures test isolation by:
1. Using a separate test data directory
2. Creating fresh test data for each test
3. Cleaning up after tests
4. Never touching the real tracker_data directory
"""

import pytest
import pandas as pd
import shutil
from pathlib import Path
import tempfile
import sys
import os

# Add parent directory to path so we can import scout_tracker
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scout_tracker import config
from scout_tracker import data


@pytest.fixture(scope="function")
def test_data_dir(tmp_path):
    """
    Create a temporary test data directory for each test.
    This ensures tests never touch the real tracker_data directory.
    """
    test_dir = tmp_path / "test_tracker_data"
    test_dir.mkdir()

    # Temporarily override the DATA_DIR in scout_tracker.config module
    original_data_dir = config.DATA_DIR
    config.DATA_DIR = test_dir

    # Update all file paths
    config.ROSTER_FILE = test_dir / "Roster.csv"
    config.REQUIREMENT_KEY_FILE = test_dir / "Requirement_Key.csv"
    config.MEETINGS_FILE = test_dir / "Meetings.csv"
    config.ATTENDANCE_FILE = test_dir / "Meeting_Attendance.csv"

    yield test_dir

    # Restore original paths after test
    config.DATA_DIR = original_data_dir
    config.ROSTER_FILE = original_data_dir / "Roster.csv"
    config.REQUIREMENT_KEY_FILE = original_data_dir / "Requirement_Key.csv"
    config.MEETINGS_FILE = original_data_dir / "Meetings.csv"
    config.ATTENDANCE_FILE = original_data_dir / "Meeting_Attendance.csv"


@pytest.fixture
def sample_roster():
    """Create sample roster data for testing - matches current scout_tracker.py schema."""
    return pd.DataFrame({
        "Scout Name": ["Alice Anderson", "Bob Brown", "Charlie Chen"]
    })


@pytest.fixture
def sample_requirements():
    """Create sample requirement key data for testing."""
    return pd.DataFrame({
        "Req_ID": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"],
        "Adventure": ["Bobcat", "Bobcat", "Fun on the Run"],
        "Requirement_Description": [
            "Get to know members of your den",
            "Learn Scout Law",
            "Identify five food groups"
        ],
        "Required": [True, True, True],
        "Rank": ["Lion", "Lion", "Lion"]
    })


@pytest.fixture
def sample_meetings():
    """Create sample meetings data for testing."""
    return pd.DataFrame({
        "Meeting_Date": ["2024-01-15", "2024-01-22", "2024-01-29"],
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3"],
        "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"]
    })


@pytest.fixture
def sample_attendance():
    """Create sample attendance data for testing."""
    return pd.DataFrame({
        "Meeting_Date": ["2024-01-15", "2024-01-15", "2024-01-22"],
        "Scout_Name": ["Alice Anderson", "Bob Brown", "Alice Anderson"]
    })


@pytest.fixture
def initialized_test_env(test_data_dir, sample_roster, sample_requirements,
                         sample_meetings, sample_attendance):
    """
    Create a fully initialized test environment with sample data.
    """
    # Save sample data to test directory
    sample_roster.to_csv(config.ROSTER_FILE, index=False)
    sample_requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    sample_meetings.to_csv(config.MEETINGS_FILE, index=False)
    sample_attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    return {
        "data_dir": test_data_dir,
        "roster": sample_roster,
        "requirements": sample_requirements,
        "meetings": sample_meetings,
        "attendance": sample_attendance
    }


@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    """
    Clear Streamlit cache before each test to ensure test isolation.
    """
    # This will be called automatically before each test
    if hasattr(data, 'clear_cache'):
        try:
            data.clear_cache()
        except:
            pass  # Cache might not exist yet

    yield

    # Clear again after test
    if hasattr(data, 'clear_cache'):
        try:
            data.clear_cache()
        except:
            pass


@pytest.fixture
def mock_streamlit_session_state(monkeypatch):
    """
    Mock Streamlit's session state for testing.
    """
    class MockSessionState(dict):
        def __init__(self):
            super().__init__()
            self.update({
                'onboarding_complete': False,
                'current_page': 'Dashboard'
            })

    mock_state = MockSessionState()

    # This would need to be adapted based on how we test Streamlit components
    return mock_state

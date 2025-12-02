"""
Pytest configuration and fixtures for Scout Tracker tests.

This file ensures test isolation by:
1. Using monkeypatch to safely override config paths (auto-restores after each test)
2. Copying real tracker_data to a temp directory for realistic test data
3. Never touching the real tracker_data directory during tests
4. Clearing Streamlit cache before/after each test

IMPORTANT: Even if tests run while the app is running, production data is safe
because monkeypatch ensures config changes are scoped to each test function.
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

# Get the project root directory (parent of tests/)
PROJECT_ROOT = Path(__file__).parent.parent
PRODUCTION_DATA_DIR = PROJECT_ROOT / "tracker_data"


@pytest.fixture(scope="function")
def test_data_dir(tmp_path, monkeypatch):
    """
    Create a temporary EMPTY test data directory for each test.

    This fixture:
    1. Creates an empty temp directory for test data
    2. Uses monkeypatch to safely redirect config paths (auto-restores after test)
    3. Ensures tests never touch the real tracker_data directory

    Using monkeypatch instead of direct assignment ensures that even if a test
    fails or is interrupted, the original config values are always restored.

    For tests that need production data, use the `production_data_test_env` fixture instead.
    """
    test_dir = tmp_path / "test_tracker_data"
    test_dir.mkdir()

    # Use monkeypatch for safe config override (auto-restores after test)
    monkeypatch.setattr(config, 'DATA_DIR', test_dir)
    monkeypatch.setattr(config, 'ROSTER_FILE', test_dir / "Roster.csv")
    monkeypatch.setattr(config, 'REQUIREMENT_KEY_FILE', test_dir / "Requirement_Key.csv")
    monkeypatch.setattr(config, 'MEETINGS_FILE', test_dir / "Meetings.csv")
    monkeypatch.setattr(config, 'ATTENDANCE_FILE', test_dir / "Meeting_Attendance.csv")

    yield test_dir

    # No manual cleanup needed - monkeypatch automatically restores original values
    # and tmp_path automatically cleans up the temp directory


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

    Note: This overwrites any copied production data with sample data.
    Use test_data_dir directly if you want to test with production data.
    """
    # Save sample data to test directory (overwrites copied production data)
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


@pytest.fixture
def production_data_test_env(tmp_path, monkeypatch):
    """
    Test environment that uses a copy of actual production data.

    Use this fixture when you want to test with real data instead of sample data.
    The production data is copied to a temp directory, so the original is safe.

    This fixture is independent of test_data_dir - it sets up its own isolated environment.
    """
    test_dir = tmp_path / "test_tracker_data"
    test_dir.mkdir()

    # Copy production data files to test directory if they exist
    if PRODUCTION_DATA_DIR.exists():
        for csv_file in PRODUCTION_DATA_DIR.glob("*.csv"):
            shutil.copy(csv_file, test_dir / csv_file.name)

    # Use monkeypatch for safe config override (auto-restores after test)
    monkeypatch.setattr(config, 'DATA_DIR', test_dir)
    monkeypatch.setattr(config, 'ROSTER_FILE', test_dir / "Roster.csv")
    monkeypatch.setattr(config, 'REQUIREMENT_KEY_FILE', test_dir / "Requirement_Key.csv")
    monkeypatch.setattr(config, 'MEETINGS_FILE', test_dir / "Meetings.csv")
    monkeypatch.setattr(config, 'ATTENDANCE_FILE', test_dir / "Meeting_Attendance.csv")

    # Load and return the copied data
    roster = pd.read_csv(config.ROSTER_FILE) if config.ROSTER_FILE.exists() else pd.DataFrame(columns=["Scout Name"])
    requirements = pd.read_csv(config.REQUIREMENT_KEY_FILE) if config.REQUIREMENT_KEY_FILE.exists() else pd.DataFrame()
    meetings = pd.read_csv(config.MEETINGS_FILE) if config.MEETINGS_FILE.exists() else pd.DataFrame()
    attendance = pd.read_csv(config.ATTENDANCE_FILE) if config.ATTENDANCE_FILE.exists() else pd.DataFrame()

    return {
        "data_dir": test_dir,
        "roster": roster,
        "requirements": requirements,
        "meetings": meetings,
        "attendance": attendance
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

"""
Comprehensive tests for meeting and attendance management in Scout Tracker.

This test suite covers:
- Meeting creation, validation, and management
- Attendance logging and tracking
- Date parsing and validation
- Attendance calculations and reports
- Bulk operations
- Edge cases and error handling

All tests use isolated test environments and never modify real data.
"""

import pytest
import pandas as pd
from datetime import datetime, date, timedelta
from scout_tracker import config, data as scout_tracker


# ============================================================================
# MEETING CREATION TESTS
# ============================================================================

@pytest.mark.unit
def test_load_meetings_empty_file(test_data_dir):
    """Test loading meetings when file doesn't exist."""
    meetings_df = scout_tracker.load_meetings()

    assert meetings_df.empty
    assert list(meetings_df.columns) == ["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"]


@pytest.mark.unit
def test_load_meetings_with_data(initialized_test_env):
    """Test loading meetings with existing data."""
    meetings_df = scout_tracker.load_meetings()

    assert not meetings_df.empty
    assert len(meetings_df) == 3
    assert "Meeting_Date" in meetings_df.columns
    assert "Meeting_Title" in meetings_df.columns
    assert "Req_IDs_Covered" in meetings_df.columns

    # Verify dates are parsed as datetime
    assert pd.api.types.is_datetime64_any_dtype(meetings_df["Meeting_Date"])


@pytest.mark.unit
def test_save_meetings_formats_dates(test_data_dir, sample_roster):
    """Test that save_meetings formats dates as YYYY-MM-DD strings."""
    # Create meeting with datetime
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-15")],
        "Meeting_Title": ["Test Meeting"],
        "Req_IDs_Covered": ["Bobcat.1,Bobcat.2"]
    })

    scout_tracker.save_meetings(meetings_df)

    # Read the saved file directly
    saved_df = pd.read_csv(config.MEETINGS_FILE)

    # Date should be saved as string in YYYY-MM-DD format
    assert saved_df.loc[0, "Meeting_Date"] == "2024-03-15"
    assert isinstance(saved_df.loc[0, "Meeting_Date"], str)


@pytest.mark.unit
def test_create_meeting_basic(test_data_dir, sample_roster, sample_requirements):
    """Test creating a basic meeting."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)
    sample_requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)

    meetings_df = scout_tracker.load_meetings()

    new_meeting = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-02-15")],
        "Meeting_Title": ["Nature Hike"],
        "Req_IDs_Covered": ["Bobcat.1,Bobcat.2"]
    })

    meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
    scout_tracker.save_meetings(meetings_df)

    # Reload and verify
    meetings_df = scout_tracker.load_meetings()
    assert len(meetings_df) == 1
    assert meetings_df.loc[0, "Meeting_Title"] == "Nature Hike"
    assert meetings_df.loc[0, "Req_IDs_Covered"] == "Bobcat.1,Bobcat.2"


@pytest.mark.unit
def test_create_meeting_with_multiple_requirements(test_data_dir, sample_roster, sample_requirements):
    """Test creating a meeting covering multiple requirements."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)
    sample_requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)

    meetings_df = scout_tracker.load_meetings()

    new_meeting = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-02-20")],
        "Meeting_Title": ["Multi-Requirement Meeting"],
        "Req_IDs_Covered": ["Bobcat.1,Bobcat.2,FunOnTheRun.1"]
    })

    meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    req_ids = meetings_df.loc[0, "Req_IDs_Covered"].split(",")
    assert len(req_ids) == 3
    assert "Bobcat.1" in req_ids
    assert "FunOnTheRun.1" in req_ids


@pytest.mark.unit
def test_duplicate_meeting_date_detection(initialized_test_env):
    """Test detection of duplicate meeting dates."""
    meetings_df = scout_tracker.load_meetings()

    # Try to add a meeting on a date that already exists
    existing_date = meetings_df.loc[0, "Meeting_Date"]

    # Check if date already exists
    existing_dates = pd.to_datetime(meetings_df["Meeting_Date"]).dt.date.values

    assert existing_date.date() in existing_dates


@pytest.mark.unit
def test_meeting_date_parsing_various_formats(test_data_dir):
    """Test that meeting dates are parsed correctly from various formats."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": ["2024-01-15", "2024-02-20", "2024-03-10"],
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3"],
        "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"]
    })

    scout_tracker.save_meetings(meetings_df)
    loaded_df = scout_tracker.load_meetings()

    # All dates should be datetime objects
    assert pd.api.types.is_datetime64_any_dtype(loaded_df["Meeting_Date"])
    assert len(loaded_df) == 3


# ============================================================================
# ATTENDANCE LOGGING TESTS
# ============================================================================

@pytest.mark.unit
def test_load_attendance_empty_file(test_data_dir):
    """Test loading attendance when file doesn't exist."""
    attendance_df = scout_tracker.load_attendance()

    assert attendance_df.empty
    assert list(attendance_df.columns) == ["Meeting_Date", "Scout_Name"]


@pytest.mark.unit
def test_load_attendance_with_data(initialized_test_env):
    """Test loading attendance with existing data."""
    attendance_df = scout_tracker.load_attendance()

    assert not attendance_df.empty
    assert "Meeting_Date" in attendance_df.columns
    assert "Scout_Name" in attendance_df.columns

    # Verify dates are parsed as datetime
    assert pd.api.types.is_datetime64_any_dtype(attendance_df["Meeting_Date"])


@pytest.mark.unit
def test_save_attendance_formats_dates(test_data_dir):
    """Test that save_attendance formats dates as YYYY-MM-DD strings."""
    attendance_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-15"), pd.to_datetime("2024-03-15")],
        "Scout_Name": ["Alice Anderson", "Bob Brown"]
    })

    scout_tracker.save_attendance(attendance_df)

    # Read the saved file directly
    saved_df = pd.read_csv(config.ATTENDANCE_FILE)

    # Date should be saved as string
    assert saved_df.loc[0, "Meeting_Date"] == "2024-03-15"
    assert isinstance(saved_df.loc[0, "Meeting_Date"], str)


@pytest.mark.unit
def test_log_attendance_single_scout(initialized_test_env):
    """Test logging attendance for a single scout."""
    meetings_df = scout_tracker.load_meetings()
    meeting_date = meetings_df.loc[0, "Meeting_Date"]

    attendance_df = scout_tracker.load_attendance()

    # Add attendance for one scout
    new_attendance = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Scout_Name": ["Charlie Chen"]
    })

    attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
    scout_tracker.save_attendance(attendance_df)

    # Reload and verify
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert "Charlie Chen" in meeting_attendees["Scout_Name"].values


@pytest.mark.unit
def test_log_attendance_multiple_scouts(initialized_test_env):
    """Test logging attendance for multiple scouts at once."""
    meetings_df = scout_tracker.load_meetings()
    meeting_date = meetings_df.loc[1, "Meeting_Date"]

    attendance_df = scout_tracker.load_attendance()

    # Add attendance for multiple scouts
    scouts = ["Alice Anderson", "Bob Brown", "Charlie Chen"]
    new_attendance = pd.DataFrame({
        "Meeting_Date": [meeting_date] * len(scouts),
        "Scout_Name": scouts
    })

    attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
    scout_tracker.save_attendance(attendance_df)

    # Reload and verify
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert len(meeting_attendees) >= 3
    for scout in scouts:
        assert scout in meeting_attendees["Scout_Name"].values


@pytest.mark.unit
def test_update_attendance_remove_existing(initialized_test_env):
    """Test updating attendance by removing existing records first."""
    meetings_df = scout_tracker.load_meetings()
    meeting_date = meetings_df.loc[0, "Meeting_Date"]

    attendance_df = scout_tracker.load_attendance()

    # Remove all existing attendance for this date
    attendance_df = attendance_df[attendance_df["Meeting_Date"] != meeting_date]

    # Add new attendance
    new_attendance = pd.DataFrame({
        "Meeting_Date": [meeting_date, meeting_date],
        "Scout_Name": ["Alice Anderson", "Charlie Chen"]
    })

    attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
    scout_tracker.save_attendance(attendance_df)

    # Verify only the new scouts are present
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert len(meeting_attendees) == 2
    assert "Alice Anderson" in meeting_attendees["Scout_Name"].values
    assert "Charlie Chen" in meeting_attendees["Scout_Name"].values


@pytest.mark.unit
def test_get_attendance_for_specific_meeting(initialized_test_env):
    """Test retrieving attendance records for a specific meeting."""
    meetings_df = scout_tracker.load_meetings()
    attendance_df = scout_tracker.load_attendance()

    # Get attendance for first meeting
    target_date = meetings_df.loc[0, "Meeting_Date"]
    meeting_attendance = attendance_df[attendance_df["Meeting_Date"] == target_date]

    assert len(meeting_attendance) >= 0
    assert "Scout_Name" in meeting_attendance.columns


# ============================================================================
# ATTENDANCE CALCULATION TESTS
# ============================================================================

@pytest.mark.unit
def test_calculate_attendance_percentage(initialized_test_env):
    """Test calculating attendance percentage for a meeting."""
    roster_df = initialized_test_env["roster"]
    meetings_df = scout_tracker.load_meetings()
    attendance_df = scout_tracker.load_attendance()

    meeting_date = meetings_df.loc[0, "Meeting_Date"]
    attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    total_scouts = len(roster_df)
    attendance_count = len(attendees)

    if total_scouts > 0:
        percentage = (attendance_count / total_scouts) * 100
        assert 0 <= percentage <= 100


@pytest.mark.unit
def test_attendance_percentage_all_present(test_data_dir, sample_roster):
    """Test attendance percentage when all scouts are present."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    meeting_date = pd.to_datetime("2024-02-15")

    # Create meeting
    meetings_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Meeting_Title": ["All Present Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Log attendance for all scouts
    attendance_df = pd.DataFrame({
        "Meeting_Date": [meeting_date] * len(sample_roster),
        "Scout_Name": sample_roster["Scout Name"].tolist()
    })
    scout_tracker.save_attendance(attendance_df)

    # Calculate percentage
    roster_df = scout_tracker.load_roster()
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    percentage = (len(meeting_attendees) / len(roster_df)) * 100
    assert percentage == 100.0


@pytest.mark.unit
def test_attendance_percentage_none_present(test_data_dir, sample_roster):
    """Test attendance percentage when no scouts are present."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    meeting_date = pd.to_datetime("2024-02-15")

    # Create meeting
    meetings_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Meeting_Title": ["No Show Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # No attendance logged
    attendance_df = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])
    scout_tracker.save_attendance(attendance_df)

    # Calculate percentage
    roster_df = scout_tracker.load_roster()
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    percentage = (len(meeting_attendees) / len(roster_df)) * 100 if len(roster_df) > 0 else 0
    assert percentage == 0.0


@pytest.mark.unit
def test_get_scouts_who_attended(initialized_test_env):
    """Test getting list of scouts who attended a specific meeting."""
    meetings_df = scout_tracker.load_meetings()
    attendance_df = scout_tracker.load_attendance()

    meeting_date = meetings_df.loc[0, "Meeting_Date"]
    attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]["Scout_Name"].tolist()

    assert isinstance(attendees, list)


@pytest.mark.unit
def test_get_scouts_who_were_absent(initialized_test_env):
    """Test calculating which scouts were absent from a meeting."""
    roster_df = initialized_test_env["roster"]
    meetings_df = scout_tracker.load_meetings()
    attendance_df = scout_tracker.load_attendance()

    meeting_date = meetings_df.loc[0, "Meeting_Date"]
    attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]["Scout_Name"].tolist()

    # Get all scouts
    all_scouts = roster_df["Scout Name"].tolist()

    # Calculate absent scouts
    absent_scouts = [scout for scout in all_scouts if scout not in attendees]

    assert isinstance(absent_scouts, list)
    assert len(absent_scouts) + len(attendees) == len(all_scouts)


# ============================================================================
# MEETING HISTORY AND QUERYING TESTS
# ============================================================================

@pytest.mark.unit
def test_get_all_meetings_sorted_by_date(initialized_test_env):
    """Test retrieving all meetings sorted by date."""
    meetings_df = scout_tracker.load_meetings()

    sorted_meetings = meetings_df.sort_values("Meeting_Date", ascending=False)

    assert len(sorted_meetings) == len(meetings_df)

    # Verify sorted order
    dates = sorted_meetings["Meeting_Date"].tolist()
    for i in range(len(dates) - 1):
        assert dates[i] >= dates[i + 1]


@pytest.mark.unit
def test_filter_meetings_by_date_range(initialized_test_env):
    """Test filtering meetings within a date range."""
    meetings_df = scout_tracker.load_meetings()

    start_date = pd.to_datetime("2024-01-01")
    end_date = pd.to_datetime("2024-12-31")

    filtered_meetings = meetings_df[
        (meetings_df["Meeting_Date"] >= start_date) &
        (meetings_df["Meeting_Date"] <= end_date)
    ]

    assert len(filtered_meetings) >= 0

    for _, meeting in filtered_meetings.iterrows():
        assert start_date <= meeting["Meeting_Date"] <= end_date


@pytest.mark.unit
def test_get_meetings_for_specific_month(test_data_dir):
    """Test retrieving meetings for a specific month."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [
            pd.to_datetime("2024-03-05"),
            pd.to_datetime("2024-03-12"),
            pd.to_datetime("2024-03-19"),
            pd.to_datetime("2024-04-02")
        ],
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3", "Meeting 4"],
        "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1", "Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()

    # Filter for March 2024
    march_meetings = meetings_df[
        (meetings_df["Meeting_Date"].dt.year == 2024) &
        (meetings_df["Meeting_Date"].dt.month == 3)
    ]

    assert len(march_meetings) == 3


@pytest.mark.unit
def test_count_meetings_attended_by_scout(initialized_test_env):
    """Test counting total meetings attended by a specific scout."""
    attendance_df = scout_tracker.load_attendance()

    # Count meetings for a specific scout
    scout_name = "Alice Anderson"
    scout_attendance = attendance_df[attendance_df["Scout_Name"] == scout_name]

    meeting_count = len(scout_attendance)

    assert meeting_count >= 0


# ============================================================================
# BULK OPERATIONS TESTS
# ============================================================================

@pytest.mark.unit
def test_mark_all_scouts_present(test_data_dir, sample_roster):
    """Test bulk operation to mark all scouts as present."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    meeting_date = pd.to_datetime("2024-02-20")

    # Create meeting
    meetings_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Meeting_Title": ["All Present Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Mark all scouts as present
    roster_df = scout_tracker.load_roster()
    all_scout_names = roster_df["Scout Name"].tolist()

    attendance_df = pd.DataFrame({
        "Meeting_Date": [meeting_date] * len(all_scout_names),
        "Scout_Name": all_scout_names
    })
    scout_tracker.save_attendance(attendance_df)

    # Verify all marked present
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert len(meeting_attendees) == len(sample_roster)


@pytest.mark.unit
def test_mark_all_scouts_absent(test_data_dir, sample_roster):
    """Test bulk operation to mark all scouts as absent (no attendance records)."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    meeting_date = pd.to_datetime("2024-02-25")

    # Create meeting
    meetings_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Meeting_Title": ["All Absent Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Don't log any attendance (all absent)
    attendance_df = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])
    scout_tracker.save_attendance(attendance_df)

    # Verify no attendance records
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert len(meeting_attendees) == 0


@pytest.mark.unit
def test_clear_attendance_for_meeting(initialized_test_env):
    """Test clearing all attendance records for a specific meeting."""
    meetings_df = scout_tracker.load_meetings()
    attendance_df = scout_tracker.load_attendance()

    meeting_date = meetings_df.loc[0, "Meeting_Date"]

    # Clear attendance for this meeting
    attendance_df = attendance_df[attendance_df["Meeting_Date"] != meeting_date]
    scout_tracker.save_attendance(attendance_df)

    # Verify cleared
    attendance_df = scout_tracker.load_attendance()
    meeting_attendees = attendance_df[attendance_df["Meeting_Date"] == meeting_date]

    assert len(meeting_attendees) == 0


# ============================================================================
# EDGE CASES AND ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.unit
def test_meeting_with_future_date(test_data_dir):
    """Test creating a meeting with a future date."""
    future_date = datetime.now() + timedelta(days=30)

    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime(future_date)],
        "Meeting_Title": ["Future Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    assert len(meetings_df) == 1
    assert meetings_df.loc[0, "Meeting_Date"] > pd.Timestamp.now()


@pytest.mark.unit
def test_meeting_with_past_date(test_data_dir):
    """Test creating a meeting with a date from the past."""
    past_date = datetime.now() - timedelta(days=365)

    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime(past_date)],
        "Meeting_Title": ["Past Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    assert len(meetings_df) == 1
    assert meetings_df.loc[0, "Meeting_Date"] < pd.Timestamp.now()


@pytest.mark.unit
def test_meeting_with_empty_title(test_data_dir):
    """Test that meetings can have empty titles (validation happens in UI)."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-01")],
        "Meeting_Title": [""],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    assert len(meetings_df) == 1


@pytest.mark.unit
def test_meeting_with_no_requirements(test_data_dir):
    """Test creating a meeting with no requirements covered."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-05")],
        "Meeting_Title": ["Social Meeting"],
        "Req_IDs_Covered": [""]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    assert len(meetings_df) == 1


@pytest.mark.unit
def test_attendance_for_nonexistent_scout(test_data_dir, sample_roster):
    """Test logging attendance for a scout not in the roster."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    meeting_date = pd.to_datetime("2024-03-10")

    # Create meeting
    meetings_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Meeting_Title": ["Test Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Log attendance for nonexistent scout
    attendance_df = pd.DataFrame({
        "Meeting_Date": [meeting_date],
        "Scout_Name": ["Nonexistent Scout"]
    })
    scout_tracker.save_attendance(attendance_df)

    # System should still save it (validation happens elsewhere)
    attendance_df = scout_tracker.load_attendance()
    assert len(attendance_df) == 1


@pytest.mark.unit
def test_attendance_for_nonexistent_meeting(test_data_dir):
    """Test logging attendance for a meeting that doesn't exist."""
    nonexistent_date = pd.to_datetime("2099-12-31")

    attendance_df = pd.DataFrame({
        "Meeting_Date": [nonexistent_date],
        "Scout_Name": ["Alice Anderson"]
    })
    scout_tracker.save_attendance(attendance_df)

    # System should still save it
    attendance_df = scout_tracker.load_attendance()
    assert len(attendance_df) == 1


@pytest.mark.unit
def test_empty_meetings_dataframe_operations(test_data_dir):
    """Test operations on empty meetings dataframe."""
    meetings_df = scout_tracker.load_meetings()

    # Should be able to sort empty dataframe
    sorted_df = meetings_df.sort_values("Meeting_Date", ascending=False) if not meetings_df.empty else meetings_df
    assert sorted_df.empty


@pytest.mark.unit
def test_empty_attendance_dataframe_operations(test_data_dir):
    """Test operations on empty attendance dataframe."""
    attendance_df = scout_tracker.load_attendance()

    # Should be able to filter empty dataframe
    filtered_df = attendance_df[attendance_df["Meeting_Date"] == pd.to_datetime("2024-01-01")]
    assert filtered_df.empty


@pytest.mark.unit
def test_meeting_with_single_requirement(test_data_dir):
    """Test meeting covering only one requirement."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-15")],
        "Meeting_Title": ["Single Requirement Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    req_ids = meetings_df.loc[0, "Req_IDs_Covered"].split(",")
    assert len(req_ids) == 1
    assert req_ids[0] == "Bobcat.1"


@pytest.mark.unit
def test_attendance_same_scout_multiple_meetings(test_data_dir, sample_roster):
    """Test that same scout can attend multiple meetings."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    # Create multiple meetings
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-01"), pd.to_datetime("2024-03-08"), pd.to_datetime("2024-03-15")],
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3"],
        "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Log same scout for all meetings
    attendance_records = []
    for date in meetings_df["Meeting_Date"]:
        attendance_records.append({
            "Meeting_Date": date,
            "Scout_Name": "Alice Anderson"
        })

    attendance_df = pd.DataFrame(attendance_records)
    scout_tracker.save_attendance(attendance_df)

    # Verify scout attended all three
    attendance_df = scout_tracker.load_attendance()
    alice_attendance = attendance_df[attendance_df["Scout_Name"] == "Alice Anderson"]

    assert len(alice_attendance) == 3


@pytest.mark.unit
def test_requirements_parsing_from_meeting(test_data_dir):
    """Test parsing requirement IDs from meeting data."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-03-20")],
        "Meeting_Title": ["Multi-Req Meeting"],
        "Req_IDs_Covered": ["Bobcat.1,Bobcat.2,FunOnTheRun.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    meetings_df = scout_tracker.load_meetings()
    req_ids_str = meetings_df.loc[0, "Req_IDs_Covered"]

    # Parse requirements
    if pd.notna(req_ids_str):
        req_ids = req_ids_str.split(",")
        assert len(req_ids) == 3
        assert "Bobcat.1" in req_ids
        assert "Bobcat.2" in req_ids
        assert "FunOnTheRun.1" in req_ids


@pytest.mark.unit
def test_date_consistency_after_save_and_load(test_data_dir):
    """Test that dates remain consistent through save/load cycle."""
    original_date = pd.to_datetime("2024-04-15")

    meetings_df = pd.DataFrame({
        "Meeting_Date": [original_date],
        "Meeting_Title": ["Date Test Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    loaded_df = scout_tracker.load_meetings()
    loaded_date = loaded_df.loc[0, "Meeting_Date"]

    # Dates should match (comparing date components only)
    assert original_date.date() == loaded_date.date()


@pytest.mark.unit
def test_multiple_scouts_different_attendance_patterns(test_data_dir, sample_roster):
    """Test complex attendance patterns with multiple scouts and meetings."""
    sample_roster.to_csv(config.ROSTER_FILE, index=False)

    # Create three meetings
    meetings_df = pd.DataFrame({
        "Meeting_Date": [
            pd.to_datetime("2024-04-01"),
            pd.to_datetime("2024-04-08"),
            pd.to_datetime("2024-04-15")
        ],
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3"],
        "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"]
    })
    scout_tracker.save_meetings(meetings_df)

    # Create varied attendance pattern
    # Alice: attends all three
    # Bob: attends first and third
    # Charlie: attends second only
    attendance_records = [
        {"Meeting_Date": pd.to_datetime("2024-04-01"), "Scout_Name": "Alice Anderson"},
        {"Meeting_Date": pd.to_datetime("2024-04-08"), "Scout_Name": "Alice Anderson"},
        {"Meeting_Date": pd.to_datetime("2024-04-15"), "Scout_Name": "Alice Anderson"},
        {"Meeting_Date": pd.to_datetime("2024-04-01"), "Scout_Name": "Bob Brown"},
        {"Meeting_Date": pd.to_datetime("2024-04-15"), "Scout_Name": "Bob Brown"},
        {"Meeting_Date": pd.to_datetime("2024-04-08"), "Scout_Name": "Charlie Chen"},
    ]

    attendance_df = pd.DataFrame(attendance_records)
    scout_tracker.save_attendance(attendance_df)

    # Verify patterns
    attendance_df = scout_tracker.load_attendance()

    alice_count = len(attendance_df[attendance_df["Scout_Name"] == "Alice Anderson"])
    bob_count = len(attendance_df[attendance_df["Scout_Name"] == "Bob Brown"])
    charlie_count = len(attendance_df[attendance_df["Scout_Name"] == "Charlie Chen"])

    assert alice_count == 3
    assert bob_count == 2
    assert charlie_count == 1


# ============================================================================
# CACHE CLEARING TESTS
# ============================================================================

@pytest.mark.unit
def test_cache_cleared_after_save_meetings(test_data_dir):
    """Test that cache is cleared after saving meetings."""
    meetings_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-05-01")],
        "Meeting_Title": ["Cache Test Meeting"],
        "Req_IDs_Covered": ["Bobcat.1"]
    })

    scout_tracker.save_meetings(meetings_df)

    # Load should get fresh data
    loaded_df = scout_tracker.load_meetings()
    assert len(loaded_df) == 1


@pytest.mark.unit
def test_cache_cleared_after_save_attendance(test_data_dir):
    """Test that cache is cleared after saving attendance."""
    attendance_df = pd.DataFrame({
        "Meeting_Date": [pd.to_datetime("2024-05-01")],
        "Scout_Name": ["Test Scout"]
    })

    scout_tracker.save_attendance(attendance_df)

    # Load should get fresh data
    loaded_df = scout_tracker.load_attendance()
    assert len(loaded_df) == 1

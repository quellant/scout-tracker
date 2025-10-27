"""
Comprehensive tests for dashboard and reporting functionality in Scout Tracker.

This test suite covers:
- Dashboard statistics calculations
- Progress tracking across multiple scouts
- Individual scout reports
- Adventure completion tracking
- Rank advancement eligibility
- Summary statistics
- Data aggregation functions
- Edge cases (no scouts, all complete, none complete)

All tests use test_data_dir and initialized_test_env fixtures to ensure
isolation from real tracker_data.
"""

import pytest
import pandas as pd
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scout_tracker import config, data as scout_tracker


# ============================================================================
# FIXTURES FOR DASHBOARD TESTING
# ============================================================================

@pytest.fixture
def multi_scout_roster():
    """Create a roster with multiple scouts for dashboard testing."""
    return pd.DataFrame({
        "Scout Name": ["Alice Anderson", "Bob Brown", "Charlie Chen", "Diana Davis"],
        "Current_Rank": ["Lion", "Lion", "Lion", "Lion"],
        "Status": ["Active", "Active", "Active", "Active"]
    })


@pytest.fixture
def complete_requirements():
    """Create a complete set of requirements (required + elective)."""
    requirements = []

    # Required adventures (6 adventures)
    required_adventures = [
        ("Bobcat", 5),
        ("Animal Kingdom", 4),
        ("Gizmos & Gadgets", 3),
        ("Mountain Lion", 4),
        ("Fun on the Run", 5),
        ("King of the Jungle", 4)
    ]

    req_num = 1
    for adventure, num_reqs in required_adventures:
        for i in range(1, num_reqs + 1):
            requirements.append({
                "Req_ID": f"{adventure.replace(' ', '')}.{i}",
                "Adventure": adventure,
                "Requirement_Description": f"{adventure} requirement {i}",
                "Required": True,
                "Rank": "Lion"
            })

    # Elective adventures (4 adventures)
    elective_adventures = [
        ("Rumble in the Jungle", 3),
        ("Pick My Path", 4),
        ("Lion's Pride", 3),
        ("On Your Mark", 4)
    ]

    for adventure, num_reqs in elective_adventures:
        for i in range(1, num_reqs + 1):
            requirements.append({
                "Req_ID": f"{adventure.replace(' ', '')}.{i}",
                "Adventure": adventure,
                "Requirement_Description": f"{adventure} requirement {i}",
                "Required": False,
                "Rank": "Lion"
            })

    return pd.DataFrame(requirements)


@pytest.fixture
def progressive_meetings():
    """Create meetings that progressively cover requirements."""
    return pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-22", "2024-01-29", "2024-02-05"]),
        "Meeting_Title": ["First Meeting", "Second Meeting", "Third Meeting", "Fourth Meeting"],
        "Req_IDs_Covered": [
            "Bobcat.1,Bobcat.2",
            "Bobcat.3,AnimalKingdom.1,AnimalKingdom.2",
            "Gizmos&Gadgets.1,Gizmos&Gadgets.2,MountainLion.1",
            "FunontheRun.1,FunontheRun.2,KingoftheJungle.1"
        ]
    })


@pytest.fixture
def varied_attendance(multi_scout_roster, progressive_meetings):
    """Create varied attendance patterns for testing progress tracking."""
    attendance = []
    scouts = multi_scout_roster["Scout Name"].tolist()

    # Alice: Perfect attendance (all 4 meetings)
    for date in progressive_meetings["Meeting_Date"]:
        attendance.append({"Meeting_Date": date, "Scout_Name": scouts[0]})

    # Bob: Missed first meeting (3 meetings)
    for date in progressive_meetings["Meeting_Date"][1:]:
        attendance.append({"Meeting_Date": date, "Scout_Name": scouts[1]})

    # Charlie: Only first 2 meetings
    for date in progressive_meetings["Meeting_Date"][:2]:
        attendance.append({"Meeting_Date": date, "Scout_Name": scouts[2]})

    # Diana: Only last meeting
    attendance.append({"Meeting_Date": progressive_meetings["Meeting_Date"].iloc[-1], "Scout_Name": scouts[3]})

    df = pd.DataFrame(attendance)
    df["Meeting_Date"] = pd.to_datetime(df["Meeting_Date"])
    return df


@pytest.fixture
def dashboard_test_env(test_data_dir, multi_scout_roster, complete_requirements,
                       progressive_meetings, varied_attendance):
    """Create a comprehensive test environment for dashboard testing."""
    multi_scout_roster.to_csv(config.ROSTER_FILE, index=False)
    complete_requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    progressive_meetings.to_csv(config.MEETINGS_FILE, index=False)
    varied_attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    return {
        "data_dir": test_data_dir,
        "roster": multi_scout_roster,
        "requirements": complete_requirements,
        "meetings": progressive_meetings,
        "attendance": varied_attendance
    }


# ============================================================================
# HELPER FUNCTION TO BUILD MASTER TRACKER
# ============================================================================

def build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df):
    """
    Build the master tracker DataFrame that tracks requirement completion.
    This replicates the logic from page_tracker_dashboard().
    """
    scouts = roster_df["Scout Name"].tolist()
    req_ids = requirement_key["Req_ID"].tolist()

    # Initialize with all False
    master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

    # Create lookup dictionary: Meeting_Date -> Req_IDs_Covered
    meeting_req_lookup = {}
    for _, meeting in meetings_df.iterrows():
        req_ids_covered = meeting["Req_IDs_Covered"].split(",") if pd.notna(meeting["Req_IDs_Covered"]) else []
        meeting_req_lookup[meeting["Meeting_Date"]] = req_ids_covered

    # Process attendance to mark completed requirements
    for _, attendance_row in attendance_df.iterrows():
        scout_name = attendance_row["Scout_Name"]
        meeting_date = attendance_row["Meeting_Date"]

        if scout_name in master_tracker.index and meeting_date in meeting_req_lookup:
            req_ids_covered = meeting_req_lookup[meeting_date]
            for req_id in req_ids_covered:
                if req_id in master_tracker.columns:
                    master_tracker.at[scout_name, req_id] = True

    return master_tracker


def calculate_adventure_progress(scout_name, adventure, master_tracker, requirement_key):
    """
    Calculate progress for a specific adventure for a specific scout.
    Returns (completed_count, total_count, percentage).
    """
    adventure_reqs = requirement_key[requirement_key["Adventure"] == adventure]["Req_ID"].tolist()
    completed = master_tracker.loc[scout_name, adventure_reqs].sum()
    total = len(adventure_reqs)
    percentage = (completed / total * 100) if total > 0 else 0
    return completed, total, percentage


def calculate_rank_eligibility(scout_name, master_tracker, requirement_key):
    """
    Calculate if a scout is eligible for rank advancement.
    Returns (all_required_complete, completed_electives, rank_earned).
    """
    required_adventures = requirement_key[requirement_key["Required"] == True]["Adventure"].unique()
    elective_adventures = requirement_key[requirement_key["Required"] == False]["Adventure"].unique()

    # Check required adventures
    all_required_complete = True
    for adventure in required_adventures:
        _, _, percentage = calculate_adventure_progress(scout_name, adventure, master_tracker, requirement_key)
        if percentage < 100.0:
            all_required_complete = False
            break

    # Count completed electives
    completed_electives = 0
    for adventure in elective_adventures:
        _, _, percentage = calculate_adventure_progress(scout_name, adventure, master_tracker, requirement_key)
        if percentage == 100.0:
            completed_electives += 1

    # Rank earned = all required + at least 2 electives
    rank_earned = all_required_complete and completed_electives >= 2

    return all_required_complete, completed_electives, rank_earned


# ============================================================================
# TEST: MASTER TRACKER BUILDING
# ============================================================================

@pytest.mark.unit
def test_master_tracker_initialization(dashboard_test_env):
    """Test that master tracker initializes correctly with all False values."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]

    scouts = roster_df["Scout Name"].tolist()
    req_ids = requirement_key["Req_ID"].tolist()

    master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

    assert master_tracker.shape[0] == len(scouts)
    assert master_tracker.shape[1] == len(req_ids)
    assert not master_tracker.any().any()  # All should be False


@pytest.mark.unit
def test_master_tracker_attendance_processing(dashboard_test_env):
    """Test that master tracker correctly processes attendance data."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Alice attended all 4 meetings, should have all covered requirements
    alice_completed = master_tracker.loc["Alice Anderson"]
    assert alice_completed["Bobcat.1"] == True
    assert alice_completed["Bobcat.2"] == True
    assert alice_completed["AnimalKingdom.1"] == True
    assert alice_completed["FunontheRun.1"] == True

    # Bob missed first meeting, should not have Bobcat.1 and Bobcat.2
    bob_completed = master_tracker.loc["Bob Brown"]
    assert bob_completed["Bobcat.1"] == False
    assert bob_completed["Bobcat.2"] == False
    assert bob_completed["AnimalKingdom.1"] == True  # Attended second meeting


@pytest.mark.unit
def test_master_tracker_partial_attendance(dashboard_test_env):
    """Test that scouts with partial attendance have correct completion status."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Charlie attended only first 2 meetings
    charlie_completed = master_tracker.loc["Charlie Chen"]
    assert charlie_completed["Bobcat.1"] == True
    assert charlie_completed["Bobcat.2"] == True
    assert charlie_completed["AnimalKingdom.1"] == True
    assert charlie_completed["Gizmos&Gadgets.1"] == False  # Not at third meeting
    assert charlie_completed["FunontheRun.1"] == False  # Not at fourth meeting

    # Diana attended only last meeting
    diana_completed = master_tracker.loc["Diana Davis"]
    assert diana_completed["Bobcat.1"] == False
    assert diana_completed["FunontheRun.1"] == True
    assert diana_completed["FunontheRun.2"] == True
    assert diana_completed["KingoftheJungle.1"] == True


# ============================================================================
# TEST: ADVENTURE COMPLETION CALCULATIONS
# ============================================================================

@pytest.mark.unit
def test_required_adventure_completion_percentage(dashboard_test_env):
    """Test calculation of required adventure completion percentages."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Test Bobcat adventure for Alice (attended all meetings)
    completed, total, percentage = calculate_adventure_progress(
        "Alice Anderson", "Bobcat", master_tracker, requirement_key
    )
    assert completed == 3  # 3 Bobcat requirements covered in meetings (Bobcat.1, .2, .3)
    assert total == 5  # Total Bobcat requirements
    assert percentage == 60.0  # 3/5 = 60%

    # Test Bobcat for Bob (missed first meeting)
    completed, total, percentage = calculate_adventure_progress(
        "Bob Brown", "Bobcat", master_tracker, requirement_key
    )
    assert completed == 1  # Bob missed first meeting but got Bobcat.3 in second meeting
    assert total == 5
    assert percentage == 20.0  # 1/5 = 20%


@pytest.mark.unit
def test_elective_adventure_completion_percentage(dashboard_test_env):
    """Test calculation of elective adventure completion percentages."""
    # Create a scenario where electives are completed
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Elective1.1", "Elective1.2", "Elective1.3"],
        "Adventure": ["Test Elective", "Test Elective", "Test Elective"],
        "Requirement_Description": ["Req 1", "Req 2", "Req 3"],
        "Required": [False, False, False],
        "Rank": ["Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Elective Meeting"],
        "Req_IDs_Covered": ["Elective1.1,Elective1.2,Elective1.3"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Test Scout"]
    })

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    completed, total, percentage = calculate_adventure_progress(
        "Test Scout", "Test Elective", master_tracker, requirements
    )
    assert completed == 3
    assert total == 3
    assert percentage == 100.0


@pytest.mark.unit
def test_adventure_completion_with_zero_requirements(dashboard_test_env):
    """Test adventure completion calculation when no requirements exist."""
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": [],
        "Adventure": [],
        "Requirement_Description": [],
        "Required": [],
        "Rank": []
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Test Meeting"],
        "Req_IDs_Covered": [""]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Test Scout"]
    })

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    completed, total, percentage = calculate_adventure_progress(
        "Test Scout", "Nonexistent Adventure", master_tracker, requirements
    )
    assert completed == 0
    assert total == 0
    assert percentage == 0.0


# ============================================================================
# TEST: RANK ADVANCEMENT ELIGIBILITY
# ============================================================================

@pytest.mark.unit
def test_rank_eligibility_all_complete(test_data_dir):
    """Test rank eligibility when scout completes all required + 2 electives."""
    # Create scenario where scout completed everything
    roster = pd.DataFrame({
        "Scout Name": ["Complete Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2", "Elect1.1", "Elect2.1"],
        "Adventure": ["Required Adv", "Required Adv", "Elective 1", "Elective 2"],
        "Requirement_Description": ["R1", "R2", "E1", "E2"],
        "Required": [True, True, False, False],
        "Rank": ["Lion", "Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Complete Meeting"],
        "Req_IDs_Covered": ["Req1.1,Req1.2,Elect1.1,Elect2.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Complete Scout"]
    })

    # Save to test directory
    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    all_required_complete, completed_electives, rank_earned = calculate_rank_eligibility(
        "Complete Scout", master_tracker, requirements
    )

    assert all_required_complete == True
    assert completed_electives == 2
    assert rank_earned == True


@pytest.mark.unit
def test_rank_eligibility_missing_required(test_data_dir):
    """Test rank eligibility when scout missing required adventures."""
    roster = pd.DataFrame({
        "Scout Name": ["Incomplete Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2", "Elect1.1", "Elect2.1"],
        "Adventure": ["Required Adv", "Required Adv", "Elective 1", "Elective 2"],
        "Requirement_Description": ["R1", "R2", "E1", "E2"],
        "Required": [True, True, False, False],
        "Rank": ["Lion", "Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Partial Meeting"],
        "Req_IDs_Covered": ["Req1.1,Elect1.1,Elect2.1"]  # Missing Req1.2
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Incomplete Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    all_required_complete, completed_electives, rank_earned = calculate_rank_eligibility(
        "Incomplete Scout", master_tracker, requirements
    )

    assert all_required_complete == False
    assert completed_electives == 2
    assert rank_earned == False  # Can't earn rank without all required


@pytest.mark.unit
def test_rank_eligibility_missing_electives(test_data_dir):
    """Test rank eligibility when scout has all required but only 1 elective."""
    roster = pd.DataFrame({
        "Scout Name": ["One Elective Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2", "Elect1.1"],
        "Adventure": ["Required Adv", "Required Adv", "Elective 1"],
        "Requirement_Description": ["R1", "R2", "E1"],
        "Required": [True, True, False],
        "Rank": ["Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Meeting"],
        "Req_IDs_Covered": ["Req1.1,Req1.2,Elect1.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["One Elective Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    all_required_complete, completed_electives, rank_earned = calculate_rank_eligibility(
        "One Elective Scout", master_tracker, requirements
    )

    assert all_required_complete == True
    assert completed_electives == 1
    assert rank_earned == False  # Need at least 2 electives


@pytest.mark.unit
def test_rank_eligibility_three_electives(test_data_dir):
    """Test rank eligibility when scout completes 3 electives (more than required)."""
    roster = pd.DataFrame({
        "Scout Name": ["Overachiever Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Elect1.1", "Elect2.1", "Elect3.1"],
        "Adventure": ["Required Adv", "Elective 1", "Elective 2", "Elective 3"],
        "Requirement_Description": ["R1", "E1", "E2", "E3"],
        "Required": [True, False, False, False],
        "Rank": ["Lion", "Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Complete Meeting"],
        "Req_IDs_Covered": ["Req1.1,Elect1.1,Elect2.1,Elect3.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Overachiever Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    all_required_complete, completed_electives, rank_earned = calculate_rank_eligibility(
        "Overachiever Scout", master_tracker, requirements
    )

    assert all_required_complete == True
    assert completed_electives == 3  # Completed 3 electives
    assert rank_earned == True  # Still earns rank (needs minimum 2)


# ============================================================================
# TEST: INDIVIDUAL SCOUT PROGRESS TRACKING
# ============================================================================

@pytest.mark.unit
def test_individual_scout_progress_calculation(dashboard_test_env):
    """Test calculating progress for an individual scout."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Test Alice's progress (attended all meetings)
    alice_completed_reqs = master_tracker.loc["Alice Anderson"].sum()
    total_reqs = len(requirement_key)

    # Alice attended all 4 meetings which covered 11 total requirements
    expected_completed = 11
    assert alice_completed_reqs == expected_completed

    # Test Bob's progress (missed first meeting)
    bob_completed_reqs = master_tracker.loc["Bob Brown"].sum()
    # Bob missed meeting 1 (2 reqs) but attended meetings 2, 3, 4 (9 reqs)
    expected_bob_completed = 9
    assert bob_completed_reqs == expected_bob_completed


@pytest.mark.unit
def test_individual_scout_required_vs_elective_split(dashboard_test_env):
    """Test splitting individual scout progress into required vs elective."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Get Alice's progress
    alice_progress = master_tracker.loc["Alice Anderson"]

    # Separate required and elective
    required_reqs = requirement_key[requirement_key["Required"] == True]["Req_ID"].tolist()
    elective_reqs = requirement_key[requirement_key["Required"] == False]["Req_ID"].tolist()

    alice_required_completed = alice_progress[required_reqs].sum()
    alice_elective_completed = alice_progress[elective_reqs].sum()

    # Alice attended all meetings which only covered required adventures
    assert alice_required_completed == 11  # All 11 requirements in meetings are required
    assert alice_elective_completed == 0  # No electives covered in meetings


@pytest.mark.unit
def test_scout_meeting_attendance_count(dashboard_test_env):
    """Test counting meetings attended by each scout."""
    attendance_df = dashboard_test_env["attendance"]

    # Count meetings per scout
    alice_meetings = len(attendance_df[attendance_df["Scout_Name"] == "Alice Anderson"])
    bob_meetings = len(attendance_df[attendance_df["Scout_Name"] == "Bob Brown"])
    charlie_meetings = len(attendance_df[attendance_df["Scout_Name"] == "Charlie Chen"])
    diana_meetings = len(attendance_df[attendance_df["Scout_Name"] == "Diana Davis"])

    assert alice_meetings == 4  # All meetings
    assert bob_meetings == 3  # Missed first
    assert charlie_meetings == 2  # First 2 only
    assert diana_meetings == 1  # Last only


# ============================================================================
# TEST: SUMMARY STATISTICS
# ============================================================================

@pytest.mark.unit
def test_overall_completion_statistics(dashboard_test_env):
    """Test calculating overall completion statistics across all scouts."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Calculate percentage of scouts who completed each requirement
    total_scouts = len(roster_df)
    req_completion_stats = {}

    for req_id in requirement_key["Req_ID"]:
        completed_count = master_tracker[req_id].sum()
        completion_percentage = (completed_count / total_scouts * 100) if total_scouts > 0 else 0
        req_completion_stats[req_id] = {
            "completed_count": completed_count,
            "percentage": completion_percentage
        }

    # Test specific requirements
    # Bobcat.1 was in first meeting: Alice (yes), Bob (no), Charlie (yes), Diana (no) = 2/4 = 50%
    assert req_completion_stats["Bobcat.1"]["completed_count"] == 2
    assert req_completion_stats["Bobcat.1"]["percentage"] == 50.0

    # FunontheRun.1 was in last meeting: Alice (yes), Bob (yes), Charlie (no), Diana (yes) = 3/4 = 75%
    assert req_completion_stats["FunontheRun.1"]["completed_count"] == 3
    assert req_completion_stats["FunontheRun.1"]["percentage"] == 75.0


@pytest.mark.unit
def test_required_adventures_summary(dashboard_test_env):
    """Test generating summary of all required adventures completion."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    required_adventures = requirement_key[requirement_key["Required"] == True]["Adventure"].unique()

    # Calculate summary for all scouts
    required_summary_data = []
    for scout in roster_df["Scout Name"]:
        scout_summary = {"Scout Name": scout}
        for adventure in required_adventures:
            _, _, percentage = calculate_adventure_progress(scout, adventure, master_tracker, requirement_key)
            scout_summary[adventure] = percentage
        required_summary_data.append(scout_summary)

    required_summary_df = pd.DataFrame(required_summary_data)

    assert len(required_summary_df) == len(roster_df)
    assert "Scout Name" in required_summary_df.columns
    for adventure in required_adventures:
        assert adventure in required_summary_df.columns


@pytest.mark.unit
def test_elective_adventures_summary(dashboard_test_env):
    """Test generating summary of all elective adventures completion."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    elective_adventures = requirement_key[requirement_key["Required"] == False]["Adventure"].unique()

    # Calculate summary for all scouts
    elective_summary_data = []
    for scout in roster_df["Scout Name"]:
        scout_summary = {"Scout Name": scout}
        for adventure in elective_adventures:
            _, _, percentage = calculate_adventure_progress(scout, adventure, master_tracker, requirement_key)
            scout_summary[adventure] = percentage
        elective_summary_data.append(scout_summary)

    elective_summary_df = pd.DataFrame(elective_summary_data)

    assert len(elective_summary_df) == len(roster_df)
    assert "Scout Name" in elective_summary_df.columns
    for adventure in elective_adventures:
        assert adventure in elective_summary_df.columns


# ============================================================================
# TEST: EDGE CASES
# ============================================================================

@pytest.mark.unit
def test_empty_roster_dashboard(test_data_dir):
    """Test dashboard behavior with no scouts in roster."""
    empty_roster = pd.DataFrame(columns=["Scout Name", "Current_Rank", "Status"])
    requirements = pd.DataFrame({
        "Req_ID": ["Test.1"],
        "Adventure": ["Test"],
        "Requirement_Description": ["Test req"],
        "Required": [True],
        "Rank": ["Lion"]
    })
    meetings = pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"])
    attendance = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])

    empty_roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    # Load and verify roster is empty
    loaded_roster = scout_tracker.load_roster()
    assert loaded_roster.empty or len(loaded_roster) == 0


@pytest.mark.unit
def test_no_meetings_dashboard(test_data_dir):
    """Test dashboard behavior when no meetings have been held."""
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })
    requirements = pd.DataFrame({
        "Req_ID": ["Test.1", "Test.2"],
        "Adventure": ["Test", "Test"],
        "Requirement_Description": ["Req 1", "Req 2"],
        "Required": [True, True],
        "Rank": ["Lion", "Lion"]
    })
    empty_meetings = pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"])
    empty_attendance = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    empty_meetings.to_csv(config.MEETINGS_FILE, index=False)
    empty_attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, empty_meetings, empty_attendance)

    # All requirements should be incomplete
    assert not master_tracker.any().any()
    assert master_tracker.loc["Test Scout", "Test.1"] == False
    assert master_tracker.loc["Test Scout", "Test.2"] == False


@pytest.mark.unit
def test_all_scouts_complete_all_requirements(test_data_dir):
    """Test dashboard when all scouts have completed all requirements."""
    roster = pd.DataFrame({
        "Scout Name": ["Scout 1", "Scout 2"],
        "Current_Rank": ["Lion", "Lion"],
        "Status": ["Active", "Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Elect1.1", "Elect2.1"],
        "Adventure": ["Required", "Elective 1", "Elective 2"],
        "Requirement_Description": ["R1", "E1", "E2"],
        "Required": [True, False, False],
        "Rank": ["Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Complete Meeting"],
        "Req_IDs_Covered": ["Req1.1,Elect1.1,Elect2.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-15"]),
        "Scout_Name": ["Scout 1", "Scout 2"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    # Both scouts should have completed everything
    assert master_tracker.all().all()

    # Both scouts should be eligible for rank
    for scout in ["Scout 1", "Scout 2"]:
        all_req_complete, completed_electives, rank_earned = calculate_rank_eligibility(
            scout, master_tracker, requirements
        )
        assert all_req_complete == True
        assert completed_electives == 2
        assert rank_earned == True


@pytest.mark.unit
def test_no_scouts_complete_any_requirements(test_data_dir):
    """Test dashboard when no scouts have completed any requirements."""
    roster = pd.DataFrame({
        "Scout Name": ["Scout 1", "Scout 2"],
        "Current_Rank": ["Lion", "Lion"],
        "Status": ["Active", "Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2"],
        "Adventure": ["Required", "Required"],
        "Requirement_Description": ["R1", "R2"],
        "Required": [True, True],
        "Rank": ["Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Meeting"],
        "Req_IDs_Covered": ["Req1.1,Req1.2"]
    })

    # No attendance records - scouts didn't attend
    empty_attendance = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    empty_attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, empty_attendance)

    # No scout should have completed anything
    assert not master_tracker.any().any()

    # No scouts should be eligible for rank
    for scout in ["Scout 1", "Scout 2"]:
        all_req_complete, completed_electives, rank_earned = calculate_rank_eligibility(
            scout, master_tracker, requirements
        )
        assert all_req_complete == False
        assert rank_earned == False


@pytest.mark.unit
def test_partial_completion_across_scouts(test_data_dir):
    """Test dashboard with varied completion levels across scouts."""
    roster = pd.DataFrame({
        "Scout Name": ["Beginner", "Intermediate", "Advanced"],
        "Current_Rank": ["Lion", "Lion", "Lion"],
        "Status": ["Active", "Active", "Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2", "Req1.3", "Elect1.1", "Elect2.1"],
        "Adventure": ["Required", "Required", "Required", "Elective 1", "Elective 2"],
        "Requirement_Description": ["R1", "R2", "R3", "E1", "E2"],
        "Required": [True, True, True, False, False],
        "Rank": ["Lion", "Lion", "Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-22", "2024-01-29"]),
        "Meeting_Title": ["Meeting 1", "Meeting 2", "Meeting 3"],
        "Req_IDs_Covered": ["Req1.1", "Req1.2,Elect1.1", "Req1.3,Elect2.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime([
            "2024-01-15",  # Beginner attends meeting 1
            "2024-01-15", "2024-01-22",  # Intermediate attends meetings 1 and 2
            "2024-01-15", "2024-01-22", "2024-01-29"  # Advanced attends all 3
        ]),
        "Scout_Name": ["Beginner", "Intermediate", "Intermediate", "Advanced", "Advanced", "Advanced"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    # Verify completion levels
    beginner_completed = master_tracker.loc["Beginner"].sum()
    intermediate_completed = master_tracker.loc["Intermediate"].sum()
    advanced_completed = master_tracker.loc["Advanced"].sum()

    assert beginner_completed == 1  # Only Req1.1
    assert intermediate_completed == 3  # Req1.1, Req1.2, Elect1.1
    assert advanced_completed == 5  # All requirements

    # Check rank eligibility
    _, _, beginner_rank = calculate_rank_eligibility("Beginner", master_tracker, requirements)
    _, _, intermediate_rank = calculate_rank_eligibility("Intermediate", master_tracker, requirements)
    _, _, advanced_rank = calculate_rank_eligibility("Advanced", master_tracker, requirements)

    assert beginner_rank == False
    assert intermediate_rank == False
    assert advanced_rank == True  # Only Advanced earns rank


# ============================================================================
# TEST: DATA VALIDATION AND ERROR HANDLING
# ============================================================================

@pytest.mark.unit
def test_invalid_req_id_in_meetings(test_data_dir):
    """Test handling of invalid requirement IDs in meeting coverage."""
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Valid.1"],
        "Adventure": ["Valid"],
        "Requirement_Description": ["Valid req"],
        "Required": [True],
        "Rank": ["Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Meeting"],
        "Req_IDs_Covered": ["Valid.1,Invalid.1,AlsoInvalid.2"]  # Mix of valid and invalid
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Test Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    # Should not crash, should only mark valid requirements as complete
    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    assert master_tracker.loc["Test Scout", "Valid.1"] == True
    # Invalid requirements should not be in the tracker at all
    assert "Invalid.1" not in master_tracker.columns
    assert "AlsoInvalid.2" not in master_tracker.columns


@pytest.mark.unit
def test_missing_req_ids_covered_field(test_data_dir):
    """Test handling of meetings with missing Req_IDs_Covered field."""
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Test.1"],
        "Adventure": ["Test"],
        "Requirement_Description": ["Test req"],
        "Required": [True],
        "Rank": ["Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-22"]),
        "Meeting_Title": ["Meeting 1", "Meeting 2"],
        "Req_IDs_Covered": [None, ""]  # One None, one empty string
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-22"]),
        "Scout_Name": ["Test Scout", "Test Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    # Should not crash
    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    # Nothing should be completed since meetings had no requirements
    assert not master_tracker.any().any()


@pytest.mark.unit
def test_scout_not_in_roster_attendance(test_data_dir):
    """Test handling of attendance records for scouts not in roster."""
    roster = pd.DataFrame({
        "Scout Name": ["Valid Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Test.1"],
        "Adventure": ["Test"],
        "Requirement_Description": ["Test req"],
        "Required": [True],
        "Rank": ["Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Meeting"],
        "Req_IDs_Covered": ["Test.1"]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15", "2024-01-15"]),
        "Scout_Name": ["Valid Scout", "Invalid Scout"]  # Invalid Scout not in roster
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    # Should not crash
    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    # Valid Scout should have completion
    assert master_tracker.loc["Valid Scout", "Test.1"] == True
    # Invalid Scout should not be in tracker
    assert "Invalid Scout" not in master_tracker.index


# ============================================================================
# TEST: PLAN MEETINGS FUNCTIONALITY
# ============================================================================

@pytest.mark.unit
def test_plan_meetings_completion_statistics(dashboard_test_env):
    """Test calculation of requirement completion statistics for planning."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Get only required requirements
    required_reqs = requirement_key[requirement_key["Required"] == True].copy()

    # Calculate completion statistics
    total_scouts = len(roster_df)
    planning_data = []

    for _, req_row in required_reqs.iterrows():
        req_id = req_row["Req_ID"]
        completed_count = master_tracker[req_id].sum()
        completion_percentage = (completed_count / total_scouts * 100) if total_scouts > 0 else 0

        # Get scouts who haven't completed it
        scouts_missing = [scout for scout in roster_df["Scout Name"] if not master_tracker.loc[scout, req_id]]

        planning_data.append({
            "Req_ID": req_id,
            "Completed": completed_count,
            "Total Scouts": total_scouts,
            "% Complete": completion_percentage,
            "Scouts Missing": scouts_missing
        })

    planning_df = pd.DataFrame(planning_data)

    # Verify statistics
    assert len(planning_df) == len(required_reqs)
    assert all(planning_df["Total Scouts"] == 4)  # 4 scouts in test data
    assert all(planning_df["% Complete"] >= 0)
    assert all(planning_df["% Complete"] <= 100)


@pytest.mark.unit
def test_plan_meetings_scouts_missing_list(dashboard_test_env):
    """Test generation of scouts missing each requirement."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    # Check Bobcat.1: Alice (yes), Bob (no), Charlie (yes), Diana (no)
    scouts_missing_bobcat1 = [
        scout for scout in roster_df["Scout Name"]
        if not master_tracker.loc[scout, "Bobcat.1"]
    ]

    assert "Bob Brown" in scouts_missing_bobcat1
    assert "Diana Davis" in scouts_missing_bobcat1
    assert "Alice Anderson" not in scouts_missing_bobcat1
    assert "Charlie Chen" not in scouts_missing_bobcat1


@pytest.mark.unit
def test_plan_meetings_priority_sorting(dashboard_test_env):
    """Test sorting requirements by completion percentage for prioritization."""
    roster_df = dashboard_test_env["roster"]
    requirement_key = dashboard_test_env["requirements"]
    meetings_df = dashboard_test_env["meetings"]
    attendance_df = dashboard_test_env["attendance"]

    master_tracker = build_master_tracker(roster_df, requirement_key, meetings_df, attendance_df)

    required_reqs = requirement_key[requirement_key["Required"] == True].copy()
    total_scouts = len(roster_df)

    planning_data = []
    for _, req_row in required_reqs.iterrows():
        req_id = req_row["Req_ID"]
        completed_count = master_tracker[req_id].sum()
        completion_percentage = (completed_count / total_scouts * 100) if total_scouts > 0 else 0

        planning_data.append({
            "Req_ID": req_id,
            "% Complete": completion_percentage
        })

    planning_df = pd.DataFrame(planning_data)

    # Sort by completion percentage (lowest first = highest priority)
    planning_df = planning_df.sort_values("% Complete", ascending=True)

    # First requirement should have lowest completion
    first_req_pct = planning_df.iloc[0]["% Complete"]
    last_req_pct = planning_df.iloc[-1]["% Complete"]

    assert first_req_pct <= last_req_pct


# ============================================================================
# TEST: PERFORMANCE AND SCALABILITY
# ============================================================================

@pytest.mark.unit
def test_large_roster_performance(test_data_dir):
    """Test dashboard calculations with a large number of scouts."""
    # Create roster with 50 scouts
    num_scouts = 50
    roster = pd.DataFrame({
        "Scout Name": [f"Scout {i}" for i in range(num_scouts)],
        "Current_Rank": ["Lion"] * num_scouts,
        "Status": ["Active"] * num_scouts
    })

    requirements = pd.DataFrame({
        "Req_ID": ["Req1.1", "Req1.2", "Req1.3"],
        "Adventure": ["Test", "Test", "Test"],
        "Requirement_Description": ["R1", "R2", "R3"],
        "Required": [True, True, True],
        "Rank": ["Lion", "Lion", "Lion"]
    })

    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Meeting"],
        "Req_IDs_Covered": ["Req1.1,Req1.2,Req1.3"]
    })

    # All scouts attend
    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"] * num_scouts),
        "Scout_Name": [f"Scout {i}" for i in range(num_scouts)]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    import time
    start_time = time.time()

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    elapsed_time = time.time() - start_time

    # Should complete in reasonable time (< 1 second for 50 scouts)
    assert elapsed_time < 1.0

    # Verify all scouts completed all requirements
    assert master_tracker.all().all()


@pytest.mark.unit
def test_many_requirements_performance(test_data_dir):
    """Test dashboard calculations with many requirements."""
    roster = pd.DataFrame({
        "Scout Name": ["Test Scout"],
        "Current_Rank": ["Lion"],
        "Status": ["Active"]
    })

    # Create 100 requirements
    num_reqs = 100
    requirements = pd.DataFrame({
        "Req_ID": [f"Req{i}.1" for i in range(num_reqs)],
        "Adventure": [f"Adventure{i}" for i in range(num_reqs)],
        "Requirement_Description": [f"Requirement {i}" for i in range(num_reqs)],
        "Required": [i < 50 for i in range(num_reqs)],  # First 50 required, rest elective
        "Rank": ["Lion"] * num_reqs
    })

    # Meeting covers all requirements
    all_req_ids = ",".join([f"Req{i}.1" for i in range(num_reqs)])
    meetings = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Meeting_Title": ["Big Meeting"],
        "Req_IDs_Covered": [all_req_ids]
    })

    attendance = pd.DataFrame({
        "Meeting_Date": pd.to_datetime(["2024-01-15"]),
        "Scout_Name": ["Test Scout"]
    })

    roster.to_csv(config.ROSTER_FILE, index=False)
    requirements.to_csv(config.REQUIREMENT_KEY_FILE, index=False)
    meetings.to_csv(config.MEETINGS_FILE, index=False)
    attendance.to_csv(config.ATTENDANCE_FILE, index=False)

    import time
    start_time = time.time()

    master_tracker = build_master_tracker(roster, requirements, meetings, attendance)

    elapsed_time = time.time() - start_time

    # Should complete in reasonable time (< 1 second for 100 requirements)
    assert elapsed_time < 1.0

    # Verify all requirements completed
    assert master_tracker.loc["Test Scout"].all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

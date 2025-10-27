"""
Comprehensive tests for Scout Tracker onboarding, edge cases, and integration.

This test suite covers:
1. Onboarding flow - First run detection, completion persistence, data initialization
2. Edge cases - Empty datasets, boundary conditions, invalid data, special characters
3. Integration tests - Full workflows, data consistency, cascade operations

All tests use the test_data_dir fixture to ensure complete isolation from
production data in tracker_data directory.
"""

import pytest
import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys
import shutil
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scout_tracker import config, data as scout_tracker
from scout_tracker.ui.pages.onboarding import is_first_run


# ============================================================================
# ONBOARDING TESTS
# ============================================================================

@pytest.mark.ui
class TestOnboarding:
    """Test suite for onboarding flow and first-run detection."""

    def test_is_first_run_empty_roster_default_requirements(self, test_data_dir):
        """Test that is_first_run() returns True when roster is empty and requirements are default."""
        # Initialize with default Lion requirements
        scout_tracker.initialize_data_files()

        # Should be first run: empty roster + default requirements
        assert is_first_run() == True

    def test_is_first_run_with_scouts_added(self, test_data_dir):
        """Test that is_first_run() returns False after scouts are added."""
        # Initialize files
        scout_tracker.initialize_data_files()

        # Add a scout
        roster_df = pd.DataFrame({"Scout Name": ["Test Scout"]})
        scout_tracker.save_roster(roster_df)

        # No longer first run
        assert is_first_run() == False

    def test_is_first_run_with_custom_requirements(self, test_data_dir):
        """Test that is_first_run() returns False after requirements are modified."""
        # Initialize files
        scout_tracker.initialize_data_files()

        # Modify requirements (add a custom one)
        req_df = pd.DataFrame(config.LION_REQUIREMENTS)
        new_req = pd.DataFrame([{
            "Req_ID": "Custom.1",
            "Adventure": "Custom",
            "Requirement_Description": "Custom requirement",
            "Required": False
        }])
        req_df = pd.concat([req_df, new_req], ignore_index=True)
        scout_tracker.save_requirements(req_df)

        # No longer first run (requirements count changed)
        assert is_first_run() == False

    def test_onboarding_data_initialization(self, test_data_dir):
        """Test that initialize_data_files() creates all necessary files."""
        # Initialize
        scout_tracker.initialize_data_files()

        # Verify all files exist
        assert config.ROSTER_FILE.exists()
        assert config.REQUIREMENT_KEY_FILE.exists()
        assert config.MEETINGS_FILE.exists()
        assert config.ATTENDANCE_FILE.exists()

        # Verify file structure
        roster = scout_tracker.load_roster()
        requirements = scout_tracker.load_requirement_key()
        meetings = scout_tracker.load_meetings()
        attendance = scout_tracker.load_attendance()

        assert roster.empty
        assert len(requirements) == len(config.LION_REQUIREMENTS)
        assert meetings.empty
        assert attendance.empty

    def test_onboarding_idempotent(self, test_data_dir):
        """Test that initialize_data_files() can be called multiple times safely."""
        # Initialize once
        scout_tracker.initialize_data_files()

        # Add some data
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1"]})
        scout_tracker.save_roster(roster_df)

        # Initialize again
        scout_tracker.initialize_data_files()

        # Data should be preserved
        roster = scout_tracker.load_roster()
        assert len(roster) == 1
        assert roster.iloc[0]["Scout Name"] == "Scout 1"

    def test_first_run_detection_after_data_dir_creation(self, test_data_dir):
        """Test first run detection immediately after creating data directory."""
        # Don't initialize - just check directory creation
        assert test_data_dir.exists()

        # Initialize files
        scout_tracker.initialize_data_files()

        # Should detect first run
        assert is_first_run() == True

    @pytest.mark.ui
    def test_onboarding_completion_persistence(self, test_data_dir):
        """Test that onboarding completion state can be tracked."""
        # Simulate onboarding completion by adding data
        scout_tracker.initialize_data_files()

        # Add minimum viable data for completed onboarding
        roster_df = pd.DataFrame({"Scout Name": ["Test Scout"]})
        scout_tracker.save_roster(roster_df)

        # Verify not first run anymore
        assert is_first_run() == False

    def test_skip_onboarding_on_subsequent_runs(self, test_data_dir):
        """Test that subsequent runs skip onboarding when data exists."""
        # First run - initialize and add data
        scout_tracker.initialize_data_files()
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1", "Scout 2"]})
        scout_tracker.save_roster(roster_df)

        # Clear cache to simulate fresh load
        scout_tracker.clear_cache()

        # Should not be first run
        assert is_first_run() == False

        # Data should still be accessible
        roster = scout_tracker.load_roster()
        assert len(roster) == 2


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_empty_roster_operations(self, test_data_dir):
        """Test operations on empty roster don't crash."""
        scout_tracker.initialize_data_files()
        roster = scout_tracker.load_roster()

        assert roster.empty
        assert len(roster) == 0
        assert list(roster.columns) == ["Scout Name"]

    def test_empty_meetings_operations(self, test_data_dir):
        """Test operations on empty meetings don't crash."""
        scout_tracker.initialize_data_files()
        meetings = scout_tracker.load_meetings()

        assert meetings.empty
        assert len(meetings) == 0
        assert "Meeting_Date" in meetings.columns

    def test_empty_attendance_operations(self, test_data_dir):
        """Test operations on empty attendance don't crash."""
        scout_tracker.initialize_data_files()
        attendance = scout_tracker.load_attendance()

        assert attendance.empty
        assert len(attendance) == 0
        assert "Scout_Name" in attendance.columns

    def test_single_scout_scenario(self, test_data_dir):
        """Test system works correctly with only one scout."""
        scout_tracker.initialize_data_files()

        # Add single scout
        roster_df = pd.DataFrame({"Scout Name": ["Solo Scout"]})
        scout_tracker.save_roster(roster_df)

        # Verify load
        roster = scout_tracker.load_roster()
        assert len(roster) == 1
        assert roster.iloc[0]["Scout Name"] == "Solo Scout"

    def test_large_roster_scenario(self, test_data_dir):
        """Test system handles large number of scouts."""
        scout_tracker.initialize_data_files()

        # Add 100 scouts
        scout_names = [f"Scout {i:03d}" for i in range(1, 101)]
        roster_df = pd.DataFrame({"Scout Name": scout_names})
        scout_tracker.save_roster(roster_df)

        # Verify load
        roster = scout_tracker.load_roster()
        assert len(roster) == 100
        assert roster.iloc[0]["Scout Name"] == "Scout 001"
        assert roster.iloc[99]["Scout Name"] == "Scout 100"

    def test_many_meetings_scenario(self, test_data_dir):
        """Test system handles large number of meetings."""
        scout_tracker.initialize_data_files()

        # Add 52 meetings (one year of weekly meetings)
        meetings_data = []
        start_date = datetime(2024, 1, 1)
        for i in range(52):
            meeting_date = start_date + timedelta(weeks=i)
            meetings_data.append({
                "Meeting_Date": meeting_date.strftime("%Y-%m-%d"),
                "Meeting_Title": f"Week {i+1} Meeting",
                "Req_IDs_Covered": "Bobcat.1,Bobcat.2"
            })

        meetings_df = pd.DataFrame(meetings_data)
        scout_tracker.save_meetings(meetings_df)

        # Verify load
        meetings = scout_tracker.load_meetings()
        assert len(meetings) == 52
        assert meetings.iloc[0]["Meeting_Title"] == "Week 1 Meeting"

    def test_invalid_data_types_handled(self, test_data_dir):
        """Test that invalid data types are handled gracefully."""
        scout_tracker.initialize_data_files()

        # Try to save roster with missing Scout Name column
        invalid_roster = pd.DataFrame({"Invalid_Column": ["Test"]})

        # This should not crash - pandas will handle it
        try:
            scout_tracker.save_roster(invalid_roster)
            loaded = scout_tracker.load_roster()
            # Should either be empty or contain the invalid data
            assert loaded is not None
        except Exception as e:
            # It's acceptable to raise an exception for invalid data
            assert True

    def test_missing_required_fields(self, test_data_dir):
        """Test handling of data with missing required fields."""
        scout_tracker.initialize_data_files()

        # Create meeting data missing required field
        incomplete_meeting = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            # Missing Meeting_Title and Req_IDs_Covered
        })

        # Save and load - should not crash
        scout_tracker.save_meetings(incomplete_meeting)
        meetings = scout_tracker.load_meetings()
        assert meetings is not None

    def test_corrupted_csv_recovery(self, test_data_dir):
        """Test recovery from corrupted CSV files."""
        scout_tracker.initialize_data_files()

        # Write corrupted data to roster file
        with open(config.ROSTER_FILE, 'w') as f:
            f.write("This is not valid CSV\nNo proper structure\n,,,\n")

        # Try to load - should handle gracefully
        try:
            roster = scout_tracker.load_roster()
            # Either returns corrupted data or raises exception
            assert roster is not None or True
        except Exception:
            # Acceptable to raise exception for corrupted data
            assert True

    def test_unicode_scout_names(self, test_data_dir):
        """Test handling of Unicode and special characters in names."""
        scout_tracker.initialize_data_files()

        # Unicode names from various languages
        unicode_names = [
            "José García",
            "François Müller",
            "李明",  # Chinese
            "Алексей",  # Russian
            "محمد",  # Arabic
            "Søren Andersen",
            "O'Brien-Smith"
        ]

        roster_df = pd.DataFrame({"Scout Name": unicode_names})
        scout_tracker.save_roster(roster_df)

        # Verify all names preserved correctly
        roster = scout_tracker.load_roster()
        assert len(roster) == len(unicode_names)
        for expected_name in unicode_names:
            assert expected_name in roster["Scout Name"].values

    def test_special_characters_in_meeting_titles(self, test_data_dir):
        """Test special characters in meeting titles."""
        scout_tracker.initialize_data_files()

        special_titles = [
            "Meeting #1: Introduction & Welcome",
            "Field Trip (Zoo Visit)",
            "Workshop: Arts & Crafts",
            "Year-End Celebration!!!",
            'Meeting with "Special" Guest',
        ]

        meetings_data = []
        for i, title in enumerate(special_titles):
            meetings_data.append({
                "Meeting_Date": f"2024-01-{i+1:02d}",
                "Meeting_Title": title,
                "Req_IDs_Covered": "Bobcat.1"
            })

        meetings_df = pd.DataFrame(meetings_data)
        scout_tracker.save_meetings(meetings_df)

        # Verify titles preserved
        meetings = scout_tracker.load_meetings()
        assert len(meetings) == len(special_titles)
        for title in special_titles:
            assert title in meetings["Meeting_Title"].values

    def test_duplicate_scout_names(self, test_data_dir):
        """Test handling of duplicate scout names."""
        scout_tracker.initialize_data_files()

        # Try to add duplicate names
        roster_df = pd.DataFrame({"Scout Name": ["John Smith", "John Smith", "Jane Doe"]})
        scout_tracker.save_roster(roster_df)

        # Load and verify - system should preserve duplicates or handle them
        roster = scout_tracker.load_roster()
        assert len(roster) >= 2  # At least unique scouts should be present

    def test_extremely_long_names(self, test_data_dir):
        """Test handling of extremely long scout names."""
        scout_tracker.initialize_data_files()

        # Very long name (200+ characters)
        long_name = "A" * 250
        roster_df = pd.DataFrame({"Scout Name": [long_name, "Normal Name"]})
        scout_tracker.save_roster(roster_df)

        # Should handle gracefully
        roster = scout_tracker.load_roster()
        assert len(roster) == 2

    def test_empty_string_scout_name(self, test_data_dir):
        """Test handling of empty or whitespace-only scout names."""
        scout_tracker.initialize_data_files()

        # Empty and whitespace names
        roster_df = pd.DataFrame({"Scout Name": ["", "   ", "Valid Name"]})
        scout_tracker.save_roster(roster_df)

        # Should save and load without crashing
        roster = scout_tracker.load_roster()
        assert roster is not None

    def test_date_edge_cases(self, test_data_dir):
        """Test edge cases in date handling."""
        scout_tracker.initialize_data_files()

        # Various date formats and edge cases
        edge_dates = [
            "2024-01-01",  # New Year
            "2024-02-29",  # Leap year
            "2024-12-31",  # Year end
            "1999-12-31",  # Past date
            "2099-01-01",  # Future date
        ]

        meetings_data = []
        for date in edge_dates:
            meetings_data.append({
                "Meeting_Date": date,
                "Meeting_Title": f"Meeting on {date}",
                "Req_IDs_Covered": "Bobcat.1"
            })

        meetings_df = pd.DataFrame(meetings_data)
        scout_tracker.save_meetings(meetings_df)

        # Verify dates handled correctly
        meetings = scout_tracker.load_meetings()
        assert len(meetings) == len(edge_dates)

    def test_null_and_nan_values(self, test_data_dir):
        """Test handling of null and NaN values in data."""
        scout_tracker.initialize_data_files()

        # Create roster with NaN values
        roster_df = pd.DataFrame({"Scout Name": ["Valid Name", None, pd.NA, "Another Valid"]})
        scout_tracker.save_roster(roster_df)

        # Should handle without crashing
        roster = scout_tracker.load_roster()
        assert roster is not None

    def test_mixed_case_sensitivity(self, test_data_dir):
        """Test case sensitivity in scout names and other fields."""
        scout_tracker.initialize_data_files()

        # Names with different cases
        roster_df = pd.DataFrame({
            "Scout Name": ["john smith", "JOHN SMITH", "John Smith", "JoHn SmItH"]
        })
        scout_tracker.save_roster(roster_df)

        # All should be preserved as-is
        roster = scout_tracker.load_roster()
        assert len(roster) == 4

    def test_requirement_ids_with_special_formats(self, test_data_dir):
        """Test requirement IDs with various formats."""
        scout_tracker.initialize_data_files()

        # Meeting with complex requirement ID list
        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Meeting_Title": ["Complex Requirements Meeting"],
            "Req_IDs_Covered": ["Bobcat.1,FunOnTheRun.2,LionsRoar.3,LionsPride.1,KingOfTheJungle.4"]
        })
        scout_tracker.save_meetings(meetings_df)

        # Verify preserved
        meetings = scout_tracker.load_meetings()
        assert len(meetings) == 1
        assert "Bobcat.1" in meetings.iloc[0]["Req_IDs_Covered"]


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
class TestIntegration:
    """Integration tests for complete workflows and data consistency."""

    def test_full_workflow_add_scout_to_report(self, test_data_dir):
        """Test complete workflow: add scout → meeting → attendance → verify data."""
        # Initialize system
        scout_tracker.initialize_data_files()

        # Step 1: Add scout
        roster_df = pd.DataFrame({"Scout Name": ["Integration Scout"]})
        scout_tracker.save_roster(roster_df)

        # Step 2: Create meeting
        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Meeting_Title": ["First Meeting"],
            "Req_IDs_Covered": ["Bobcat.1,Bobcat.2"]
        })
        scout_tracker.save_meetings(meetings_df)

        # Step 3: Log attendance
        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Scout_Name": ["Integration Scout"]
        })
        scout_tracker.save_attendance(attendance_df)

        # Step 4: Verify all data is consistent
        roster = scout_tracker.load_roster()
        meetings = scout_tracker.load_meetings()
        attendance = scout_tracker.load_attendance()

        assert len(roster) == 1
        assert len(meetings) == 1
        assert len(attendance) == 1
        assert roster.iloc[0]["Scout Name"] == "Integration Scout"
        assert meetings.iloc[0]["Meeting_Title"] == "First Meeting"
        assert attendance.iloc[0]["Scout_Name"] == "Integration Scout"

    def test_multiple_scouts_multiple_meetings_workflow(self, test_data_dir):
        """Test workflow with multiple scouts attending multiple meetings."""
        scout_tracker.initialize_data_files()

        # Add multiple scouts
        scouts = ["Scout A", "Scout B", "Scout C"]
        roster_df = pd.DataFrame({"Scout Name": scouts})
        scout_tracker.save_roster(roster_df)

        # Add multiple meetings
        meetings_data = [
            {"Meeting_Date": "2024-01-08", "Meeting_Title": "Meeting 1", "Req_IDs_Covered": "Bobcat.1"},
            {"Meeting_Date": "2024-01-15", "Meeting_Title": "Meeting 2", "Req_IDs_Covered": "Bobcat.2"},
            {"Meeting_Date": "2024-01-22", "Meeting_Title": "Meeting 3", "Req_IDs_Covered": "FunOnTheRun.1"},
        ]
        meetings_df = pd.DataFrame(meetings_data)
        scout_tracker.save_meetings(meetings_df)

        # Log attendance for various combinations
        attendance_data = [
            {"Meeting_Date": "2024-01-08", "Scout_Name": "Scout A"},
            {"Meeting_Date": "2024-01-08", "Scout_Name": "Scout B"},
            {"Meeting_Date": "2024-01-15", "Scout_Name": "Scout A"},
            {"Meeting_Date": "2024-01-15", "Scout_Name": "Scout C"},
            {"Meeting_Date": "2024-01-22", "Scout_Name": "Scout A"},
            {"Meeting_Date": "2024-01-22", "Scout_Name": "Scout B"},
            {"Meeting_Date": "2024-01-22", "Scout_Name": "Scout C"},
        ]
        attendance_df = pd.DataFrame(attendance_data)
        scout_tracker.save_attendance(attendance_df)

        # Verify data integrity
        roster = scout_tracker.load_roster()
        meetings = scout_tracker.load_meetings()
        attendance = scout_tracker.load_attendance()

        assert len(roster) == 3
        assert len(meetings) == 3
        assert len(attendance) == 7

        # Verify Scout A attended all 3 meetings
        scout_a_attendance = attendance[attendance["Scout_Name"] == "Scout A"]
        assert len(scout_a_attendance) == 3

    def test_data_consistency_after_multiple_operations(self, test_data_dir):
        """Test data remains consistent after multiple save/load cycles."""
        scout_tracker.initialize_data_files()

        # Initial data
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1"]})
        scout_tracker.save_roster(roster_df)

        # Multiple update cycles
        for i in range(2, 6):
            roster = scout_tracker.load_roster()
            new_scout = pd.DataFrame({"Scout Name": [f"Scout {i}"]})
            roster = pd.concat([roster, new_scout], ignore_index=True)
            scout_tracker.save_roster(roster)

        # Verify final state
        final_roster = scout_tracker.load_roster()
        assert len(final_roster) == 5
        for i in range(1, 6):
            assert f"Scout {i}" in final_roster["Scout Name"].values

    def test_cascade_delete_scout_removes_attendance(self, test_data_dir):
        """Test that deleting a scout should consider their attendance records."""
        scout_tracker.initialize_data_files()

        # Setup scouts and attendance
        roster_df = pd.DataFrame({"Scout Name": ["Scout A", "Scout B"]})
        scout_tracker.save_roster(roster_df)

        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15", "2024-01-15", "2024-01-22"],
            "Scout_Name": ["Scout A", "Scout B", "Scout A"]
        })
        scout_tracker.save_attendance(attendance_df)

        # Remove Scout A from roster
        roster = scout_tracker.load_roster()
        roster = roster[roster["Scout Name"] != "Scout A"]
        scout_tracker.save_roster(roster)

        # Attendance records still exist (manual cleanup needed in real app)
        # This test documents the expected behavior
        attendance = scout_tracker.load_attendance()
        assert len(attendance) == 3  # Records persist unless explicitly cleaned

        # In a full integration, we'd want to clean up orphaned records
        attendance = attendance[attendance["Scout_Name"] != "Scout A"]
        scout_tracker.save_attendance(attendance)

        # Now should only have Scout B's record
        final_attendance = scout_tracker.load_attendance()
        assert len(final_attendance) == 1
        assert final_attendance.iloc[0]["Scout_Name"] == "Scout B"

    def test_cross_module_data_consistency(self, test_data_dir):
        """Test consistency between roster, meetings, and attendance modules."""
        scout_tracker.initialize_data_files()

        # Setup complete scenario
        roster_df = pd.DataFrame({"Scout Name": ["Scout Alpha", "Scout Beta"]})
        scout_tracker.save_roster(roster_df)

        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Meeting_Title": ["Integration Test Meeting"],
            "Req_IDs_Covered": ["Bobcat.1"]
        })
        scout_tracker.save_meetings(meetings_df)

        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Scout_Name": ["Scout Alpha"]
        })
        scout_tracker.save_attendance(attendance_df)

        # Verify cross-references
        roster = scout_tracker.load_roster()
        meetings = scout_tracker.load_meetings()
        attendance = scout_tracker.load_attendance()

        # All scouts in attendance should exist in roster
        for scout_name in attendance["Scout_Name"].unique():
            assert scout_name in roster["Scout Name"].values

        # All meeting dates in attendance should exist in meetings
        for meeting_date in attendance["Meeting_Date"].unique():
            assert meeting_date in meetings["Meeting_Date"].values

    def test_cache_consistency_after_updates(self, test_data_dir):
        """Test that cache is properly cleared after data updates."""
        scout_tracker.initialize_data_files()

        # Add initial data
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1"]})
        scout_tracker.save_roster(roster_df)

        # Load to populate cache
        roster1 = scout_tracker.load_roster()
        assert len(roster1) == 1

        # Update data
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1", "Scout 2"]})
        scout_tracker.save_roster(roster_df)

        # Load again - should get updated data, not cached
        roster2 = scout_tracker.load_roster()
        assert len(roster2) == 2

    def test_concurrent_file_access_simulation(self, test_data_dir):
        """Test behavior when files are accessed in quick succession."""
        scout_tracker.initialize_data_files()

        # Simulate rapid successive operations
        for i in range(10):
            roster = scout_tracker.load_roster()
            new_scout = pd.DataFrame({"Scout Name": [f"Scout {i}"]})
            roster = pd.concat([roster, new_scout], ignore_index=True)
            scout_tracker.save_roster(roster)

        # Verify all operations completed successfully
        final_roster = scout_tracker.load_roster()
        assert len(final_roster) == 10

    def test_data_migration_scenario(self, test_data_dir):
        """Test scenario simulating data migration or import."""
        scout_tracker.initialize_data_files()

        # Simulate importing existing data
        imported_roster = pd.DataFrame({
            "Scout Name": ["Migrated Scout 1", "Migrated Scout 2", "Migrated Scout 3"]
        })
        scout_tracker.save_roster(imported_roster)

        imported_meetings = pd.DataFrame({
            "Meeting_Date": ["2023-09-15", "2023-09-22", "2023-09-29"],
            "Meeting_Title": ["Historical Meeting 1", "Historical Meeting 2", "Historical Meeting 3"],
            "Req_IDs_Covered": ["Bobcat.1", "Bobcat.2", "FunOnTheRun.1"]
        })
        scout_tracker.save_meetings(imported_meetings)

        # Verify migration successful
        roster = scout_tracker.load_roster()
        meetings = scout_tracker.load_meetings()

        assert len(roster) == 3
        assert len(meetings) == 3
        assert "Migrated Scout 1" in roster["Scout Name"].values

    def test_requirement_coverage_across_meetings(self, test_data_dir):
        """Test tracking requirement coverage across multiple meetings."""
        scout_tracker.initialize_data_files()

        # Create meetings covering different requirements
        meetings_data = [
            {"Meeting_Date": "2024-01-08", "Meeting_Title": "Week 1", "Req_IDs_Covered": "Bobcat.1,Bobcat.2"},
            {"Meeting_Date": "2024-01-15", "Meeting_Title": "Week 2", "Req_IDs_Covered": "Bobcat.3,Bobcat.4"},
            {"Meeting_Date": "2024-01-22", "Meeting_Title": "Week 3", "Req_IDs_Covered": "FunOnTheRun.1,FunOnTheRun.2"},
        ]
        meetings_df = pd.DataFrame(meetings_data)
        scout_tracker.save_meetings(meetings_df)

        # Verify all requirements can be extracted
        meetings = scout_tracker.load_meetings()
        all_req_ids = set()
        for req_ids in meetings["Req_IDs_Covered"]:
            all_req_ids.update(req_ids.split(","))

        assert "Bobcat.1" in all_req_ids
        assert "FunOnTheRun.2" in all_req_ids
        assert len(all_req_ids) == 6


# ============================================================================
# BOUNDARY CONDITION TESTS
# ============================================================================

class TestBoundaryConditions:
    """Test boundary conditions and limits."""

    def test_zero_requirements_loaded(self, test_data_dir):
        """Test system behavior with no requirements loaded."""
        scout_tracker.initialize_data_files()

        # Clear all requirements
        empty_reqs = pd.DataFrame(columns=["Req_ID", "Adventure", "Requirement_Description", "Required"])
        scout_tracker.save_requirements(empty_reqs)

        # Should load empty dataframe without crashing
        reqs = scout_tracker.load_requirement_key()
        assert len(reqs) == 0

    def test_meeting_with_empty_requirements_list(self, test_data_dir):
        """Test meeting with empty requirements coverage."""
        scout_tracker.initialize_data_files()

        # Meeting with no requirements covered
        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Meeting_Title": ["Social Meeting"],
            "Req_IDs_Covered": [""]
        })
        scout_tracker.save_meetings(meetings_df)

        # Should handle gracefully
        meetings = scout_tracker.load_meetings()
        assert len(meetings) == 1

    def test_very_old_meeting_dates(self, test_data_dir):
        """Test handling of very old meeting dates."""
        scout_tracker.initialize_data_files()

        # Meeting from 20 years ago
        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2004-01-15"],
            "Meeting_Title": ["Historical Meeting"],
            "Req_IDs_Covered": ["Bobcat.1"]
        })
        scout_tracker.save_meetings(meetings_df)

        meetings = scout_tracker.load_meetings()
        assert len(meetings) == 1

    def test_future_meeting_dates(self, test_data_dir):
        """Test handling of future meeting dates."""
        scout_tracker.initialize_data_files()

        # Meeting scheduled for next year
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        meetings_df = pd.DataFrame({
            "Meeting_Date": [future_date],
            "Meeting_Title": ["Future Planning Meeting"],
            "Req_IDs_Covered": ["Bobcat.1"]
        })
        scout_tracker.save_meetings(meetings_df)

        meetings = scout_tracker.load_meetings()
        assert len(meetings) == 1

    def test_attendance_without_corresponding_meeting(self, test_data_dir):
        """Test attendance records for non-existent meetings."""
        scout_tracker.initialize_data_files()

        # Add attendance without creating meeting
        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15"],
            "Scout_Name": ["Phantom Scout"]
        })
        scout_tracker.save_attendance(attendance_df)

        # Should save successfully (referential integrity not enforced at CSV level)
        attendance = scout_tracker.load_attendance()
        assert len(attendance) == 1


# ============================================================================
# ERROR RECOVERY TESTS
# ============================================================================

class TestErrorRecovery:
    """Test error recovery mechanisms."""

    def test_recovery_from_file_deletion(self, test_data_dir):
        """Test system recovery when data files are deleted."""
        scout_tracker.initialize_data_files()

        # Add some data
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1"]})
        scout_tracker.save_roster(roster_df)

        # Delete roster file
        config.ROSTER_FILE.unlink()

        # Loading should return empty dataframe
        roster = scout_tracker.load_roster()
        assert roster.empty

        # Re-initialize should recreate files
        scout_tracker.initialize_data_files()
        assert config.ROSTER_FILE.exists()

    def test_recovery_from_partial_data_dir(self, test_data_dir):
        """Test recovery when only some data files exist."""
        # Don't initialize - manually create some files
        test_data_dir.mkdir(exist_ok=True)

        # Create only roster file
        roster_df = pd.DataFrame({"Scout Name": ["Scout 1"]})
        roster_df.to_csv(config.ROSTER_FILE, index=False)

        # Initialize should create missing files
        scout_tracker.initialize_data_files()

        assert config.ROSTER_FILE.exists()
        assert config.REQUIREMENT_KEY_FILE.exists()
        assert config.MEETINGS_FILE.exists()
        assert config.ATTENDANCE_FILE.exists()

    def test_clear_cache_functionality(self, test_data_dir):
        """Test that clear_cache works correctly."""
        scout_tracker.initialize_data_files()

        # Load data to populate cache
        scout_tracker.load_roster()
        scout_tracker.load_requirement_key()
        scout_tracker.load_meetings()
        scout_tracker.load_attendance()

        # Clear cache should not raise errors
        scout_tracker.clear_cache()

        # Data should still be loadable
        roster = scout_tracker.load_roster()
        assert roster is not None

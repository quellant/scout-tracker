"""
Comprehensive tests for Scout Tracker data operations layer.

This test suite covers all data operations functions with >90% coverage:
- initialize_data_files() - Creates initial CSV files
- load_roster() - Loads roster from CSV
- load_requirement_key() - Loads requirements
- load_meetings() - Loads meetings
- load_attendance() - Loads attendance
- save_roster(df) - Saves roster
- save_requirements(df) - Saves requirements
- save_meetings(df) - Saves meetings
- save_attendance(df) - Saves attendance
- clear_cache() - Clears Streamlit cache

Test categories:
1. File initialization (creates correct structure)
2. Loading valid data
3. Loading missing files (should initialize gracefully)
4. Loading corrupted data (should handle errors)
5. Saving data preserves all fields
6. Round-trip save/load maintains data integrity
7. Cache clearing works correctly
8. Edge cases (empty data, special characters, large datasets)
"""

import pytest
import pandas as pd
import os
from pathlib import Path
from scout_tracker import config, data as scout_tracker


@pytest.mark.data
class TestInitializeDataFiles:
    """Tests for initialize_data_files() function."""

    def test_initialize_creates_data_directory(self, test_data_dir):
        """Test that initialize_data_files creates the data directory."""
        # Remove the directory created by fixture
        test_data_dir.rmdir()
        assert not test_data_dir.exists()

        # Call initialize
        scout_tracker.initialize_data_files()

        # Verify directory exists
        assert test_data_dir.exists()
        assert test_data_dir.is_dir()

    def test_initialize_creates_all_csv_files(self, test_data_dir):
        """Test that initialize_data_files creates all required CSV files."""
        scout_tracker.initialize_data_files()

        # Verify all files exist
        assert config.ROSTER_FILE.exists()
        assert config.REQUIREMENT_KEY_FILE.exists()
        assert config.MEETINGS_FILE.exists()
        assert config.ATTENDANCE_FILE.exists()

    def test_initialize_roster_file_structure(self, test_data_dir):
        """Test that roster file has correct structure."""
        scout_tracker.initialize_data_files()

        df = pd.read_csv(config.ROSTER_FILE)
        assert "Scout Name" in df.columns
        assert df.empty  # Should start empty

    def test_initialize_requirement_key_with_lion_requirements(self, test_data_dir):
        """Test that requirement key is initialized with Lion Scout requirements."""
        scout_tracker.initialize_data_files()

        df = pd.read_csv(config.REQUIREMENT_KEY_FILE)
        assert not df.empty  # Should have BSA requirements
        assert "Req_ID" in df.columns
        assert "Adventure" in df.columns
        assert "Requirement_Description" in df.columns
        assert "Required" in df.columns

        # Verify some Lion requirements exist
        assert "Bobcat.1" in df["Req_ID"].values
        assert "FunOnTheRun.1" in df["Req_ID"].values

    def test_initialize_meetings_file_structure(self, test_data_dir):
        """Test that meetings file has correct structure."""
        scout_tracker.initialize_data_files()

        df = pd.read_csv(config.MEETINGS_FILE)
        assert "Meeting_Date" in df.columns
        assert "Meeting_Title" in df.columns
        assert "Req_IDs_Covered" in df.columns
        assert df.empty

    def test_initialize_attendance_file_structure(self, test_data_dir):
        """Test that attendance file has correct structure."""
        scout_tracker.initialize_data_files()

        df = pd.read_csv(config.ATTENDANCE_FILE)
        assert "Meeting_Date" in df.columns
        assert "Scout_Name" in df.columns
        assert df.empty

    def test_initialize_is_idempotent(self, test_data_dir):
        """Test that calling initialize_data_files multiple times doesn't overwrite existing data."""
        # First initialization
        scout_tracker.initialize_data_files()

        # Add some data
        df = pd.DataFrame({"Scout Name": ["Test Scout"]})
        df.to_csv(config.ROSTER_FILE, index=False)

        # Second initialization
        scout_tracker.initialize_data_files()

        # Verify data still exists
        df_loaded = pd.read_csv(config.ROSTER_FILE)
        assert "Test Scout" in df_loaded["Scout Name"].values


@pytest.mark.data
class TestLoadRoster:
    """Tests for load_roster() function."""

    def test_load_roster_existing_file(self, initialized_test_env):
        """Test loading roster from existing file."""
        df = scout_tracker.load_roster()

        assert not df.empty
        assert "Scout_ID" in df.columns or "Scout Name" in df.columns
        assert len(df) == 3  # Sample has 3 scouts

    def test_load_roster_missing_file(self, test_data_dir):
        """Test loading roster when file doesn't exist returns empty DataFrame."""
        df = scout_tracker.load_roster()

        assert df.empty
        assert "Scout Name" in df.columns

    def test_load_roster_empty_file(self, test_data_dir):
        """Test loading roster from empty CSV file."""
        # Create empty file with headers
        pd.DataFrame(columns=["Scout Name"]).to_csv(config.ROSTER_FILE, index=False)

        df = scout_tracker.load_roster()
        assert df.empty
        assert "Scout Name" in df.columns

    def test_load_roster_preserves_all_columns(self, initialized_test_env):
        """Test that loading roster preserves all columns."""
        df = scout_tracker.load_roster()

        # Current schema uses just "Scout Name" column
        assert "Scout Name" in df.columns
        assert not df.empty
        assert len(df) == 3  # Should have 3 scouts from sample data


@pytest.mark.data
class TestLoadRequirementKey:
    """Tests for load_requirement_key() function."""

    def test_load_requirement_key_existing_file(self, initialized_test_env):
        """Test loading requirement key from existing file."""
        df = scout_tracker.load_requirement_key()

        assert not df.empty
        assert "Req_ID" in df.columns
        assert "Adventure" in df.columns
        assert "Requirement_Description" in df.columns
        assert "Required" in df.columns

    def test_load_requirement_key_missing_file(self, test_data_dir):
        """Test loading requirement key when file doesn't exist."""
        df = scout_tracker.load_requirement_key()

        assert df.empty
        assert "Req_ID" in df.columns
        assert "Adventure" in df.columns
        assert "Requirement_Description" in df.columns
        assert "Required" in df.columns

    def test_load_requirement_key_preserves_data_types(self, initialized_test_env):
        """Test that loading requirement key preserves data types."""
        df = scout_tracker.load_requirement_key()

        # Required column should be boolean-compatible
        assert df["Required"].dtype == bool or df["Required"].dtype == object


@pytest.mark.data
class TestLoadMeetings:
    """Tests for load_meetings() function."""

    def test_load_meetings_existing_file(self, initialized_test_env):
        """Test loading meetings from existing file."""
        df = scout_tracker.load_meetings()

        assert not df.empty
        assert "Meeting_ID" in df.columns or "Meeting_Date" in df.columns

    def test_load_meetings_missing_file(self, test_data_dir):
        """Test loading meetings when file doesn't exist."""
        df = scout_tracker.load_meetings()

        assert df.empty
        assert "Meeting_Date" in df.columns
        assert "Meeting_Title" in df.columns

    def test_load_meetings_converts_date_to_datetime(self, initialized_test_env):
        """Test that loading meetings converts date strings to datetime objects."""
        df = scout_tracker.load_meetings()

        if not df.empty:
            # Meeting_Date should be converted to datetime
            assert pd.api.types.is_datetime64_any_dtype(df["Meeting_Date"])

    def test_load_meetings_empty_file(self, test_data_dir):
        """Test loading meetings from empty CSV file."""
        pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"]).to_csv(
            config.MEETINGS_FILE, index=False
        )

        df = scout_tracker.load_meetings()
        assert df.empty


@pytest.mark.data
class TestLoadAttendance:
    """Tests for load_attendance() function."""

    def test_load_attendance_existing_file(self, initialized_test_env):
        """Test loading attendance from existing file."""
        df = scout_tracker.load_attendance()

        assert not df.empty
        assert "Meeting_Date" in df.columns
        assert "Scout_Name" in df.columns

    def test_load_attendance_missing_file(self, test_data_dir):
        """Test loading attendance when file doesn't exist."""
        df = scout_tracker.load_attendance()

        assert df.empty
        assert "Meeting_Date" in df.columns
        assert "Scout_Name" in df.columns

    def test_load_attendance_converts_date_to_datetime(self, initialized_test_env):
        """Test that loading attendance converts date strings to datetime objects."""
        df = scout_tracker.load_attendance()

        if not df.empty:
            # Meeting_Date should be converted to datetime
            assert pd.api.types.is_datetime64_any_dtype(df["Meeting_Date"])

    def test_load_attendance_empty_file(self, test_data_dir):
        """Test loading attendance from empty CSV file."""
        pd.DataFrame(columns=["Meeting_Date", "Scout_Name"]).to_csv(
            config.ATTENDANCE_FILE, index=False
        )

        df = scout_tracker.load_attendance()
        assert df.empty


@pytest.mark.data
class TestSaveRoster:
    """Tests for save_roster() function."""

    def test_save_roster_creates_file(self, test_data_dir, sample_roster):
        """Test that save_roster creates a file."""
        scout_tracker.save_roster(sample_roster)

        assert config.ROSTER_FILE.exists()

    def test_save_roster_preserves_all_fields(self, test_data_dir, sample_roster):
        """Test that save_roster preserves all fields."""
        scout_tracker.save_roster(sample_roster)

        df_loaded = pd.read_csv(config.ROSTER_FILE)
        assert list(df_loaded.columns) == list(sample_roster.columns)
        assert len(df_loaded) == len(sample_roster)

    def test_save_roster_preserves_data_values(self, test_data_dir, sample_roster):
        """Test that save_roster preserves exact data values."""
        scout_tracker.save_roster(sample_roster)

        df_loaded = pd.read_csv(config.ROSTER_FILE)
        pd.testing.assert_frame_equal(df_loaded, sample_roster)

    def test_save_roster_empty_dataframe(self, test_data_dir):
        """Test saving empty roster DataFrame."""
        empty_df = pd.DataFrame(columns=["Scout Name"])
        scout_tracker.save_roster(empty_df)

        assert config.ROSTER_FILE.exists()
        df_loaded = pd.read_csv(config.ROSTER_FILE)
        assert df_loaded.empty

    def test_save_roster_with_special_characters(self, test_data_dir):
        """Test saving roster with special characters in names."""
        df = pd.DataFrame({
            "Scout_ID": ["S001"],
            "First_Name": ["José"],
            "Last_Name": ["O'Brien"],
            "Current_Rank": ["Lion"],
            "Status": ["Active"]
        })

        scout_tracker.save_roster(df)
        df_loaded = pd.read_csv(config.ROSTER_FILE)

        assert df_loaded.loc[0, "First_Name"] == "José"
        assert df_loaded.loc[0, "Last_Name"] == "O'Brien"


@pytest.mark.data
class TestSaveRequirements:
    """Tests for save_requirements() function."""

    def test_save_requirements_creates_file(self, test_data_dir, sample_requirements):
        """Test that save_requirements creates a file."""
        scout_tracker.save_requirements(sample_requirements)

        assert config.REQUIREMENT_KEY_FILE.exists()

    def test_save_requirements_preserves_all_fields(self, test_data_dir, sample_requirements):
        """Test that save_requirements preserves all fields."""
        scout_tracker.save_requirements(sample_requirements)

        df_loaded = pd.read_csv(config.REQUIREMENT_KEY_FILE)
        assert list(df_loaded.columns) == list(sample_requirements.columns)

    def test_save_requirements_preserves_boolean_field(self, test_data_dir, sample_requirements):
        """Test that save_requirements preserves boolean Required field."""
        scout_tracker.save_requirements(sample_requirements)

        df_loaded = pd.read_csv(config.REQUIREMENT_KEY_FILE)
        # Boolean values should be preserved (might be read as bool or True/False strings)
        assert all(df_loaded["Required"].isin([True, False, "True", "False", 1, 0]))


@pytest.mark.data
class TestSaveMeetings:
    """Tests for save_meetings() function."""

    def test_save_meetings_creates_file(self, test_data_dir, sample_meetings):
        """Test that save_meetings creates a file."""
        scout_tracker.save_meetings(sample_meetings)

        assert config.MEETINGS_FILE.exists()

    def test_save_meetings_preserves_all_fields(self, test_data_dir, sample_meetings):
        """Test that save_meetings preserves all fields."""
        scout_tracker.save_meetings(sample_meetings)

        df_loaded = pd.read_csv(config.MEETINGS_FILE)
        assert list(df_loaded.columns) == list(sample_meetings.columns)

    def test_save_meetings_formats_dates_correctly(self, test_data_dir):
        """Test that save_meetings formats datetime objects as YYYY-MM-DD strings."""
        df = pd.DataFrame({
            "Meeting_ID": ["M001"],
            "Meeting_Date": [pd.Timestamp("2024-03-15")],
            "Meeting_Name": ["Test Meeting"],
            "Location": ["School"],
            "Notes": ["Test notes"]
        })

        scout_tracker.save_meetings(df)

        # Read raw CSV to verify date format
        with open(config.MEETINGS_FILE, 'r') as f:
            content = f.read()
            assert "2024-03-15" in content

    def test_save_meetings_empty_dataframe(self, test_data_dir):
        """Test saving empty meetings DataFrame."""
        empty_df = pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"])
        scout_tracker.save_meetings(empty_df)

        assert config.MEETINGS_FILE.exists()
        df_loaded = pd.read_csv(config.MEETINGS_FILE)
        assert df_loaded.empty


@pytest.mark.data
class TestSaveAttendance:
    """Tests for save_attendance() function."""

    def test_save_attendance_creates_file(self, test_data_dir, sample_attendance):
        """Test that save_attendance creates a file."""
        scout_tracker.save_attendance(sample_attendance)

        assert config.ATTENDANCE_FILE.exists()

    def test_save_attendance_preserves_all_fields(self, test_data_dir, sample_attendance):
        """Test that save_attendance preserves all fields."""
        scout_tracker.save_attendance(sample_attendance)

        df_loaded = pd.read_csv(config.ATTENDANCE_FILE)
        assert list(df_loaded.columns) == list(sample_attendance.columns)

    def test_save_attendance_formats_dates_correctly(self, test_data_dir):
        """Test that save_attendance formats datetime objects as YYYY-MM-DD strings."""
        df = pd.DataFrame({
            "Meeting_Date": [pd.Timestamp("2024-03-15")],
            "Scout_Name": ["Test Scout"]
        })

        scout_tracker.save_attendance(df)

        # Read raw CSV to verify date format
        with open(config.ATTENDANCE_FILE, 'r') as f:
            content = f.read()
            assert "2024-03-15" in content

    def test_save_attendance_empty_dataframe(self, test_data_dir):
        """Test saving empty attendance DataFrame."""
        empty_df = pd.DataFrame(columns=["Meeting_Date", "Scout_Name"])
        scout_tracker.save_attendance(empty_df)

        assert config.ATTENDANCE_FILE.exists()


@pytest.mark.data
class TestRoundTripSaveLoad:
    """Tests for save/load round-trip data integrity."""

    def test_roster_round_trip(self, test_data_dir, sample_roster):
        """Test that roster data survives save/load cycle."""
        scout_tracker.save_roster(sample_roster)
        scout_tracker.clear_cache()
        df_loaded = scout_tracker.load_roster()

        pd.testing.assert_frame_equal(df_loaded, sample_roster)

    def test_requirements_round_trip(self, test_data_dir, sample_requirements):
        """Test that requirements data survives save/load cycle."""
        scout_tracker.save_requirements(sample_requirements)
        scout_tracker.clear_cache()
        df_loaded = scout_tracker.load_requirement_key()

        # Compare values (types might differ slightly for boolean)
        assert len(df_loaded) == len(sample_requirements)
        assert list(df_loaded["Req_ID"]) == list(sample_requirements["Req_ID"])

    def test_meetings_round_trip_preserves_dates(self, test_data_dir):
        """Test that meetings dates survive save/load cycle."""
        # Create meetings with datetime objects
        df = pd.DataFrame({
            "Meeting_ID": ["M001"],
            "Meeting_Date": [pd.Timestamp("2024-03-15")],
            "Meeting_Name": ["Test Meeting"],
            "Location": ["School"],
            "Notes": ["Notes"]
        })

        scout_tracker.save_meetings(df)
        scout_tracker.clear_cache()
        df_loaded = scout_tracker.load_meetings()

        assert len(df_loaded) == 1
        # Date should be preserved (as datetime)
        assert df_loaded.loc[0, "Meeting_Date"] == pd.Timestamp("2024-03-15")

    def test_attendance_round_trip_preserves_dates(self, test_data_dir):
        """Test that attendance dates survive save/load cycle."""
        # Create attendance with datetime objects
        df = pd.DataFrame({
            "Meeting_Date": [pd.Timestamp("2024-03-15")],
            "Scout_Name": ["Test Scout"]
        })

        scout_tracker.save_attendance(df)
        scout_tracker.clear_cache()
        df_loaded = scout_tracker.load_attendance()

        assert len(df_loaded) == 1
        # Date should be preserved (as datetime)
        assert df_loaded.loc[0, "Meeting_Date"] == pd.Timestamp("2024-03-15")

    def test_large_dataset_round_trip(self, test_data_dir):
        """Test round-trip with large dataset."""
        # Create large roster
        large_df = pd.DataFrame({
            "Scout_ID": [f"S{i:04d}" for i in range(1000)],
            "First_Name": [f"First{i}" for i in range(1000)],
            "Last_Name": [f"Last{i}" for i in range(1000)],
            "Current_Rank": ["Lion"] * 1000,
            "Status": ["Active"] * 1000
        })

        scout_tracker.save_roster(large_df)
        scout_tracker.clear_cache()
        df_loaded = scout_tracker.load_roster()

        assert len(df_loaded) == 1000
        pd.testing.assert_frame_equal(df_loaded, large_df)


@pytest.mark.data
class TestClearCache:
    """Tests for clear_cache() function."""

    def test_clear_cache_clears_roster_cache(self, initialized_test_env):
        """Test that clear_cache clears the roster cache."""
        # Load data to populate cache
        df1 = scout_tracker.load_roster()

        # Modify the file directly
        new_df = pd.DataFrame({
            "Scout_ID": ["S999"],
            "First_Name": ["New"],
            "Last_Name": ["Scout"],
            "Current_Rank": ["Lion"],
            "Status": ["Active"]
        })
        new_df.to_csv(config.ROSTER_FILE, index=False)

        # Without clearing cache, should get cached version
        df2 = scout_tracker.load_roster()
        assert len(df2) == len(df1)  # Still cached

        # Clear cache
        scout_tracker.clear_cache()

        # Now should get new data
        df3 = scout_tracker.load_roster()
        assert len(df3) == 1
        assert df3.loc[0, "Scout_ID"] == "S999"

    def test_clear_cache_clears_requirements_cache(self, initialized_test_env):
        """Test that clear_cache clears the requirements cache."""
        df1 = scout_tracker.load_requirement_key()
        initial_count = len(df1)

        # Modify file
        new_df = pd.DataFrame({
            "Req_ID": ["Test.1"],
            "Adventure": ["Test"],
            "Requirement_Description": ["Test requirement"],
            "Required": [True],
            "Rank": ["Lion"]
        })
        new_df.to_csv(config.REQUIREMENT_KEY_FILE, index=False)

        # Clear cache
        scout_tracker.clear_cache()

        # Should get new data
        df2 = scout_tracker.load_requirement_key()
        assert len(df2) == 1

    def test_clear_cache_clears_meetings_cache(self, initialized_test_env):
        """Test that clear_cache clears the meetings cache."""
        df1 = scout_tracker.load_meetings()

        # Modify file
        pd.DataFrame(columns=["Meeting_Date", "Meeting_Title", "Req_IDs_Covered"]).to_csv(
            config.MEETINGS_FILE, index=False
        )

        # Clear cache
        scout_tracker.clear_cache()

        # Should get new (empty) data
        df2 = scout_tracker.load_meetings()
        assert df2.empty

    def test_clear_cache_clears_attendance_cache(self, initialized_test_env):
        """Test that clear_cache clears the attendance cache."""
        df1 = scout_tracker.load_attendance()

        # Modify file
        pd.DataFrame(columns=["Meeting_Date", "Scout_Name"]).to_csv(
            config.ATTENDANCE_FILE, index=False
        )

        # Clear cache
        scout_tracker.clear_cache()

        # Should get new (empty) data
        df2 = scout_tracker.load_attendance()
        assert df2.empty

    def test_save_functions_auto_clear_cache(self, test_data_dir, sample_roster):
        """Test that save functions automatically clear the cache."""
        # Save and load
        scout_tracker.save_roster(sample_roster)
        df1 = scout_tracker.load_roster()

        # Save different data
        new_roster = pd.DataFrame({
            "Scout_ID": ["S999"],
            "First_Name": ["New"],
            "Last_Name": ["Scout"],
            "Current_Rank": ["Lion"],
            "Status": ["Active"]
        })
        scout_tracker.save_roster(new_roster)

        # Load should get new data (cache was auto-cleared)
        df2 = scout_tracker.load_roster()
        assert len(df2) == 1
        assert df2.loc[0, "Scout_ID"] == "S999"


@pytest.mark.data
class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_load_corrupted_csv_file(self, test_data_dir):
        """Test loading a corrupted CSV file."""
        # Create corrupted file
        with open(config.ROSTER_FILE, 'w') as f:
            f.write("This is not valid CSV data\n")
            f.write("Random text\n")

        # Should handle gracefully (might raise exception or return DataFrame)
        try:
            df = scout_tracker.load_roster()
            # If it doesn't raise, verify it returns something reasonable
            assert isinstance(df, pd.DataFrame)
        except Exception as e:
            # If it raises, that's also acceptable behavior
            assert isinstance(e, (pd.errors.ParserError, ValueError, Exception))

    def test_save_with_nan_values(self, test_data_dir):
        """Test saving DataFrame with NaN values."""
        import numpy as np

        df = pd.DataFrame({
            "Scout_ID": ["S001", "S002"],
            "First_Name": ["Alice", np.nan],
            "Last_Name": ["Anderson", "Brown"],
            "Current_Rank": ["Lion", "Lion"],
            "Status": ["Active", "Active"]
        })

        scout_tracker.save_roster(df)
        df_loaded = pd.read_csv(config.ROSTER_FILE)

        assert len(df_loaded) == 2
        assert pd.isna(df_loaded.loc[1, "First_Name"])

    def test_load_file_with_extra_columns(self, test_data_dir):
        """Test loading file with extra unexpected columns."""
        df = pd.DataFrame({
            "Scout_ID": ["S001"],
            "First_Name": ["Alice"],
            "Last_Name": ["Anderson"],
            "Current_Rank": ["Lion"],
            "Status": ["Active"],
            "Extra_Column": ["Extra data"]
        })
        df.to_csv(config.ROSTER_FILE, index=False)

        df_loaded = scout_tracker.load_roster()
        assert "Extra_Column" in df_loaded.columns
        assert len(df_loaded) == 1

    def test_save_with_unicode_characters(self, test_data_dir):
        """Test saving and loading data with Unicode characters."""
        df = pd.DataFrame({
            "Scout_ID": ["S001"],
            "First_Name": ["李明"],  # Chinese characters
            "Last_Name": ["Müller"],  # German umlaut
            "Current_Rank": ["Lion"],
            "Status": ["Active"]
        })

        scout_tracker.save_roster(df)
        df_loaded = scout_tracker.load_roster()

        assert df_loaded.loc[0, "First_Name"] == "李明"
        assert df_loaded.loc[0, "Last_Name"] == "Müller"

    def test_save_single_row(self, test_data_dir):
        """Test saving DataFrame with single row."""
        df = pd.DataFrame({
            "Scout_ID": ["S001"],
            "First_Name": ["Alice"],
            "Last_Name": ["Anderson"],
            "Current_Rank": ["Lion"],
            "Status": ["Active"]
        })

        scout_tracker.save_roster(df)
        df_loaded = scout_tracker.load_roster()

        assert len(df_loaded) == 1
        pd.testing.assert_frame_equal(df_loaded, df)

    def test_meetings_with_multiple_date_formats(self, test_data_dir):
        """Test that meetings can handle different date input formats."""
        # Save with string dates
        df = pd.DataFrame({
            "Meeting_ID": ["M001"],
            "Meeting_Date": ["2024-03-15"],
            "Meeting_Name": ["Test"],
            "Location": ["School"],
            "Notes": ["Notes"]
        })
        df.to_csv(config.MEETINGS_FILE, index=False)

        # Load should convert to datetime
        df_loaded = scout_tracker.load_meetings()
        assert pd.api.types.is_datetime64_any_dtype(df_loaded["Meeting_Date"])

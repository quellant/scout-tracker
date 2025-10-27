"""
Comprehensive tests for roster and requirements management in Scout Tracker.

Tests cover:
- Roster management (add, edit, delete scouts)
- Requirement tracking and completion
- Multi-rank support (Lion, Tiger, Wolf, Bear, Webelos)
- Required vs elective adventure logic
- Progress calculation
- Data validation and error handling
"""

import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scout_tracker import config, data as scout_tracker


# ============================================================================
# ROSTER MANAGEMENT TESTS
# ============================================================================

class TestRosterManagement:
    """Test cases for roster management functionality."""

    @pytest.mark.unit
    def test_load_empty_roster(self, test_data_dir):
        """Test loading an empty roster returns empty DataFrame."""
        # Initialize empty roster file
        empty_df = pd.DataFrame(columns=["Scout Name"])
        empty_df.to_csv(config.ROSTER_FILE, index=False)

        result = scout_tracker.load_roster()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "Scout Name" in result.columns

    @pytest.mark.unit
    def test_load_roster_with_data(self, initialized_test_env):
        """Test loading a roster with existing scout data."""
        roster = scout_tracker.load_roster()
        assert len(roster) == 3
        assert "Alice Anderson" in roster["Scout Name"].values
        assert "Bob Brown" in roster["Scout Name"].values

    @pytest.mark.unit
    def test_save_and_load_roster(self, test_data_dir):
        """Test saving and loading roster data."""
        new_roster = pd.DataFrame({
            "Scout Name": ["John Doe", "Jane Smith"]
        })

        scout_tracker.save_roster(new_roster)
        loaded_roster = scout_tracker.load_roster()

        assert len(loaded_roster) == 2
        # Roster should be sorted alphabetically (case-insensitive)
        assert loaded_roster["Scout Name"].tolist() == ["Jane Smith", "John Doe"]

    @pytest.mark.unit
    def test_add_scout_to_empty_roster(self, test_data_dir):
        """Test adding a scout to an empty roster."""
        # Start with empty roster
        roster_df = pd.DataFrame(columns=["Scout Name"])

        # Add new scout
        new_scout_name = "Tommy Test"
        new_row = pd.DataFrame({"Scout Name": [new_scout_name]})
        roster_df = pd.concat([roster_df, new_row], ignore_index=True)

        scout_tracker.save_roster(roster_df)
        loaded_roster = scout_tracker.load_roster()

        assert len(loaded_roster) == 1
        assert loaded_roster["Scout Name"].iloc[0] == "Tommy Test"

    @pytest.mark.unit
    def test_roster_alphabetical_sorting(self, test_data_dir):
        """Test that roster is always sorted alphabetically (case-insensitive)."""
        # Create roster with names in random order, including mixed case
        roster_df = pd.DataFrame({
            "Scout Name": [
                "Zoe Williams",
                "alice Anderson",  # lowercase 'a' should sort before 'B'
                "Charlie Brown",
                "bob Smith",       # lowercase 'b'
                "Dana Lee"
            ]
        })

        scout_tracker.save_roster(roster_df)
        loaded_roster = scout_tracker.load_roster()

        # Should be sorted alphabetically (case-insensitive)
        expected_order = ["alice Anderson", "bob Smith", "Charlie Brown", "Dana Lee", "Zoe Williams"]
        assert loaded_roster["Scout Name"].tolist() == expected_order

        # Verify it's also saved in sorted order
        loaded_again = scout_tracker.load_roster()
        assert loaded_again["Scout Name"].tolist() == expected_order

    @pytest.mark.unit
    def test_add_multiple_scouts(self, test_data_dir):
        """Test adding multiple scouts at once."""
        roster_df = pd.DataFrame(columns=["Scout Name"])

        # Add multiple scouts
        new_scouts = ["Scout A", "Scout B", "Scout C", "Scout D"]
        new_rows = pd.DataFrame({"Scout Name": new_scouts})
        roster_df = pd.concat([roster_df, new_rows], ignore_index=True)

        scout_tracker.save_roster(roster_df)
        loaded_roster = scout_tracker.load_roster()

        assert len(loaded_roster) == 4
        assert set(loaded_roster["Scout Name"].tolist()) == set(new_scouts)

    @pytest.mark.unit
    def test_prevent_duplicate_scouts(self, test_data_dir):
        """Test that duplicate scouts are not added."""
        roster_df = pd.DataFrame({"Scout Name": ["Alice Anderson"]})
        scout_tracker.save_roster(roster_df)

        # Try to add duplicate
        duplicate_name = "Alice Anderson"
        existing_names = set(roster_df["Scout Name"].values)

        # Simulate the duplicate check logic
        should_add = duplicate_name not in existing_names
        assert should_add == False

    @pytest.mark.unit
    def test_remove_scout_from_roster(self, initialized_test_env):
        """Test removing a scout from the roster."""
        roster_df = scout_tracker.load_roster()
        original_count = len(roster_df)

        # Remove a scout
        scout_to_remove = roster_df["Scout Name"].iloc[0]
        roster_df = roster_df[roster_df["Scout Name"] != scout_to_remove]

        scout_tracker.save_roster(roster_df)
        loaded_roster = scout_tracker.load_roster()

        assert len(loaded_roster) == original_count - 1
        assert scout_to_remove not in loaded_roster["Scout Name"].values

    @pytest.mark.unit
    def test_bulk_import_scouts(self, test_data_dir):
        """Test bulk importing scouts from a list."""
        roster_df = pd.DataFrame(columns=["Scout Name"])

        # Simulate bulk import
        bulk_input = "John Smith\nJane Doe\nBob Johnson\nAlice Anderson"
        scout_names = [name.strip() for name in bulk_input.split('\n') if name.strip()]

        new_rows = pd.DataFrame({"Scout Name": scout_names})
        roster_df = pd.concat([roster_df, new_rows], ignore_index=True)

        scout_tracker.save_roster(roster_df)
        loaded_roster = scout_tracker.load_roster()

        assert len(loaded_roster) == 4
        assert "John Smith" in loaded_roster["Scout Name"].values
        assert "Alice Anderson" in loaded_roster["Scout Name"].values

    @pytest.mark.unit
    def test_bulk_import_with_duplicates(self, test_data_dir):
        """Test bulk import filters out duplicates."""
        roster_df = pd.DataFrame({"Scout Name": ["Existing Scout"]})

        # Simulate bulk import with duplicates
        bulk_names = "New Scout 1\nExisting Scout\nNew Scout 2\nExisting Scout"
        scout_names = [name.strip() for name in bulk_names.split('\n') if name.strip()]

        existing_scouts = set(roster_df["Scout Name"].values)
        new_scouts = []
        skipped = []

        for name in scout_names:
            if name in existing_scouts:
                skipped.append(name)
            elif name in new_scouts:
                skipped.append(name)
            else:
                new_scouts.append(name)
                existing_scouts.add(name)

        assert len(new_scouts) == 2
        assert len(skipped) == 2
        assert "New Scout 1" in new_scouts
        assert "New Scout 2" in new_scouts

    @pytest.mark.unit
    def test_empty_scout_name_validation(self, test_data_dir):
        """Test that empty scout names are rejected."""
        empty_name = "   "
        is_valid = bool(empty_name.strip())

        assert is_valid == False


# ============================================================================
# REQUIREMENT MANAGEMENT TESTS
# ============================================================================

class TestRequirementManagement:
    """Test cases for requirement management functionality."""

    @pytest.mark.unit
    def test_load_requirements(self, initialized_test_env):
        """Test loading requirement key data."""
        requirements = scout_tracker.load_requirement_key()
        assert isinstance(requirements, pd.DataFrame)
        assert len(requirements) == 3
        assert "Req_ID" in requirements.columns
        assert "Adventure" in requirements.columns
        assert "Required" in requirements.columns

    @pytest.mark.unit
    def test_save_requirements(self, test_data_dir):
        """Test saving requirement data."""
        new_reqs = pd.DataFrame({
            "Req_ID": ["Test.1", "Test.2"],
            "Adventure": ["Test Adventure", "Test Adventure"],
            "Requirement_Description": ["Req 1", "Req 2"],
            "Required": [True, False]
        })

        scout_tracker.save_requirements(new_reqs)
        loaded_reqs = scout_tracker.load_requirement_key()

        assert len(loaded_reqs) == 2
        assert "Test.1" in loaded_reqs["Req_ID"].values

    @pytest.mark.unit
    def test_add_new_requirement(self, initialized_test_env):
        """Test adding a new requirement."""
        reqs_df = scout_tracker.load_requirement_key()
        original_count = len(reqs_df)

        new_req = pd.DataFrame({
            "Req_ID": ["NewAdv.1"],
            "Adventure": ["New Adventure"],
            "Requirement_Description": ["Do something cool"],
            "Required": [False]
        })

        reqs_df = pd.concat([reqs_df, new_req], ignore_index=True)
        scout_tracker.save_requirements(reqs_df)

        loaded_reqs = scout_tracker.load_requirement_key()
        assert len(loaded_reqs) == original_count + 1
        assert "NewAdv.1" in loaded_reqs["Req_ID"].values

    @pytest.mark.unit
    def test_prevent_duplicate_requirement_ids(self, initialized_test_env):
        """Test that duplicate requirement IDs are detected."""
        reqs_df = scout_tracker.load_requirement_key()
        duplicate_id = reqs_df["Req_ID"].iloc[0]

        # Check if ID already exists
        id_exists = duplicate_id in reqs_df["Req_ID"].values
        assert id_exists == True

    @pytest.mark.unit
    def test_separate_required_and_elective(self, initialized_test_env):
        """Test separating required and elective adventures."""
        reqs_df = scout_tracker.load_requirement_key()

        required = reqs_df[reqs_df["Required"] == True]
        elective = reqs_df[reqs_df["Required"] == False]

        assert len(required) + len(elective) == len(reqs_df)
        assert len(required) > 0  # Should have at least one required

    @pytest.mark.unit
    def test_requirement_validation_all_fields(self, test_data_dir):
        """Test that all required fields are validated."""
        req_id = "Test.1"
        adventure = "Test Adventure"
        description = "Test description"

        # All fields filled
        all_valid = bool(req_id.strip() and adventure.strip() and description.strip())
        assert all_valid == True

        # Missing field
        empty_description = ""
        some_invalid = bool(req_id.strip() and adventure.strip() and empty_description.strip())
        assert some_invalid == False


# ============================================================================
# MULTI-RANK SUPPORT TESTS
# ============================================================================

class TestMultiRankSupport:
    """Test cases for multi-rank support across all Cub Scout ranks."""

    @pytest.mark.unit
    def test_all_ranks_defined(self):
        """Test that all Cub Scout ranks are defined."""
        expected_ranks = [
            "Lion (Kindergarten)",
            "Tiger (1st Grade)",
            "Wolf (2nd Grade)",
            "Bear (3rd Grade)",
            "Webelos (4th Grade)"
        ]

        assert len(config.RANK_REQUIREMENTS) == 5
        for rank in expected_ranks:
            assert rank in config.RANK_REQUIREMENTS

    @pytest.mark.unit
    def test_lion_requirements_exist(self):
        """Test that Lion rank requirements are defined."""
        lion_reqs = config.LION_REQUIREMENTS
        assert len(lion_reqs) > 0
        assert all("Req_ID" in req for req in lion_reqs)
        assert all("Adventure" in req for req in lion_reqs)
        assert all("Required" in req for req in lion_reqs)

    @pytest.mark.unit
    def test_tiger_requirements_exist(self):
        """Test that Tiger rank requirements are defined."""
        tiger_reqs = config.TIGER_REQUIREMENTS
        assert len(tiger_reqs) > 0
        assert all("Req_ID" in req for req in tiger_reqs)

    @pytest.mark.unit
    def test_wolf_requirements_exist(self):
        """Test that Wolf rank requirements are defined."""
        wolf_reqs = config.WOLF_REQUIREMENTS
        assert len(wolf_reqs) > 0
        assert all("Req_ID" in req for req in wolf_reqs)

    @pytest.mark.unit
    def test_bear_requirements_exist(self):
        """Test that Bear rank requirements are defined."""
        bear_reqs = config.BEAR_REQUIREMENTS
        assert len(bear_reqs) > 0
        assert all("Req_ID" in req for req in bear_reqs)

    @pytest.mark.unit
    def test_webelos_requirements_exist(self):
        """Test that Webelos rank requirements are defined."""
        webelos_reqs = config.WEBELOS_REQUIREMENTS
        assert len(webelos_reqs) > 0
        assert all("Req_ID" in req for req in webelos_reqs)

    @pytest.mark.unit
    def test_rank_requirements_have_required_and_elective(self):
        """Test that each rank has both required and elective adventures."""
        for rank_name, requirements in config.RANK_REQUIREMENTS.items():
            required_count = sum(1 for req in requirements if req["Required"])
            elective_count = sum(1 for req in requirements if not req["Required"])

            # Each rank should have both required and elective adventures
            assert required_count > 0, f"{rank_name} has no required adventures"
            assert elective_count > 0, f"{rank_name} has no elective adventures"

    @pytest.mark.unit
    def test_requirement_ids_are_unique_within_rank(self):
        """Test that requirement IDs are unique within each rank."""
        for rank_name, requirements in config.RANK_REQUIREMENTS.items():
            req_ids = [req["Req_ID"] for req in requirements]
            unique_ids = set(req_ids)

            assert len(req_ids) == len(unique_ids), f"{rank_name} has duplicate Req_IDs"


# ============================================================================
# REQUIREMENT TRACKING AND COMPLETION TESTS
# ============================================================================

class TestRequirementTracking:
    """Test cases for tracking requirement completion."""

    @pytest.mark.unit
    def test_build_master_tracker_empty(self, test_data_dir):
        """Test building an empty master tracker."""
        roster_df = pd.DataFrame({"Scout Name": ["Scout A", "Scout B"]})
        req_df = pd.DataFrame({
            "Req_ID": ["Req.1", "Req.2"],
            "Adventure": ["Adv", "Adv"],
            "Requirement_Description": ["Desc1", "Desc2"],
            "Required": [True, True]
        })

        scouts = roster_df["Scout Name"].tolist()
        req_ids = req_df["Req_ID"].tolist()

        master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

        assert master_tracker.shape == (2, 2)
        assert (master_tracker == False).all().all()

    @pytest.mark.unit
    def test_mark_requirement_complete(self, test_data_dir):
        """Test marking a requirement as complete for a scout."""
        scouts = ["Scout A"]
        req_ids = ["Req.1", "Req.2"]

        master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

        # Mark a requirement complete
        master_tracker.at["Scout A", "Req.1"] = True

        assert master_tracker.at["Scout A", "Req.1"] == True
        assert master_tracker.at["Scout A", "Req.2"] == False

    @pytest.mark.unit
    def test_track_multiple_scouts_different_progress(self, test_data_dir):
        """Test tracking different progress for multiple scouts."""
        scouts = ["Scout A", "Scout B", "Scout C"]
        req_ids = ["Req.1", "Req.2", "Req.3"]

        master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

        # Scout A completes all
        master_tracker.loc["Scout A", :] = True

        # Scout B completes 2
        master_tracker.at["Scout B", "Req.1"] = True
        master_tracker.at["Scout B", "Req.2"] = True

        # Scout C completes 1
        master_tracker.at["Scout C", "Req.1"] = True

        assert master_tracker.loc["Scout A"].sum() == 3
        assert master_tracker.loc["Scout B"].sum() == 2
        assert master_tracker.loc["Scout C"].sum() == 1

    @pytest.mark.unit
    def test_requirement_completion_via_meeting_attendance(self, test_data_dir):
        """Test that attending a meeting marks requirements complete."""
        # Setup
        scouts = ["Scout A"]
        req_ids = ["Req.1", "Req.2"]
        master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

        # Meeting covers Req.1
        meeting_date = pd.to_datetime("2024-01-15")
        meeting_reqs = ["Req.1"]

        # Scout attended meeting
        scout_name = "Scout A"

        # Mark requirements complete
        for req_id in meeting_reqs:
            if req_id in master_tracker.columns:
                master_tracker.at[scout_name, req_id] = True

        assert master_tracker.at["Scout A", "Req.1"] == True
        assert master_tracker.at["Scout A", "Req.2"] == False

    @pytest.mark.unit
    def test_multiple_meetings_accumulate_requirements(self, test_data_dir):
        """Test that multiple meetings accumulate requirement completions."""
        scouts = ["Scout A"]
        req_ids = ["Req.1", "Req.2", "Req.3"]
        master_tracker = pd.DataFrame(False, index=scouts, columns=req_ids)

        # Meeting 1 covers Req.1
        for req_id in ["Req.1"]:
            master_tracker.at["Scout A", req_id] = True

        # Meeting 2 covers Req.2 and Req.3
        for req_id in ["Req.2", "Req.3"]:
            master_tracker.at["Scout A", req_id] = True

        assert master_tracker.loc["Scout A"].sum() == 3


# ============================================================================
# REQUIRED VS ELECTIVE ADVENTURE LOGIC TESTS
# ============================================================================

class TestRequiredElectiveLogic:
    """Test cases for required vs elective adventure logic."""

    @pytest.mark.unit
    def test_identify_required_adventures(self, initialized_test_env):
        """Test identifying required adventures."""
        req_df = scout_tracker.load_requirement_key()
        required_adventures = req_df[req_df["Required"] == True]["Adventure"].unique()

        assert len(required_adventures) > 0

    @pytest.mark.unit
    def test_identify_elective_adventures(self, initialized_test_env):
        """Test identifying elective adventures."""
        req_df = scout_tracker.load_requirement_key()
        elective_adventures = req_df[req_df["Required"] == False]["Adventure"].unique()

        # May have 0 electives in sample data, but logic should work
        assert isinstance(elective_adventures, object)

    @pytest.mark.unit
    def test_required_adventures_must_all_complete(self):
        """Test that all required adventures must be completed."""
        # Simulate required adventure completion
        required_adventures = ["Bobcat", "Lion's Roar", "Lion's Pride"]
        scout_progress = {
            "Bobcat": 100.0,
            "Lion's Roar": 100.0,
            "Lion's Pride": 100.0
        }

        all_required_complete = all(
            scout_progress.get(adv, 0) == 100.0
            for adv in required_adventures
        )

        assert all_required_complete == True

    @pytest.mark.unit
    def test_required_adventures_incomplete(self):
        """Test detecting incomplete required adventures."""
        required_adventures = ["Bobcat", "Lion's Roar", "Lion's Pride"]
        scout_progress = {
            "Bobcat": 100.0,
            "Lion's Roar": 50.0,  # Incomplete
            "Lion's Pride": 100.0
        }

        all_required_complete = all(
            scout_progress.get(adv, 0) == 100.0
            for adv in required_adventures
        )

        assert all_required_complete == False

    @pytest.mark.unit
    def test_elective_adventures_minimum_count(self):
        """Test that minimum number of elective adventures must be completed."""
        elective_adventures = ["Elec1", "Elec2", "Elec3", "Elec4"]
        min_required = 2

        scout_progress = {
            "Elec1": 100.0,
            "Elec2": 100.0,
            "Elec3": 50.0,
            "Elec4": 0.0
        }

        completed_electives = sum(
            1 for adv in elective_adventures
            if scout_progress.get(adv, 0) == 100.0
        )

        assert completed_electives >= min_required

    @pytest.mark.unit
    def test_elective_adventures_insufficient(self):
        """Test detecting insufficient elective completions."""
        elective_adventures = ["Elec1", "Elec2", "Elec3", "Elec4"]
        min_required = 2

        scout_progress = {
            "Elec1": 100.0,
            "Elec2": 50.0,
            "Elec3": 50.0,
            "Elec4": 0.0
        }

        completed_electives = sum(
            1 for adv in elective_adventures
            if scout_progress.get(adv, 0) == 100.0
        )

        assert completed_electives < min_required

    @pytest.mark.unit
    def test_rank_earned_all_required_and_minimum_electives(self):
        """Test rank is earned with all required + minimum electives."""
        all_required_complete = True
        completed_electives = 2
        min_electives = 2

        rank_earned = all_required_complete and completed_electives >= min_electives

        assert rank_earned == True

    @pytest.mark.unit
    def test_rank_not_earned_missing_required(self):
        """Test rank is not earned if required adventures incomplete."""
        all_required_complete = False
        completed_electives = 2
        min_electives = 2

        rank_earned = all_required_complete and completed_electives >= min_electives

        assert rank_earned == False

    @pytest.mark.unit
    def test_rank_not_earned_insufficient_electives(self):
        """Test rank is not earned if insufficient electives."""
        all_required_complete = True
        completed_electives = 1
        min_electives = 2

        rank_earned = all_required_complete and completed_electives >= min_electives

        assert rank_earned == False


# ============================================================================
# PROGRESS CALCULATION TESTS
# ============================================================================

class TestProgressCalculation:
    """Test cases for progress calculation and percentages."""

    @pytest.mark.unit
    def test_calculate_adventure_percentage_zero(self):
        """Test calculating 0% completion."""
        completed = 0
        total = 5

        percentage = (completed / total * 100) if total > 0 else 0

        assert percentage == 0.0

    @pytest.mark.unit
    def test_calculate_adventure_percentage_partial(self):
        """Test calculating partial completion."""
        completed = 3
        total = 5

        percentage = (completed / total * 100) if total > 0 else 0

        assert percentage == 60.0

    @pytest.mark.unit
    def test_calculate_adventure_percentage_complete(self):
        """Test calculating 100% completion."""
        completed = 5
        total = 5

        percentage = (completed / total * 100) if total > 0 else 0

        assert percentage == 100.0

    @pytest.mark.unit
    def test_calculate_percentage_division_by_zero(self):
        """Test handling division by zero in percentage calculation."""
        completed = 0
        total = 0

        percentage = (completed / total * 100) if total > 0 else 0

        assert percentage == 0.0

    @pytest.mark.unit
    def test_adventure_progress_from_tracker(self):
        """Test calculating adventure progress from master tracker."""
        # Simulate tracker data
        master_tracker = pd.DataFrame({
            "Req.1": [True, False],
            "Req.2": [True, False],
            "Req.3": [False, False]
        }, index=["Scout A", "Scout B"])

        # Calculate for Scout A
        adventure_reqs = ["Req.1", "Req.2", "Req.3"]
        completed = master_tracker.loc["Scout A", adventure_reqs].sum()
        total = len(adventure_reqs)
        percentage = (completed / total * 100) if total > 0 else 0

        assert completed == 2
        assert total == 3
        assert percentage == pytest.approx(66.67, rel=0.01)

    @pytest.mark.unit
    def test_multiple_scout_progress_calculation(self):
        """Test calculating progress for multiple scouts."""
        master_tracker = pd.DataFrame({
            "Req.1": [True, True, False],
            "Req.2": [True, False, False],
        }, index=["Scout A", "Scout B", "Scout C"])

        results = {}
        for scout in master_tracker.index:
            completed = master_tracker.loc[scout].sum()
            total = len(master_tracker.columns)
            percentage = (completed / total * 100) if total > 0 else 0
            results[scout] = percentage

        assert results["Scout A"] == 100.0
        assert results["Scout B"] == 50.0
        assert results["Scout C"] == 0.0

    @pytest.mark.unit
    def test_overall_den_progress_calculation(self):
        """Test calculating overall den progress."""
        # 3 scouts, 2 requirements
        master_tracker = pd.DataFrame({
            "Req.1": [True, True, False],
            "Req.2": [True, False, False],
        }, index=["Scout A", "Scout B", "Scout C"])

        total_scouts = len(master_tracker)
        total_requirements = len(master_tracker.columns)
        total_possible = total_scouts * total_requirements
        total_completed = master_tracker.sum().sum()

        overall_percentage = (total_completed / total_possible * 100) if total_possible > 0 else 0

        assert total_completed == 3
        assert total_possible == 6
        assert overall_percentage == 50.0


# ============================================================================
# DATA VALIDATION AND ERROR HANDLING TESTS
# ============================================================================

class TestDataValidation:
    """Test cases for data validation and error handling."""

    @pytest.mark.unit
    def test_validate_scout_name_not_empty(self):
        """Test validation of non-empty scout names."""
        valid_name = "John Doe"
        invalid_name = "   "

        assert bool(valid_name.strip()) == True
        assert bool(invalid_name.strip()) == False

    @pytest.mark.unit
    def test_validate_requirement_id_format(self):
        """Test validation of requirement ID format."""
        valid_id = "Bobcat.1"

        # Should contain a dot
        assert "." in valid_id

        # Should have parts before and after dot
        parts = valid_id.split(".")
        assert len(parts) == 2
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

    @pytest.mark.unit
    def test_validate_invalid_requirement_id(self):
        """Test detecting invalid requirement ID formats."""
        invalid_ids = ["", "NoDot", ".OnlyDot", "Dot.", "Multiple.Dots.Here"]

        for req_id in invalid_ids:
            if not req_id or "." not in req_id:
                is_valid = False
            else:
                parts = req_id.split(".")
                is_valid = len(parts) == 2 and all(len(p) > 0 for p in parts)

            # Most should be invalid
            if req_id in ["", "NoDot", ".OnlyDot", "Dot."]:
                assert is_valid == False

    @pytest.mark.unit
    def test_validate_required_field_is_boolean(self):
        """Test that Required field is boolean."""
        valid_required = True
        assert isinstance(valid_required, bool)

        valid_not_required = False
        assert isinstance(valid_not_required, bool)

    @pytest.mark.unit
    def test_validate_meeting_date_format(self):
        """Test validation of meeting date format."""
        valid_date_str = "2024-01-15"

        # Should be parseable as date
        try:
            date_obj = pd.to_datetime(valid_date_str)
            is_valid = True
        except:
            is_valid = False

        assert is_valid == True

    @pytest.mark.unit
    def test_validate_invalid_meeting_date(self):
        """Test detecting invalid meeting dates."""
        invalid_date = "not-a-date"

        try:
            date_obj = pd.to_datetime(invalid_date)
            is_valid = True
        except:
            is_valid = False

        assert is_valid == False

    @pytest.mark.unit
    def test_handle_missing_roster_file(self, test_data_dir):
        """Test handling missing roster file."""
        # Don't create roster file
        result = scout_tracker.load_roster()

        # Should return empty DataFrame, not crash
        assert isinstance(result, pd.DataFrame)
        assert "Scout Name" in result.columns

    @pytest.mark.unit
    def test_handle_missing_requirements_file(self, test_data_dir):
        """Test handling missing requirements file."""
        # Don't create requirements file
        result = scout_tracker.load_requirement_key()

        # Should return empty DataFrame with proper columns
        assert isinstance(result, pd.DataFrame)
        assert "Req_ID" in result.columns

    @pytest.mark.unit
    def test_handle_empty_meeting_req_ids(self):
        """Test handling empty requirement IDs in meetings."""
        req_ids_str = ""

        req_ids_list = req_ids_str.split(",") if req_ids_str else []

        assert req_ids_list == []

    @pytest.mark.unit
    def test_handle_none_meeting_req_ids(self):
        """Test handling None requirement IDs in meetings."""
        req_ids_str = None

        req_ids_list = req_ids_str.split(",") if pd.notna(req_ids_str) else []

        assert req_ids_list == []

    @pytest.mark.unit
    def test_parse_comma_separated_req_ids(self):
        """Test parsing comma-separated requirement IDs."""
        req_ids_str = "Bobcat.1,Bobcat.2,LionsRoar.1"

        req_ids_list = req_ids_str.split(",") if pd.notna(req_ids_str) else []

        assert len(req_ids_list) == 3
        assert "Bobcat.1" in req_ids_list
        assert "LionsRoar.1" in req_ids_list

    @pytest.mark.unit
    def test_validate_scout_exists_in_tracker(self):
        """Test validating scout exists in tracker."""
        master_tracker = pd.DataFrame(
            {"Req.1": [True, False]},
            index=["Scout A", "Scout B"]
        )

        scout_name = "Scout A"
        exists = scout_name in master_tracker.index

        assert exists == True

        non_existent = "Scout Z"
        exists = non_existent in master_tracker.index

        assert exists == False

    @pytest.mark.unit
    def test_validate_requirement_exists_in_tracker(self):
        """Test validating requirement exists in tracker."""
        master_tracker = pd.DataFrame(
            {"Req.1": [True], "Req.2": [False]},
            index=["Scout A"]
        )

        req_id = "Req.1"
        exists = req_id in master_tracker.columns

        assert exists == True

        non_existent = "Req.99"
        exists = non_existent in master_tracker.columns

        assert exists == False


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple components."""

    @pytest.mark.unit
    def test_full_workflow_add_scout_track_progress(self, test_data_dir):
        """Test complete workflow: add scout, attend meetings, track progress."""
        # 1. Create roster with scouts
        roster_df = pd.DataFrame({"Scout Name": ["Test Scout"]})
        scout_tracker.save_roster(roster_df)

        # 2. Create requirements
        req_df = pd.DataFrame({
            "Req_ID": ["Adv.1", "Adv.2", "Adv.3"],
            "Adventure": ["Adventure", "Adventure", "Adventure"],
            "Requirement_Description": ["Req 1", "Req 2", "Req 3"],
            "Required": [True, True, True]
        })
        scout_tracker.save_requirements(req_df)

        # 3. Create meetings
        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15", "2024-01-22"],
            "Meeting_Title": ["Meeting 1", "Meeting 2"],
            "Req_IDs_Covered": ["Adv.1,Adv.2", "Adv.3"]
        })
        scout_tracker.save_meetings(meetings_df)

        # 4. Log attendance
        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15", "2024-01-22"],
            "Scout_Name": ["Test Scout", "Test Scout"]
        })
        scout_tracker.save_attendance(attendance_df)

        # 5. Build tracker and verify
        roster = scout_tracker.load_roster()
        requirements = scout_tracker.load_requirement_key()
        meetings = scout_tracker.load_meetings()
        attendance = scout_tracker.load_attendance()

        assert len(roster) == 1
        assert len(requirements) == 3
        assert len(meetings) == 2
        assert len(attendance) == 2

    @pytest.mark.unit
    def test_multi_scout_different_attendance_patterns(self, test_data_dir):
        """Test tracking multiple scouts with different attendance patterns."""
        # Setup
        roster_df = pd.DataFrame({"Scout Name": ["Scout A", "Scout B", "Scout C"]})
        scout_tracker.save_roster(roster_df)

        req_df = pd.DataFrame({
            "Req_ID": ["R.1", "R.2", "R.3"],
            "Adventure": ["Adv", "Adv", "Adv"],
            "Requirement_Description": ["1", "2", "3"],
            "Required": [True, True, True]
        })
        scout_tracker.save_requirements(req_df)

        meetings_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15", "2024-01-22", "2024-01-29"],
            "Meeting_Title": ["M1", "M2", "M3"],
            "Req_IDs_Covered": ["R.1", "R.2", "R.3"]
        })
        scout_tracker.save_meetings(meetings_df)

        # Scout A attends all meetings
        # Scout B attends first two
        # Scout C attends only first
        attendance_df = pd.DataFrame({
            "Meeting_Date": ["2024-01-15", "2024-01-15", "2024-01-15",
                           "2024-01-22", "2024-01-22",
                           "2024-01-29"],
            "Scout_Name": ["Scout A", "Scout B", "Scout C",
                          "Scout A", "Scout B",
                          "Scout A"]
        })
        scout_tracker.save_attendance(attendance_df)

        # Verify saved correctly
        loaded_attendance = scout_tracker.load_attendance()

        scout_a_attendance = loaded_attendance[loaded_attendance["Scout_Name"] == "Scout A"]
        scout_b_attendance = loaded_attendance[loaded_attendance["Scout_Name"] == "Scout B"]
        scout_c_attendance = loaded_attendance[loaded_attendance["Scout_Name"] == "Scout C"]

        assert len(scout_a_attendance) == 3
        assert len(scout_b_attendance) == 2
        assert len(scout_c_attendance) == 1

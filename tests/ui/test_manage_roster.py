"""
UI tests for the Manage Roster page.

Tests scout addition, removal, and roster display functionality.
"""

import pytest
from .conftest import click_nav_item, wait_for_streamlit


class TestManageRoster:
    """Test suite for Manage Roster page."""

    def test_page_loads(self, page):
        """Test that the Manage Roster page loads correctly."""
        # Page should load on Manage Roster by default
        assert page.is_visible("text=Manage Roster")
        assert page.is_visible("text=Add or remove scouts from your den's roster")

    def test_roster_displays_existing_scouts(self, page):
        """Test that existing scouts are displayed in the roster."""
        # Check that the roster section is visible
        assert page.is_visible("text=Current Den Roster")

        # Get roster data
        scouts = page.evaluate("""
            () => {
                const cells = Array.from(document.querySelectorAll('td'));
                return cells.map(cell => cell.textContent.trim())
                           .filter(text => text && text !== 'Scout Name');
            }
        """)

        # Should have some scouts in the roster
        assert len(scouts) > 0

    def test_add_scout_form_visible(self, page):
        """Test that the add scout form is displayed."""
        assert page.is_visible("text=Add Scouts")
        assert page.is_visible("text=Add One Scout")
        assert page.is_visible("input[aria-label='Scout Name']")

    def test_add_scout_functionality(self, page, test_data_backup):
        """Test adding a new scout to the roster."""
        # Get initial scout count
        initial_scouts = page.evaluate("""
            () => {
                const cells = Array.from(document.querySelectorAll('td'));
                return cells.map(cell => cell.textContent.trim())
                           .filter(text => text && text !== 'Scout Name').length;
            }
        """)

        # Fill in scout name
        page.fill("input[aria-label='Scout Name']", "UI Test Scout")

        # Click Add Scout button
        page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const addButton = buttons.find(btn => btn.textContent.includes('Add Scout'));
                if (addButton) addButton.click();
            }
        """)

        # Wait for Streamlit to update
        wait_for_streamlit(page, 3000)

        # Verify scout was added by checking if it appears in Plan Meetings
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page, 2000)

        # Check if the new scout appears in the "Still need" lists
        page_content = page.content()
        assert "UI Test Scout" in page_content

    def test_remove_scout_interface_visible(self, page):
        """Test that the remove scout interface is displayed."""
        assert page.is_visible("text=Select a scout to remove:")
        assert page.is_visible("button:has-text('Remove Selected Scout')")

    def test_bulk_import_tab_exists(self, page):
        """Test that the bulk import tab is available."""
        assert page.is_visible("text=Bulk Import")

    def test_workflow_guide_displayed(self, page):
        """Test that the workflow guide is shown."""
        assert page.is_visible("text=Workflow:")
        assert page.is_visible("text=Add scouts to roster")
        assert page.is_visible("text=Configure requirements")
        assert page.is_visible("text=Plan & create meetings")


@pytest.mark.slow
class TestManageRosterIntegration:
    """Integration tests for Manage Roster page."""

    def test_scout_appears_across_all_pages(self, page, test_data_backup):
        """Test that a newly added scout appears on all relevant pages."""
        # Add a scout
        page.fill("input[aria-label='Scout Name']", "Integration Test Scout")
        page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const addButton = buttons.find(btn => btn.textContent.includes('Add Scout'));
                if (addButton) addButton.click();
            }
        """)
        wait_for_streamlit(page, 3000)

        # Check Dashboard
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page, 2000)
        assert "Integration Test Scout" in page.content()

        # Check Individual Reports
        click_nav_item(page, "Individual Reports")
        wait_for_streamlit(page, 2000)
        # Should be in the scout selector dropdown
        page.click("select")
        assert page.is_visible("text=Integration Test Scout")

        # Check Log Attendance
        click_nav_item(page, "Log Attendance")
        wait_for_streamlit(page, 2000)
        assert "Integration Test Scout" in page.content()

"""
UI tests for the Tracker Dashboard page.

Tests progress visualization and summary displays.
"""

import pytest
from .conftest import click_nav_item, wait_for_streamlit


class TestTrackerDashboard:
    """Test suite for Tracker Dashboard page."""

    def test_page_loads(self, page):
        """Test that the dashboard loads correctly."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        assert page.is_visible("text=Tracker Dashboard")
        assert page.is_visible("text=View progress for all scouts")

    def test_adventure_completion_summary_visible(self, page):
        """Test that adventure completion summary is displayed."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        assert page.is_visible("text=Adventure Completion Summary")

    def test_required_adventures_table_visible(self, page):
        """Test that required adventures table is displayed."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        assert page.is_visible("text=Required Adventures (Must complete all 6)")

        # Check for required adventure columns
        assert page.is_visible("text=Bobcat")
        assert page.is_visible("text=Fun on the Run")
        assert page.is_visible("text=Lion's Roar")

    def test_elective_adventures_table_visible(self, page):
        """Test that elective adventures table is displayed."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        assert page.is_visible("text=Elective Adventures (Must complete any 2)")

    def test_scouts_listed_in_tables(self, page):
        """Test that scouts are listed in the progress tables."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        # Get scout names from the table
        scouts = page.evaluate("""
            () => {
                const cells = Array.from(document.querySelectorAll('td'));
                return cells.map(cell => cell.textContent.trim())
                           .filter(text => text && text.length > 3 && !text.includes('%'));
            }
        """)

        # Should have multiple scouts
        assert len(scouts) > 0

    def test_progress_percentages_displayed(self, page):
        """Test that progress percentages are shown."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        # Check for percentage values in the page
        page_content = page.content()
        assert "%" in page_content

    def test_rank_completion_status_visible(self, page):
        """Test that Lion Rank completion status section exists."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        # Scroll down to see rank completion
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        wait_for_streamlit(page, 1000)

        assert page.is_visible("text=Lion Rank Completion Status")

    def test_rank_status_columns(self, page):
        """Test that rank status table has expected columns."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        wait_for_streamlit(page, 1000)

        # Check for rank status columns
        assert page.is_visible("text=Scout Name")
        assert page.is_visible("text=Required Complete")
        assert page.is_visible("text=Electives Complete")
        assert page.is_visible("text=Lion Rank Earned")


@pytest.mark.slow
class TestDashboardIntegration:
    """Integration tests for Dashboard page."""

    def test_dashboard_reflects_attendance_data(self, page):
        """Test that dashboard shows progress based on logged attendance."""
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        # Get a scout's progress
        dashboard_data = page.evaluate("""
            () => {
                const rows = Array.from(document.querySelectorAll('tr'));
                const tripRow = rows.find(row => row.textContent.includes('Trip Beatty'));
                if (tripRow) {
                    const cells = Array.from(tripRow.querySelectorAll('td'));
                    return cells.map(cell => cell.textContent.trim());
                }
                return [];
            }
        """)

        # Should have data for this scout
        assert len(dashboard_data) > 0

        # Navigate to individual reports to verify consistency
        click_nav_item(page, "Individual Reports")
        wait_for_streamlit(page)

        # Select Trip Beatty
        page.evaluate("""
            () => {
                const select = document.querySelector('select');
                if (select) {
                    select.value = 'Trip Beatty';
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        """)
        wait_for_streamlit(page, 2000)

        # Progress should be visible
        assert page.is_visible("text=Progress Summary for Trip Beatty")

    def test_dashboard_updates_with_new_scouts(self, page, test_data_backup):
        """Test that dashboard includes newly added scouts."""
        # Add a scout
        click_nav_item(page, "Manage Roster")
        wait_for_streamlit(page)

        page.fill("input[aria-label='Scout Name']", "Dashboard Test Scout")
        page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const addButton = buttons.find(btn => btn.textContent.includes('Add Scout'));
                if (addButton) addButton.click();
            }
        """)
        wait_for_streamlit(page, 3000)

        # Check dashboard
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page, 2000)

        # New scout should appear in the dashboard
        assert "Dashboard Test Scout" in page.content()

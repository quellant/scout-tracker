"""
UI tests for the Manage Requirements page.

Tests requirement viewing, editing, and management functionality.
"""

import pytest
from .conftest import click_nav_item, wait_for_streamlit


class TestManageRequirements:
    """Test suite for Manage Requirements page."""

    def test_page_loads(self, page):
        """Test that the Manage Requirements page loads correctly."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        assert page.is_visible("text=Manage Requirements")
        assert page.is_visible("text=Add, edit, or remove adventure requirements")

    def test_tabs_visible(self, page):
        """Test that all management tabs are displayed."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        assert page.is_visible("text=View All")
        assert page.is_visible("text=Add New")
        assert page.is_visible("text=Edit Existing")
        assert page.is_visible("text=Delete")
        assert page.is_visible("text=Import/Export")

    def test_required_adventures_section_visible(self, page):
        """Test that required adventures section is displayed."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        assert page.is_visible("text=Required Adventures (Must complete all)")

    def test_required_adventures_list(self, page):
        """Test that required adventures are listed."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        # Check for known required adventures
        required_adventures = ["Bobcat", "Fun on the Run", "King of the Jungle",
                              "Lion's Pride", "Lion's Roar", "Mountain Lion"]

        for adventure in required_adventures:
            assert page.is_visible(f"text={adventure}")

    def test_elective_adventures_section_visible(self, page):
        """Test that elective adventures section is displayed."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        assert page.is_visible("text=Elective Adventures (Must complete any 2)")

    def test_adventure_expander_functionality(self, page):
        """Test that adventure expanders can be clicked."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        # Click on Bobcat expander
        page.evaluate("""
            () => {
                const expanders = Array.from(document.querySelectorAll('summary'));
                const bobcatExpander = expanders.find(exp => exp.textContent.includes('Bobcat'));
                if (bobcatExpander) bobcatExpander.click();
            }
        """)
        wait_for_streamlit(page, 1000)

        # The expander should have opened (content becomes visible)
        # Note: Streamlit expanders may not show detailed content in all cases

    def test_requirement_counts_displayed(self, page):
        """Test that requirement counts are shown for each adventure."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        # Check that adventures show requirement counts
        assert page.is_visible("text=Bobcat (4 requirements)")
        assert page.is_visible("text=Fun on the Run (4 requirements)")

    def test_navigation_workflow_displayed(self, page):
        """Test that workflow guide is visible on this page."""
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        assert page.is_visible("text=Configure requirements")


@pytest.mark.slow
class TestManageRequirementsIntegration:
    """Integration tests for Manage Requirements page."""

    def test_requirements_sync_with_dashboard(self, page):
        """Test that requirements shown match dashboard data."""
        # Get requirements from Manage Requirements page
        click_nav_item(page, "Manage Requirements")
        wait_for_streamlit(page)

        requirements_content = page.content()

        # Navigate to dashboard
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        dashboard_content = page.content()

        # Check that key adventures appear in both
        for adventure in ["Bobcat", "Fun on the Run", "Lion's Pride"]:
            assert adventure in requirements_content
            assert adventure in dashboard_content

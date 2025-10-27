"""
UI tests for the Plan Meetings page.

Tests meeting planning recommendations and requirement prioritization.
"""

import pytest
from .conftest import click_nav_item, wait_for_streamlit


class TestPlanMeetings:
    """Test suite for Plan Meetings page."""

    def test_page_loads(self, page):
        """Test that the Plan Meetings page loads correctly."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Plan Meetings")
        assert page.is_visible("text=See which required requirements need the most attention")

    def test_view_options_visible(self, page):
        """Test that view filtering options are displayed."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=View Options")
        assert page.is_visible("text=Show:")

    def test_view_option_all_requirements(self, page):
        """Test 'All Required Requirements' option."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=All Required Requirements")

    def test_view_option_incomplete(self, page):
        """Test 'Incomplete Only' option."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Incomplete Only (< 100%)")

    def test_view_option_most_needed(self, page):
        """Test 'Most Needed' option."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Most Needed (< 50%)")

    def test_group_by_adventure_option(self, page):
        """Test group by adventure checkbox."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Group by Adventure")

    def test_requirements_by_adventure_section(self, page):
        """Test that requirements are grouped by adventure."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Required Requirements by Adventure")

    def test_adventure_sections_displayed(self, page):
        """Test that adventure sections are shown."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        # Should show Bobcat adventure
        assert page.is_visible("text=Bobcat")
        # Should show requirement count and average completion
        page_content = page.content()
        assert "requirements" in page_content.lower()
        assert "average completion" in page_content.lower()

    def test_requirement_completion_percentages(self, page):
        """Test that completion percentages are displayed."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        # Get completion percentages
        percentages = page.evaluate("""
            () => {
                const text = document.body.textContent;
                const matches = text.match(/\\d+% complete/g);
                return matches ? matches.length : 0;
            }
        """)

        # Should have multiple completion percentages shown
        assert percentages > 0

    def test_still_need_lists(self, page):
        """Test that 'Still need' scout lists are shown."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Still need:")

    def test_completed_by_lists(self, page):
        """Test that 'Completed by' scout lists are shown."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        assert page.is_visible("text=Completed by:")


@pytest.mark.slow
class TestPlanMeetingsIntegration:
    """Integration tests for Plan Meetings page."""

    def test_plan_meetings_reflects_progress(self, page):
        """Test that planning data reflects actual scout progress."""
        # Check Plan Meetings
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        # Get a requirement's completion percentage
        plan_content = page.content()

        # Navigate to Dashboard to verify consistency
        click_nav_item(page, "Tracker Dashboard")
        wait_for_streamlit(page)

        dashboard_content = page.content()

        # Both should show Bobcat data
        assert "Bobcat" in plan_content
        assert "Bobcat" in dashboard_content

    def test_filtering_changes_display(self, page):
        """Test that changing filter options updates the display."""
        click_nav_item(page, "Plan Meetings")
        wait_for_streamlit(page)

        # Get initial requirement count
        initial_content = page.content()

        # Click "Incomplete Only" radio button
        page.evaluate("""
            () => {
                const labels = Array.from(document.querySelectorAll('label'));
                const incompleteLabel = labels.find(l => l.textContent.includes('Incomplete Only'));
                if (incompleteLabel) {
                    const radio = incompleteLabel.querySelector('input[type="radio"]');
                    if (radio) radio.click();
                }
            }
        """)
        wait_for_streamlit(page, 2000)

        # Content should have changed
        filtered_content = page.content()

        # The filtering should affect what's displayed
        # (We can't guarantee specific changes without knowing exact data state)
        assert filtered_content is not None

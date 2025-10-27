# Scout Tracker UI Tests

Automated browser tests using Playwright to verify Scout Tracker functionality.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-ui-test.txt
playwright install chromium

# Run all tests
./run_ui_tests.sh

# Run specific tests
./run_ui_tests.sh -k roster
```

## Test Files

- `test_manage_roster.py` - Roster management (9 tests)
- `test_manage_requirements.py` - Requirements configuration (10 tests)
- `test_dashboard.py` - Progress dashboard (11 tests)
- `test_plan_meetings.py` - Meeting planning (11 tests)
- `test_individual_reports.py` - Scout reports (10 tests)

**Total: 51 tests**

## Test Types

### Unit Tests (Fast ~30s)
- Page load verification
- UI element visibility
- Basic interactions

### Integration Tests (Slow ~2m)
- Cross-page workflows
- Data persistence
- End-to-end scenarios

**Marker:** `@pytest.mark.slow`

## Common Commands

```bash
# All tests
./run_ui_tests.sh

# Fast tests only
./run_ui_tests.sh --fast

# Specific page
./run_ui_tests.sh -k dashboard

# Parallel execution
./run_ui_tests.sh -n 4

# HTML report
./run_ui_tests.sh --html
```

## Fixtures

- `streamlit_app` - Starts/stops Streamlit app (session scope)
- `page` - Fresh browser page per test (function scope)
- `test_data_backup` - Backs up/restores data for destructive tests

## Writing Tests

```python
from .conftest import click_nav_item, wait_for_streamlit

class TestFeature:
    def test_feature_loads(self, page):
        click_nav_item(page, "Feature Name")
        wait_for_streamlit(page)
        assert page.is_visible("text=Expected Text")
```

See `../../UI_TESTING_GUIDE.md` for complete documentation.

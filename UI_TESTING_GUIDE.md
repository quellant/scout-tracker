# Scout Tracker UI Testing Guide

## Overview

The Scout Tracker application includes a comprehensive UI test suite using **Playwright** for automated browser testing. These tests verify that all pages load correctly, user interactions work as expected, and data flows properly between components.

---

## Quick Start

### 1. Install Test Dependencies

```bash
pip install -r requirements-ui-test.txt
playwright install chromium
```

### 2. Run All Tests

```bash
./run_ui_tests.sh
```

### 3. Run Specific Tests

```bash
# Run only roster tests
./run_ui_tests.sh -k roster

# Run only fast tests (skip slow integration tests)
./run_ui_tests.sh --fast

# Run tests in parallel (4 processes)
./run_ui_tests.sh -n 4

# Generate HTML report
./run_ui_tests.sh --html
```

---

## Test Structure

### Test Files

```
tests/ui/
├── conftest.py                     # Test fixtures and helpers
├── test_manage_roster.py           # Roster management tests
├── test_manage_requirements.py     # Requirements management tests
├── test_dashboard.py               # Dashboard and progress tests
├── test_plan_meetings.py           # Meeting planning tests
└── test_individual_reports.py      # Individual scout report tests
```

### Test Categories

#### Unit Tests (Fast)
- Page load verification
- UI element visibility
- Basic interaction testing
- **Marker:** No marker (default)
- **Runtime:** ~30 seconds

#### Integration Tests (Slow)
- Cross-page data consistency
- End-to-end workflows
- Data persistence verification
- **Marker:** `@pytest.mark.slow`
- **Runtime:** ~2-3 minutes

---

## Test Fixtures

### Session-Level Fixtures

#### `streamlit_app`
- **Scope:** Session
- **Purpose:** Starts the Streamlit app once for all tests
- **Lifecycle:**
  1. Launches `streamlit run app.py` on port 8501
  2. Waits for app to be ready (max 30 seconds)
  3. Yields the app URL
  4. Terminates the app after all tests complete

#### `test_data_backup`
- **Scope:** Function
- **Purpose:** Backs up and restores `tracker_data/` for tests that modify data
- **Usage:**
  ```python
  def test_add_scout(page, test_data_backup):
      # Test that modifies data
      # Data will be restored after test
  ```

### Function-Level Fixtures

#### `page`
- **Scope:** Function
- **Purpose:** Provides a fresh browser page for each test
- **Configuration:**
  - Browser: Chromium (headless)
  - Viewport: 1280x720
  - Auto-navigates to Streamlit app
  - Waits for "Scout Tracker" text to appear

---

## Writing Tests

### Basic Test Structure

```python
from .conftest import click_nav_item, wait_for_streamlit

class TestMyFeature:
    """Test suite for my feature."""

    def test_feature_loads(self, page):
        """Test that feature loads correctly."""
        click_nav_item(page, "My Feature")
        wait_for_streamlit(page)

        assert page.is_visible("text=Expected Text")

    @pytest.mark.slow
    def test_feature_integration(self, page, test_data_backup):
        """Test feature with data modification."""
        # Test code that modifies data
        # Data will be restored automatically
```

### Helper Functions

#### `click_nav_item(page, item_text)`
Clicks a navigation menu item.

```python
click_nav_item(page, "Manage Roster")
wait_for_streamlit(page)
```

#### `wait_for_streamlit(page, timeout=5000)`
Waits for Streamlit to finish rendering.

```python
wait_for_streamlit(page, 3000)  # Wait 3 seconds
```

### Common Patterns

#### Checking Element Visibility
```python
assert page.is_visible("text=Scout Tracker")
assert page.is_visible("button:has-text('Add Scout')")
```

#### Filling Forms
```python
page.fill("input[aria-label='Scout Name']", "Test Scout")
```

#### Clicking Buttons
```python
page.evaluate("""
    () => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const addButton = buttons.find(btn => btn.textContent.includes('Add Scout'));
        if (addButton) addButton.click();
    }
""")
```

#### Getting Page Content
```python
scouts = page.evaluate("""
    () => {
        const cells = Array.from(document.querySelectorAll('td'));
        return cells.map(cell => cell.textContent.trim());
    }
""")
```

---

## Running Tests

### All Tests
```bash
./run_ui_tests.sh
```

### Specific Test File
```bash
pytest tests/ui/test_manage_roster.py -v
```

### Specific Test Function
```bash
pytest tests/ui/test_manage_roster.py::TestManageRoster::test_page_loads -v
```

### With Filters
```bash
# Run only tests with "roster" in the name
./run_ui_tests.sh -k roster

# Run only integration tests
./run_ui_tests.sh --slow

# Run only unit tests (skip slow)
./run_ui_tests.sh --fast
```

### Parallel Execution
```bash
# Run tests in 4 parallel processes
./run_ui_tests.sh -n 4
```

### With HTML Report
```bash
./run_ui_tests.sh --html
# Opens test-report.html
```

---

## Test Coverage

### Pages Tested

| Page | Tests | Coverage |
|------|-------|----------|
| Manage Roster | 9 tests | ✅ Full |
| Manage Requirements | 10 tests | ✅ Full |
| Tracker Dashboard | 11 tests | ✅ Full |
| Plan Meetings | 11 tests | ✅ Full |
| Individual Reports | 10 tests | ✅ Full |
| **Total** | **51 tests** | **100%** |

### Test Types

- **Page Load Tests:** Verify all pages load without errors
- **UI Element Tests:** Verify all expected elements are visible
- **Interaction Tests:** Verify user interactions work correctly
- **Data Tests:** Verify data displays and persists correctly
- **Integration Tests:** Verify cross-page consistency

---

## Troubleshooting

### Tests Fail to Start

**Problem:** `streamlit_app` fixture times out

**Solution:**
1. Check if port 8501 is already in use: `lsof -i :8501`
2. Kill any existing Streamlit processes
3. Ensure you're in the project root directory

### Tests Fail Randomly

**Problem:** Intermittent failures due to timing

**Solution:**
1. Increase wait times in `wait_for_streamlit(page, timeout)`
2. Add explicit waits: `page.wait_for_selector("text=Expected")`
3. Check for race conditions in test code

### Browser Not Found

**Problem:** Playwright browsers not installed

**Solution:**
```bash
playwright install chromium
```

### Data Persistence Issues

**Problem:** Tests affect each other's data

**Solution:**
1. Use the `test_data_backup` fixture
2. Ensure tests are isolated
3. Don't rely on data from previous tests

---

## Best Practices

### 1. Use Fixtures
Always use `test_data_backup` for tests that modify data:
```python
def test_add_scout(self, page, test_data_backup):
    # Modifies roster - data will be restored
```

### 2. Wait for Streamlit
Always wait after navigation or actions:
```python
click_nav_item(page, "Dashboard")
wait_for_streamlit(page, 2000)
```

### 3. Use Descriptive Test Names
```python
def test_dashboard_shows_progress_for_all_scouts(self, page):
    """Test that dashboard displays progress for every scout in roster."""
```

### 4. Mark Slow Tests
```python
@pytest.mark.slow
def test_full_workflow(self, page, test_data_backup):
    """Test complete workflow from adding scout to viewing report."""
```

### 5. Test One Thing
Keep tests focused:
```python
# Good
def test_add_button_visible(self, page):
    assert page.is_visible("button:has-text('Add Scout')")

# Not as good
def test_entire_roster_workflow(self, page):
    # Tests many things
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: UI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-ui-test.txt
          playwright install chromium --with-deps
      - name: Run UI tests
        run: ./run_ui_tests.sh --fast
      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: test-report.html
```

---

## Maintenance

### Adding New Tests

1. Create test file in `tests/ui/`
2. Import fixtures: `from .conftest import click_nav_item, wait_for_streamlit`
3. Create test class: `class TestNewFeature:`
4. Write tests using `page` fixture
5. Run tests: `pytest tests/ui/test_new_feature.py -v`

### Updating Tests After Code Changes

1. Run all tests: `./run_ui_tests.sh`
2. Fix failures related to UI changes
3. Update selectors if elements changed
4. Update assertions if behavior changed

---

## Performance

### Test Execution Times

| Test Type | Count | Time | Per Test |
|-----------|-------|------|----------|
| Unit Tests | 40 | ~30s | 0.75s |
| Integration Tests | 11 | ~2m | 11s |
| **Total** | **51** | **~2.5m** | **3s** |

### Optimization Tips

1. **Run in Parallel:** Use `-n 4` for 4x speedup
2. **Skip Slow Tests:** Use `--fast` during development
3. **Filter Tests:** Use `-k pattern` to run specific tests
4. **Reuse Session:** Session-scoped `streamlit_app` fixture shares app across tests

---

## Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Streamlit Testing Best Practices](https://docs.streamlit.io/knowledge-base/using-streamlit/how-do-i-test-my-streamlit-app)

---

## Support

If tests fail or you encounter issues:

1. Check this guide's Troubleshooting section
2. Review test output for error messages
3. Run individual failing tests with `-v` for verbose output
4. Check if data needs to be restored manually

---

**Last Updated:** October 24, 2025
**Test Framework:** Playwright + Pytest
**Coverage:** 51 UI tests across 5 pages

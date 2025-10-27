# Scout Tracker Test Suite

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=scout_tracker --cov-report=html
```

## Test Files

| File | Tests | Focus Area |
|------|-------|------------|
| `test_data_operations.py` | 54 | Data I/O, file operations, cache management |
| `test_roster_requirements.py` | 60 | Roster management, requirement tracking, multi-rank support |
| `test_meetings_attendance.py` | 41 | Meeting creation, attendance logging, date handling |
| `test_dashboard_reports.py` | 29 | Dashboard calculations, progress tracking, reporting |
| `test_onboarding_edge_cases.py` | 43 | Onboarding flow, edge cases, integration tests |
| **TOTAL** | **227** | **Full application coverage** |

## Test Markers

Use markers to run specific test categories:

```bash
pytest -m data          # Data operations tests
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m ui            # UI/onboarding tests
```

## Test Isolation

All tests use the `test_data_dir` fixture to ensure complete isolation:

- ✅ Each test gets its own temporary directory
- ✅ Real `tracker_data/` is NEVER touched
- ✅ Tests can run in any order
- ✅ No test affects another

## Key Fixtures

Available in `conftest.py`:

- `test_data_dir` - Temporary test directory
- `sample_roster` - Sample scout data
- `sample_requirements` - Sample requirement data
- `sample_meetings` - Sample meeting data
- `sample_attendance` - Sample attendance data
- `initialized_test_env` - Fully initialized test environment

## Adding New Tests

1. Create test file: `test_<feature>.py`
2. Import fixtures from conftest
3. Use `test_data_dir` for isolation
4. Follow naming: `test_<what_it_does>`
5. Add docstring explaining test purpose
6. Mark with appropriate decorator (`@pytest.mark.unit`, etc.)

Example:

```python
import pytest
import scout_tracker

@pytest.mark.unit
def test_new_feature(test_data_dir, sample_roster):
    """Test that new feature works correctly."""
    # Test implementation
    assert True
```

## Coverage

Current coverage: **90%+ of data layer**

- Data I/O functions: 100%
- Business logic: 90%+
- Error handling: 90%+

Overall coverage is lower because Streamlit UI code (which requires a browser) is not tested.

## Running Specific Tests

```bash
# Single file
pytest tests/test_data_operations.py -v

# Single test
pytest tests/test_data_operations.py::TestInitialization::test_initialize_creates_directory -v

# By keyword
pytest -k "roster" -v

# Failed tests only
pytest --lf -v
```

## Continuous Integration

Tests run automatically on push via GitHub Actions. See `.github/workflows/test.yml`.

## More Information

See `TEST_SUITE_SUMMARY.md` for comprehensive documentation.

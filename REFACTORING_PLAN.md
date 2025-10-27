# Scout Tracker Refactoring Plan

## Current State
- **File:** `scout_tracker.py` (2,347 lines)
- **Structure:** Monolithic file with everything mixed together
- **Functions:** 20 functions total

## Problems with Current Structure
1. Single 2,347-line file is hard to navigate
2. Constants, data I/O, business logic, and UI all mixed together
3. Difficult to test individual components
4. Hard to maintain and extend
5. Violates Single Responsibility Principle

## Proposed New Structure

```
scout_tracker/              # New package directory
├── __init__.py
├── __main__.py            # Entry point: python -m scout_tracker
├── config/
│   ├── __init__.py
│   └── constants.py       # All REQUIREMENTS data, DATA_DIR
├── data/
│   ├── __init__.py
│   ├── io.py             # File I/O: load/save functions
│   └── cache.py          # Streamlit cache management
├── services/
│   ├── __init__.py
│   ├── roster.py         # Roster business logic
│   ├── requirements.py   # Requirement tracking logic
│   ├── meetings.py       # Meeting management logic
│   ├── attendance.py     # Attendance tracking logic
│   └── reports.py        # Dashboard calculations, reports
├── ui/
│   ├── __init__.py
│   ├── app.py            # Main app, navigation, routing
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py
│       ├── roster.py
│       ├── requirements.py
│       ├── meetings.py
│       ├── attendance.py
│       ├── plan_meetings.py
│       ├── individual_reports.py
│       └── onboarding.py
└── app.py                # Top-level entry: streamlit run app.py
```

## Migration Strategy

### Phase 1: Extract Constants & Configuration
**Files to create:**
- `scout_tracker/config/__init__.py`
- `scout_tracker/config/constants.py`

**Content:**
- DATA_DIR, file paths
- LION_REQUIREMENTS, TIGER_REQUIREMENTS, etc.
- RANK_REQUIREMENTS dictionary

### Phase 2: Extract Data Layer
**Files to create:**
- `scout_tracker/data/__init__.py`
- `scout_tracker/data/io.py`
- `scout_tracker/data/cache.py`

**Functions to move:**
- `initialize_data_files()`
- `load_roster()`, `load_requirement_key()`, `load_meetings()`, `load_attendance()`
- `save_roster()`, `save_requirements()`, `save_meetings()`, `save_attendance()`
- `clear_cache()`

### Phase 3: Extract Business Logic
**Files to create:**
- `scout_tracker/services/roster.py`
- `scout_tracker/services/requirements.py`
- `scout_tracker/services/meetings.py`
- `scout_tracker/services/attendance.py`
- `scout_tracker/services/reports.py`

**Content:**
- Helper functions extracted from UI pages
- Progress calculations
- Eligibility checks
- Data aggregation logic

### Phase 4: Extract UI Pages
**Files to create:**
- `scout_tracker/ui/app.py`
- `scout_tracker/ui/pages/*.py` (8 page modules)

**Functions to move:**
- `page_manage_roster()` → `ui/pages/roster.py`
- `page_manage_requirements()` → `ui/pages/requirements.py`
- `page_manage_meetings()` → `ui/pages/meetings.py`
- `page_log_attendance()` → `ui/pages/attendance.py`
- `page_tracker_dashboard()` → `ui/pages/dashboard.py`
- `page_plan_meetings()` → `ui/pages/plan_meetings.py`
- `page_individual_scout_reports()` → `ui/pages/individual_reports.py`
- `page_onboarding()` → `ui/pages/onboarding.py`
- `main()` → `ui/app.py`

### Phase 5: Create Entry Points
**Files to create:**
- `scout_tracker/__init__.py` - Package exports
- `scout_tracker/__main__.py` - For `python -m scout_tracker`
- `app.py` - Top-level for `streamlit run app.py`

### Phase 6: Update Tests
**Files to update:**
- `tests/conftest.py` - Update imports
- All test files - Update imports from scout_tracker.* to new structure

### Phase 7: Verify & Increase Coverage
- Run all tests
- Check coverage
- Add tests for newly exposed services layer
- Target: 90% coverage of all non-UI code

## Benefits of New Structure

1. **Separation of Concerns**
   - Constants separate from logic
   - Data I/O separate from business logic
   - Business logic separate from UI

2. **Testability**
   - Easy to test services independently
   - Mock data layer for service tests
   - No Streamlit dependency in tests for services

3. **Maintainability**
   - Easy to find specific functionality
   - Clear module boundaries
   - Single Responsibility Principle

4. **Extensibility**
   - Easy to add new ranks
   - Easy to add new reports
   - Easy to add new pages

5. **Better Coverage**
   - Can test services layer thoroughly
   - Clear separation enables better unit tests
   - Easier to reach 90% coverage

## Backward Compatibility

Old entry point will still work:
```bash
# Old way (still works via app.py wrapper)
streamlit run app.py

# New way
python -m scout_tracker

# Also works
streamlit run scout_tracker/ui/app.py
```

## Rollout Plan

1. ✅ Create new directory structure
2. ✅ Extract constants
3. ✅ Extract data layer
4. ✅ Extract services layer
5. ✅ Extract UI pages
6. ✅ Create entry points
7. ✅ Update tests
8. ✅ Verify all tests pass
9. ✅ Add service layer tests
10. ✅ Reach 90% coverage

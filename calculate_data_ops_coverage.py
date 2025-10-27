#!/usr/bin/env python3
"""
Calculate coverage percentage specifically for data operations functions.
This script parses the coverage.xml file and extracts coverage for only
the data operations functions we're testing.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Line ranges for each function (start, end inclusive)
FUNCTION_RANGES = {
    'initialize_data_files': (788, 813),
    'load_roster': (820, 825),
    'load_requirement_key': (828, 833),
    'load_meetings': (836, 843),
    'load_attendance': (846, 853),
    'clear_cache': (855, 860),
    'save_roster': (862, 865),
    'save_requirements': (867, 870),
    'save_meetings': (872, 879),
    'save_attendance': (881, 888)
}

def calculate_coverage():
    """Calculate coverage for data operations functions."""
    coverage_file = Path('coverage.xml')

    if not coverage_file.exists():
        print("ERROR: coverage.xml not found. Run tests with --cov first.")
        return

    tree = ET.parse(coverage_file)
    root = tree.getroot()

    # Find scout_tracker.py in the coverage report
    scout_tracker_class = None
    for package in root.findall('.//package'):
        for cls in package.findall('.//class'):
            if cls.get('filename').endswith('scout_tracker.py'):
                scout_tracker_class = cls
                break
        if scout_tracker_class:
            break

    if not scout_tracker_class:
        print("ERROR: scout_tracker.py not found in coverage report")
        return

    # Get all lines with coverage info
    covered_lines = set()
    total_lines = set()

    for line in scout_tracker_class.findall('.//line'):
        line_num = int(line.get('number'))
        hits = int(line.get('hits', 0))

        # Check if this line is in any of our target functions
        for func_name, (start, end) in FUNCTION_RANGES.items():
            if start <= line_num <= end:
                total_lines.add(line_num)
                if hits > 0:
                    covered_lines.add(line_num)
                break

    # Calculate coverage
    if not total_lines:
        print("ERROR: No lines found for target functions")
        return

    coverage_pct = (len(covered_lines) / len(total_lines)) * 100

    print("=" * 70)
    print("DATA OPERATIONS FUNCTIONS COVERAGE REPORT")
    print("=" * 70)
    print(f"\nTotal executable lines: {len(total_lines)}")
    print(f"Covered lines: {len(covered_lines)}")
    print(f"Coverage: {coverage_pct:.2f}%")
    print()

    # Show per-function coverage
    print("Per-Function Coverage:")
    print("-" * 70)

    for func_name, (start, end) in sorted(FUNCTION_RANGES.items()):
        func_total = 0
        func_covered = 0

        for line_num in range(start, end + 1):
            if line_num in total_lines:
                func_total += 1
                if line_num in covered_lines:
                    func_covered += 1

        if func_total > 0:
            func_pct = (func_covered / func_total) * 100
            status = "✓" if func_pct >= 90 else "✗"
            print(f"{status} {func_name:30s} {func_covered:3d}/{func_total:3d} lines ({func_pct:6.2f}%)")
        else:
            print(f"  {func_name:30s} No executable lines found")

    print("=" * 70)

    if coverage_pct >= 90:
        print(f"\n✓ SUCCESS: Coverage {coverage_pct:.2f}% exceeds 90% requirement")
        return 0
    else:
        print(f"\n✗ FAIL: Coverage {coverage_pct:.2f}% is below 90% requirement")
        return 1

if __name__ == '__main__':
    exit(calculate_coverage())

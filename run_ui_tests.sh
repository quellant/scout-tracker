#!/bin/bash
# Scout Tracker UI Test Runner
# Runs Playwright UI tests for the Scout Tracker application

set -e  # Exit on error

echo ""
echo "========================================"
echo " Scout Tracker UI Test Runner"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required to run tests."
    exit 1
fi

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "ERROR: Must run from project root directory (where app.py is located)"
    exit 1
fi

echo "[1/4] Checking test dependencies..."

# Check if pytest is installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "Installing test dependencies..."
    pip install -r requirements-ui-test.txt
else
    echo "Test dependencies already installed"
fi

# Check if Playwright browsers are installed
echo ""
echo "[2/4] Checking Playwright browsers..."
if ! python3 -m playwright install --help &>/dev/null; then
    echo "Installing Playwright..."
    pip install playwright
fi

# Install Playwright browsers if not already installed
python3 -m playwright install chromium --with-deps

echo ""
echo "[3/4] Running UI tests..."
echo ""

# Parse command line arguments
TEST_FILTER=""
PARALLEL=""
VERBOSE="-v"
HTML_REPORT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--filter)
            TEST_FILTER="-k $2"
            shift 2
            ;;
        -n|--parallel)
            PARALLEL="-n $2"
            shift 2
            ;;
        -q|--quiet)
            VERBOSE=""
            shift
            ;;
        --html)
            HTML_REPORT="--html=test-report.html --self-contained-html"
            shift
            ;;
        --slow)
            TEST_FILTER="-m slow"
            shift
            ;;
        --fast)
            TEST_FILTER="-m 'not slow'"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -k, --filter PATTERN    Run only tests matching PATTERN"
            echo "  -n, --parallel N        Run tests in N parallel processes"
            echo "  -q, --quiet             Reduce output verbosity"
            echo "  --html                  Generate HTML test report"
            echo "  --slow                  Run only slow integration tests"
            echo "  --fast                  Run only fast unit tests (skip slow tests)"
            echo "  -h, --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                      # Run all tests"
            echo "  $0 -k roster            # Run only roster tests"
            echo "  $0 -n 4                 # Run tests in 4 parallel processes"
            echo "  $0 --fast               # Run only fast tests"
            echo "  $0 --html               # Generate HTML report"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Run pytest with Playwright
python3 -m pytest tests/ui/ \
    $VERBOSE \
    $TEST_FILTER \
    $PARALLEL \
    $HTML_REPORT \
    --tb=short \
    --timeout=60

TEST_RESULT=$?

echo ""
echo "[4/4] Test run complete"
echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo "========================================"
    echo " ✅ ALL TESTS PASSED"
    echo "========================================"
else
    echo "========================================"
    echo " ❌ SOME TESTS FAILED"
    echo "========================================"
    echo ""
    echo "Check the output above for details."
fi

if [ -n "$HTML_REPORT" ]; then
    echo ""
    echo "HTML report generated: test-report.html"
fi

echo ""

exit $TEST_RESULT

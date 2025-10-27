#!/bin/bash
# Build script for Scout Tracker standalone executable bundle (Linux/Mac)
# This creates a NO-PYTHON-REQUIRED distribution
# Updated for modular package structure

set -e  # Exit on error

echo ""
echo "========================================"
echo " Building Scout Tracker Executable"
echo " (Refactored Modular Version)"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required to BUILD the executable."
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if scout_tracker package exists
if [ ! -d "scout_tracker" ]; then
    echo "ERROR: scout_tracker package not found!"
    echo "Please ensure you're in the project root directory."
    exit 1
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py entry point not found!"
    echo "Please ensure you're in the project root directory."
    exit 1
fi

echo "[1/6] Installing build dependencies..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install pyinstaller pandas streamlit --quiet

echo "[2/6] Building executable bundle (this may take 2-5 minutes)..."
echo "      This creates a folder with all files needed to run without Python."
echo "      Entry point: app.py (refactored modular structure)"
pyinstaller scout_tracker.spec --clean --noconfirm

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed! Check the output above for errors."
    exit 1
fi

echo "[3/6] Verifying build output..."
if [ ! -f "dist/ScoutTracker/ScoutTracker" ]; then
    echo ""
    echo "ERROR: Build failed - ScoutTracker executable not found!"
    echo "Check the output above for errors."
    exit 1
fi

echo "[4/6] Creating user-friendly launcher scripts..."

# Create bash launcher
cat > dist/ScoutTracker/start_scout_tracker.sh << 'EOF'
#!/bin/bash
# Scout Tracker Launcher for Linux/Mac

# Colors for terminal output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

clear
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}     SCOUT TRACKER - Starting...${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "    Opening Scout Tracker in your web browser..."
echo ""
echo "========================================"
echo "KEEP THIS TERMINAL OPEN while using the app"
echo "Press Ctrl+C to stop Scout Tracker"
echo "========================================"
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Run the executable
./ScoutTracker
EOF

chmod +x dist/ScoutTracker/start_scout_tracker.sh

# Create Mac .command launcher (double-clickable on macOS)
cat > dist/ScoutTracker/start_scout_tracker.command << 'EOF'
#!/bin/bash
# Scout Tracker Launcher for macOS (double-clickable)

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Run the bash launcher
./start_scout_tracker.sh
EOF

chmod +x dist/ScoutTracker/start_scout_tracker.command

echo "[5/6] Creating Quick Start guide..."
cat > dist/ScoutTracker/QUICK_START.txt << 'EOF'
================================================================================
                        SCOUT TRACKER - QUICK START
================================================================================

HOW TO USE (1 STEP!):

  Linux:
    - Open terminal in this folder
    - Run: ./start_scout_tracker.sh

  macOS:
    - Double-click "start_scout_tracker.command"
    - Or in terminal: ./start_scout_tracker.sh

That's it! The app will open in your web browser.

================================================================================
                              IMPORTANT NOTES
================================================================================

  NO PYTHON INSTALLATION REQUIRED!

  ✓ Keep the terminal window open while using the app
  ✓ To STOP: Press Ctrl+C in the terminal
  ✓ Your data is saved in the "tracker_data" folder
  ✓ First launch may take 10-30 seconds

TROUBLESHOOTING:

  Problem: "Permission denied" error
  Solution: Run: chmod +x start_scout_tracker.sh

  Problem: Browser doesn't open
  Solution: Manually go to http://localhost:8501

  Problem: App won't start
  Solution: Close terminal and try again

================================================================================

REFACTORED VERSION NOTES:

  - Built from modular package structure (scout_tracker/)
  - Entry point: app.py
  - All functionality preserved from original version

================================================================================
EOF

echo "[6/6] Creating README..."
cat > dist/ScoutTracker/README.md << 'EOF'
# Scout Tracker - Standalone Distribution

This is a standalone version of Scout Tracker that **does not require Python** to be installed.

## Quick Start

### Linux
```bash
./start_scout_tracker.sh
```

### macOS
Double-click `start_scout_tracker.command` or run in terminal:
```bash
./start_scout_tracker.sh
```

## What's Included

- `ScoutTracker` - The main executable (includes Python + all dependencies)
- `start_scout_tracker.sh` - Launcher script for Linux/Mac
- `start_scout_tracker.command` - Double-clickable launcher for macOS
- `_internal/` - Required libraries and dependencies
- `QUICK_START.txt` - Simple instructions

## Data Storage

All your data is stored in the `tracker_data` folder that will be created when you first run the app. You can back up this folder to save your data.

## Stopping the App

Press `Ctrl+C` in the terminal window to stop the application.

## System Requirements

- Linux: Any modern distribution (tested on Ubuntu 20.04+)
- macOS: 10.13 (High Sierra) or later
- ~200MB disk space

## Troubleshooting

### Permission Denied
If you get a "permission denied" error, run:
```bash
chmod +x start_scout_tracker.sh
chmod +x ScoutTracker
```

### Browser Doesn't Open
The app runs at http://localhost:8501 - manually open this in your browser.

### Port Already in Use
If port 8501 is in use, Streamlit will try 8502, 8503, etc. Check the terminal output for the actual port.

---

Generated with PyInstaller
EOF

echo ""
echo "========================================"
echo " BUILD SUCCESSFUL!"
echo "========================================"
echo ""
echo " Location: dist/ScoutTracker/"
echo ""
echo " Package Info:"
echo " - Built from refactored modular structure"
echo " - Entry point: app.py"
echo " - Package: scout_tracker/"
echo ""
echo " Next steps:"
echo " 1. Test: cd dist/ScoutTracker && ./start_scout_tracker.sh"
echo " 2. Distribute: Zip or tar the entire 'ScoutTracker' folder"
echo " 3. Users: Extract and run start_scout_tracker.sh"
echo ""
echo " NO PYTHON REQUIRED for end users!"
echo ""
echo "========================================"

# Show size
if [ -d "dist/ScoutTracker" ]; then
    SIZE=$(du -sh dist/ScoutTracker | cut -f1)
    echo " Package size: $SIZE"
    echo "========================================"
fi

"""
Script to create a portable Windows package for Scout Tracker.
This creates a folder that can be zipped and distributed to Windows users.
"""

import os
import shutil
from pathlib import Path

def create_portable_package():
    """Create a portable distribution package."""

    # Create distribution folder
    dist_folder = Path("ScoutTracker_Portable")
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    dist_folder.mkdir()

    print(f"Creating portable package in {dist_folder}/...")

    # Create app subfolder for technical files
    app_folder = dist_folder / "app"
    app_folder.mkdir()

    # Copy application files to app subfolder
    # Copy the modular package structure
    shutil.copytree("scout_tracker", app_folder / "scout_tracker")
    shutil.copy("app.py", app_folder)
    shutil.copy("requirements.txt", app_folder)
    shutil.copy("README.md", app_folder)

    # Create ONE-CLICK launcher script that handles everything
    launcher_content = """@echo off
title Scout Tracker
color 0A
cls

echo.
echo    ========================================
echo         SCOUT TRACKER - Starting...
echo    ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    cls
    echo.
    echo    ========================================
    echo         ERROR: Python Not Found
    echo    ========================================
    echo.
    echo    Python is required but not installed.
    echo.
    echo    SOLUTION:
    echo    1. Run "INSTALL_PYTHON.bat" in this folder
    echo       (or manually install from python.org)
    echo.
    echo    2. Then run this file again
    echo.
    echo    ========================================
    echo.
    pause
    exit /b 1
)

REM Check/install dependencies on first run
if not exist "app\\.setup_complete" (
    echo    Setting up Scout Tracker for first use...
    echo    This only happens once and may take 1-2 minutes.
    echo.
    echo    [1/2] Updating pip...
    python -m pip install --upgrade pip --quiet
    echo    [2/2] Installing Scout Tracker...
    cd app
    python -m pip install -r requirements.txt --quiet
    cd ..
    echo.> app\\.setup_complete
    echo    Setup complete!
    echo.
)

echo    Opening Scout Tracker in your web browser...
echo.
echo    ========================================
echo    KEEP THIS WINDOW OPEN while using the app
echo    Close this window to stop Scout Tracker
echo    ========================================
echo.

cd app
python -m streamlit run app.py --server.headless=false
cd ..
"""

    with open(dist_folder / "START_TRACKER.bat", "w") as f:
        f.write(launcher_content)

    # Create super-simple Quick Start guide
    quick_start = """================================================================================
                        SCOUT TRACKER - QUICK START
================================================================================

HOW TO USE (2 STEPS):

  STEP 1: Install Python (ONE TIME ONLY)
          - Double-click "INSTALL_PYTHON.bat"
          - Follow the installer (check "Add Python to PATH")
          - If you already have Python installed, skip this step

  STEP 2: Start Scout Tracker
          - Double-click "START_TRACKER.bat"
          - Wait for your web browser to open
          - Keep the black window open while using the app

That's it! Everything else is automatic.

================================================================================
                              IMPORTANT NOTES
================================================================================

  ✓ First launch takes 1-2 minutes (one-time setup)
  ✓ Later launches are instant
  ✓ To STOP the app: Close the black window
  ✓ Your data is saved in the "tracker_data" folder

TROUBLESHOOTING:

  Problem: "Python not found" error
  Solution: Run INSTALL_PYTHON.bat or install from python.org

  Problem: Browser doesn't open
  Solution: Manually go to http://localhost:8501

  Problem: App won't start
  Solution: Close all black windows and try again

================================================================================

For detailed information, see README.md in the "app" folder.

"""

    with open(dist_folder / "QUICK_START.txt", "w") as f:
        f.write(quick_start)

    # Create Python installer helper
    python_installer = """@echo off
title Install Python for Scout Tracker
color 0B
cls

echo.
echo    ========================================
echo         PYTHON INSTALLATION HELPER
echo    ========================================
echo.
echo    This will help you download and install Python.
echo.
echo    IMPORTANT STEPS:
echo    1. A web page will open in your browser
echo    2. Click the yellow "Download Python" button
echo    3. Run the downloaded file
echo    4. CHECK THE BOX: "Add Python to PATH"
echo    5. Click "Install Now"
echo.
echo    ========================================
echo.
pause

REM Open Python download page
start https://www.python.org/downloads/

echo.
echo    Browser opened! Follow the steps above.
echo.
echo    After installing Python:
echo    - Restart your computer (important!)
echo    - Then run START_TRACKER.bat
echo.
pause
"""

    with open(dist_folder / "INSTALL_PYTHON.bat", "w") as f:
        f.write(python_installer)

    print(f"\n✅ Portable package created successfully!")
    print(f"\n📦 Package structure:")
    print(f"   ScoutTracker_Portable/")
    print(f"   ├── QUICK_START.txt          ← Users read this first")
    print(f"   ├── START_TRACKER.bat        ← ONE-CLICK to run (auto-installs)")
    print(f"   ├── INSTALL_PYTHON.bat       ← Helper to install Python")
    print(f"   └── app/                     ← Technical files")
    print(f"       ├── scout_tracker/       ← Modular package structure")
    print(f"       ├── app.py               ← Entry point (refactored)")
    print(f"       ├── requirements.txt")
    print(f"       └── README.md")
    print(f"\n📤 Distribution instructions:")
    print(f"   1. Zip the '{dist_folder}' folder")
    print(f"   2. Send to users")
    print(f"   3. Users extract and double-click START_TRACKER.bat")
    print(f"\n💡 User experience:")
    print(f"   - First time: 1-2 minute setup (automatic)")
    print(f"   - After that: Instant start")
    print(f"   - No manual dependency installation needed!")
    print(f"\n📍 Package location: {dist_folder.absolute()}")

if __name__ == "__main__":
    create_portable_package()

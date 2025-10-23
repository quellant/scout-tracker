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

    # Copy application files
    shutil.copy("scout_tracker.py", dist_folder)
    shutil.copy("requirements.txt", dist_folder)
    shutil.copy("README.md", dist_folder)

    # Create launcher script
    launcher_content = """@echo off
title Scout Tracker
echo ========================================
echo Scout Tracker
echo ========================================
echo.
echo Starting application...
echo The app will open in your default web browser.
echo.
echo To stop the application, close this window.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "venv" (
    echo First time setup - Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

REM Run the application
python -m streamlit run scout_tracker.py --server.headless=false
"""

    with open(dist_folder / "START_TRACKER.bat", "w") as f:
        f.write(launcher_content)

    # Create installation instructions
    install_instructions = """# Scout Tracker - Installation Instructions

## Quick Start (3 steps)

### Step 1: Install Python (if not already installed)
1. Download Python 3.9 or higher from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check the box "Add Python to PATH" during installation
4. Click "Install Now"

### Step 2: Install Dependencies
1. Double-click `INSTALL_DEPENDENCIES.bat`
2. Wait for installation to complete
3. Press any key to close the window

### Step 3: Run the Application
1. Double-click `START_TRACKER.bat`
2. The application will open in your web browser automatically
3. Keep the black window open while using the app

## Stopping the Application
- Close the black command window to stop the application

## Troubleshooting

### "Python is not installed" error
- Make sure Python is installed from https://www.python.org/downloads/
- Make sure you checked "Add Python to PATH" during installation
- Restart your computer after installing Python

### Browser doesn't open automatically
- Manually open your web browser and go to: http://localhost:8501

### Application won't start
1. Close all black windows
2. Double-click `START_TRACKER.bat` again

## Data Storage
All your data is stored in the `tracker_data` folder in the same location as this application.
You can back up this folder to save your data.

## Support
For issues or questions, refer to the README.md file.
"""

    with open(dist_folder / "INSTALLATION_INSTRUCTIONS.txt", "w") as f:
        f.write(install_instructions)

    # Create dependency installer
    dep_installer = """@echo off
title Installing Scout Tracker Dependencies
echo ========================================
echo Installing Dependencies
echo ========================================
echo.
echo This will install the required packages...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run START_TRACKER.bat to launch the application.
echo.
pause
"""

    with open(dist_folder / "INSTALL_DEPENDENCIES.bat", "w") as f:
        f.write(dep_installer)

    print(f"\n✅ Portable package created successfully!")
    print(f"\nNext steps:")
    print(f"1. Zip the '{dist_folder}' folder")
    print(f"2. Distribute the zip file to users")
    print(f"3. Users should:")
    print(f"   - Extract the zip")
    print(f"   - Follow INSTALLATION_INSTRUCTIONS.txt")
    print(f"\nPackage location: {dist_folder.absolute()}")

if __name__ == "__main__":
    create_portable_package()

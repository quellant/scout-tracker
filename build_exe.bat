@echo off
REM Build script for Scout Tracker Windows executable (Refactored Version)
REM This creates a NO-PYTHON-REQUIRED distribution
REM Updated for modular package structure

title Building Scout Tracker Executable
color 0B

echo.
echo ========================================
echo  Building Scout Tracker Executable
echo  (Refactored Modular Version)
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is required to BUILD the executable.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if scout_tracker package exists
if not exist scout_tracker\ (
    echo ERROR: scout_tracker package not found!
    echo Please ensure you're in the project root directory.
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist app.py (
    echo ERROR: app.py entry point not found!
    echo Please ensure you're in the project root directory.
    pause
    exit /b 1
)

echo [1/5] Installing build dependencies...
pip install pyinstaller pandas streamlit --quiet

echo [2/5] Building executable bundle (this may take 2-5 minutes)...
echo       This creates a folder with all files needed to run without Python.
echo       Entry point: app.py (refactored modular structure)
pyinstaller scout_tracker.spec --clean --noconfirm

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: Build failed! Check the output above for errors.
    pause
    exit /b 1
)

echo [3/5] Verifying build output...
if not exist dist\ScoutTracker\ScoutTracker.exe (
    color 0C
    echo ERROR: Build failed - ScoutTracker.exe not found!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo [4/5] Creating user-friendly launcher...
echo @echo off > dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo title Scout Tracker >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo color 0A >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo cls >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo. >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo. >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    ======================================== >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo         SCOUT TRACKER - Starting... >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    ======================================== >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo. >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    Opening Scout Tracker in your web browser... >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo. >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    ======================================== >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    KEEP THIS WINDOW OPEN while using the app >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    Close this window to stop Scout Tracker >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo    ======================================== >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo echo. >> dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo ScoutTracker.exe >> dist\ScoutTracker\START_SCOUT_TRACKER.bat

echo [5/5] Creating Quick Start guide...
echo ================================================================================ > dist\ScoutTracker\QUICK_START.txt
echo                         SCOUT TRACKER - QUICK START >> dist\ScoutTracker\QUICK_START.txt
echo ================================================================================ >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo HOW TO USE (1 STEP!): >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo   Double-click "START_SCOUT_TRACKER.bat" >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo That's it! The app will open in your web browser. >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo ================================================================================ >> dist\ScoutTracker\QUICK_START.txt
echo                               IMPORTANT NOTES >> dist\ScoutTracker\QUICK_START.txt
echo ================================================================================ >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo   NO PYTHON INSTALLATION REQUIRED! >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo   - Keep the black window open while using the app >> dist\ScoutTracker\QUICK_START.txt
echo   - To STOP: Close the black window >> dist\ScoutTracker\QUICK_START.txt
echo   - Your data is saved in the "tracker_data" folder >> dist\ScoutTracker\QUICK_START.txt
echo   - First launch may take 10-30 seconds >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo TROUBLESHOOTING: >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo   Browser doesn't open? Go to: http://localhost:8501 >> dist\ScoutTracker\QUICK_START.txt
echo   App won't start? Close all windows and try again >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo ================================================================================ >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo REFACTORED VERSION NOTES: >> dist\ScoutTracker\QUICK_START.txt
echo   - Built from modular package structure (scout_tracker/) >> dist\ScoutTracker\QUICK_START.txt
echo   - Entry point: app.py >> dist\ScoutTracker\QUICK_START.txt
echo   - All functionality preserved from original version >> dist\ScoutTracker\QUICK_START.txt
echo. >> dist\ScoutTracker\QUICK_START.txt
echo ================================================================================ >> dist\ScoutTracker\QUICK_START.txt

color 0A
echo.
echo ========================================
echo  BUILD SUCCESSFUL!
echo ========================================
echo.
echo  Location: dist\ScoutTracker\
echo.
echo  Package Info:
echo  - Built from refactored modular structure
echo  - Entry point: app.py
echo  - Package: scout_tracker/
echo.
echo  Next steps:
echo  1. Test: Run dist\ScoutTracker\START_SCOUT_TRACKER.bat
echo  2. Distribute: Zip the entire "ScoutTracker" folder
echo  3. Users: Extract and double-click START_SCOUT_TRACKER.bat
echo.
echo  NO PYTHON REQUIRED for end users!
echo.
echo ========================================
pause

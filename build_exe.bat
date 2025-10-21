@echo off
REM Build script for Lion Scout Tracker Windows executable

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile --windowed ^
    --name "LionScoutTracker" ^
    --add-data "tracker_data;tracker_data" ^
    --hidden-import streamlit ^
    --hidden-import streamlit.web.cli ^
    --hidden-import streamlit.runtime.scriptrunner.magic_funcs ^
    --collect-all streamlit ^
    lion_tracker.py

echo.
echo Build complete! Executable is in the dist folder.
pause

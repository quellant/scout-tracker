# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Scout Tracker (Refactored Version)
This creates a standalone executable bundle that doesn't require Python installation.

Updated for modular package structure with scout_tracker/ package.
"""

block_cipher = None

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Collect all Streamlit files and dependencies
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')

# Collect scout_tracker package
scout_tracker_datas, scout_tracker_binaries, scout_tracker_hiddenimports = collect_all('scout_tracker')

# Additional hidden imports needed for Streamlit to work
hidden_imports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.web.server',
    'streamlit.web.server.server',
    'streamlit.runtime',
    'streamlit.runtime.state',
    'streamlit.runtime.state.session_state',
    'pandas',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.skiplist',
    'altair',
    'pyarrow',
    'PIL',
    'PIL._tkinter_finder',
    'click',
    'toml',
    'validators',
    'watchdog',
    'tornado',
    # Scout Tracker package modules
    'scout_tracker',
    'scout_tracker.config',
    'scout_tracker.config.constants',
    'scout_tracker.data',
    'scout_tracker.data.io',
    'scout_tracker.data.cache',
    'scout_tracker.ui',
    'scout_tracker.ui.app',
    'scout_tracker.ui.pages',
    'scout_tracker.ui.pages.attendance',
    'scout_tracker.ui.pages.dashboard',
    'scout_tracker.ui.pages.individual_reports',
    'scout_tracker.ui.pages.meeting_reports',
    'scout_tracker.ui.pages.meetings',
    'scout_tracker.ui.pages.onboarding',
    'scout_tracker.ui.pages.plan_meetings',
    'scout_tracker.ui.pages.requirements',
    'scout_tracker.ui.pages.roster',
]

# Combine all hidden imports
all_hidden_imports = list(set(
    hidden_imports +
    streamlit_hiddenimports +
    pandas_hiddenimports +
    scout_tracker_hiddenimports
))

# Combine all data files
all_datas = streamlit_datas + pandas_datas + scout_tracker_datas

a = Analysis(
    ['app.py'],  # Updated to use new entry point
    pathex=[],
    binaries=streamlit_binaries + pandas_binaries + scout_tracker_binaries,
    datas=all_datas,
    hiddenimports=all_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScoutTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # MUST be True for Streamlit to show server status
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScoutTracker',
)

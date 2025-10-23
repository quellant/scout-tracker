# Distribution Guide for Scout Tracker

## Recommended Approach: Portable Package ⭐

This is the **easiest and most reliable** method for distributing your Streamlit app to Windows users.

### How to Create the Distribution Package

1. **Run the packaging script:**
   ```bash
   python create_portable_package.py
   ```

2. **Create a zip file:**
   - Right-click the `ScoutTracker_Portable` folder
   - Select "Send to" → "Compressed (zipped) folder"
   - Name it `ScoutTracker_v1.0.zip`

3. **Distribute the zip file:**
   - Upload to Google Drive, Dropbox, or email it
   - Users download and extract the zip file

### User Installation (3 Simple Steps)

Users just need to:
1. **Install Python** (one-time, from python.org)
2. **Run `INSTALL_DEPENDENCIES.bat`** (one-time setup)
3. **Double-click `START_TRACKER.bat`** (every time they want to use it)

**Advantages:**
- ✅ Simple and reliable
- ✅ Small download size (~50 KB)
- ✅ Easy to update (just replace scout_tracker.py)
- ✅ Users can easily back up their data
- ✅ Works on any Windows version

**Disadvantages:**
- ❌ Requires Python installation (but only once)
- ❌ Requires internet connection for initial setup

---

## Alternative: True Executable with PyInstaller

If you want a true `.exe` file (no Python installation required), use PyInstaller:

### Prerequisites
```bash
pip install pyinstaller
```

### Create the Executable

Create a file called `build_spec.py`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lion_tracker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.state',
        'streamlit.components.v1',
        'altair',
        'pyarrow',
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScoutTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Then run:
```bash
pyinstaller build_spec.py
```

**Advantages:**
- ✅ No Python installation required
- ✅ Single executable file
- ✅ Professional appearance

**Disadvantages:**
- ❌ Large file size (150-300 MB)
- ❌ Slower startup time
- ❌ May trigger antivirus warnings
- ❌ Complex to update
- ❌ More difficult to debug issues

---

## Alternative: Streamlit Cloud (Free Hosting)

For the **absolute easiest distribution**, host it online for free:

### Steps:
1. Create a free account at [share.streamlit.io](https://share.streamlit.io)
2. Push your code to GitHub
3. Deploy your app (takes 2 minutes)
4. Share the URL with users

**Advantages:**
- ✅ No installation needed for users
- ✅ Access from any device (computer, tablet, phone)
- ✅ Always the latest version
- ✅ No distribution hassles

**Disadvantages:**
- ❌ Requires internet connection
- ❌ Data is stored in the cloud (privacy concern for some)
- ❌ Limited to Streamlit Cloud's resources

---

## Comparison Table

| Method | Ease of Distribution | File Size | Python Required | Best For |
|--------|---------------------|-----------|-----------------|----------|
| **Portable Package** | ⭐⭐⭐⭐⭐ | ~50 KB | Yes (one-time) | Den leaders comfortable with basic software installation |
| **PyInstaller .exe** | ⭐⭐⭐ | ~200 MB | No | Users who can't install Python |
| **Streamlit Cloud** | ⭐⭐⭐⭐⭐ | 0 KB | No | Multiple dens, always-updated |

---

## Recommended Distribution Message

When sending to users, include this message:

```
Hi! I've created a Cub Scout Advancement Tracker to help with tracking scout progress.

SETUP (One-time, 5 minutes):
1. Download and extract the attached zip file
2. Install Python from https://www.python.org/downloads/
   (Make sure to check "Add Python to PATH" during installation)
3. Double-click INSTALL_DEPENDENCIES.bat and wait for it to finish

TO USE THE APP:
- Double-click START_TRACKER.bat
- The app will open in your web browser
- Keep the black window open while using the app

YOUR DATA:
- All your data is stored in the "tracker_data" folder
- Back up this folder to save your progress

Questions? Check the INSTALLATION_INSTRUCTIONS.txt file or let me know!
```

---

## My Recommendation

For den leaders distributing to other den leaders:
👉 **Use the Portable Package method**

Reasons:
- Easiest to create and maintain
- Small download size
- Users have full control of their data
- Easy to update (just replace one file)
- Reliable and transparent

"""
Validation script to check if the project is ready for PyInstaller build.
Run this before attempting to build the executable.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def check_required_files():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'scout_tracker.spec',
        'requirements.txt',
    ]

    required_dirs = [
        'scout_tracker',
    ]

    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} MISSING")
            all_exist = False

    for dir_name in required_dirs:
        if Path(dir_name).is_dir():
            print(f"✓ {dir_name}/ package exists")
        else:
            print(f"✗ {dir_name}/ package MISSING")
            all_exist = False

    return all_exist

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'PyInstaller': 'pyinstaller',
    }

    all_installed = True
    for display_name, import_name in required_packages.items():
        try:
            if import_name == 'pyinstaller':
                import PyInstaller
                module = PyInstaller
            else:
                module = __import__(import_name)

            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name} {version} installed")
        except ImportError:
            print(f"✗ {display_name} NOT INSTALLED")
            all_installed = False

    return all_installed

def check_pyinstaller_hooks():
    """Check if PyInstaller hooks work"""
    try:
        from PyInstaller.utils.hooks import collect_all

        # Test Streamlit collection
        st_datas, st_bins, st_imports = collect_all('streamlit')
        print(f"✓ PyInstaller can collect Streamlit ({len(st_datas)} files)")

        # Test Pandas collection
        pd_datas, pd_bins, pd_imports = collect_all('pandas')
        print(f"✓ PyInstaller can collect Pandas ({len(pd_datas)} files)")

        # Test scout_tracker package collection
        tracker_datas, tracker_bins, tracker_imports = collect_all('scout_tracker')
        print(f"✓ PyInstaller can collect scout_tracker ({len(tracker_imports)} imports)")

        return True
    except Exception as e:
        print(f"✗ PyInstaller hooks failed: {e}")
        return False

def check_spec_file_syntax():
    """Validate spec file syntax"""
    try:
        with open('scout_tracker.spec', 'r') as f:
            spec_content = f.read()

        # Try to compile it
        compile(spec_content, 'scout_tracker.spec', 'exec')
        print(f"✓ scout_tracker.spec has valid syntax")
        return True
    except SyntaxError as e:
        print(f"✗ scout_tracker.spec has syntax error: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ scout_tracker.spec not found")
        return False

def check_app_imports():
    """Check if the app can import its dependencies"""
    try:
        # Check if app.py entry point exists and is valid
        with open('app.py', 'r') as f:
            app_content = f.read()

        if 'scout_tracker' in app_content:
            print(f"✓ app.py imports scout_tracker package")
        else:
            print(f"⚠ app.py might not import scout_tracker package")

        # Check scout_tracker package structure
        package_modules = [
            'scout_tracker/__init__.py',
            'scout_tracker/config/__init__.py',
            'scout_tracker/data/__init__.py',
            'scout_tracker/ui/__init__.py',
        ]

        all_modules_exist = True
        for module in package_modules:
            if Path(module).exists():
                print(f"✓ {module} exists")
            else:
                print(f"✗ {module} MISSING")
                all_modules_exist = False

        return all_modules_exist
    except FileNotFoundError as e:
        print(f"✗ Required file not found: {e}")
        return False

def main():
    print("=" * 60)
    print("Scout Tracker - Build Readiness Validation")
    print("(Refactored Modular Version)")
    print("=" * 60)
    print()

    print("Checking Python version...")
    py_ok = check_python_version()
    print()

    print("Checking required files...")
    files_ok = check_required_files()
    print()

    print("Checking dependencies...")
    deps_ok = check_dependencies()
    print()

    print("Checking PyInstaller hooks...")
    hooks_ok = check_pyinstaller_hooks()
    print()

    print("Checking spec file syntax...")
    spec_ok = check_spec_file_syntax()
    print()

    print("Checking app imports...")
    app_ok = check_app_imports()
    print()

    print("=" * 60)
    if all([py_ok, files_ok, deps_ok, hooks_ok, spec_ok, app_ok]):
        print("✅ BUILD READY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  - On Windows: Run build_exe.bat")
        print("  - On Linux/Mac: Run ./build_exe.sh")
        print()
        print("Build output:")
        print("  - Entry point: app.py (refactored modular structure)")
        print("  - Package: scout_tracker/ (config, data, ui modules)")
        return 0
    else:
        print("❌ BUILD NOT READY - Fix issues above")
        print("=" * 60)
        print()
        if not deps_ok:
            print("To install dependencies:")
            print("  pip install -r requirements.txt pyinstaller")
        return 1

if __name__ == "__main__":
    sys.exit(main())

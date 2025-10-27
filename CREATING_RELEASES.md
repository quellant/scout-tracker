# Creating Releases with Automated Builds

Scout Tracker uses GitHub Actions to automatically build Windows, Linux, and macOS executables when you create a release.

## 📦 What Gets Built Automatically

When you create a release, GitHub Actions will automatically:

1. ✅ Build standalone executables for:
   - **Windows** - ScoutTracker-Windows.zip
   - **Linux** - ScoutTracker-Linux.tar.gz
   - **macOS** - ScoutTracker-macOS.zip

2. ✅ Each includes:
   - Standalone executable (no Python required)
   - One-click launcher script
   - README with instructions

3. ✅ Upload all executables to the GitHub release page

Users can then download ready-to-run versions without needing Python!

---

## 🚀 How to Create a Release

### Method 1: Using Git Tags (Recommended)

```bash
# 1. Make sure all changes are committed
git status

# 2. Create a version tag (use semantic versioning: vMAJOR.MINOR.PATCH)
git tag -a v1.0.0 -m "Initial public release"

# 3. Push the tag to GitHub
git push origin v1.0.0
```

This creates the tag, but you still need to create the release on GitHub (next section).

### Method 2: Using GitHub Web Interface

1. Go to your repository: https://github.com/RobertCoop/scout-tracker
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Click **Choose a tag** → Type `v1.0.0` → Click **Create new tag on publish**
5. Fill in release details:
   - **Release title**: `Scout Tracker v1.0.0 - Initial Release`
   - **Description**: Add release notes (see template below)
6. Click **Publish release**

The GitHub Actions workflow will automatically start building executables!

---

## 📝 Release Notes Template

Use this template when creating your GitHub release:

```markdown
# Scout Tracker v1.0.0

## 🎉 Initial Public Release

A free, open-source advancement tracker for Cub Scout den leaders!

## ✨ Features

- 📋 Roster management for all ranks (Lion through Webelos)
- 📚 Pre-loaded BSA requirements for all ranks
- 📅 Meeting planning and attendance tracking
- 📊 Automated progress calculation
- 📈 Individual scout reports
- 📋 Meeting reports
- 🏕️ Works completely offline - your data stays local

## 📦 Downloads

Choose the download for your operating system:

- **Windows**: Download `ScoutTracker-Windows.zip`
  - Extract the ZIP file
  - Double-click `START_SCOUT_TRACKER.bat`

- **Linux**: Download `ScoutTracker-Linux.tar.gz`
  - Extract: `tar -xzf ScoutTracker-Linux.tar.gz`
  - Run: `./start_scout_tracker.sh`

- **macOS**: Download `ScoutTracker-macOS.zip`
  - Extract the ZIP file
  - Double-click `start_scout_tracker.command`

## 🐛 Known Issues

None currently. Please report issues at: https://github.com/RobertCoop/scout-tracker/issues

## 📄 License

Licensed under CC BY-NC-SA 4.0 (free for non-commercial use)

## 🙏 Acknowledgments

Built for the scouting community by volunteer developers.
```

---

## ⏱️ Build Time

The automated build process takes approximately **10-15 minutes**:
- Windows build: ~5 minutes
- Linux build: ~4 minutes
- macOS build: ~5 minutes

You can watch the progress:
1. Go to the **Actions** tab in your repository
2. Click on the "Build Release Executables" workflow
3. Watch each build complete

---

## 🔍 Monitoring the Build

### Check Build Status

1. Go to: https://github.com/RobertCoop/scout-tracker/actions
2. Find your release workflow (will be named after your release)
3. Click to see detailed build logs

### Build Badges (Optional)

Add to README.md to show build status:

```markdown
![Build Status](https://github.com/RobertCoop/scout-tracker/actions/workflows/build-release.yml/badge.svg)
```

---

## 📥 Manual Trigger (Testing)

You can also trigger builds manually without creating a release:

1. Go to **Actions** → **Build Release Executables**
2. Click **Run workflow**
3. Enter a version number (e.g., "1.0.0-test")
4. Click **Run workflow**

This creates build artifacts but doesn't create a GitHub release.
Useful for testing before official release.

---

## 🐛 Troubleshooting

### Build Failed?

Common issues:

1. **Missing dependency in spec file**
   - Check the error log in GitHub Actions
   - Add missing import to `scout_tracker.spec`
   - Commit and create a new tag

2. **Import error during build**
   - Verify all Python files have proper imports
   - Test locally: `pyinstaller scout_tracker.spec`

3. **Executable won't run**
   - Check console errors
   - Ensure all data files are included in spec
   - Test with: `pyinstaller scout_tracker.spec --clean`

### Testing Builds Locally

Before creating a release, test the build locally:

**Windows:**
```cmd
pip install pyinstaller
pyinstaller scout_tracker.spec --clean
cd dist\ScoutTracker
ScoutTracker.exe
```

**Linux/Mac:**
```bash
pip install pyinstaller
pyinstaller scout_tracker.spec --clean
cd dist/ScoutTracker
./ScoutTracker
```

---

## 📋 Version Numbering

Use [Semantic Versioning](https://semver.org/):

- `v1.0.0` - Major release (breaking changes)
- `v1.1.0` - Minor release (new features, backward compatible)
- `v1.0.1` - Patch release (bug fixes)

Examples:
- `v1.0.0` - Initial public release
- `v1.1.0` - Added "Meeting Reports" feature
- `v1.0.1` - Fixed attendance logging bug

---

## 🎯 Release Checklist

Before creating a release:

- [ ] All tests passing (`pytest tests/`)
- [ ] No deprecation warnings
- [ ] README.md up to date
- [ ] CHANGELOG.md updated (if you have one)
- [ ] Version number decided (vX.Y.Z)
- [ ] Test build locally works
- [ ] Commit all changes
- [ ] Push to GitHub

After creating release:

- [ ] Wait for automated builds to complete
- [ ] Download and test each platform's executable
- [ ] Announce to community (forums, social media)
- [ ] Monitor for issues

---

## 🎉 Your First Release

For your first public release:

```bash
# 1. Ensure everything is committed
git status

# 2. Create version tag
git tag -a v1.0.0 -m "Scout Tracker v1.0.0 - Initial public release"

# 3. Push tag
git push origin v1.0.0

# 4. Go to GitHub and create release from tag
# 5. Wait for builds to complete (~15 minutes)
# 6. Download and test executables
# 7. Share with the scouting community!
```

---

## 📚 Additional Resources

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Semantic Versioning](https://semver.org/)
- [PyInstaller Documentation](https://pyinstaller.org/)

---

**Need help?** Open an issue at: https://github.com/RobertCoop/scout-tracker/issues

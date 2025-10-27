# Scout Tracker v1.0.1

## 🆕 New Features

### PDF Export for Meeting Lists

Export all your meetings to a professional PDF report with one page per meeting!

**New "Export Meeting List" Button** on the Meeting Reports page allows you to:
- Generate a comprehensive PDF of all meetings in chronological order
- One page per meeting with complete details
- Professional formatting with BSA-inspired styling

**Each meeting page includes:**
- 📅 Meeting title and date
- 👥 Attendance summary (total scouts, present, absent, attendance %)
- ✅ Lists of present and absent scouts
- 📚 Requirements covered, grouped by adventure (Required/Elective)
- 📋 Full requirement descriptions with IDs

**Perfect for:**
- End-of-year recordkeeping
- Sharing with pack leadership
- Parent conferences
- Archival documentation
- Advancement coordination meetings

**How to use:**
1. Navigate to Meeting Reports page
2. Click "📄 Export Meeting List" button
3. Click "⬇️ Download PDF" when ready
4. Save to your preferred location

The PDF filename includes the current date (e.g., `Meeting_List_20251027.pdf`) for easy organization.

## 🐛 Bug Fixes

None in this release.

## 🔧 Technical Changes

- Added `reportlab>=4.0.0` dependency for PDF generation
- New `scout_tracker.services.pdf_export` module with `generate_meeting_list_pdf()` function
- Enhanced Meeting Reports page with export functionality
- Professional PDF styling with tables, headers, and proper pagination

## 📦 Downloads

Download the latest version for your operating system:

- **Windows**: `ScoutTracker-Windows.zip`
- **Linux**: `ScoutTracker-Linux.tar.gz`
- **macOS**: `ScoutTracker-macOS.zip`

## 🔄 Upgrade Notes

If upgrading from v1.0.0:
1. Download and extract the new version
2. Copy your `tracker_data` folder from the old version to the new version
3. Run the application as usual

Your existing data will work seamlessly with v1.0.1.

## 📄 License

CC BY-NC-SA 4.0 (free for non-commercial use)

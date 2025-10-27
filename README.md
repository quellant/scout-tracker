# Cub Scout Advancement Tracker

A local web application designed to help Cub Scout den leaders track advancement for any rank level (Lion, Tiger, Wolf, Bear, Webelos).

## Features

- **Roster Management**: Add and remove scouts from your den
- **Requirements Management**: Full CRUD operations for scout adventure requirements
- **Meeting Planning**: Define meetings with dates, titles, and covered requirements
- **Attendance Logging**: Quick check-off system for meeting attendance
- **Automated Progress Tracking**: Automatic calculation of scout advancement based on attendance
- **Visual Dashboard**: Progress bars showing completion percentage for each adventure
- **Individual Scout Reports**: Detailed progress reports with meeting attendance and completion tracking

## Installation

1. Ensure you have Python 3.9 or higher installed

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser to the URL shown (typically `http://localhost:8501`)

3. Follow the workflow:
   - **Manage Roster**: Add your scouts
   - **Manage Requirements**: Review and customize the requirements (pre-loaded with official BSA requirements for all ranks)
   - **Manage Meetings**: Create meetings and specify which requirements you'll cover
   - **Log Attendance**: After each meeting, check off who attended
   - **Tracker Dashboard**: View each scout's progress automatically

## Customizing for Your Den's Rank Level

**The application comes pre-loaded with requirements for all Cub Scout ranks** with comprehensive pre-packaged requirements:

### Option 1: Use Pre-Packaged Requirements (Easiest)
1. Go to **Manage Requirements** → **Import/Export** tab
2. Scroll to **"📦 Load Pre-Packaged Requirements"**
3. Select your rank from the dropdown:
   - Lion (Kindergarten) - *Detailed requirements*
   - Tiger (1st Grade) - *Detailed requirements*
   - Wolf (2nd Grade) - *Detailed requirements*
   - Bear (3rd Grade) - *Detailed requirements*
   - Webelos (4th Grade) - *Detailed requirements*
4. Click **"📥 Load [Rank] Requirements"** and confirm

**Note:** All ranks include detailed requirements that can be further customized after loading.

### Option 2: Use Default Lion Scout Requirements
- The app starts with Lion Scout requirements pre-loaded with full detail, making it ready to use immediately for Lion dens

### Option 3: Customize Requirements Manually
1. Use the **Add Requirement**, **Edit Requirement**, or **Delete Requirement** tabs to customize
2. Or start from scratch: Click "🗑️ Clear All Requirements" and add your own

### Option 4: Share Requirements Between Dens
1. One den leader exports their requirements (**Manage Requirements** → **Import/Export** → Download CSV)
2. Share the CSV file with other den leaders
3. Other leaders import the CSV (**Import/Export** → Upload CSV)

### CSV Format for Requirements
```csv
Req_ID,Adventure,Requirement_Description,Required
Tiger.1,Tiger Circles,1. Gather the items...,True
Tiger.2,Tiger Circles,2. With your adult partner...,True
```

- **Req_ID**: Unique identifier (e.g., "Tiger.1", "Wolf.2")
- **Adventure**: Name of the adventure
- **Requirement_Description**: Full description of what scouts must do
- **Required**: `True` for required adventures, `False` for electives

## Data Storage

All data is stored locally in CSV files in the `tracker_data/` directory:

- `Roster.csv`: Scout names
- `Requirement_Key.csv`: Scout requirements (fully editable through the app)
- `Meetings.csv`: Meeting details and requirements covered
- `Meeting_Attendance.csv`: Attendance records

## Default Requirements Structure (Lion Rank)

The application comes pre-loaded with official BSA Lion Scout requirements as the default:

### Required Adventures (Must complete all 6):
1. **Bobcat** (4 requirements)
2. **Fun on the Run** (4 requirements)
3. **Lion's Roar** (4 requirements)
4. **Lion's Pride** (3 requirements)
5. **King of the Jungle** (4 requirements)
6. **Mountain Lion** (4 requirements)

### Elective Adventures (Must complete any 2):
1. **Build It Up, Knock It Down** (3 requirements)
2. **Champions for Nature** (4 requirements)
3. **Count On Me** (3 requirements)
4. **Gizmos and Gadgets** (3 requirements)

You can add, edit, or remove requirements through the "Manage Requirements" page to customize for your den's needs.

## How It Works

The tracker automatically calculates which requirements each scout has completed by cross-referencing:
1. Which meetings each scout attended (from Meeting Attendance)
2. Which requirements were covered at each meeting (from Meetings)

This means you only need to:
1. Define your meetings once
2. Log attendance after each meeting
3. View the automatically updated progress dashboard

## Rank Completion Tracking

The tracker automatically calculates and displays when a scout has earned their rank based on the requirements loaded.

**Example: Lion Rank**
To earn the Lion rank, scouts must complete:
- All 6 required adventures (23 requirements total)
- Any 2 elective adventures (6-8 requirements depending on which electives)

Each rank has its own completion criteria which are tracked automatically in the dashboard and individual reports.

## Data Portability

All your data is stored in simple CSV files, which means you can:
- Back up your data by copying the `tracker_data/` folder
- Share your data with co-leaders
- Import/export to spreadsheet programs if needed
- Keep your data even if you stop using the application

## Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.9+
- **Data Layer**: Pandas with CSV storage
- **Architecture**: Single-page app with sidebar navigation

## Troubleshooting

**Data not saving?**
- Check that the application has write permissions in its directory

**Requirements don't show up?**
- Delete the `tracker_data/Requirement_Key.csv` file and restart the app to regenerate with defaults

**Need to reset everything?**
- Delete the entire `tracker_data/` directory and restart the app

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License** (CC BY-NC-SA 4.0).

### You are free to:

- ✅ **Use** - Use this software for personal, educational, or non-profit purposes
- ✅ **Share** - Copy and redistribute the material in any medium or format
- ✅ **Adapt** - Remix, transform, and build upon the material

### Under the following terms:

- **Attribution** - You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial** - You may not use the material for commercial purposes or monetary gain
- **ShareAlike** - If you remix, transform, or build upon the material, you must distribute your contributions under the same license

### What this means:

- ✅ Perfect for scout leaders, dens, packs, and troops
- ✅ Schools and educational organizations can use it freely
- ✅ You can modify it for your specific needs
- ✅ You can share your improvements with others
- ❌ Cannot be sold or used in paid products/services
- ❌ Cannot be included in commercial software

See the [LICENSE](LICENSE) file for the complete legal text.

### Note on BSA Content

All BSA program content, adventure names, and requirement descriptions remain the intellectual property of Scouting America (formerly Boy Scouts of America). This license applies to the software implementation only.

## Support

For BSA program questions, consult official Scouting America resources at [scouting.org](https://www.scouting.org).

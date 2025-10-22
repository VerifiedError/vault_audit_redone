# Vault Audit System

A simple, automated system for tracking bags in Rochester Armored Car's vault. Automatically identifies which bags have been sitting in the vault for 3 or more days.

## What Does This Do?

Every day, you receive a container-holdover Excel file showing which bags are in the vault. This system:

1. **Automatically tracks every bag** when you upload the Excel file
2. **Remembers when each bag first appeared** in the vault
3. **Calculates how many days** each bag has been sitting there
4. **Highlights bags that need attention** (3+ days old) in bright red with a 🔥 flame emoji

**No manual scanning required!** Just upload your daily Excel file and the system does the rest.

---

## How Bag Tracking Works

### Daily Workflow

**Every Morning:**
1. You receive today's container-holdover Excel file via email
2. Open the Vault Audit System in your browser
3. Click "Upload Container File" and select today's Excel
4. The system automatically:
   - Records all bag labels with today's date
   - Checks if any bags appeared in previous days
   - Calculates days in vault for each bag
   - Shows you which bags are >=3 days old

**That's it!** No need to physically scan bags or manually track dates.

### Example Timeline

Let's say bag "SF-001" appears in your container-holdover files for 5 days straight:

```
Monday (Day 1):    Upload Excel → System records SF-001 with date: Oct 11
Tuesday (Day 2):   Upload Excel → System sees SF-001 again (1 day old)
Wednesday (Day 3): Upload Excel → System sees SF-001 again (2 days old)
Thursday (Day 4):  Upload Excel → System sees SF-001 again (3 days old) 🔥
                   Export report → SF-001 appears in red section!
Friday (Day 5):    Upload Excel → SF-001 still there (4 days old) 🔥
                   Export report → SF-001 highlighted as needing pickup
```

### What Gets Tracked

The system tracks **every unique bag label** in your container-holdover Excel files:

✅ **Tracked Automatically:**
- Bag ID numbers (e.g., "SF-BAG-001", "DG61136438")
- ATM fill labels (e.g., "9956P-51664")
- Customer deposit bags
- All unique identifiers

❌ **Ignored (Filtered Out):**
- Generic labels like "Bags", "Labels"
- Coin type descriptions (e.g., "Boxes : Quarters")

---

## How to Use

### First Time Setup

1. **Install Python** (if not already installed)
   - Download from python.org
   - Version 3.8 or newer

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Application**
   - Windows: Double-click `start.bat`
   - Or run: `python app.py`

4. **Open Your Browser**
   - Navigate to: http://localhost:5000
   - Bookmark this for easy access

### Daily Use

1. **Upload Today's Container File**
   - Click "Choose File" button
   - Select your container-holdover Excel file
   - Click "Upload"
   - System confirms upload and shows total bags

2. **Review (Optional)**
   - The upload response shows how many bags are >=3 days old
   - You can scan individual bags if needed (but not required)

3. **Export Report**
   - Click "Export Audit Results"
   - Opens Excel file showing:
     - **Column A**: All bags >=3 days old (🔥 flame emoji)
     - **Column B**: Date bag first appeared
     - **Column C**: Total days in vault

4. **Take Action**
   - Review bags in red section
   - Schedule pickup for old bags
   - Share report with management

---

## Understanding the Excel Export

When you export a report, you get an Excel file with two sheets:

### Summary Sheet

Shows overall statistics:
- **Total Containers in Onsite**: How many bags are in vault today
- **Labels >=3 Days in Vault**: Count of old bags (🔥 with flame emoji)
- **Unmatched Labels**: Bags scanned but not in today's holdover file
- **Not Scanned**: Bags in holdover file but not physically verified

### Results Sheet

Three main sections:

**1. Labels >=3 Days in Vault (Columns A-C)** ← Most Important!
- Lists every bag that's been sitting for 3+ days
- Shows exact date it first appeared
- Shows total days in vault
- Everything in red/pink with flame emoji 🔥

**2. Unmatched Labels (Column E)**
- Physical bags found that aren't in today's container file
- Might need investigation

**3. Not Scanned (Column H)**
- Bags in container file but not physically verified
- Optional - only if you scan bags

---

## Demo Example

We've included 5 demo Excel files to show exactly how the system works.

### Demo Files Location

```
demo_sheets/
├── container-holdover-day1-20251011.xlsx  (Oct 11, 2025)
├── container-holdover-day2-20251012.xlsx  (Oct 12, 2025)
├── container-holdover-day3-20251013.xlsx  (Oct 13, 2025)
├── container-holdover-day4-20251014.xlsx  (Oct 14, 2025)
└── container-holdover-day5-20251015.xlsx  (Oct 15, 2025)
```

### What's in the Demo Files

**Persistent Bags** (appear in ALL 5 files):
- SF-BAG-001
- SF-BAG-002
- SF-BAG-003
- SF-BAG-004
- SF-BAG-005

These represent bags that sit in the vault for 5 days straight.

**Varying Bags** (different each day):
- Day 1: SF-VAR-001, SF-VAR-002, SF-VAR-003
- Day 2: SF-VAR-004, SF-VAR-005, SF-VAR-006
- And so on...

These represent normal turnover - bags that get picked up quickly.

### Running the Demo

**Step 1: Upload Day 1**
```
1. Start the application
2. Upload: demo_sheets/container-holdover-day1-20251011.xlsx
3. Click "Export Audit Results"
4. Open Excel file

Result: "Labels >=3 Days in Vault" section is EMPTY
        (Bags are only 0 days old)
```

**Step 2: Upload Day 2**
```
1. Upload: demo_sheets/container-holdover-day2-20251012.xlsx
2. Export report

Result: Still empty
        (Persistent bags are only 1 day old)
```

**Step 3: Upload Day 3**
```
1. Upload: demo_sheets/container-holdover-day3-20251013.xlsx
2. Export report

Result: Still empty
        (Persistent bags are only 2 days old)
```

**Step 4: Upload Day 4** ← This is where it gets interesting!
```
1. Upload: demo_sheets/container-holdover-day4-20251014.xlsx
2. Export report
3. Open Excel

Result: "Labels >=3 Days in Vault" now shows:
        🔥 SF-BAG-001  |  2025-10-11  |  3
        🔥 SF-BAG-002  |  2025-10-11  |  3
        🔥 SF-BAG-003  |  2025-10-11  |  3
        🔥 SF-BAG-004  |  2025-10-11  |  3
        🔥 SF-BAG-005  |  2025-10-11  |  3

        All 5 persistent bags are now flagged!
```

**Step 5: Upload Day 5**
```
1. Upload: demo_sheets/container-holdover-day5-20251015.xlsx
2. Export report

Result: Same 5 bags, but now showing:
        🔥 SF-BAG-001  |  2025-10-11  |  4
        (Days increased to 4)
```

### What This Demo Proves

✅ The system **automatically remembers** when bags first appear
✅ It **correctly calculates** days in vault
✅ It **highlights old bags** exactly on day 3
✅ **No scanning required** - just upload Excel files
✅ Works with **real dates from the Excel files**

---

## Real-World Usage Tips

### Best Practices

1. **Upload Files Daily**
   - Do this first thing every morning
   - Takes less than 30 seconds
   - Keeps tracking accurate

2. **Check for Red Flags**
   - After uploading, look at the upload response
   - If it says "5 labels >=3 days old" - take action!
   - Export report for details

3. **Share Reports**
   - Export creates a professional Excel file
   - Email to supervisors/management
   - Keep copies for records

4. **Clear Old Data (Optional)**
   - Database grows over time
   - Can delete vault_audit.db to reset
   - System creates new database automatically

### Common Questions

**Q: What if I miss a day?**
A: No problem! The system calculates days from the **first time** a bag appeared. Missing a day doesn't affect tracking.

**Q: What if a bag gets picked up and comes back later?**
A: The system tracks based on import dates. If bag "ABC" appears on Oct 1st, disappears for a week, then reappears on Oct 10th - it will show as a "new" entry starting Oct 10th.

**Q: Do I need to scan bags?**
A: No! The old system required scanning. The new system works purely from Excel uploads. Scanning is optional for verification only.

**Q: Can I see history for a specific bag?**
A: Yes! The database stores complete history. You can query individual bag records through the API.

**Q: What happens to the database over time?**
A: It grows slowly. Each bag takes about 1KB. Even with 10,000 bags tracked over a year, database stays under 50MB.

---

## Technical Requirements

- **Python**: 3.8 or newer
- **Operating System**: Windows, Mac, or Linux
- **Browser**: Any modern browser (Chrome, Firefox, Edge)
- **Excel**: Microsoft Excel 2010 or newer to view reports

### Dependencies

All automatically installed with `pip install -r requirements.txt`:
- Flask 3.0.0 (web server)
- openpyxl 3.1.5 (Excel file handling)
- SQLAlchemy 2.0.23 (database)
- pytz 2024.1 (timezone handling)

---

## Folder Structure

```
vault_audit/
├── app.py                      # Main application
├── requirements.txt            # Python packages needed
├── start.bat                   # Quick start for Windows
├── modules/
│   ├── parser/                 # Reads Excel files
│   ├── auditor/                # Matches labels
│   ├── database/               # Stores tracking data
│   └── export/                 # Creates Excel reports
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── images/                 # Rochester branding
│   └── sound/                  # Audio feedback
├── uploads/                    # Temporary Excel storage
├── exports/                    # Generated reports
└── vault_audit.db              # Tracking database
```

---

## Support

If you encounter issues:

1. Check that all files uploaded correctly to GitHub
2. Verify Python and packages are installed
3. Make sure container-holdover Excel files have correct format
4. Check that dates are being extracted from cell B1 of Parameters sheet

---

## Version History

**v3.0 - Import-Based Tracking** (Current)
- ✨ Automatic tracking from Excel uploads
- ✨ No scanning required for duration tracking
- ✨ Labels >=3 days automatically identified
- ✨ Enhanced export with dates and days visible

**v2.9 - Vault Duration Tracking**
- Added duration calculations
- Color coding based on days in vault
- Flame emoji for old bags

**v2.0 - Rochester Brand Integration**
- Professional UI with Rochester colors
- Tooltips and audio feedback
- Dark mode support

---

## License

Proprietary - Rochester Armored Car
For internal use only

---

## Credits

Developed for Rochester Armored Car vault operations to improve bag tracking and reduce holdover times.

Built with Flask, Python, and automated Excel processing.

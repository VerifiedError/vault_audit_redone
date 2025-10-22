# CLAUDE.md

Development Vault Audit: D:\vault_audit_redone\vault_audit

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Version History

**v3.0 - Database Write Timing & Complete Restart**
- **CRITICAL BEHAVIOR CHANGE**: Database writes now ONLY occur when "Complete Audit" button is clicked
- Removed database write from `/upload` endpoint - file uploads no longer persist to database
- Moved `record_import()` from upload to `/audit` endpoint
- Individual label scans stored in browser only (not written to database until audit completion)
- Enhanced restart functionality to completely clear all state
- Restart button now clears: sessionStorage, containerData, scanned labels, results, container info, scan status
- Re-uploading same file after restart treated as fresh/first-time upload
- Next upload after restart requires new "Complete Audit" to write to database
- Files modified: `app.py` (moved DB writes), `templates/index.html` (enhanced restartAudit())

**v2.12 - Remove Fire Emoji from Results Sheet**
- Removed 🔥 emoji prefix from Label ID column in Results sheet "BAGS IN VAULT 3+ DAYS" section
- Kept fire emoji in Summary sheet "Labels >=3 Days in Vault: 🔥 {count}" for visual emphasis
- Cleaner, more professional appearance in detailed Results sheet
- Files modified: `modules/export/exporter.py` (lines 104, 125)

**v2.11 - Prevent Multiple Audit Button Clicks**
- Disabled "Complete Audit" button immediately when clicked to prevent duplicate requests
- Button text changes to "Processing..." during audit execution
- Visual feedback: 60% opacity, "not-allowed" cursor during processing
- Automatically re-enables button on completion, error, or validation failure
- Applies to both bulk and individual scan mode buttons
- Files modified: `templates/index.html` (`runAudit()` function)

**v2.10 - Enhanced Scan Input Design**
- Modernized individual scan mode section for higher quality, professional appearance
- Container improvements: rounded-2xl, p-10, border-2, shadow-lg, max-w-4xl
- Enhanced input field: border-2, px-6 py-5, text-lg, focus:ring-4 with blue ring effect
- Improved Add Label button: px-10 py-5, hover:scale-105, min-width 140px, shadow-lg
- Better spacing: gap-4 between elements, mb-8 bottom margin
- Modern focus states with smooth transitions (duration-200)
- Files modified: `templates/index.html` (lines 493-516)

**v2.9 - Vault Duration Tracking & Visual Indicators**
- Added comprehensive time tracking for matched bags in Excel export
- New summary statistics: "Total Days in Vault" (sum of all bag durations) and ">3 Days in Vault" (count)
- RGB color coding for matched labels based on vault duration:
  - Green: 0-1 days in vault
  - Yellow: 2-3 days in vault
  - Red: >3 days in vault
- Flame emoji 🔥 prefix for bags exceeding 3 days in vault
- Duration tooltips on each matched label showing exact days
- Database enhancement: `get_bag_durations()` method calculates days from first_scan_datetime to present
- Export function signature updated to accept `bag_durations` parameter
- Summary statistics displayed in blue (Total Days) and red (>3 Days count) with flame emoji
- Files modified: `db_manager.py` (new method), `exporter.py` (duration logic), `app.py` (export route)

**v2.8 - Results UI Color Redesign**
- Redesigned "Not Scanned" results section with softer, easier-to-read color palette
- Replaced bright yellow (#f5bc0e) with professional gray-blue scheme for better readability
- Summary card: Gray-blue gradient background (#f5f7fa to #e8eaf0) with slate border (#64748b)
- Summary card label: Slate blue text (#64748b), count text in dark slate (#334155)
- Detailed list: Light slate background (#f8fafc) with subtle border (#cbd5e1)
- Individual labels: Dark slate text (#475569) for optimal contrast and eye comfort
- Maintains visual distinction while reducing eye strain from bright yellow color
- Updated both HTML styling and JavaScript label generation

**v2.7 - Audio Volume Controls**
- Implemented comprehensive volume control system for scan audio feedback
- Added "Audio Settings" section in settings modal with two independent volume sliders
- Success Sound slider: Controls volume for valid scan audio (0-100%, default 50%)
- Invalid Sound slider: Controls volume for invalid scan audio (0-100%, default 50%)
- Visual volume indicators show current percentage value in real-time
- Custom styled range sliders with Rochester brand colors (navy #2a3887 for success, red #ed1c24 for invalid)
- Dynamic slider background gradient shows filled/unfilled portions based on current value
- Volume settings persist in localStorage (`successVolume`, `invalidVolume`)
- Functions: `updateSuccessVolume()`, `updateInvalidVolume()`, `initVolumeSettings()`
- Applied volume to HTML5 audio elements when playing sounds

**v2.6 - Bulk Scan Mode Toggle Setting**
- Added toggle switch in settings to enable/disable bulk scan mode
- New "Scan Options" section in settings modal with professional toggle switch UI
- Setting persisted in localStorage as `bulkScanEnabled` (default: true)
- When disabled, entire scan mode toggle UI is hidden (both "Bulk Scan" and "Individual Scan" buttons)
- Individual scan mode becomes the only visible option when bulk scan is disabled
- If bulk mode is active when disabled, automatically switches to individual mode
- CSS toggle switch with Rochester brand colors (gray inactive, navy #2a3887 active)
- Functions: `toggleBulkScanMode()`, `updateBulkScanVisibility()`, `initBulkScanSetting()`

**v2.5 - Dynamic Scan Status Messages**
- Updated scan status indicator with dynamic messages based on scan progress
- Initial state: "🎯 Start Scanning Labels" (when no labels scanned)
- After first scan: "🎯 Continue Scanning Labels" (when labels exist)
- Status automatically resets to "Start Scanning Labels" when all labels are removed or cleared
- Updates occur in `addLabel()`, `removeLabel()`, and `clearScannedLabels()` functions

**v2.4 - Dark Mode Input Text Visibility Fix**
- Fixed text visibility issue in dark mode for scan input field
- Added CSS rule: `input.themed-input-bg` and `textarea.themed-input-bg` now use `var(--text-primary)` for color
- Input text now properly adapts to theme: dark text (#233947) in light mode, light text (#f7fafc) in dark mode
- Ensures scanned labels are clearly visible in both light and dark themes

**v2.3 - Active Scan Visual Indicator**
- Added prominent visual indicator when scan input field is active and ready
- Status banner appears when input is focused with pulsing blue dot animation
- Enhanced input field glow effect with pulsing blue border (Rochester brand blue #448ccb)
- Indicator automatically shows on focus, hides on blur
- JavaScript functions: `showScanIndicator()`, `hideScanIndicator()`

**v2.2 - Auto-Focus Individual Scan After Upload**
- Automatic workflow optimization: After container file upload, page auto-scrolls to scan section
- Individual scan input field automatically focused and ready for immediate scanning
- Smooth scroll animation (500ms) to scan section with 100ms delay for UI rendering
- Eliminates need for manual clicking/scrolling - users can start scanning immediately after upload
- Individual Scan mode selected by default (no manual mode toggle required)

**v2.1 - Audio Feedback for Scan Results**
- Added dual audio feedback system for scan validation
- Success sound (MP3): Plays when scanned label matches expected labels ("✓ Found")
- Invalid sound (MP3): Plays when scanned label does NOT match expected labels ("✗ Not Found")
- Created `static/sound/` directory structure for audio assets
- Both sounds reset to start for each scan, fail gracefully if browser blocks autoplay
- Audio elements: `successScanSound` and `invalidScanSound` with Flask url_for routing
- Files: `vault_audit/static/sound/succesful_scan.mp3` and `invalid_scan.mp3` (MP3 format for better browser compatibility)

**v2.0 - Rochester Brand Style Integration & Comprehensive Tooltips**
- Applied Rochester Armored Car brand style guide with exact colors (#233947, #909095, #2a3887, #448ccb, #ed1c24, #f5bc0e)
- Implemented Titillium Web Bold (headlines) and Lato (body/buttons) typography per brand guidelines
- Added comprehensive tooltip system using pure CSS `data-tooltip` attributes on every interactive element
- Enhanced UI with gradient cards, smooth hover animations, better spacing and contrast
- Improved button hover effects (lift transform, shadow enhancement)
- Maintained simplicity while elevating visual design to professional brand standards
- File: `vault_audit/templates/index.html` (900 lines)

---

## Project Overview

Vault audit system for Rochester Armored Car that matches scanned bag labels against expected containers from Excel files.

**Core Workflow**: Upload Excel → Scan bags → Match labels → Export report

### Dependencies
- **openpyxl 3.1.5** - Excel file parsing and export generation
- **Flask 3.0.0** - Web framework for UI and API endpoints
- **SQLAlchemy 2.0.23** - ORM for SQLite database operations
- **pytz 2024.1** - Timezone handling (UTC storage, CST display)

---

## Development Commands

### Setup & Run
```bash
# Install dependencies (run from project root)
pip install -r requirements.txt

# Start application (Windows) - recommended
start.bat
# This automatically opens browser at http://localhost:5000 and starts Flask server

# Start manually (alternative)
cd vault_audit
python app.py
```

### Access
- **Web Interface**: http://localhost:5000
- **Database**: `vault_audit/vault_audit.db` (SQLite, auto-created on first run)
- **Upload folder**: `vault_audit/uploads/` (auto-created)
- **Export folder**: `vault_audit/exports/` (auto-created)
- **Audio assets**: `vault_audit/static/sound/` (must contain `succesful_scan.mp3` and `invalid_scan.mp3`)

### Utility Scripts (run from project root)
```bash
python analyze_excel.py      # Analyze Excel structure and display sheet info
python get_sample_data.py    # Extract sample data from Excel files
```

## Excel File Format

**Sample**: `D:\vault_audit_redone\container-holdover.xlsx`

### Structure
Two sheets: **Parameters** (metadata) + **Dynamic Location Sheet** (e.g., "Sioux Falls")

**Parameters Sheet** (cells A1-B4):
- Created At, Created By, Carrier, Carrier Location (format: "Rochester Armored Car : Sioux Falls")

**Location Sheet Headers**:
Origin, Destination, Type, Departure date, Arrival date, Labels, Count, Value (USD)

### Label Filtering
Excludes generic types from `Labels` column: "Bags", "Labels", coin-type variants (Pennies, Nickels, Dimes, Quarters, etc. in Boxes/Bags/Non-std formats)

See `parser.py:6-30` for full `FILTERED_LABELS` set.

## Architecture

### Flask Application State (CRITICAL)
**Global variables** maintain session state (reset on server restart):
- `container_data` - Currently loaded Excel data (set by `/upload`)
- `auditor` - VaultAuditor instance (initialized by `/upload`)
- `last_audit_result` - Required for export functionality (set by `/audit`)

**Important**:
- These globals are NOT persisted - server restart clears all state
- User must re-upload Excel file after server restart to enable auditing
- Export requires prior audit in same session (`last_audit_result` must exist)
- Multiple users share same globals - this is single-user application

### Database
- **Engine**: SQLite at `vault_audit/vault_audit.db` (auto-created on first run)
- **ORM**: SQLAlchemy 2.0.23 with scoped sessions (`db_manager.py:11`)
- **Timezone**: UTC storage, CST display in exports (pytz 2024.1)
- **Models**:
  - `BagRecord` (individual scan tracking with first/last scan times)
  - `LocationTracker` (location-level statistics and duration calculations)
- **Session Management**: Scoped sessions prevent thread conflicts, sessions closed in finally blocks

### Module Structure
```
vault_audit/modules/
├── models/         # Data classes (Parameters, Transaction, ContainerData, AuditResult)
├── parser/         # Excel parsing, label extraction, filtering
├── auditor/        # Set-based label matching (matched/unmatched/not_scanned)
├── export/         # Excel generation with openpyxl (color-coded, tooltips)
└── database/       # DatabaseManager with automatic location tracking
```

**Import Pattern**: Always use full paths from `vault_audit` root:
```python
from modules.parser.parser import parse_container_file
from modules.models.models import Parameters
```

### Key Implementation Details

**Label Matching** (`auditor.py:9-21`):
- Set operations: `matched = scanned ∩ expected`, `unmatched = scanned - expected`, `not_scanned = expected - scanned`
- Scanned labels are trimmed and deduplicated before matching

**Database Auto-Tracking** (`app.py:65-112`, `db_manager.py:20-56`):
- **IMPORTANT**: Database writes ONLY occur when "Complete Audit" button is clicked (via `/audit` endpoint)
- File upload (`/upload`) does NOT write to database - only parses and stores in memory
- Individual scans stored in browser sessionStorage only (not persisted to database)
- On "Complete Audit": records import via `record_import()` and all scanned labels via `record_scan()`
- Automatically updates `LocationTracker` with days tracked calculation
- Tracks: first/last scan dates, scan counts, unique bags per location
- `record_scan()` increments scan_count for existing bags or creates new record with scan_count=1
- Restart clears all state; next upload treated as fresh (requires new "Complete Audit" to persist)

**Vault Duration Tracking** (`db_manager.py:170-189`, `exporter.py:39-125`):
- `get_bag_durations()` calculates days from `first_scan_datetime` (UTC) to current time
- Export uses duration data to apply color coding (green 0-1 days, yellow 2-3 days, red >3 days)
- Only bags with ≥3 days in vault appear in "Labels >=3 Days in Vault" section of export
- Flame emoji 🔥 prefix added to bags exceeding 3 days

**Carrier Location Extraction** (`parser.py:34-40`):
- Input: "Rochester Armored Car : Sioux Falls" → Output: "Sioux Falls"
- Splits on " : " delimiter, extracts second part

**Label Filtering** (`parser.py:6-30`):
- `FILTERED_LABELS` set excludes generic coin types and non-specific labels
- Prevents "Bags : Pennies", "Boxes : Quarters", etc. from being treated as valid labels
- Only specific, unique bag identifiers are included in `valid_labels`

## API Endpoints

### Core Workflow
- **`POST /upload`** - Parse Excel → Store in `container_data` global → Return metadata + valid labels list
  - Validates .xlsx extension, saves to `uploads/`, returns location info and sorted valid labels
  - **Does NOT write to database** - only parses and stores in memory
- **`POST /audit`** - Match scanned vs expected → **Record to DB** → Return results + location stats
  - Accepts JSON: `{"scanned_labels": ["label1", "label2", ...]}`
  - **This is where database writes occur**: calls `record_import()` and `record_scan()` for each label
  - Records import tracking via `db_manager.record_import()` (first-time or update)
  - Records each scanned label to `BagRecord` table via `db_manager.record_scan()`
  - Returns matched/unmatched/not_scanned labels + location tracking stats + import stats
- **`GET /export`** - Generate Excel from `last_audit_result` → Download file
  - Requires prior audit (uses `last_audit_result` global)
  - Fetches labels >=3 days via `db_manager.get_labels_over_3_days()` (import-based tracking)
  - Fetches import durations via `db_manager.get_import_duration_stats()`
  - Returns `vault_audit_report_YYYYMMDD_HHMMSS.xlsx` with summary and results sheets

### Database Operations
- **`GET /bags/<label_id>`** - Scan history for specific bag (404 if not found)
- **`GET /bags?limit=N&offset=N`** - All bags ordered by first scan desc (paginated)
- **`GET /bags/location/<location>`** - All bags for specific carrier location
- **`DELETE /bags/<label_id>`** - Remove bag record (404 if not found)

### Static Routes
- **`GET /`** - Serves `templates/index.html` (main UI)
- **`GET /static/sound/*.mp3`** - Audio feedback files for scans (MP3 format for compatibility)

**Data Flow**: Upload (memory only) → Scan labels (browser storage) → **Complete Audit (DB write)** → Export
- Upload parses Excel and stores in `container_data` global (no DB write)
- Individual scans stored in browser sessionStorage (no DB write)
- "Complete Audit" button triggers `/audit` endpoint which writes to database
- Export depends on prior audit completing successfully

---

## Frontend Design

### Rochester Brand Style Guide
**Colors** (from `D:\Rochester_BrandStyleGuide.pdf`):
- Primary Dark: `#233947` - Main text, headers
- Primary Gray: `#909095` - Secondary text, borders
- Accent Navy: `#2a3887` - Primary buttons, active states
- Accent Blue: `#448ccb` - Info, statistics, matched items
- Accent Red: `#ed1c24` - Errors, unmatched items
- Accent Gold: `#f5bc0e` - Warnings, not scanned items

**Typography**:
- **Titillium Web Bold** - Headlines (h1, h2, h3)
- **Lato Bold** - Subheadlines, buttons
- **Lato Regular** - Body copy, inputs

### Tooltip System
**Implementation**: Pure CSS tooltips using `data-tooltip` attributes
- Appears on hover over ANY interactive element
- Dark background (`#233947`) with white text
- Smooth fade-in animation (0.2s)
- Triangle pointer positioned above element
- Multi-line support via `data-tooltip-multiline` class

**Coverage**: Headers, buttons, inputs, cards, statistics, scan modes, results, theme toggles, individual labels

### Scan Modes
- **Individual** (default): Real-time validation, instant green/red feedback, duplicate scans ignored
- **Bulk**: Textarea for pasting multiple labels (one per line)

### UI Capabilities
- **File Upload**: Drag-drop or click-to-browse, .xlsx validation, blue highlight on drag hover, upload section hides after successful upload
- **Restart Button**: Circular arrow icon in header, completely clears session and resets to initial state, re-shows upload section
- **Session Persistence**: Auto-saves upload state to sessionStorage, restores on page refresh, maintains workflow across browser refresh
- **Theme System**: Light/dark mode with localStorage persistence, CSS variables, settings modal (gear/cog icon)
- **Scan Mode Control**: Toggle switch in settings to enable/disable bulk scan mode (default: enabled)
- **Scan Input**: Modern design with rounded-2xl borders, p-10 spacing, focus:ring-4 blue effect, hover:scale-105 button animation
- **Complete Audit Button**: Disables during processing, shows "Processing..." text, prevents duplicate clicks, re-enables on completion/error
- **Statistics Display**: "Total Labels in Onsite", "Days Tracked" (appears after first audit)
- **Card Animations**: Hover lift effect on buttons (-2px transform), shadow enhancement on cards
- **Audio Feedback**: Dual MP3 sound system - success sound for matched labels, invalid sound for unmatched labels (individual scan mode)
- **Volume Controls**: Independent volume sliders for success/invalid sounds (0-100%, default 50%) in settings modal
- **Responsive**: Mobile-friendly with Tailwind breakpoints (md:, lg:)

### Excel Export Format
- **Filename**: `vault_audit_report_YYYYMMDD_HHMMSS.xlsx`
- **Summary Sheet**: Metadata, timestamps (CST), audit summary with tooltips, fire emoji 🔥 on "Labels >=3 Days in Vault" count
- **Results Sheet**: Simple vertical layout with three sections:
  - **Section 1**: "BAGS IN VAULT 3+ DAYS" (Label ID, First Seen, Days columns with red fill, no emoji in Label ID)
  - **Section 2**: "UNMATCHED LABELS" (red fill, bags scanned but not in expected list)
  - **Section 3**: "NOT SCANNED" (orange fill, expected bags not physically scanned)
  - Each section shows "None" if empty

---

## Database Schema

**BagRecord** - Individual scan tracking:
- `label_id` (PK, indexed), `first_scan_datetime`, `carrier_location`, `scan_count`, `last_scan_datetime`

**LocationTracker** - Location-level statistics:
- `carrier_location` (PK, indexed), `first_scan_date`, `last_scan_date`, `total_days_tracked`, `total_unique_bags`, `total_scans`

Auto-updated on every `/audit` request via `db_manager.record_scan()` and `update_location_stats()`.
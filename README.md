# Vault Audit System

A professional vault audit system for Rochester Armored Car that matches scanned bag labels against expected containers from Excel files.

![Rochester Armored Car](vault_audit/static/images/logo.png)

## Features

- **Excel Upload**: Drag-and-drop container Excel files for processing
- **Smart Label Scanning**: Individual or bulk scan modes with real-time validation
- **Audio Feedback**: Success and error sounds with volume controls
- **Duration Tracking**: Automatic tracking of bags in vault with visual indicators
- **Professional Reports**: Export detailed Excel reports with color-coded results
- **Dark Mode**: Toggle between light and dark themes
- **Database Persistence**: SQLite database tracks all scans and locations

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vault_audit_redone.git
cd vault_audit_redone

# Install dependencies
pip install -r requirements.txt

# Run the application
start.bat  # Windows
# OR
cd vault_audit && python app.py  # Manual start
```

The application will open automatically at `http://localhost:5000`

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy 2.0.23 with SQLite
- **Excel Processing**: openpyxl 3.1.5
- **Timezone**: pytz 2024.1
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Fonts**: Titillium Web Bold, Lato (Rochester brand typography)

## Workflow

1. **Upload**: Drag or select an Excel container file
2. **Scan**: Use individual or bulk scan mode to capture bag labels
3. **Audit**: Click "Complete Audit" to match scanned vs expected labels
4. **Export**: Download detailed Excel report with color-coded results

## Database Schema

- **BagRecord**: Individual bag scan tracking with timestamps
- **LocationTracker**: Location-level statistics and duration calculations

## Color-Coded Results

- 🟢 **Green**: 0-1 days in vault
- 🟡 **Yellow**: 2-3 days in vault
- 🔴 **Red**: >3 days in vault (flagged with 🔥)

## API Endpoints

- `POST /upload` - Upload and parse Excel file
- `POST /audit` - Run audit and record to database
- `GET /export` - Download Excel report
- `GET /bags/<label_id>` - Get bag scan history
- `GET /bags/location/<location>` - Get all bags for location
- `DELETE /bags/<label_id>` - Remove bag record

## Project Structure

```
vault_audit/
├── modules/
│   ├── models/      # Data models
│   ├── parser/      # Excel parsing
│   ├── auditor/     # Label matching logic
│   ├── export/      # Excel export generation
│   └── database/    # Database management
├── static/
│   ├── images/      # Logos and icons
│   └── sound/       # Audio feedback files
├── templates/
│   └── index.html   # Main UI
├── uploads/         # Uploaded Excel files
├── exports/         # Generated reports
└── app.py           # Flask application
```

## Rochester Brand Colors

- Primary Dark: `#233947`
- Primary Gray: `#909095`
- Accent Navy: `#2a3887`
- Accent Blue: `#448ccb`
- Accent Red: `#ed1c24`
- Accent Gold: `#f5bc0e`

## Important Notes

⚠️ **Deployment Considerations**:
- This application uses SQLite with file storage
- **NOT recommended for Vercel** due to ephemeral filesystem
- Better suited for: Railway, Render, PythonAnywhere, or traditional hosting
- Global state requires single-server deployment

## License

Proprietary - Rochester Armored Car

## Version

v3.0 - Database Write Timing & Complete Restart

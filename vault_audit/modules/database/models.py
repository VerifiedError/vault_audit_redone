from sqlalchemy import Column, Integer, String, DateTime, Date, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import pytz
import json

Base = declarative_base()

class BagRecord(Base):
    __tablename__ = 'bag_records'

    id = Column(Integer, primary_key=True)
    label_id = Column(String, unique=True, nullable=False, index=True)
    first_scan_datetime = Column(DateTime, nullable=False)
    carrier_location = Column(String, nullable=False)
    scan_count = Column(Integer, default=1)
    last_scan_datetime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BagRecord(label_id='{self.label_id}', location='{self.carrier_location}', scans={self.scan_count})>"

    def to_dict(self):
        cst = pytz.timezone('America/Chicago')
        first_scan_cst = self.first_scan_datetime.replace(tzinfo=pytz.utc).astimezone(cst) if self.first_scan_datetime else None
        last_scan_cst = self.last_scan_datetime.replace(tzinfo=pytz.utc).astimezone(cst) if self.last_scan_datetime else None

        return {
            'id': self.id,
            'label_id': self.label_id,
            'first_scan_datetime': first_scan_cst.strftime("%m/%d/%y %H:%M:%S CST") if first_scan_cst else None,
            'carrier_location': self.carrier_location,
            'scan_count': self.scan_count,
            'last_scan_datetime': last_scan_cst.strftime("%m/%d/%y %H:%M:%S CST") if last_scan_cst else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class LocationTracker(Base):
    __tablename__ = 'location_trackers'

    id = Column(Integer, primary_key=True)
    carrier_location = Column(String, unique=True, nullable=False, index=True)
    first_scan_date = Column(Date, nullable=False)
    last_scan_date = Column(Date, nullable=False)
    total_days_tracked = Column(Integer, default=0)
    total_unique_bags = Column(Integer, default=0)
    total_scans = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<LocationTracker(location='{self.carrier_location}', days={self.total_days_tracked}, bags={self.total_unique_bags})>"

    def to_dict(self):
        return {
            'id': self.id,
            'carrier_location': self.carrier_location,
            'first_scan_date': self.first_scan_date.strftime("%m/%d/%y") if self.first_scan_date else None,
            'last_scan_date': self.last_scan_date.strftime("%m/%d/%y") if self.last_scan_date else None,
            'total_days_tracked': self.total_days_tracked,
            'total_unique_bags': self.total_unique_bags,
            'total_scans': self.total_scans,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ImportRecord(Base):
    """Tracks each Excel file import with all labels from that import"""
    __tablename__ = 'import_records'

    id = Column(Integer, primary_key=True)
    import_date = Column(Date, nullable=False, index=True)  # Date from Excel "Created At"
    carrier_location = Column(String, nullable=False, index=True)
    total_labels = Column(Integer, default=0)
    labels_json = Column(Text, nullable=False)  # JSON list of all valid labels
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ImportRecord(date='{self.import_date}', location='{self.carrier_location}', labels={self.total_labels})>"

    def get_labels(self):
        """Parse JSON string to list"""
        return json.loads(self.labels_json) if self.labels_json else []

    def set_labels(self, labels_list):
        """Convert list to JSON string"""
        self.labels_json = json.dumps(labels_list)
        self.total_labels = len(labels_list)

    def to_dict(self):
        return {
            'id': self.id,
            'import_date': self.import_date.strftime("%Y-%m-%d") if self.import_date else None,
            'carrier_location': self.carrier_location,
            'total_labels': self.total_labels,
            'labels': self.get_labels(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LabelImportHistory(Base):
    """Tracks individual label appearances across multiple imports"""
    __tablename__ = 'label_import_history'

    id = Column(Integer, primary_key=True)
    label_id = Column(String, nullable=False, index=True)
    carrier_location = Column(String, nullable=False, index=True)
    first_import_date = Column(Date, nullable=False)  # First time this label appeared
    last_import_date = Column(Date, nullable=False)   # Most recent appearance
    import_count = Column(Integer, default=1)         # How many imports it appeared in
    import_dates_json = Column(Text, nullable=False)  # JSON list of all import dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<LabelImportHistory(label='{self.label_id}', count={self.import_count}, days={self.get_days_in_vault()})>"

    def get_import_dates(self):
        """Parse JSON string to list of date strings"""
        return json.loads(self.import_dates_json) if self.import_dates_json else []

    def set_import_dates(self, dates_list):
        """Convert list of dates to JSON string"""
        # Convert date objects to strings for JSON serialization
        dates_str = [d.strftime("%Y-%m-%d") if isinstance(d, date) else d for d in dates_list]
        self.import_dates_json = json.dumps(dates_str)
        self.import_count = len(dates_str)

    def get_days_in_vault(self):
        """Calculate days from first import to today"""
        if not self.first_import_date:
            return 0
        return (date.today() - self.first_import_date).days

    def to_dict(self):
        return {
            'id': self.id,
            'label_id': self.label_id,
            'carrier_location': self.carrier_location,
            'first_import_date': self.first_import_date.strftime("%Y-%m-%d") if self.first_import_date else None,
            'last_import_date': self.last_import_date.strftime("%Y-%m-%d") if self.last_import_date else None,
            'import_count': self.import_count,
            'import_dates': self.get_import_dates(),
            'days_in_vault': self.get_days_in_vault(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
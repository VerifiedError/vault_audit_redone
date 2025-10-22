from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from modules.database.models import Base, BagRecord, LocationTracker, ImportRecord, LabelImportHistory
from datetime import datetime, date
import os

class DatabaseManager:
    def __init__(self, db_path='vault_audit.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def record_scan(self, label_id: str, carrier_location: str) -> dict:
        session = self.get_session()
        try:
            bag = session.query(BagRecord).filter_by(label_id=label_id).first()

            now = datetime.utcnow()

            if bag:
                bag.scan_count += 1
                bag.last_scan_datetime = now
                bag.updated_at = now
                is_first_scan = False
            else:
                bag = BagRecord(
                    label_id=label_id,
                    first_scan_datetime=now,
                    carrier_location=carrier_location,
                    scan_count=1,
                    last_scan_datetime=now
                )
                session.add(bag)
                is_first_scan = True

            session.commit()

            # Update location tracking
            self.update_location_stats(session, carrier_location, is_first_scan)

            result = bag.to_dict()
            result['is_first_scan'] = is_first_scan
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_location_stats(self, session, carrier_location: str, is_new_bag: bool):
        """Update location tracking statistics"""
        today = date.today()

        location_tracker = session.query(LocationTracker).filter_by(carrier_location=carrier_location).first()

        if not location_tracker:
            # Create new location tracker
            location_tracker = LocationTracker(
                carrier_location=carrier_location,
                first_scan_date=today,
                last_scan_date=today,
                total_days_tracked=1,
                total_unique_bags=1 if is_new_bag else 0,
                total_scans=1
            )
            session.add(location_tracker)
        else:
            # Update existing tracker
            location_tracker.last_scan_date = today
            location_tracker.total_days_tracked = (today - location_tracker.first_scan_date).days + 1
            if is_new_bag:
                location_tracker.total_unique_bags += 1
            location_tracker.total_scans += 1

        session.commit()

    def get_location_stats(self, carrier_location: str):
        """Get tracking stats for specific location"""
        session = self.get_session()
        try:
            tracker = session.query(LocationTracker).filter_by(carrier_location=carrier_location).first()
            return tracker.to_dict() if tracker else None
        finally:
            session.close()

    def get_all_location_stats(self):
        """Get tracking stats for all locations"""
        session = self.get_session()
        try:
            trackers = session.query(LocationTracker).all()
            return [tracker.to_dict() for tracker in trackers]
        finally:
            session.close()

    def get_location_duration(self, carrier_location: str):
        """Get days tracked for specific location"""
        session = self.get_session()
        try:
            tracker = session.query(LocationTracker).filter_by(carrier_location=carrier_location).first()
            return tracker.total_days_tracked if tracker else 0
        finally:
            session.close()

    def get_bag_by_label(self, label_id: str):
        session = self.get_session()
        try:
            bag = session.query(BagRecord).filter_by(label_id=label_id).first()
            return bag.to_dict() if bag else None
        finally:
            session.close()

    def get_all_bags(self, limit=None, offset=None):
        session = self.get_session()
        try:
            query = session.query(BagRecord).order_by(BagRecord.first_scan_datetime.desc())

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            bags = query.all()
            return [bag.to_dict() for bag in bags]
        finally:
            session.close()

    def get_bags_by_location(self, carrier_location: str):
        session = self.get_session()
        try:
            bags = session.query(BagRecord).filter_by(carrier_location=carrier_location).all()
            return [bag.to_dict() for bag in bags]
        finally:
            session.close()

    def delete_bag(self, label_id: str) -> bool:
        session = self.get_session()
        try:
            bag = session.query(BagRecord).filter_by(label_id=label_id).first()
            if bag:
                session.delete(bag)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_stats(self):
        session = self.get_session()
        try:
            total_bags = session.query(BagRecord).count()
            total_scans = session.query(func.sum(BagRecord.scan_count)).scalar() or 0

            return {
                'total_unique_bags': total_bags,
                'total_scans': total_scans
            }
        finally:
            session.close()

    def get_bag_durations(self, label_ids: list[str]) -> dict:
        """Get days in vault for specific bag labels"""
        session = self.get_session()
        try:
            bags = session.query(BagRecord).filter(BagRecord.label_id.in_(label_ids)).all()

            result = {}
            now = datetime.utcnow()

            for bag in bags:
                days_in_vault = (now - bag.first_scan_datetime).days
                result[bag.label_id] = {
                    'days_in_vault': days_in_vault,
                    'first_scan': bag.first_scan_datetime,
                    'is_over_3_days': days_in_vault > 3
                }

            return result
        finally:
            session.close()

    # ===== IMPORT TRACKING METHODS =====

    def record_import(self, import_date: date, carrier_location: str, valid_labels: list[str]) -> dict:
        """
        Record an Excel file import and track all labels from that import.

        Args:
            import_date: Date from Excel Parameters sheet "Created At"
            carrier_location: Carrier location from Excel
            valid_labels: List of all valid labels from the Excel file

        Returns:
            dict with import stats and labels that are >=3 days old
        """
        session = self.get_session()
        try:
            # Create import record
            import_record = ImportRecord(
                import_date=import_date,
                carrier_location=carrier_location
            )
            import_record.set_labels(valid_labels)
            session.add(import_record)

            # Update label import history for each label
            labels_over_3_days = []
            new_labels = []
            updated_labels = []

            for label in valid_labels:
                label = label.strip()
                if not label:
                    continue

                # Find existing history for this label at this location
                history = session.query(LabelImportHistory).filter_by(
                    label_id=label,
                    carrier_location=carrier_location
                ).first()

                if history:
                    # Update existing history
                    existing_dates = history.get_import_dates()

                    # Convert date to string for comparison
                    date_str = import_date.strftime("%Y-%m-%d")

                    # Only add if this date isn't already recorded
                    if date_str not in existing_dates:
                        existing_dates.append(date_str)
                        history.set_import_dates(existing_dates)
                        history.last_import_date = import_date

                        # Update first_import_date if this is earlier
                        if import_date < history.first_import_date:
                            history.first_import_date = import_date

                        updated_labels.append(label)

                    # Check if >=3 days old
                    days_in_vault = history.get_days_in_vault()
                    if days_in_vault >= 3:
                        labels_over_3_days.append({
                            'label_id': label,
                            'days_in_vault': days_in_vault,
                            'first_import_date': history.first_import_date.strftime("%Y-%m-%d"),
                            'import_count': history.import_count
                        })
                else:
                    # Create new history record
                    history = LabelImportHistory(
                        label_id=label,
                        carrier_location=carrier_location,
                        first_import_date=import_date,
                        last_import_date=import_date
                    )
                    history.set_import_dates([import_date.strftime("%Y-%m-%d")])
                    session.add(history)
                    new_labels.append(label)

            session.commit()

            return {
                'success': True,
                'import_date': import_date.strftime("%Y-%m-%d"),
                'carrier_location': carrier_location,
                'total_labels': len(valid_labels),
                'new_labels_count': len(new_labels),
                'updated_labels_count': len(updated_labels),
                'labels_over_3_days': labels_over_3_days,
                'labels_over_3_days_count': len(labels_over_3_days)
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_labels_over_3_days(self, carrier_location: str = None) -> list:
        """
        Get all labels that have been in vault for >=3 days.

        Args:
            carrier_location: Optional filter by location

        Returns:
            List of dicts with label info
        """
        session = self.get_session()
        try:
            query = session.query(LabelImportHistory)

            if carrier_location:
                query = query.filter_by(carrier_location=carrier_location)

            histories = query.all()

            labels_over_3_days = []
            today = date.today()

            for history in histories:
                days_in_vault = (today - history.first_import_date).days

                if days_in_vault >= 3:
                    labels_over_3_days.append({
                        'label_id': history.label_id,
                        'carrier_location': history.carrier_location,
                        'days_in_vault': days_in_vault,
                        'first_import_date': history.first_import_date.strftime("%Y-%m-%d"),
                        'last_import_date': history.last_import_date.strftime("%Y-%m-%d"),
                        'import_count': history.import_count,
                        'import_dates': history.get_import_dates()
                    })

            # Sort by days in vault (descending)
            labels_over_3_days.sort(key=lambda x: x['days_in_vault'], reverse=True)

            return labels_over_3_days

        finally:
            session.close()

    def get_label_import_history(self, label_id: str, carrier_location: str = None) -> dict:
        """Get import history for a specific label"""
        session = self.get_session()
        try:
            query = session.query(LabelImportHistory).filter_by(label_id=label_id)

            if carrier_location:
                query = query.filter_by(carrier_location=carrier_location)

            history = query.first()

            return history.to_dict() if history else None

        finally:
            session.close()

    def get_all_import_records(self, carrier_location: str = None, limit: int = None) -> list:
        """Get all import records"""
        session = self.get_session()
        try:
            query = session.query(ImportRecord).order_by(ImportRecord.import_date.desc())

            if carrier_location:
                query = query.filter_by(carrier_location=carrier_location)

            if limit:
                query = query.limit(limit)

            records = query.all()
            return [record.to_dict() for record in records]

        finally:
            session.close()

    def get_import_duration_stats(self, label_ids: list[str], carrier_location: str) -> dict:
        """
        Get import-based duration stats for labels (used in export).
        This replaces scan-based duration tracking.
        """
        session = self.get_session()
        try:
            histories = session.query(LabelImportHistory).filter(
                LabelImportHistory.label_id.in_(label_ids),
                LabelImportHistory.carrier_location == carrier_location
            ).all()

            result = {}
            today = date.today()

            for history in histories:
                days_in_vault = (today - history.first_import_date).days
                result[history.label_id] = {
                    'days_in_vault': days_in_vault,
                    'first_import_date': history.first_import_date,
                    'is_over_3_days': days_in_vault >= 3,
                    'import_count': history.import_count
                }

            return result
        finally:
            session.close()
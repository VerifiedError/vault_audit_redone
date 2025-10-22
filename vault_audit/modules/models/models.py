from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Parameters:
    created_at: str
    created_by: str
    carrier: str
    carrier_location: str
    created_at_date: Optional[date] = None  # Actual date object for import tracking


@dataclass
class Transaction:
    origin: str
    destination: str
    type: str
    departure_date: str
    arrival_date: str
    labels: list[str]
    total_count: float
    total_value: float


@dataclass
class ContainerData:
    parameters: Parameters
    location_name: str
    valid_labels: set[str]
    transactions: list[Transaction]


@dataclass
class AuditResult:
    total_scanned: int
    matched_labels: set[str]
    unmatched_labels: set[str]
    expected_not_scanned: set[str]
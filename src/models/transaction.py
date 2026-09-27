from datetime import date, datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class Transaction:
    date: date
    amount: Decimal
    currency: str
    description: str
    source: str
    transaction_type: str

    dt: Optional[datetime] = None
    transaction_id: Optional[str] = None
    raw_description: Optional[str] = None
    raw_type: Optional[str] = None
    counterparty_name: Optional[str] = None
    counterparty_iban: Optional[str] = None
    mcc_code: Optional[str] = None
    merchant_category: Optional[str] = None
    fee: Optional[Decimal] = None
import csv
from datetime import datetime
from decimal import Decimal
from normalizers.base import BaseNormalizer
from models.transaction import Transaction

TYPE_MAP = {
    "Interest on cash": "savings",
    "Card debit": "spending",
    "Deposit": "transfer",
}

class Trading212Normalizer(BaseNormalizer):
    def normalize(self, file_path: str) -> list[Transaction]:
        transactions = []
        with open(file_path) as csv_file:
            for row in csv.DictReader(csv_file):
                dt = datetime.fromisoformat(row["Time (UTC)"])
                amount = Decimal(row["Gross Total"])
                currency = row["Currency (Gross Total)"]
                description = row["Merchant name"] or row["Notes"] or ""
                merchant_category = row["Merchant category"]
                identifier = row["ID"]
                source = "trading_212"
                transaction_type = TYPE_MAP[row["Action"]]

                transaction = Transaction(
                    dt.date(), amount, currency, description, source, transaction_type,
                    dt=dt,
                    transaction_id=identifier,
                    merchant_category=merchant_category,
                    raw_type=row["Action"],
                )
                transactions.append(transaction)

        return transactions
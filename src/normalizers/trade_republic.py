import csv
from datetime import datetime, date
from decimal import Decimal
from normalizers.base import BaseNormalizer
from models.transaction import Transaction

TYPE_MAP = {
    "CARD_TRANSACTION": "spending",
    "CARD_TRANSACTION_INTERNATIONAL": "spending",
    "INTEREST_PAYMENT": "income",
    "TRANSFER_INSTANT_INBOUND": "transfer",
    "BUY": "investing",
}

class TradeRepublicNormalizer(BaseNormalizer):
    def normalize(self, file_path: str) -> list[Transaction]:
        transactions = []
        with open(file_path) as csv_file:
            for row in csv.DictReader(csv_file):
                dt = datetime.fromisoformat(row["datetime"])
                transaction_date = date.fromisoformat(row["date"])
                amount = Decimal(row["amount"])
                currency = row["currency"]
                description = row["name"] or row["description"] or ""
                source = "trade_republic"
                transaction_type = TYPE_MAP[row["type"]]
                fee = Decimal(row["fee"]) if row["fee"] else None

                transaction = Transaction(
                    transaction_date, amount, currency, description, source, transaction_type,
                    dt=dt,
                    transaction_id=row["transaction_id"],
                    raw_type=row["type"],
                    counterparty_name=row["counterparty_name"] or None,
                    counterparty_iban=row["counterparty_iban"] or None,
                    mcc_code=row["mcc_code"] or None,
                    fee=fee,
                )
                transactions.append(transaction)

        return transactions
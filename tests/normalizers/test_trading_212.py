import io
from decimal import Decimal

from normalizers.trading_212 import Trading212Normalizer

FIXTURE = "tests/fixtures/trading_212_sample.csv"

def test_interest_row():
    transactions = Trading212Normalizer().normalize(FIXTURE)
    t = transactions[0]
    assert t.transaction_type == "savings"
    assert t.amount == Decimal("0.11")
    assert t.currency == "EUR"
    assert t.description == "Interest on cash"

def test_card_debit_row():
    transactions = Trading212Normalizer().normalize(FIXTURE)
    t = transactions[1]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-159.11")
    assert t.currency == "EUR"
    assert t.description == "Revolut"

def test_deposit_row():
    transactions = Trading212Normalizer().normalize(FIXTURE)
    t = transactions[2]
    assert t.transaction_type == "transfer"
    assert t.amount == Decimal("300.00")
    assert t.currency == "EUR"
    assert t.description == "Transaction ID: 132"
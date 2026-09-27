from decimal import Decimal

from normalizers.trade_republic import TradeRepublicNormalizer

FIXTURE = "tests/fixtures/trade_republic_sample.csv"


def test_card_transaction():
    transactions = TradeRepublicNormalizer().normalize(FIXTURE)
    t = transactions[0]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-12.50")
    assert t.currency == "EUR"
    assert t.description == "Sample Merchant"
    assert t.mcc_code == "5331"


def test_card_transaction_international():
    transactions = TradeRepublicNormalizer().normalize(FIXTURE)
    t = transactions[1]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-8.99")
    assert t.currency == "EUR"
    assert t.description == "Sample Merchant"
    assert t.mcc_code == "5411"


def test_transfer_inbound():
    transactions = TradeRepublicNormalizer().normalize(FIXTURE)
    t = transactions[2]
    assert t.transaction_type == "transfer"
    assert t.amount == Decimal("300.00")
    assert t.currency == "EUR"
    assert t.description == "A B TESTUSER"
    assert t.counterparty_iban == "NL00TEST0000000001"


def test_interest_payment():
    transactions = TradeRepublicNormalizer().normalize(FIXTURE)
    t = transactions[3]
    assert t.transaction_type == "income"
    assert t.amount == Decimal("0.37")
    assert t.currency == "EUR"
    assert t.description == "Interest payment for payout collection 00000000-0000-0000-0000-000000000000"


def test_buy():
    transactions = TradeRepublicNormalizer().normalize(FIXTURE)
    t = transactions[4]
    assert t.transaction_type == "investing"
    assert t.amount == Decimal("-15.00")
    assert t.currency == "EUR"
    assert t.description == "S&P 500 USD (Acc)"
from decimal import Decimal

from normalizers.abn_amro import ABNAmroNormalizer

FIXTURE = "tests/fixtures/abn_amro_sample.mt940"

def test_sepa_incasso():
    transactions = ABNAmroNormalizer().normalize(FIXTURE)
    t = transactions[0]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-49.00")
    assert t.currency == "EUR"
    assert t.counterparty_name == "SAMPLE SUBSCRIPTION"


def test_sepa_overboeking_transfer():
    transactions = ABNAmroNormalizer().normalize(FIXTURE)
    t = transactions[3]
    assert t.transaction_type == "transfer"
    assert t.amount == Decimal("-400.00")
    assert t.currency == "EUR"
    assert t.counterparty_iban == "NL44TRBK0000000001"


def test_bea():
    transactions = ABNAmroNormalizer().normalize(FIXTURE)
    t = transactions[4]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-7.19")
    assert t.currency == "EUR"
    assert t.description == "SAMPLE SUPERMARKET"


def test_ecom():
    transactions = ABNAmroNormalizer().normalize(FIXTURE)
    t = transactions[6]
    assert t.transaction_type == "spending"
    assert t.amount == Decimal("-44.98")
    assert t.currency == "EUR"
    assert t.description == "SAMPLE ONLINE STORE"


def test_sepa_overboeking_income():
    transactions = ABNAmroNormalizer().normalize(FIXTURE)
    t = transactions[9]
    assert t.transaction_type == "income"
    assert t.amount == Decimal("1275.65")
    assert t.currency == "EUR"
    assert t.description == "SALARIS SEPTEMBER"
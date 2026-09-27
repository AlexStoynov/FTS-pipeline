import re
from datetime import date
from decimal import Decimal

from normalizers.base import BaseNormalizer
from models.transaction import Transaction

try:
    from config import KNOWN_OWN_IBANS
except ImportError:
    KNOWN_OWN_IBANS = set()

TAG_RE = re.compile(r"^:[A-Z0-9]{2,3}[F]?:")
FIELD_61_RE = re.compile(r":61:(\d{6})\d{2,4}([CD])(\d+),(\d*)")


def _parse_amount(whole: str, cents: str, direction: str) -> Decimal:
    # build a Decimal from the two groups, make negative if direction == "D"
    decim_value = Decimal(f"{whole}.{cents.ljust(2, '0') if cents else '00'}")

    if direction == "D":
        return -decim_value

    return decim_value

def _extract_field(tag: str, text: str) -> str | None:
    # extract /TAG/value/ from a SEPA description block using regex
    # return None if not found
    m = re.search(f"/{tag}/(.+?)(?=/[A-Z]+/|$)", text)
    return m.group(1).strip() if m else None

def _detect_type(direction: str, desc: str, counterparty_iban: str | None) -> str:
    if "SEPA INCASSO" in desc:
        return "spending"
    elif desc.startswith("BEA") or desc.startswith("ECOM"):
        return "spending"
    elif "IDEAL" in desc:
        return "spending"
    elif "SEPA OVERBOEKING" in desc:
        if counterparty_iban in KNOWN_OWN_IBANS:
            return "transfer"
        elif direction == "C":
            return "income"
        else:
            return "spending"
    else:
        return "spending"


class ABNAmroNormalizer(BaseNormalizer):
    def normalize(self, file_path: str) -> list[Transaction]:
        transactions = []

        with open(file_path, encoding="utf-8") as f:
            lines = f.read().splitlines()

        i = 0
        while i < len(lines):
            m = FIELD_61_RE.match(lines[i])
            if not m:
                i += 1
                continue

            # parse :61:
            date_str, direction, whole, cents = m.group(1), m.group(2), m.group(3), m.group(4)
            transaction_date = date(2000 + int(date_str[:2]), int(date_str[2:4]), int(date_str[4:6]))  # convert YYMMDD string to date object
            amount = _parse_amount(whole, cents, direction)

            # collect :86: block — advance i, gather lines until next tag or "-"
            i += 1
            desc_lines = []

            if i < len(lines) and lines[i].startswith(":86:"):
                desc_lines.append(lines[i])
                i += 1

            while i < len(lines) and not TAG_RE.match(lines[i]) and lines[i] != "-":
                desc_lines.append(lines[i])
                i += 1

            if desc_lines and desc_lines[0].startswith(":86:"):
                desc_lines[0] = desc_lines[0][4:]

            desc_block = "".join(desc_lines)

            # strip the ":86:" prefix from the first desc line if present
            # (hint: desc_lines[0] will start with ":86:")

            # extract fields
            counterparty_iban = _extract_field("IBAN", desc_block)
            counterparty_name = _extract_field("NAME", desc_block)

            if desc_block.startswith("BEA") or desc_block.startswith("ECOM"):
                first_line = desc_lines[0] if desc_lines else ""
                parts = re.split(r'\s{2,}', first_line)
                description = parts[1].strip() if len(parts) > 1 else ""
            else:
                description = _extract_field("REMI", desc_block) or counterparty_name or ""

            transaction_type = _detect_type(direction, desc_block, counterparty_iban)

            transactions.append(Transaction(
                transaction_date, amount, "EUR", description or "", "abn_amro", transaction_type,
                raw_type=desc_block.split("/")[0].strip() or desc_block[:20],
                counterparty_name=counterparty_name,
                counterparty_iban=counterparty_iban,
            ))

        return transactions
"""Wrapper tương thích; implementation dùng chung nằm trong src/spendwise."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from spendwise.cli import main
from spendwise.domain.transactions import (
    CATEGORIES, COLUMNS, MAX_AMOUNT, Transaction, ValidationError, parse_amount, parse_row,
)
from spendwise.services.csv_reader import MAX_BYTES, MAX_ROWS, read_transactions
from spendwise.services.reports import summarize


if __name__ == "__main__":
    raise SystemExit(main())

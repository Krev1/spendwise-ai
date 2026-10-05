"""CLI preview CSV: gọi services và hiển thị kết quả hoặc lỗi input."""

import argparse
import json
import sys
from pathlib import Path

from spendwise.domain.transactions import ValidationError
from spendwise.services.csv_reader import read_transactions
from spendwise.services.reports import summarize


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Kiểm tra CSV và xem trước tổng hợp thu chi")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--month", help="Lọc YYYY-MM, ví dụ 2026-10")
    arguments = parser.parse_args()
    try:
        result = summarize(read_transactions(arguments.csv_path), arguments.month)
    except (ValidationError, OSError) as error:
        print(f"Lỗi: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

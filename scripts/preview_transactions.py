"""Điểm chạy từ checkout; giúp dùng src/ mà chưa cần cài package editable."""

import sys
from pathlib import Path

# Bootstrap chỉ nằm ở điểm chạy; domain/services không tự sửa import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from spendwise.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

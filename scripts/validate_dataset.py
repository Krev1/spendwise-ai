"""Read-only validation. Do not redirect reports containing real IDs into Git."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from spendwise.data.dataset import MAX_BYTES, DatasetError, audit_dataset


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Kiểm tra dataset ML sáu cột, không train.")
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    try:
        with args.dataset.open("rb") as stream:
            report = audit_dataset(stream.read(MAX_BYTES + 1))
    except (OSError, DatasetError) as error:
        print(f"Lỗi dataset: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Only the committed fictional seed is supported by this prototype CLI."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spendwise.data.dataset import MAX_BYTES
from spendwise.data.splitting import SplitError, build_bundle, verify_bundle, write_bundle


def bounded_read(path: Path) -> bytes:
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise SplitError("Input vượt giới hạn byte.")
    return raw


def seed_bundle() -> dict[str, bytes]:
    guideline = (ROOT / "docs/05_data_and_ml.md").read_text(encoding="utf-8")
    try:
        start = guideline.index("## 2. Bộ nhãn") + len("## 2. Bộ nhãn")
        end = guideline.index("## 3. Kế hoạch", start)
        section = guideline[start:end]
    except ValueError:
        raise SplitError("Không tìm được guideline nhãn section 2.") from None
    return build_bundle(
        bounded_read(ROOT / "data/seed/v0.1/expense_descriptions_vi.csv"),
        bounded_read(ROOT / "data/seed/v0.1/provenance.csv"),
        bounded_read(ROOT / "data/recipes/prototype_split_relations.csv"),
        section.encode("utf-8"),
    )


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Audit/split seed hư cấu; không fit hoặc đo metric.")
    parser.add_argument("--output", type=Path, default=ROOT / "data/splits/seed-v0.1-prototype")
    parser.add_argument("--write", action="store_true", help="Tạo bundle mới; không overwrite lock khác nội dung.")
    args = parser.parse_args()
    try:
        expected = seed_bundle()
        if args.write:
            status = write_bundle(args.output, expected)
        elif args.output.exists():
            verify_bundle(args.output, expected)
            status = "verified_existing"
        else:
            status = "preview_only"
        audit = json.loads(expected["audit.json"])
    except OSError:
        print("Lỗi split: không đọc/ghi được bundle hoặc input local.", file=sys.stderr)
        return 1
    except (SplitError, UnicodeError) as error:
        print(f"Lỗi split: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": status, **audit}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

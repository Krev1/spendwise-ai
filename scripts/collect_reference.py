"""Verify the pinned public SYNTHETIC reference; no scraping or bank connection."""

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical_bytes(raw: bytes) -> bytes:
    return raw.decode("utf-8").replace("\r\n", "\n").encode("utf-8")


def verify_reference(root: Path = ROOT, online: bool = False) -> dict:
    manifest = json.loads((root / "data/reference/source_manifest.json").read_text(encoding="utf-8"))
    result = {"source_id": manifest["source_id"], "commit": manifest["commit"], "mode": "online" if online else "offline", "files": []}
    for entry in manifest["files"]:
        local = canonical_bytes((root / entry["snapshot_path"]).read_bytes())
        if hashlib.sha256(local).hexdigest() != entry["sha256_utf8_lf"]:
            raise ValueError(f"Hash snapshot không khớp: {entry['snapshot_path']}")
        if online:
            # URL fixed by the reviewed manifest, not supplied by a transaction/user.
            with urllib.request.urlopen(entry["url"], timeout=30) as response:
                remote = response.read(2_000_001)
            if len(remote) > 2_000_000 or hashlib.sha256(remote).hexdigest() != entry["sha256_repository_bytes"]:
                raise ValueError("Hash file nguồn tại commit cố định không khớp.")
            if hashlib.sha256(canonical_bytes(remote)).hexdigest() != entry["sha256_utf8_lf"]:
                raise ValueError("Hash nguồn sau chuẩn hóa newline không khớp.")
        result["files"].append({"path": entry["snapshot_path"], "sha256_utf8_lf": entry["sha256_utf8_lf"], "verified": True})
    return result


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Đối chiếu snapshot/giấy phép nguồn hư cấu tại commit cố định.")
    parser.add_argument("--verify-online", action="store_true", help="Đọc lại raw GitHub; cần mạng. Mặc định chỉ kiểm tra offline.")
    args = parser.parse_args()
    try:
        print(json.dumps(verify_reference(online=args.verify_online), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print(f"Lỗi nguồn dữ liệu: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

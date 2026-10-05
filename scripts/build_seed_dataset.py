"""Build only reviewed fictional recipes; deterministic and offline."""

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from collect_reference import verify_reference
from spendwise.data.dataset import FIELDS, audit_dataset, normalize_text, remove_diacritics

SEED_DIR = "data/seed/v0.1"
PROVENANCE_FIELDS = (
    "record_id", "annotation_status", "pattern_family_id", "normalized_text_hash",
    "transformation", "original_phrase_id", "source_id", "source_commit",
    "source_row", "annotation_rationale",
)
SELECTION_FIELDS = ("source_row", "original_description", "description_base", "decision", "related_record_id", "reason")


def csv_bytes(fields, rows) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def table(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def strip_demo_codes(text: str) -> str:
    # Source README declares fictional records. Strip only trailing numeric tokens;
    # do not run this rule on arbitrary real descriptions (e.g. course names).
    return re.sub(r"(?:\s+\d+)+$", "", text).strip()


def build_outputs(root: Path = ROOT) -> dict[str, bytes]:
    verify_reference(root)
    manifest = json.loads((root / "data/reference/source_manifest.json").read_text(encoding="utf-8"))
    rows, provenance, decisions = [], [], []
    text_keys = set()
    noop_variants = 0

    def add(record_id, description, label, group_id, source, family, phrase_id, source_row, rationale):
        nonlocal noop_variants
        for suffix, text, transformation in [("", description, "original_vi" if source == "author_synthetic" else "translated_en_to_vi"),
                                              ("_nd", remove_diacritics(description), "diacritic_removed")]:
            if suffix and text == description:
                noop_variants += 1
                continue
            key = normalize_text(text)
            if key in text_keys:
                raise ValueError(f"Recipe trùng: {record_id + suffix}; cần sửa/audit recipe, không âm thầm nhân bản.")
            text_keys.add(key)
            rows.append(dict(zip(FIELDS, [record_id + suffix, text, label, group_id, source, "true"])))
            provenance.append(dict(zip(PROVENANCE_FIELDS, [
                record_id + suffix, "ai_draft", family, hashlib.sha256(key.encode("utf-8")).hexdigest(),
                transformation, phrase_id, "spendwise_authored" if source == "author_synthetic" else manifest["source_id"],
                "" if source == "author_synthetic" else manifest["commit"], source_row, rationale,
            ])))

    for recipe in table(root / "data/recipes/seed_phrases.csv"):
        rationale = "Ví dụ hư cấu được trợ lý AI soạn theo guideline v0.1; chưa có người kiểm tra độc lập."
        if recipe["pattern_family_id"] == "tpl_khac_thieu_ngu_canh":
            rationale += " Kịch bản giả lập đã hỏi lại nhưng không bổ sung được; không phải phản hồi của người thật."
        add("seed_" + recipe["phrase_id"], recipe["description"], recipe["label"], recipe["pattern_family_id"],
            "author_synthetic", recipe["pattern_family_id"], recipe["phrase_id"], "",
            rationale)

    mapping = {r["source_description_base"]: r for r in table(root / "data/recipes/public_adaptations.csv")}
    selected = {}
    for source_row, row in enumerate(table(root / "data/reference/pfa_demo_transactions.csv"), 2):
        base = strip_demo_codes(row["Description"])
        record_id = ""
        if Decimal(row["Amount"]) >= 0:
            decision, reason = "excluded_nonexpense", "Số tiền nguồn không âm: thu/hoàn tiền, ngoài bài toán khoản chi."
        elif base not in mapping:
            decision, reason = "excluded_unmapped", "Tên cửa hàng/mô tả chưa rõ hoặc ranh giới nhãn chưa chốt; không tự suy đoán vật đã mua."
        elif base in selected:
            decision, reason = "merged_same_source_description", "Cùng mô tả nguồn sau bỏ mã demo; giữ một mô tả canonical, không coi là mẫu độc lập."
            record_id = selected[base]
        else:
            recipe = mapping[base]
            record_id = f"pub_pfa_{source_row:03d}"
            family = "pfa_" + re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_")
            add(record_id, recipe["description_vi"], recipe["label"], "public_pfa_demo", "public_synthetic",
                family, base, str(source_row), recipe["annotation_rationale"] + "; ai_draft, cần người rà soát bản dịch và nhãn.")
            selected[base] = record_id
            decision, reason = "selected_translation", "Chọn mô tả có dịch vụ/sản phẩm đủ rõ theo ánh xạ dự thảo có version."
        decisions.append(dict(zip(SELECTION_FIELDS, [source_row, row["Description"], base, decision, record_id, reason])))
    if set(mapping) != set(selected):
        raise ValueError("Recipe ánh xạ chứa mô tả không có trong phần khoản chi nguồn.")

    dataset = csv_bytes(FIELDS, rows)
    prov = csv_bytes(PROVENANCE_FIELDS, provenance)
    selection = csv_bytes(SELECTION_FIELDS, decisions)
    report = {
        "dataset_version": "0.1", "created_on": "2026-10-05", **audit_dataset(dataset),
        "annotation_status_counts": {"ai_draft": len(rows)}, "human_reviewed_records": 0,
        "source_rows_collected": len(decisions),
        "source_selection_counts": {s: sum(d["decision"] == s for d in decisions) for s in sorted({d["decision"] for d in decisions})},
        "authored_base_phrases": len(table(root / "data/recipes/seed_phrases.csv")),
        "public_base_translations": len(selected), "no_op_diacritic_variants_skipped": noop_variants,
        "provenance_sha256": hashlib.sha256(prov).hexdigest(), "source_selection_sha256": hashlib.sha256(selection).hexdigest(),
        "recipe_sha256": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in ["data/recipes/seed_phrases.csv", "data/recipes/public_adaptations.csv"]},
        "split_status": "not_created", "trained_models": 0, "real_performance_metrics": None,
    }
    return {"expense_descriptions_vi.csv": dataset, "provenance.csv": prov, "source_selection.csv": selection,
            "audit_report.json": (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")}


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Tái tạo seed hư cấu offline; mặc định đối chiếu byte với snapshot.")
    parser.add_argument("--write", action="store_true", help="Ghi lại bốn file seed/audit cố định; chỉ dùng khi cập nhật recipe có chủ đích.")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        directory = ROOT / SEED_DIR
        if args.write:
            directory.mkdir(parents=True, exist_ok=True)
            for name, content in outputs.items():
                (directory / name).write_bytes(content)
        else:
            mismatches = [name for name, content in outputs.items() if not (directory / name).exists() or (directory / name).read_bytes() != content]
            if mismatches:
                raise ValueError("Snapshot không khớp: " + ", ".join(mismatches))
        report = json.loads(outputs["audit_report.json"])
        print(json.dumps({"status": "written" if args.write else "reproduced_exactly", "records": report["records"], "real_records": report["real_records"], "sha256": report["sha256"]}, indent=2))
    except (OSError, ValueError, KeyError) as error:
        print(f"Lỗi xây seed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

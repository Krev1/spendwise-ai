"""Validate the six-column ML dataset; never treats AI labels as human reviewed."""

import csv
import hashlib
import io
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from spendwise.domain.transactions import CATEGORIES

FIELDS = ("record_id", "description", "label", "group_id", "source", "is_synthetic")
SOURCES = {"author_synthetic": "true", "public_synthetic": "true", "volunteer": "false"}
MAX_BYTES = 2_000_000
MAX_RECORDS = 5_000
IDENTIFIER = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
PII_PATTERN = re.compile(r"\S+@\S+|https?://|(?:\d[\s().+-]*){9,}", re.IGNORECASE)


class DatasetError(ValueError):
    """A dataset violates its contract. Error messages omit description text."""


def normalize_text(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).lower().split())


def remove_diacritics(text: str) -> str:
    """For variant audits/demo generation, not the primary model preprocessing."""
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn").replace("đ", "d").replace("Đ", "D")


@dataclass(frozen=True)
class DatasetRecord:
    record_id: str
    description: str
    label: str
    group_id: str
    source: str
    is_synthetic: bool


def read_dataset_bytes(raw: bytes) -> list[DatasetRecord]:
    if len(raw) > MAX_BYTES:
        raise DatasetError("Dataset vượt giới hạn 2.000.000 byte.")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise DatasetError("Dataset cần mã hóa UTF-8.") from None
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    records = []
    seen_ids = set()
    text_keys = {}
    folded_groups = {}
    group_sources = {}
    try:
        if tuple(next(reader, [])) != FIELDS:
            raise DatasetError("Header dataset phải đúng sáu cột ML theo thứ tự.")
        while True:
            line = reader.line_num + 1
            row = next(reader, None)
            if row is None:
                break
            prefix = f"Dòng {line}: "
            if len(row) != len(FIELDS):
                raise DatasetError(prefix + "cần đúng sáu trường, không có dòng rỗng.")
            record_id, description, label, group_id, source, synthetic = row
            if not IDENTIFIER.fullmatch(record_id) or not IDENTIFIER.fullmatch(group_id):
                raise DatasetError(prefix + "ID/nhóm cần 1–64 ký tự ASCII chữ/số/_/-.")
            if record_id in seen_ids:
                raise DatasetError(prefix + "record_id bị trùng.")
            description = unicodedata.normalize("NFC", description).strip()
            if not 1 <= len(description) <= 300 or not any(c.isalpha() for c in description):
                raise DatasetError(prefix + "mô tả cần có chữ và dài 1–300 ký tự.")
            if label not in CATEGORIES:
                raise DatasetError(prefix + "label ngoài bộ tám nhãn.")
            if source not in SOURCES or synthetic != SOURCES[source]:
                raise DatasetError(prefix + "source/is_synthetic không hợp lệ hoặc không nhất quán.")
            if group_id in group_sources and group_sources[group_id] != source:
                raise DatasetError(prefix + "một nhóm có nguồn không nhất quán.")
            key = normalize_text(description)
            if key in text_keys:
                reason = "nhãn xung đột" if text_keys[key] != label else "văn bản chuẩn hóa bị trùng"
                raise DatasetError(prefix + reason + "; cần audit/gộp trước khi dùng.")
            folded = remove_diacritics(key)
            if folded in folded_groups and folded_groups[folded] != (group_id, label):
                raise DatasetError(prefix + "biến thể khác dấu giao nhóm hoặc nhãn; cần audit.")
            records.append(DatasetRecord(record_id, description, label, group_id, source, synthetic == "true"))
            if len(records) > MAX_RECORDS:
                raise DatasetError("Dataset vượt giới hạn 5.000 bản ghi.")
            seen_ids.add(record_id)
            text_keys[key] = label
            folded_groups[folded] = (group_id, label)
            group_sources[group_id] = source
    except csv.Error:
        raise DatasetError(f"Dòng {reader.line_num}: cú pháp CSV không hợp lệ.") from None
    if not records:
        raise DatasetError("Dataset chưa có bản ghi.")
    return records


def read_dataset(path: Path | str) -> list[DatasetRecord]:
    with Path(path).open("rb") as stream:
        return read_dataset_bytes(stream.read(MAX_BYTES + 1))


def summarize_dataset(records: list[DatasetRecord]) -> dict:
    """Structural statistics, not an annotation-quality/privacy certification."""
    return {
        "records": len(records),
        "synthetic_records": sum(r.is_synthetic for r in records),
        "real_records": sum(not r.is_synthetic for r in records),
        "groups": len({r.group_id for r in records}),
        "records_by_label": {c: sum(r.label == c for r in records) for c in sorted(CATEGORIES)},
        "records_by_source": dict(sorted(Counter(r.source for r in records).items())),
        "groups_by_label": {c: len({r.group_id for r in records if r.label == c}) for c in sorted(CATEGORIES)},
        "missing_labels": sorted(CATEGORIES - {r.label for r in records}),
        "normalized_unique_descriptions": len({normalize_text(r.description) for r in records}),
        "diacritic_folded_unique_descriptions": len({remove_diacritics(normalize_text(r.description)) for r in records}),
        "potential_pii_record_ids": [r.record_id for r in records if PII_PATTERN.search(r.description)],
        "human_annotation_review": "not_verified_by_validator",
        "privacy_review": "requires_human_review",
        "real_evaluation_readiness": "not_assessed; consent, annotation and independent real split required",
    }


def audit_dataset(raw: bytes) -> dict:
    records = read_dataset_bytes(raw)
    return {"sha256": hashlib.sha256(raw).hexdigest(), "structural_validation": "passed", **summarize_dataset(records)}

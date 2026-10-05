"""Audited, immutable partitions for fictional smoke data; no model fitting."""

import csv
import hashlib
import io
import itertools
import json
import os
import platform
import re
import tempfile
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import sklearn
from sklearn.model_selection import StratifiedGroupKFold

from spendwise.data.dataset import (
    MAX_BYTES, DatasetError, normalize_text, read_dataset_bytes, remove_diacritics,
)
from spendwise.domain.transactions import CATEGORIES

PROVENANCE_FIELDS = (
    "record_id", "annotation_status", "pattern_family_id", "normalized_text_hash",
    "transformation", "original_phrase_id", "source_id", "source_commit",
    "source_row", "annotation_rationale",
)
LINK_FIELDS = ("record_a", "record_b", "relation_status", "human_reviewed", "rationale")
MANIFEST_FIELDS = (
    "record_id", "group_id", "effective_group_id", "pattern_family_id", "family_hash",
    "lineage_hash", "normalized_text_hash", "folded_text_hash", "label", "source",
    "is_synthetic", "annotation_status", "split",
)
SPLITS = ("train", "validation", "test")
PROTOCOL = "synthetic-prototype-split-v1"
SEED = 42
MAX_FOLDED_TEXTS = 500


class SplitError(ValueError):
    """Invalid inputs/partition; messages omit descriptions and private paths."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _table(raw: bytes, fields: tuple[str, ...]) -> list[dict[str, str]]:
    if len(raw) > MAX_BYTES:
        raise SplitError("Metadata vượt giới hạn byte.")
    try:
        reader = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
        if tuple(next(reader, [])) != fields:
            raise SplitError("Header metadata sai hợp đồng.")
        rows = []
        for row in reader:
            if len(row) != len(fields):
                raise SplitError("Metadata cần đủ trường, không có dòng rỗng.")
            rows.append(dict(zip(fields, row)))
    except (UnicodeError, csv.Error):
        raise SplitError("Metadata cần CSV UTF-8 hợp lệ.") from None
    return rows


def read_provenance(raw: bytes, records) -> dict[str, dict[str, str]]:
    rows = _table(raw, PROVENANCE_FIELDS)
    by_id = {row["record_id"]: row for row in rows}
    if len(by_id) != len(rows) or set(by_id) != {r.record_id for r in records}:
        raise SplitError("Provenance cần khớp mỗi ID dataset đúng một lần.")
    lineage_labels = {}
    for record in records:
        row = by_id[record.record_id]
        if row["normalized_text_hash"] != sha256(normalize_text(record.description).encode("utf-8")):
            raise SplitError("Hash văn bản provenance không khớp snapshot.")
        if row["annotation_status"] != "ai_draft":
            raise SplitError("Prototype này chỉ nhận provenance nhãn ai_draft.")
        if any(not row[field].strip() for field in ("pattern_family_id", "original_phrase_id", "source_id")):
            raise SplitError("Provenance thiếu family/phrase/source.")
        lineage = _namespace(row, "original_phrase_id")
        if lineage in lineage_labels and lineage_labels[lineage] != record.label:
            raise SplitError("Nhãn xung đột trong cùng lineage; cần rà soát trước split.")
        lineage_labels[lineage] = record.label
        if record.source == "author_synthetic":
            if row["source_commit"] or row["source_row"]:
                raise SplitError("Nguồn tự tạo không có commit/dòng nguồn công khai.")
            if row["transformation"] not in {"original_vi", "diacritic_removed"}:
                raise SplitError("Transformation nguồn tự tạo sai hợp đồng.")
        elif (not re.fullmatch(r"[0-9a-f]{40}", row["source_commit"]) or
              not re.fullmatch(r"[1-9][0-9]{0,8}", row["source_row"]) or
              int(row["source_row"]) < 2 or
              row["transformation"] not in {"translated_en_to_vi", "diacritic_removed"}):
            raise SplitError("Nguồn công khai thiếu commit/dòng/transformation hợp lệ.")
    return by_id


def read_links(raw: bytes, records) -> list[dict[str, str]]:
    links = _table(raw, LINK_FIELDS)
    ids = {r.record_id for r in records}
    seen = set()
    for row in links:
        pair = tuple(sorted((row["record_a"], row["record_b"])))
        if pair[0] == pair[1] or pair in seen or not set(pair) <= ids:
            raise SplitError("Recipe liên kết có ID thiếu/trùng hoặc self-link.")
        if row["relation_status"] != "ai_conservative_prototype" or row["human_reviewed"] != "false":
            raise SplitError("Liên kết chỉ được ghi bảo thủ AI, chưa human-reviewed.")
        if not row["rationale"].strip():
            raise SplitError("Liên kết cần lý do prototype.")
        seen.add(pair)
    return sorted(links, key=lambda row: (row["record_a"], row["record_b"]))


def _namespace(row: dict[str, str], field: str) -> tuple[str, str, str]:
    return row["source_id"], row["source_commit"], row[field]


def _key_hash(key) -> str:
    return sha256(json.dumps(key, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def effective_groups(records, provenance, links) -> dict[str, str]:
    """Union transitive relationships; similarities alone never create links."""
    parent = {r.group_id: r.group_id for r in records}

    def find(group):
        while group != parent[group]:
            parent[group] = parent[parent[group]]
            group = parent[group]
        return group

    def union(a, b):
        a, b = find(a), find(b)
        parent[max(a, b)] = min(a, b)

    first = {}
    by_id = {r.record_id: r for r in records}
    for record in records:
        row = provenance[record.record_id]
        keys = [
            ("family", _namespace(row, "pattern_family_id")),
            ("lineage", _namespace(row, "original_phrase_id")),
            ("folded", remove_diacritics(normalize_text(record.description))),
        ]
        for key in keys:
            if key in first:
                union(record.group_id, first[key])
            else:
                first[key] = record.group_id
    for link in links:
        union(by_id[link["record_a"]].group_id, by_id[link["record_b"]].group_id)
    members = defaultdict(list)
    for group in sorted(parent):
        members[find(group)].append(group)
    identifiers = {key: "eg_" + _key_hash(value) for key, value in members.items()}
    return {r.record_id: identifiers[find(r.group_id)] for r in records}


def near_duplicate_candidates(records, groups) -> list[dict]:
    representatives = {}
    for record in sorted(records, key=lambda r: r.record_id):
        folded = remove_diacritics(normalize_text(record.description))
        representatives.setdefault(folded, record)
    if len(representatives) > MAX_FOLDED_TEXTS:
        raise SplitError("Prototype audit giới hạn 500 văn bản folded để giữ budget CPU.")
    candidates = []
    for (a, ra), (b, rb) in itertools.combinations(sorted(representatives.items()), 2):
        if ra.group_id == rb.group_id:
            continue
        tokens_a, tokens_b = set(a.split()), set(b.split())
        token = len(tokens_a & tokens_b) / len(tokens_a | tokens_b)
        grams_a = {a[i:i + 3] for i in range(max(0, len(a) - 2))}
        grams_b = {b[i:i + 3] for i in range(max(0, len(b) - 2))}
        char3 = len(grams_a & grams_b) / len(grams_a | grams_b) if grams_a | grams_b else 0.0
        sequence = SequenceMatcher(None, a, b, autojunk=False).ratio()
        short, long = sorted((a, b), key=len)
        contains = len(short.split()) >= 2 and len(short) >= 8 and bool(re.search(r"(?<!\w)" + re.escape(short) + r"(?!\w)", long))
        if sequence >= 0.70 or token >= 0.50 or char3 >= 0.40 or contains:
            candidates.append({
                "record_a": ra.record_id, "record_b": rb.record_id,
                "sequence_ratio": round(sequence, 6), "token_jaccard": round(token, 6),
                "char3_jaccard": round(char3, 6), "phrase_containment": contains,
                "cross_source": ra.source != rb.source,
                "co_located_in_prototype": groups[ra.record_id] == groups[rb.record_id],
                "human_reviewed": False,
            })
    return candidates


def validate_partition(records, provenance, links, groups, assignments):
    ids = {r.record_id for r in records}
    if set(assignments) != ids or any(value not in SPLITS for value in assignments.values()):
        raise SplitError("Partition cần mỗi ID đúng một split hợp lệ.")
    if set(assignments.values()) != set(SPLITS):
        raise SplitError("Partition prototype cần ba split không rỗng.")
    owners = {}
    for record in records:
        row = provenance[record.record_id]
        keys = [
            ("group", record.group_id), ("effective", groups[record.record_id]),
            ("family", _namespace(row, "pattern_family_id")),
            ("lineage", _namespace(row, "original_phrase_id")),
            ("normalized", normalize_text(record.description)),
            ("folded", remove_diacritics(normalize_text(record.description))),
        ]
        for key in keys:
            split = assignments[record.record_id]
            if key in owners and owners[key] != split:
                raise SplitError("Rò rỉ group/family/lineage/text giữa các split.")
            owners[key] = split
    for row in links:
        if assignments[row["record_a"]] != assignments[row["record_b"]]:
            raise SplitError("Quan hệ prototype chạy qua nhiều split.")


def build_bundle(dataset_raw: bytes, provenance_raw: bytes, links_raw: bytes, guideline_raw: bytes) -> dict[str, bytes]:
    try:
        records = sorted(read_dataset_bytes(dataset_raw), key=lambda r: r.record_id)
    except DatasetError as error:
        raise SplitError(str(error)) from None
    if any(not r.is_synthetic or r.source == "volunteer" for r in records):
        raise SplitError("Grouped split prototype chỉ nhận dữ liệu hư cấu; dữ liệu thật cần protocol riêng.")
    provenance = read_provenance(provenance_raw, records)
    links = read_links(links_raw, records)
    groups = effective_groups(records, provenance, links)
    candidates = near_duplicate_candidates(records, groups)
    if len(set(groups.values())) < 7:
        raise SplitError("Cần ít nhất 7 nhóm hiệu lực cho protocol 7 fold.")
    splitter = StratifiedGroupKFold(n_splits=7, shuffle=True, random_state=SEED)
    assignments = {}
    try:
        for fold, (_, indices) in enumerate(splitter.split(
            np.zeros((len(records), 1)), [r.label for r in records], [groups[r.record_id] for r in records]
        )):
            split = "test" if fold == 0 else "validation" if fold == 1 else "train"
            for index in indices:
                assignments[records[index].record_id] = split
    except ValueError:
        raise SplitError("Không đủ cấu trúc mẫu/lớp cho protocol 7 fold.") from None
    validate_partition(records, provenance, links, groups, assignments)
    manifest = io.StringIO(newline="")
    writer = csv.DictWriter(manifest, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
    writer.writeheader()
    for record in records:
        row = provenance[record.record_id]
        writer.writerow({
            "record_id": record.record_id, "group_id": record.group_id,
            "effective_group_id": groups[record.record_id], "pattern_family_id": row["pattern_family_id"],
            "family_hash": _key_hash(_namespace(row, "pattern_family_id")),
            "lineage_hash": _key_hash(_namespace(row, "original_phrase_id")),
            "normalized_text_hash": row["normalized_text_hash"],
            "folded_text_hash": sha256(remove_diacritics(normalize_text(record.description)).encode("utf-8")),
            "label": record.label, "source": record.source, "is_synthetic": "true",
            "annotation_status": row["annotation_status"], "split": assignments[record.record_id],
        })
    per_split = {}
    targets = dict(zip(SPLITS, (0.70, 0.15, 0.15)))
    for split in SPLITS:
        subset = [r for r in records if assignments[r.record_id] == split]
        support = {label: sum(r.label == label for r in subset) for label in sorted(CATEGORIES)}
        per_split[split] = {
            "records": len(subset), "fraction": len(subset) / len(records),
            "target_fraction": targets[split], "fraction_deviation": len(subset) / len(records) - targets[split],
            "effective_groups": len({groups[r.record_id] for r in subset}),
            "folded_unique_descriptions": len({remove_diacritics(normalize_text(r.description)) for r in subset}),
            "records_by_label": support, "missing_labels": [label for label, n in support.items() if not n],
            "records_by_source": dict(sorted(Counter(r.source for r in subset).items())),
        }
    audit = {
        "purpose": "synthetic_prototype_only", "records": len(records), "real_records": 0,
        "original_groups": len({r.group_id for r in records}), "effective_groups": len(set(groups.values())),
        "pattern_families": len({_namespace(row, "pattern_family_id") for row in provenance.values()}),
        "original_phrases": len({_namespace(row, "original_phrase_id") for row in provenance.values()}),
        "folded_unique_descriptions": len({remove_diacritics(normalize_text(r.description)) for r in records}),
        "exact_normalized_duplicates": 0, "prototype_links": links,
        "near_duplicate_candidates": candidates, "human_reviewed_records": 0,
        "semantic_relationship_review": "pending_human_review",
        "partition_overlap_check": "passed_for_declared_keys_and_links",
        "per_split": per_split,
        "eight_class_partition_complete": all(not value["missing_labels"] for value in per_split.values()),
        "real_evaluation_ready": False, "research_metrics": "not_run",
    }
    files = {"split_manifest.csv": manifest.getvalue().encode("utf-8"), "audit.json": json_bytes(audit)}
    lock = {
        "protocol_version": PROTOCOL, "purpose": "synthetic_prototype_only", "seed": SEED,
        "splitter": {"class": "StratifiedGroupKFold", "n_splits": 7, "shuffle": True,
                     "test_fold": 0, "validation_fold": 1, "remaining_folds": "train"},
        "input_sha256": {"dataset": sha256(dataset_raw), "provenance": sha256(provenance_raw),
                         "relations": sha256(links_raw), "label_guideline_section": sha256(guideline_raw)},
        "label_guideline_version": "0.1; docs/05_data_and_ml.md section 2",
        "normalization": "NFC/lowercase/collapse_whitespace; accent_folding_for_audit_only",
        "near_audit": {"sequence_min": 0.70, "token_jaccard_min": 0.50, "char3_jaccard_min": 0.40,
                       "containment_min_tokens": 2, "containment_min_characters": 8, "max_folded_texts": MAX_FOLDED_TEXTS},
        "environment": {"python": platform.python_version(), "sklearn": sklearn.__version__, "numpy": np.__version__},
        "implementation_sha256": sha256(Path(__file__).read_bytes()),
        "normalizer_implementation_sha256": sha256(Path(__file__).with_name("dataset.py").read_bytes()),
        "files_sha256": {name: sha256(raw) for name, raw in files.items()},
        "test_scope": "fictional_prototype; not_independent_real_holdout",
    }
    files["lock.json"] = json_bytes(lock)
    return files


def _reject_redirects(path: Path) -> None:
    """Reject symlinks and Windows reparse points before resolving paths."""
    for candidate in (path.absolute(), *path.absolute().parents):
        if candidate.is_symlink() or candidate.is_junction():
            raise SplitError("Bundle không dùng symlink/junction hoặc thư mục cha chuyển hướng.")
        try:
            attributes = getattr(candidate.lstat(), "st_file_attributes", 0)
        except FileNotFoundError:
            continue
        if attributes & 0x400:  # FILE_ATTRIBUTE_REPARSE_POINT on Windows
            raise SplitError("Bundle không dùng reparse point.")


def verify_bundle(output: Path, expected: dict[str, bytes]) -> dict:
    """Verify by reproducible bytes, including lock; no editable lock is trusted."""
    if set(expected) != {"split_manifest.csv", "audit.json", "lock.json"}:
        raise SplitError("Bundle expected sai hợp đồng ba file.")
    _reject_redirects(output)
    if not output.is_dir():
        raise SplitError("Bundle phải là thư mục local đầy đủ.")
    for path in output.iterdir():
        _reject_redirects(path)
    if {path.name for path in output.iterdir()} != set(expected):
        raise SplitError("Bundle thiếu/thừa file; không dùng hoặc overwrite.")
    for name, raw in expected.items():
        with (output / name).open("rb") as stream:
            if stream.read(len(raw) + 1) != raw:
                raise SplitError("Bundle/hash/config/snapshot không khớp; tạo phiên bản mới có kiểm soát.")
    return json.loads(expected["audit.json"])


def load_split_ids(output: Path, expected: dict[str, bytes]) -> dict[str, tuple[str, ...]]:
    """Only expose partition IDs after checking the trusted recomputed bundle."""
    verify_bundle(output, expected)
    rows = _table(expected["split_manifest.csv"], MANIFEST_FIELDS)
    return {split: tuple(row["record_id"] for row in rows if row["split"] == split) for split in SPLITS}


def write_bundle(output: Path, expected: dict[str, bytes]) -> str:
    """Publish a complete new directory; an existing lock cannot be rewritten."""
    if set(expected) != {"split_manifest.csv", "audit.json", "lock.json"}:
        raise SplitError("Bundle sai hợp đồng; không ghi.")
    _reject_redirects(output)
    output = output.resolve()
    if output.exists():
        verify_bundle(output, expected)
        return "verified_existing"
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".split-stage-", dir=output.parent) as staging:
        if Path(staging).resolve().parent != output.parent:
            raise SplitError("Thư mục staging không thuộc output parent.")
        staged = Path(staging) / "bundle"
        staged.mkdir()
        for name, raw in expected.items():
            with (staged / name).open("xb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        verify_bundle(staged, expected)
        if output.exists():
            raise SplitError("Bundle đã xuất hiện trong lúc ghi; không overwrite.")
        staged.rename(output)
    return "created"

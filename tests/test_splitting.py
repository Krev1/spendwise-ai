"""Leakage boundaries and immutable fictional bundles, without model fitting."""

import csv
import io
import json
import os
import subprocess
from pathlib import Path

import pytest

from spendwise.data.dataset import FIELDS, normalize_text, read_dataset_bytes, remove_diacritics
from spendwise.data.splitting import (
    LINK_FIELDS, MANIFEST_FIELDS, PROVENANCE_FIELDS, SPLITS, SplitError, build_bundle,
    effective_groups, load_split_ids, read_links, read_provenance, sha256,
    validate_partition, verify_bundle, write_bundle,
)


def table(rows, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


@pytest.fixture
def inputs():
    records, provenance = [], []
    for i in range(10):
        phrase = f"mẫu cơm gia đình số {i}"
        for variant, text in (("", phrase), ("_nd", remove_diacritics(phrase))):
            record_id = f"r{i}{variant}"
            records.append(dict(zip(FIELDS, (record_id, text, "an_uong", f"g{i}", "author_synthetic", "true"))))
            provenance.append(dict(zip(PROVENANCE_FIELDS, (
                record_id, "ai_draft", f"f{i}", sha256(normalize_text(text).encode()),
                "diacritic_removed" if variant else "original_vi", f"p{i}", "fixture", "", "", "Fictional draft",
            ))))
    return records, provenance, []


def bundle(inputs):
    records, provenance, links = inputs
    return build_bundle(table(records, FIELDS), table(provenance, PROVENANCE_FIELDS),
                        table(links, LINK_FIELDS), b"fixture guideline v0.1")


def metadata(inputs):
    records, provenance, links = inputs
    parsed = read_dataset_bytes(table(records, FIELDS))
    return parsed, read_provenance(table(provenance, PROVENANCE_FIELDS), parsed), read_links(table(links, LINK_FIELDS), parsed)


def test_every_id_once_and_declared_relationships_never_cross_split(inputs):
    files = bundle(inputs)
    rows = list(csv.DictReader(io.StringIO(files["split_manifest.csv"].decode())))
    assert len(rows) == len({r["record_id"] for r in rows}) == 20
    assert {r["record_id"] for r in rows} == {r["record_id"] for r in inputs[0]}
    assert {r["split"] for r in rows} == set(SPLITS)
    for field in ("group_id", "effective_group_id", "family_hash", "lineage_hash", "folded_text_hash"):
        owners = {}
        for row in rows:
            owners.setdefault(row[field], set()).add(row["split"])
        assert all(len(splits) == 1 for splits in owners.values())
    audit = json.loads(files["audit.json"])
    assert audit["real_records"] == audit["human_reviewed_records"] == 0
    assert audit["research_metrics"] == "not_run"
    assert audit["real_evaluation_ready"] is False
    assert audit["eight_class_partition_complete"] is False
    assert audit["near_duplicate_candidates"] and audit["effective_groups"] == 10
    assert all("suc_khoe" in audit["per_split"][split]["missing_labels"] for split in SPLITS)
    assert "description" not in rows[0]


def test_reordering_inputs_preserves_partition_and_audit_but_locks_raw_snapshot(inputs):
    for a, b in (("r0", "r1"), ("r2", "r3")):
        inputs[2].append(dict(zip(LINK_FIELDS, (a, b, "ai_conservative_prototype", "false", "Fictional relation"))))
    first = bundle(inputs)
    reordered = tuple(list(reversed(rows)) for rows in inputs)
    second = bundle(reordered)
    assert first["split_manifest.csv"] == second["split_manifest.csv"]
    assert first["audit.json"] == second["audit.json"]
    assert json.loads(first["lock.json"])["input_sha256"] != json.loads(second["lock.json"])["input_sha256"]


@pytest.mark.parametrize("change", ["missing", "duplicate", "stale_hash", "human_status", "empty_family", "bad_transform", "author_commit", "lineage_label"])
def test_invalid_provenance_rejected_before_split(inputs, change):
    records, rows, _ = inputs
    if change == "missing":
        rows.pop()
    elif change == "duplicate":
        rows.append(rows[0].copy())
    elif change == "stale_hash":
        rows[0]["normalized_text_hash"] = "0" * 64
    elif change == "human_status":
        rows[0]["annotation_status"] = "human_reviewed"
    elif change == "empty_family":
        rows[0]["pattern_family_id"] = " "
    elif change == "bad_transform":
        rows[0]["transformation"] = "PRIVATE_DESCRIPTION"
    elif change == "author_commit":
        rows[0]["source_commit"] = "a" * 40
    else:
        records[2]["label"] = records[3]["label"] = "khac"
        rows[2]["original_phrase_id"] = rows[3]["original_phrase_id"] = rows[0]["original_phrase_id"]
    with pytest.raises(SplitError) as error:
        bundle(inputs)
    assert "PRIVATE_DESCRIPTION" not in str(error.value)


@pytest.mark.parametrize("source_row", ["0", "1", "-2", "02", "2.0", "２", "9" * 4301], ids=["zero", "header", "negative", "leading_zero", "decimal", "unicode", "long_integer"])
def test_public_source_row_must_point_to_csv_data(inputs, source_row):
    for record in inputs[0][:2]:
        record["source"] = "public_synthetic"
    for row in inputs[1][:2]:
        row.update(source_commit="a" * 40, source_row=source_row)
        if row["transformation"] == "original_vi":
            row["transformation"] = "translated_en_to_vi"
    with pytest.raises(SplitError, match="Nguồn công khai"):
        bundle(inputs)


def test_valid_public_source_metadata(inputs):
    for record in inputs[0][:2]:
        record["source"] = "public_synthetic"
    for row in inputs[1][:2]:
        row.update(source_commit="a" * 40, source_row="2")
        if row["transformation"] == "original_vi":
            row["transformation"] = "translated_en_to_vi"
    assert json.loads(bundle(inputs)["audit.json"])["records"] == 20


@pytest.mark.parametrize("change", ["bad_commit", "bad_utf8", "bad_header", "oversize"])
def test_metadata_encoding_commit_header_and_size(inputs, change):
    rows = inputs[1]
    raw = table(rows, PROVENANCE_FIELDS)
    if change == "bad_commit":
        inputs[0][0]["source"] = inputs[0][1]["source"] = "public_synthetic"
        rows[0].update(source_commit="a" * 39, source_row="2", transformation="translated_en_to_vi")
        raw = table(rows, PROVENANCE_FIELDS)
    elif change == "bad_utf8":
        raw = b"\xff"
    elif change == "bad_header":
        raw = table(rows, tuple(reversed(PROVENANCE_FIELDS)))
    else:
        raw = b"x" * 2_000_001
    with pytest.raises(SplitError):
        build_bundle(table(inputs[0], FIELDS), raw, table([], LINK_FIELDS), b"guideline")


def test_family_and_lineage_union_is_transitive_and_namespaced(inputs):
    # A--B share family; B--C share lineage. D has the same names in another source.
    for row in inputs[1][2:4]:
        row["pattern_family_id"] = "f0"
    for row in inputs[1][4:6]:
        row["original_phrase_id"] = "p1"
    for row in inputs[1][6:8]:
        row.update(source_id="other_fixture", pattern_family_id="f0", original_phrase_id="p1")
    records, provenance, links = metadata(inputs)
    groups = effective_groups(records, provenance, links)
    assert groups["r0"] == groups["r1"] == groups["r2"]
    assert groups["r3"] != groups["r0"]
    assert json.loads(bundle(inputs)["audit.json"])["effective_groups"] == 8


def test_explicit_cross_source_link_is_conservative_and_co_located(inputs):
    for row in inputs[1][2:4]:
        row["source_id"] = "other_fixture"
    inputs[2].append(dict(zip(LINK_FIELDS, ("r0", "r1", "ai_conservative_prototype", "false", "Unreviewed fictional relation"))))
    files = bundle(inputs)
    rows = {r["record_id"]: r for r in csv.DictReader(io.StringIO(files["split_manifest.csv"].decode()))}
    assert rows["r0"]["effective_group_id"] == rows["r1"]["effective_group_id"]
    assert rows["r0"]["split"] == rows["r1"]["split"]
    assert json.loads(files["audit.json"])["prototype_links"][0]["human_reviewed"] == "false"


@pytest.mark.parametrize("change", ["missing_id", "self", "duplicate", "claim_human", "status", "no_rationale"])
def test_invalid_links(inputs, change):
    row = dict(zip(LINK_FIELDS, ("r0", "r1", "ai_conservative_prototype", "false", "Fictional link")))
    if change == "missing_id":
        row["record_a"] = "missing"
    elif change == "self":
        row["record_b"] = "r0"
    elif change == "claim_human":
        row["human_reviewed"] = "true"
    elif change == "status":
        row["relation_status"] = "reviewed"
    elif change == "no_rationale":
        row["rationale"] = " "
    inputs[2].append(row)
    if change == "duplicate":
        inputs[2].append({**row, "record_a": "r1", "record_b": "r0"})
    with pytest.raises(SplitError):
        bundle(inputs)


def test_real_records_are_rejected_without_echo(inputs):
    for record in inputs[0][:2]:
        record.update(source="volunteer", is_synthetic="false")
    with pytest.raises(SplitError, match="hư cấu"):
        bundle(inputs)


def test_not_enough_effective_groups_fails(inputs):
    for row in inputs[1][:10]:
        row["pattern_family_id"] = "merged"
    with pytest.raises(SplitError, match="7 nhóm"):
        bundle(inputs)


def test_cpu_limit_fails_before_quadratic_scan():
    from spendwise.data.dataset import DatasetRecord
    from spendwise.data.splitting import near_duplicate_candidates
    records = [DatasetRecord(f"r{i}", f"câu thử {i}", "khac", f"g{i}", "author_synthetic", True) for i in range(501)]
    with pytest.raises(SplitError, match="500"):
        near_duplicate_candidates(records, {r.record_id: r.group_id for r in records})


@pytest.mark.parametrize("change", ["missing_id", "invalid_split", "empty_test", "group_leak"])
def test_partition_validator_rejects_unusable_assignment(inputs, change):
    records, provenance, links = metadata(inputs)
    groups = effective_groups(records, provenance, links)
    rows = list(csv.DictReader(io.StringIO(bundle(inputs)["split_manifest.csv"].decode())))
    assignments = {r["record_id"]: r["split"] for r in rows}
    if change == "missing_id":
        assignments.pop("r0")
    elif change == "invalid_split":
        assignments["r0"] = "holdout"
    elif change == "empty_test":
        assignments = {key: "train" if value == "test" else value for key, value in assignments.items()}
    else:
        assignments["r0_nd"] = next(split for split in SPLITS if split != assignments["r0"])
    with pytest.raises(SplitError):
        validate_partition(records, provenance, links, groups, assignments)


def test_write_verify_and_load_only_trusted_ids(tmp_path, inputs):
    expected = bundle(inputs)
    output = tmp_path / "new" / "bundle"
    assert write_bundle(output, expected) == "created"
    before = {path.name: path.read_bytes() for path in output.iterdir()}
    assert write_bundle(output, expected) == "verified_existing"
    assert verify_bundle(output, expected)["records"] == 20
    ids = load_split_ids(output, expected)
    assert set(ids) == set(SPLITS)
    assert sum(map(len, ids.values())) == len(set().union(*map(set, ids.values()))) == 20
    assert before == {path.name: path.read_bytes() for path in output.iterdir()}


@pytest.mark.parametrize("change", ["assignment", "label", "manifest_and_lock", "lock_only", "missing", "extra", "stale_input"])
def test_tampered_or_stale_bundle_is_not_used_or_overwritten(tmp_path, inputs, change):
    expected = bundle(inputs)
    output = tmp_path / "bundle"
    write_bundle(output, expected)
    if change in {"assignment", "label", "manifest_and_lock"}:
        rows = list(csv.DictReader(io.StringIO(expected["split_manifest.csv"].decode())))
        field = "label" if change == "label" else "split"
        rows[0][field] = "khac" if field == "label" else next(s for s in SPLITS if s != rows[0][field])
        modified = table(rows, MANIFEST_FIELDS)
        (output / "split_manifest.csv").write_bytes(modified)
        if change == "manifest_and_lock":
            lock = json.loads(expected["lock.json"])
            lock["files_sha256"]["split_manifest.csv"] = sha256(modified)
            (output / "lock.json").write_text(json.dumps(lock), encoding="utf-8")
    elif change == "lock_only":
        (output / "lock.json").write_bytes(b"{}")
    elif change == "missing":
        (output / "audit.json").unlink()
    elif change == "extra":
        (output / "extra.txt").write_bytes(b"extra")
    else:
        expected = bundle(tuple(list(reversed(rows)) for rows in inputs))
    before = {path.name: path.read_bytes() for path in output.iterdir()}
    for operation in (verify_bundle, write_bundle, load_split_ids):
        with pytest.raises(SplitError):
            operation(output, expected)
        assert before == {path.name: path.read_bytes() for path in output.iterdir()}


def test_failure_mid_write_leaves_no_published_lock(tmp_path, inputs, monkeypatch):
    expected = bundle(inputs)
    calls = 0
    def fail(_):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated disk failure")
    monkeypatch.setattr(os, "fsync", fail)
    with pytest.raises(OSError):
        write_bundle(tmp_path / "bundle", expected)
    assert list(tmp_path.iterdir()) == []


def test_target_created_during_staging_is_preserved(tmp_path, inputs, monkeypatch):
    import spendwise.data.splitting as splitting
    expected = bundle(inputs)
    output = tmp_path / "bundle"
    original_verify = splitting.verify_bundle
    def concurrent_create(staged, files):
        result = original_verify(staged, files)
        output.mkdir()
        (output / "existing.txt").write_bytes(b"keep")
        return result
    monkeypatch.setattr(splitting, "verify_bundle", concurrent_create)
    with pytest.raises(SplitError, match="xuất hiện"):
        write_bundle(output, expected)
    assert {p.name: p.read_bytes() for p in output.iterdir()} == {"existing.txt": b"keep"}
    assert list(tmp_path.iterdir()) == [output]


def test_expected_file_names_cannot_escape_bundle(tmp_path, inputs):
    expected = {**bundle(inputs), "../outside.txt": b"unexpected"}
    with pytest.raises(SplitError):
        write_bundle(tmp_path / "bundle", expected)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.skipif(os.name != "nt", reason="Windows junction boundary")
def test_windows_junction_root_and_parent_are_rejected(tmp_path, inputs):
    expected = bundle(inputs)
    target = tmp_path / "target"
    target.mkdir()
    alias = tmp_path / "alias"
    alias_literal = str(alias).replace("'", "''")
    target_literal = str(target).replace("'", "''")
    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                             "$ErrorActionPreference='Stop'; New-Item -ItemType Junction "
                             f"-Path '{alias_literal}' -Target '{target_literal}' | Out-Null"],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    try:
        assert alias.is_junction()
        for output in (alias, alias / "nested"):
            with pytest.raises(SplitError, match="junction"):
                write_bundle(output, expected)
            with pytest.raises(SplitError, match="junction"):
                verify_bundle(output, expected)
        assert list(target.iterdir()) == []
    finally:
        alias.rmdir()  # Remove only the junction, never its target tree.

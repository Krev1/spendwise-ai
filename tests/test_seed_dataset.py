import csv
import hashlib
import importlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from spendwise.data.dataset import audit_dataset, normalize_text

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data/seed/v0.1"


@pytest.fixture
def builder(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return importlib.import_module("build_seed_dataset")


def read_table(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_seed_reproduces_exactly_and_provenance_covers_every_record(builder):
    for name, generated in builder.build_outputs().items():
        assert (SEED / name).read_bytes() == generated
    rows = read_table(SEED / "expense_descriptions_vi.csv")
    provenance = {r["record_id"]: r for r in read_table(SEED / "provenance.csv")}
    assert set(provenance) == {r["record_id"] for r in rows}
    for row in rows:
        assert provenance[row["record_id"]]["normalized_text_hash"] == hashlib.sha256(normalize_text(row["description"]).encode()).hexdigest()
        assert provenance[row["record_id"]]["annotation_status"] == "ai_draft"
    report = audit_dataset((SEED / "expense_descriptions_vi.csv").read_bytes())
    assert report["records"] == 356
    assert report["real_records"] == 0
    assert report["missing_labels"] == []
    assert report["potential_pii_record_ids"] == []


def test_source_selection_covers_income_exclusion_and_canonical_merging():
    raw = read_table(ROOT / "data/reference/pfa_demo_transactions.csv")
    selection = read_table(SEED / "source_selection.csv")
    assert len(selection) == len(raw) == 100
    assert [int(r["source_row"]) for r in selection] == list(range(2, 102))
    counts = Counter(r["decision"] for r in selection)
    assert counts["excluded_nonexpense"] == 6
    assert counts["selected_translation"] == 19
    ids = {r["record_id"] for r in read_table(SEED / "expense_descriptions_vi.csv")}
    for source, decision in zip(raw, selection):
        assert source["Description"] == decision["original_description"]
        if decision["related_record_id"]:
            assert decision["related_record_id"] in ids


def test_tampered_reference_fails_before_any_output(builder, tmp_path):
    shutil.copytree(ROOT / "data/reference", tmp_path / "data/reference")
    path = tmp_path / "data/reference/pfa_demo_transactions.csv"
    path.write_bytes(path.read_bytes() + b"altered\n")
    with pytest.raises(ValueError, match="Hash snapshot"):
        builder.build_outputs(tmp_path)
    assert not (tmp_path / "data/seed").exists()


def test_trailing_dummy_codes_are_removed_without_stripping_product_words(builder):
    assert builder.strip_demo_codes("Aldi 0192 5820") == "Aldi"
    assert builder.strip_demo_codes("Steam Games 9598") == "Steam Games"
    assert builder.strip_demo_codes("PG&E Electric") == "PG&E Electric"


def test_validator_and_builder_cli_are_read_only_and_work_from_other_cwd(tmp_path):
    dataset = SEED / "expense_descriptions_vi.csv"
    before = dataset.read_bytes()
    result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_dataset.py"), str(dataset)], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["records"] == 356
    built = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/build_seed_dataset.py")], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8")
    assert built.returncode == 0, built.stderr
    assert json.loads(built.stdout)["status"] == "reproduced_exactly"
    assert dataset.read_bytes() == before
    assert list(tmp_path.iterdir()) == []


def test_invalid_cli_does_not_emit_success_or_private_description(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("wrong,private@example.invalid\n", encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_dataset.py"), str(path)], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "private@example.invalid" not in result.stderr
    assert "Traceback" not in result.stderr

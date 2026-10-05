"""Seed-only CLI previews, immutable writes, and truthful support reports."""

import csv
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/split_dataset.py"


def run_split(cwd, *args):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=30)


def test_seed_preview_reproducible_read_only_from_other_cwd(tmp_path):
    output = tmp_path / "missing"
    first, second = run_split(tmp_path, "--output", output), run_split(tmp_path, "--output", output)
    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = json.loads(first.stdout)
    assert report["status"] == "preview_only"
    assert report["records"] == 356 and report["real_records"] == 0
    assert report["effective_groups"] == 30
    assert len(report["near_duplicate_candidates"]) == 12
    assert [report["per_split"][split]["records"] for split in ("train", "validation", "test")] == [256, 50, 50]
    assert report["per_split"]["train"]["missing_labels"] == []
    assert report["per_split"]["validation"]["missing_labels"] == ["an_uong", "di_chuyen", "suc_khoe"]
    assert report["per_split"]["test"]["missing_labels"] == ["an_uong", "di_chuyen", "khac"]
    assert report["real_evaluation_ready"] is False and report["research_metrics"] == "not_run"
    assert list(tmp_path.iterdir()) == []


def test_cli_write_then_verify_and_reject_tampering(tmp_path):
    output = tmp_path / "bundle"
    created = run_split(tmp_path, "--output", output, "--write")
    assert created.returncode == 0 and created.stderr == ""
    assert json.loads(created.stdout)["status"] == "created"
    before = {path.name: path.read_bytes() for path in output.iterdir()}
    verified = run_split(tmp_path, "--output", output)
    assert verified.returncode == 0
    assert json.loads(verified.stdout)["status"] == "verified_existing"
    rows = list(csv.DictReader(io.StringIO(before["split_manifest.csv"].decode())))
    assert len(rows) == 356
    for field in ("group_id", "effective_group_id", "family_hash", "lineage_hash", "folded_text_hash"):
        owners = {}
        for row in rows:
            owners.setdefault(row[field], set()).add(row["split"])
        assert all(len(value) == 1 for value in owners.values())
    assert before == {path.name: path.read_bytes() for path in output.iterdir()}
    private_marker = b"PRIVATE_DESCRIPTION_NOT_TO_ECHO"
    (output / "lock.json").write_bytes(private_marker)
    for args in ((), ("--write",)):
        rejected = run_split(tmp_path, "--output", output, *args)
        assert rejected.returncode == 1 and rejected.stdout == ""
        assert "Lỗi split:" in rejected.stderr and private_marker.decode() not in rejected.stderr
        assert (output / "lock.json").read_bytes() == private_marker


def test_cli_has_no_private_dataset_override(tmp_path):
    result = run_split(tmp_path, "--dataset", tmp_path / "private.csv")
    assert result.returncode == 2 and result.stdout == ""
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("text", ["## 3. Kế hoạch", "## 2. Bộ nhãn\nDraft"])
def test_seed_guideline_needs_both_section_markers(tmp_path, monkeypatch, text):
    import importlib.util
    from spendwise.data.splitting import SplitError
    spec = importlib.util.spec_from_file_location("split_cli", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/05_data_and_ml.md").write_text(text, encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", tmp_path)
    with pytest.raises(SplitError, match="guideline"):
        module.seed_bundle()

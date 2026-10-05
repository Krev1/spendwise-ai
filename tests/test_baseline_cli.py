"""Demo invocation stays reproducible and never reports research metrics."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "demo_baselines.py"
FIXTURE = ROOT / "examples" / "baseline_demo.json"


def run_demo(cwd, *args):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=30)


def test_demo_reproducible_read_only_from_another_cwd(tmp_path):
    before = FIXTURE.read_bytes()
    first, second = run_demo(tmp_path), run_demo(tmp_path)
    assert first.returncode == second.returncode == 0
    assert first.stderr == second.stderr == ""
    assert first.stdout == second.stdout
    report = json.loads(first.stdout)
    assert report["is_synthetic"] is True
    assert report["fixture_sha256"] == hashlib.sha256(before).hexdigest()
    assert report["split_status"] == "not_created"
    assert report["research_evaluation"] == "not_run"
    assert report["fit_label_counts"]["an_uong"] == 3
    assert {row["dummy"]["predicted_category"] for row in report["predictions"]} == {"an_uong"}
    for row in report["predictions"]:
        assert row["keyword"]["score"] is None
        assert row["dummy"]["score"] is None
        assert row["keyword"]["requires_confirmation"] is True
    assert not any(word in first.stdout for word in ("macro_f1", "accuracy", "coverage", "metrics_test"))
    assert FIXTURE.read_bytes() == before
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("change", ["real", "bad_label", "bad_probe", "surrogate", "metadata", "bad_schema"])
def test_invalid_fixture_fails_without_partial_report_or_private_text(tmp_path, change):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    private_text = "PRIVATE_FINANCIAL_DESCRIPTION_SHOULD_NOT_BE_ECHOED"
    if change == "real":
        fixture["is_synthetic"] = False
        fixture["source"] = "volunteer"
    elif change == "bad_label":
        fixture["fit_examples"][0]["label"] = private_text
    elif change == "bad_probe":
        fixture["probes"] = [private_text * 10]
    elif change == "surrogate":
        fixture["probes"] = [private_text + "\ud800"]
    elif change == "metadata":
        fixture["fit_examples"][0]["record_id"] = private_text
    else:
        fixture = [private_text]
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(fixture, ensure_ascii=True), encoding="utf-8")
    result = run_demo(tmp_path, "--fixture", path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Lỗi baseline:" in result.stderr
    assert private_text not in result.stderr
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize("payload", [b"not json", b"\xff", b"x" * 100_001], ids=["bad_json", "bad_utf8", "too_large"])
def test_bad_encoding_structure_or_oversized_fixture(tmp_path, payload):
    path = tmp_path / "invalid.json"
    path.write_bytes(payload)
    result = run_demo(tmp_path, "--fixture", path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Lỗi baseline:" in result.stderr


def test_missing_file_has_no_traceback_or_success_output(tmp_path):
    result = run_demo(tmp_path, "--fixture", tmp_path / "missing.json")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "không đọc được fixture" in result.stderr
    assert "Traceback" not in result.stderr

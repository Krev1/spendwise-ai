"""Kiểm chứng lệnh người học chạy, bao gồm khi cwd nằm ngoài dự án."""

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/preview_transactions.py"
SAMPLE = ROOT / "examples/transactions_sample.csv"


def run_preview(path, *arguments, cwd=None):
    return subprocess.run([sys.executable, "-B", str(CLI), str(path), *arguments],
                          capture_output=True, encoding="utf-8", cwd=cwd, check=False)


def test_preview_cli_runs_from_another_directory(tmp_path):
    result = run_preview(SAMPLE, "--month", "2026-10", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert (data["rows"], data["income_vnd"], data["expense_vnd"], data["net_vnd"]) == (
        9, 5000000, 2593000, 2407000,
    )
    assert result.stderr == ""
    assert list(tmp_path.iterdir()) == []


def test_missing_input_is_a_readable_failure(tmp_path):
    result = run_preview(tmp_path / "missing.csv")
    assert result.returncode == 1
    assert "Lỗi:" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("problem", ["money", "month"])
def test_invalid_input_cannot_emit_a_successful_report(tmp_path, problem):
    source = SAMPLE
    arguments = ["--month", "2026-13"]
    if problem == "money":
        source = tmp_path / "invalid.csv"
        source.write_text(
            "transaction_id,date,transaction_type,amount_vnd,description,category\n"
            "id_1,2026-10-05,expense,12.5,Cơm,an_uong\n", encoding="utf-8",
        )
        arguments = []
    result = run_preview(source, *arguments)
    assert result.returncode == 1
    expected_field = "amount_vnd" if problem == "money" else "month"
    assert expected_field in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""

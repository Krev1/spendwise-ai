"""Read-only synthetic prototype; no split, research metrics or model files."""

import argparse
import hashlib
import json
import platform
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import sklearn
from spendwise.domain.transactions import CATEGORIES
from spendwise.ml.baselines import KeywordBaseline, MostFrequentBaseline, normalize_description

MAX_FIXTURE_BYTES = 100_000


def read_fixture(path: Path) -> tuple[dict, str]:
    with path.open("rb") as stream:
        raw = stream.read(MAX_FIXTURE_BYTES + 1)
    if len(raw) > MAX_FIXTURE_BYTES:
        raise ValueError("Fixture vượt 100.000 byte.")
    try:
        fixture = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError, ValueError):
        raise ValueError("Fixture cần JSON UTF-8 hợp lệ.") from None
    fields = {"schema_version", "source", "is_synthetic", "purpose", "fit_examples", "probes"}
    if not isinstance(fixture, dict) or set(fixture) != fields:
        raise ValueError("Fixture cần đúng schema baseline-demo-v1.")
    if (fixture["schema_version"] != "baseline-demo-v1" or fixture["source"] != "author_synthetic" or
            fixture["is_synthetic"] is not True or fixture["purpose"] != "technical_smoke_only"):
        raise ValueError("CLI chỉ nhận fixture hư cấu technical_smoke_only.")
    fit_examples, probes = fixture["fit_examples"], fixture["probes"]
    if (not isinstance(fit_examples, list) or not 1 <= len(fit_examples) <= 100 or
            not isinstance(probes, list) or not 1 <= len(probes) <= 100):
        raise ValueError("Fixture cần 1–100 fit_examples và 1–100 probes.")
    for row in fit_examples:
        if not isinstance(row, dict) or set(row) != {"description", "label"}:
            raise ValueError("Ví dụ fit chỉ có description và label.")
        normalize_description(row["description"])
        if not isinstance(row["label"], str) or row["label"] not in CATEGORIES:
            raise ValueError("Nhãn fixture ngoài bộ tám danh mục.")
    for probe in probes:
        normalize_description(probe)
    return fixture, hashlib.sha256(raw).hexdigest()


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Demo baseline từ fixture hư cấu; không đo điểm ML.")
    parser.add_argument("--fixture", type=Path, default=ROOT / "examples" / "baseline_demo.json")
    args = parser.parse_args()
    try:
        fixture, fixture_hash = read_fixture(args.fixture)
        examples, probes = fixture["fit_examples"], fixture["probes"]
        descriptions = [row["description"] for row in examples]
        labels = [row["label"] for row in examples]
        dummy = MostFrequentBaseline().fit(descriptions, labels)
        rules = KeywordBaseline()
        predictions = []
        for probe, dummy_label in zip(probes, dummy.predict(probes), strict=True):
            keyword_prediction = rules.explain(probe)
            predictions.append({
                "description": probe,
                "keyword": {**asdict(keyword_prediction), "needs_review": keyword_prediction.needs_review},
                "dummy": {"predicted_category": dummy_label, "score": None, "requires_confirmation": True},
            })
    except OSError:
        print("Lỗi baseline: không đọc được fixture.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Lỗi baseline: {error}", file=sys.stderr)
        return 1
    report = {
        "purpose": "technical_smoke_only", "source": fixture["source"], "is_synthetic": True,
        "fixture_sha256": fixture_hash, "rule_version": rules.version, "rule_sha256": rules.sha256,
        "python": platform.python_version(), "scikit_learn": sklearn.__version__,
        "dummy_strategy": "most_frequent", "seed": dummy.seed,
        "fit_example_count": len(examples), "fit_label_counts": dict(sorted(Counter(labels).items())),
        "dummy_classes": dummy.classes_, "probe_count": len(probes),
        "split_status": "not_created", "research_evaluation": "not_run",
        "limits": "Hư cấu, nhãn AI dự thảo; chưa đo chất lượng người thật, chưa calibration hoặc tích hợp app.",
        "predictions": predictions,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

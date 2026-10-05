"""Software contracts, not an evaluation of financial-text accuracy."""

import unicodedata

import pytest
from sklearn.exceptions import NotFittedError

from spendwise.ml.baselines import KeywordBaseline, KeywordRule, MostFrequentBaseline


@pytest.mark.parametrize("description,category,status", [
    ("mua nước giặt", "mua_sam", "matched"),
    ("tiền nước tháng này", "nha_o_hoa_don", "matched"),
    ("kem dưỡng da mua ở nhà thuốc", "mua_sam", "matched"),
    ("mua thuốc lá", "khac", "matched"),
    ("laptop để học", "hoc_tap", "matched"),
    ("GrabFood cơm trưa", "an_uong", "matched"),
    ("Grab đi làm", "di_chuyen", "matched"),
    ("Grab", "khac", "no_match"),
    ("học phí và cơm trưa", "khac", "conflict"),
    ("cơm trưa và vé phim", "khac", "conflict"),
    ("phí gửi bưu kiện và khám răng", "khac", "conflict"),
    ("endgame", "khac", "no_match"),
    ("game_abc", "khac", "no_match"),
    ("game\u0338xyz", "khac", "no_match"),
    ("cơm\u0338xyz", "khac", "no_match"),
    ("abc\u0338game", "khac", "no_match"),
    ("đặt lịch họp nhóm", "khac", "no_match"),
    ("com trua", "an_uong", "matched"),
    ("pho", "khac", "no_match"),  # No implicit accent stripping.
])
def test_keyword_context_conflict_and_boundaries(description, category, status):
    result = KeywordBaseline().explain(description)
    assert (result.predicted_category, result.status) == (category, status)
    assert result.score is None
    assert result.requires_confirmation is True
    assert result.needs_review == (status != "matched")


def test_normalization_evidence_and_repeated_calls_are_stable():
    baseline = KeywordBaseline()
    expected = baseline.explain("cà phê sáng")
    variant = unicodedata.normalize("NFD", "  CÀ\tPHÊ   sáng  ")
    assert baseline.explain(variant) == expected
    assert baseline.predict([variant, "xét nghiệm"]) == ["an_uong", "suc_khoe"]
    hit = expected.matches[0]
    assert "cà phê sáng"[hit.start:hit.end] == "cà phê"
    assert baseline.predict([]) == []


def test_matching_does_not_join_phrases_across_punctuation():
    result = KeywordBaseline().explain("cà, phê")
    assert result.status == "no_match"


def test_conflicting_equal_spans_and_partial_overlaps_remain_visible():
    baseline = KeywordBaseline((
        KeywordRule("an_uong", ("cơm trưa", "trà xanh")),
        KeywordRule("giai_tri", ("cơm trưa", "xanh cuối tuần")),
    ))
    assert baseline.explain("cơm trưa").status == "conflict"
    assert baseline.explain("trà xanh cuối tuần").status == "conflict"


def test_rule_hash_changes_when_vocabulary_order_or_version_changes():
    rules = (KeywordRule("an_uong", ("cơm",)), KeywordRule("giai_tri", ("game",)))
    first = KeywordBaseline(rules)
    assert first.sha256 == KeywordBaseline(rules).sha256
    assert first.sha256 != KeywordBaseline(tuple(reversed(rules))).sha256
    assert first.sha256 != KeywordBaseline(rules, version="keywords-v0.2").sha256


@pytest.mark.parametrize("invalid", ["", "   ", "?!123", "a" * 301, None, {"description": "cơm"}, "game\ud800xyz"])
def test_invalid_descriptions_rejected_without_echo(invalid):
    with pytest.raises(ValueError):
        KeywordBaseline().explain(invalid)


def test_dummy_uses_fit_majority_even_when_probes_point_to_other_classes():
    model = MostFrequentBaseline().fit(
        ["cơm trưa", "vé phim", "khám răng"], ["suc_khoe", "suc_khoe", "an_uong"]
    )
    assert model.predict(["cơm", "vé phim", "nước giặt"]) == ["suc_khoe"] * 3
    assert model.classes_ == ("an_uong", "suc_khoe")
    assert model.predict(["học phí"]) == ["suc_khoe"]
    assert model.predict([]) == []


def test_dummy_tie_follows_locked_sklearn_class_order():
    model = MostFrequentBaseline().fit(["vé phim", "cơm"], ["giai_tri", "an_uong"])
    assert model.classes_ == ("an_uong", "giai_tri")
    assert model.predict(["chuyển khoản"]) == ["an_uong"]


def test_dummy_predict_before_fit_is_an_explicit_error():
    with pytest.raises(NotFittedError):
        MostFrequentBaseline().predict(["cơm"])


@pytest.mark.parametrize("descriptions,labels", [
    ([], []), (["cơm"], []), (["cơm"], ["income"]),
    (["cơm", ""], ["an_uong", "an_uong"]),
    ([{"description": "cơm", "record_id": "id"}], ["an_uong"]),
    ("cơm", ["an_uong"]), (["cơm"], "an_uong"), (["cơm"], [None]),
])
def test_invalid_fit_cannot_replace_a_previous_fit(descriptions, labels):
    model = MostFrequentBaseline().fit(["khám răng"], ["suc_khoe"])
    with pytest.raises(ValueError):
        model.fit(descriptions, labels)
    assert model.predict(["cơm"]) == ["suc_khoe"]


def test_predict_rejects_a_single_string_or_metadata_batch():
    models = [KeywordBaseline(), MostFrequentBaseline().fit(["cơm"], ["an_uong"])]
    for model in models:
        with pytest.raises(ValueError):
            model.predict("cơm")
        with pytest.raises(ValueError):
            model.predict([{"description": "cơm", "label": "an_uong"}])

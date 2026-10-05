import csv
import io

import pytest

from spendwise.data.dataset import FIELDS, DatasetError, audit_dataset, read_dataset_bytes


def encoded(rows, fields=FIELDS):
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def row(**overrides):
    values = dict(zip(FIELDS, ["a1", "ăn trưa", "an_uong", "tpl_meal", "author_synthetic", "true"]))
    values.update(overrides)
    return [values[f] for f in FIELDS]


@pytest.mark.parametrize("overrides", [
    {"record_id": "tên"}, {"record_id": "x" * 65}, {"group_id": ""},
    {"description": "   "}, {"description": "...123"}, {"description": "a" * 301},
    {"label": "income"}, {"label": "food"}, {"source": "scraped"},
    {"is_synthetic": "True"}, {"is_synthetic": "false"},
    {"source": "volunteer", "is_synthetic": "true"},
], ids=["unicode_id", "long_id", "empty_group", "blank_description", "no_letters", "long_description", "income_label", "wrong_label", "wrong_source", "noncanonical_flag", "false_synthetic", "true_volunteer"])
def test_invalid_contract_is_rejected_without_description(overrides):
    with pytest.raises(DatasetError) as error:
        read_dataset_bytes(encoded([row(**overrides)]))
    assert "Dòng 2" in str(error.value)
    assert "ăn trưa" not in str(error.value)


def test_bom_nfc_and_allowed_sources():
    raw = encoded([row(description=" a\u0306n trưa "),
                   row(record_id="b", description="taxi", group_id="pub", source="public_synthetic"),
                   row(record_id="c", description="tiền điện", group_id="p001", source="volunteer", is_synthetic="false")])
    records = read_dataset_bytes(b"\xef\xbb\xbf" + raw)
    assert records[0].description == "ăn trưa"
    report = audit_dataset(raw)
    assert (report["real_records"], report["synthetic_records"], report["groups"]) == (1, 2, 3)
    assert report["human_annotation_review"] == "not_verified_by_validator"


@pytest.mark.parametrize("other, reason", [
    (row(description="vé xe"), "record_id"),
    (row(record_id="b", description=" ĂN   TRƯA "), "chuẩn hóa bị trùng"),
    (row(record_id="b", label="khac"), "nhãn xung đột"),
    (row(record_id="b", description="an trua", group_id="tpl_2"), "giao nhóm"),
    (row(record_id="b", description="an trua", label="khac"), "giao nhóm hoặc nhãn"),
    (row(record_id="b", description="vé xe", source="public_synthetic"), "nguồn không nhất quán"),
])
def test_duplicates_variants_and_group_consistency(other, reason):
    with pytest.raises(DatasetError, match=reason):
        read_dataset_bytes(encoded([row(), other]))


def test_diacritic_variants_in_same_group_are_distinct_but_not_independent():
    report = audit_dataset(encoded([row(), row(record_id="b", description="an trua")]))
    assert report["records"] == 2
    assert report["groups"] == 1
    assert report["normalized_unique_descriptions"] == 2
    assert report["diacritic_folded_unique_descriptions"] == 1


@pytest.mark.parametrize("raw", [
    b"\xff", b"", encoded([], FIELDS), encoded([row()], reversed(FIELDS)),
    encoded([row()[:-1]]), encoded([[]]),
    (",".join(FIELDS) + '\na,"unclosed').encode(),
    b"a" * 2_000_001,
], ids=["bad_utf8", "no_header", "header_only", "wrong_order", "missing_column", "empty_row", "bad_quote", "too_big"])
def test_encoding_header_shape_empty_quote_and_size(raw):
    with pytest.raises(DatasetError):
        read_dataset_bytes(raw)


def test_record_limit():
    rows = [row(record_id=f"r{i}", description=f"chi thử {i}") for i in range(5001)]
    assert len(read_dataset_bytes(encoded(rows[:5000]))) == 5000
    with pytest.raises(DatasetError, match="5.000"):
        read_dataset_bytes(encoded(rows))


def test_pii_flags_are_warnings_and_not_privacy_approval():
    report = audit_dataset(encoded([row(description="liên hệ demo@example.invalid")]))
    assert report["potential_pii_record_ids"] == ["a1"]
    assert report["privacy_review"] == "requires_human_review"
    assert "demo@example.invalid" not in str(report)

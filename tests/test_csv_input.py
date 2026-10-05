"""Kiểm tra file upload, giới hạn tài nguyên và định vị lỗi nhiều dòng."""

import csv
import io

import pytest

from spendwise.domain.transactions import COLUMNS, ValidationError
from spendwise.services.csv_reader import MAX_BYTES, MAX_ROWS, read_transactions, read_transactions_bytes


def csv_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(COLUMNS)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


@pytest.mark.parametrize("header", [list(reversed(COLUMNS)), [*COLUMNS[:-1], "label"]])
def test_header_order_and_names_are_required(header):
    with pytest.raises(ValidationError, match="Header"):
        read_transactions_bytes((",".join(header) + "\n").encode())


def test_invalid_utf8_is_reported():
    with pytest.raises(ValidationError, match="UTF-8"):
        read_transactions_bytes(b"\xff\xfe")


def test_unclosed_quote_is_reported_as_csv_error():
    raw = ",".join(COLUMNS) + '\nid_1,2026-10-05,expense,1,"unclosed\n'
    with pytest.raises(ValidationError, match="CSV sai cú pháp"):
        read_transactions_bytes(raw.encode())


def test_error_after_multiline_record_reports_correct_source_line():
    raw = csv_bytes([
        ["id_1", "2026-10-05", "expense", "1", "Cơm\ntrà đá", "an_uong"],
        ["id_2", "2026-02-30", "expense", "1", "Cơm", "an_uong"],
    ])
    with pytest.raises(ValidationError, match="Dòng 4: date"):
        read_transactions_bytes(raw)


def test_error_inside_multiline_record_reports_its_start():
    raw = csv_bytes([["id_1", "2026-02-30", "expense", "1", "Cơm\ntrà đá", "an_uong"]])
    with pytest.raises(ValidationError, match="Dòng 2: date"):
        read_transactions_bytes(raw)


def test_record_limit_counts_records_instead_of_physical_lines():
    rows = [[f"id_{i}", "2026-10-05", "expense", "1", "Cơm\ntrà đá", "an_uong"]
            for i in range(MAX_ROWS)]
    assert len(read_transactions_bytes(csv_bytes(rows))) == MAX_ROWS
    rows.append(["too_many", "2026-10-05", "expense", "1", "Cơm", "an_uong"])
    with pytest.raises(ValidationError, match="vượt 5000"):
        read_transactions_bytes(csv_bytes(rows))


def test_exact_byte_limit_can_be_valid_input():
    rows = [[f"id_{i}", "2026-10-05", "expense", "1", "Sample", "an_uong"]
            for i in range(MAX_ROWS)]
    padding, remainder = divmod(MAX_BYTES - len(csv_bytes(rows)), MAX_ROWS)
    for index, row in enumerate(rows):
        row[4] = " " * (padding + (remainder if index == 0 else 0)) + row[4]
    raw = csv_bytes(rows)
    assert len(raw) == MAX_BYTES
    assert len(read_transactions_bytes(raw)) == MAX_ROWS
    with pytest.raises(ValidationError, match="2000000 byte"):
        read_transactions_bytes(raw + b" ")


def test_oversized_file_is_rejected(tmp_path):
    source = tmp_path / "too_big.csv"
    source.write_bytes(b"x" * (MAX_BYTES + 1))
    with pytest.raises(ValidationError, match="2000000 byte"):
        read_transactions(source)


def test_preview_does_not_change_source_file(tmp_path):
    raw = csv_bytes([["id_1", "2026-10-05", "expense", "1", "Cơm", ""]])
    source = tmp_path / "sample.csv"
    source.write_bytes(raw)
    assert read_transactions(source)[0].category == ""
    assert source.read_bytes() == raw
    assert list(tmp_path.iterdir()) == [source]

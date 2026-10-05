"""Kiểm tra lỗi tiền/dữ liệu ảnh hưởng thật đến kết quả nhập CSV."""

import tempfile
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

from csv_contract import COLUMNS, ValidationError, parse_row, read_transactions, summarize


class CsvContractTests(unittest.TestCase):
    def row(self, **changes):
        result = dict(zip(COLUMNS, ["id_1", "2026-10-05", "expense", "45000", "Ăn trưa", "an_uong"]))
        result.update(changes)
        return result

    def read_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "sample.csv"
            target.write_text(text, encoding="utf-8-sig")
            return read_transactions(target)

    def test_reject_invalid_money(self):
        for amount in ["0", "-1", "12.5", "12,000", "1_000", "1000000000001"]:
            with self.subTest(amount=amount), self.assertRaises(ValidationError):
                parse_row(self.row(amount_vnd=amount), 2)

    def test_reject_invalid_calendar_and_date_format(self):
        for invalid_date in ["2026-02-30", "20261005", "05/10/2026"]:
            with self.subTest(date=invalid_date), self.assertRaises(ValidationError):
                parse_row(self.row(date=invalid_date), 2)

    def test_income_cannot_use_expense_category(self):
        with self.assertRaises(ValidationError):
            parse_row(self.row(transaction_type="income"), 2)

    def test_unlabeled_expense_remains_pending(self):
        result = summarize([parse_row(self.row(category=""), 2)])
        self.assertEqual(result["pending_expense_categories"], 1)
        self.assertEqual(result["expense_by_category"], {"can_xac_nhan": 45000})

    def test_reject_duplicate_id_in_batch(self):
        line = "id_1,2026-10-05,expense,45000,Ăn trưa,an_uong\n"
        with self.assertRaisesRegex(ValidationError, "trùng"):
            self.read_text(",".join(COLUMNS) + "\n" + line + line)

    def test_utf8_bom_and_quoted_description(self):
        records = self.read_text(",".join(COLUMNS) + '\nid_1,2026-10-05,expense,45000,"Cơm, trà đá",an_uong\n')
        self.assertEqual(records[0].description, "Cơm, trà đá")

    def test_reject_missing_and_extra_columns(self):
        for line in ["id_1,2026-10-05,expense,45000,Ăn trưa\n",
                     "id_1,2026-10-05,expense,45000,Ăn trưa,an_uong,extra\n"]:
            with self.subTest(line=line), self.assertRaises(ValidationError):
                self.read_text(",".join(COLUMNS) + "\n" + line)

    def test_monthly_sum_excludes_other_month_and_splits_income(self):
        rows = [parse_row(self.row(), 2),
                parse_row(self.row(transaction_id="id_2", transaction_type="income",
                                   amount_vnd="100000", category=""), 3),
                parse_row(self.row(transaction_id="id_3", date="2026-09-30"), 4)]
        result = summarize(rows, "2026-10")
        self.assertEqual((result["rows"], result["income_vnd"], result["expense_vnd"], result["net_vnd"]),
                         (2, 100000, 45000, 55000))

    def test_empty_month_has_zero_totals(self):
        result = summarize([parse_row(self.row(), 2)], "2026-11")
        self.assertEqual(result["rows"], 0)
        self.assertEqual(result["net_vnd"], 0)

    def test_invalid_month_is_rejected(self):
        with self.assertRaises(ValidationError):
            summarize([], "2026-13")

    def test_empty_batch_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.read_text(",".join(COLUMNS) + "\n")

    def test_cli_prints_vietnamese_and_correct_sample_totals(self):
        examples = Path(__file__).resolve().parent
        result = subprocess.run(
            [sys.executable, "-B", str(examples / "csv_contract.py"),
             str(examples / "transactions_sample.csv"), "--month", "2026-10"],
            capture_output=True, encoding="utf-8", check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"expense_vnd": 2593000', result.stdout)
        self.assertIn("Chỉ preview", result.stdout)

    def test_blank_line_is_rejected(self):
        with self.assertRaisesRegex(ValidationError, "dòng trống"):
            self.read_text(",".join(COLUMNS) + "\n\nid_1,2026-10-05,expense,45000,Ăn trưa,an_uong\n")

    def test_description_normalized_to_nfc(self):
        description = unicodedata.normalize("NFD", "Ăn trưa")
        record = parse_row(self.row(description=description), 2)
        self.assertEqual(record.description, "Ăn trưa")


if __name__ == "__main__":
    unittest.main()

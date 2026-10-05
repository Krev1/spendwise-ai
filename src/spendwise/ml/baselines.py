"""Versioned keyword rules and a train-only most-frequent comparison baseline."""

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

from sklearn.dummy import DummyClassifier
from sklearn.utils.validation import check_is_fitted

from spendwise.data.dataset import normalize_text
from spendwise.domain.transactions import CATEGORIES


RULE_VERSION = "keywords-v0.1"
RULE_POLICY = "letter_number_mark_underscore_boundary; longest_containing_hit; independent_conflict_to_khac"


@dataclass(frozen=True)
class KeywordRule:
    category: str
    keywords: tuple[str, ...]


# Domain-guideline rules, frozen before research split/test. Unaccented aliases
# are explicit vocabulary entries; the input itself keeps Vietnamese accents.
DEFAULT_RULES = (
    KeywordRule("an_uong", ("cơm", "phở", "cà phê", "thực phẩm", "đồ ăn", "nước", "grabfood", "com trua", "ca phe")),
    KeywordRule("di_chuyen", ("vé xe", "xe buýt", "xăng", "gửi xe", "grab đi làm", "ve xe", "do xang")),
    KeywordRule("nha_o_hoa_don", ("tiền phòng", "tiền trọ", "tiền thuê phòng", "tiền điện", "tiền nước", "internet", "cước điện thoại", "tien phong")),
    KeywordRule("hoc_tap", ("học phí", "giáo trình", "sách luyện thi", "khóa học", "laptop để học", "hoc phi", "giao trinh")),
    KeywordRule("mua_sam", ("áo", "quần", "tai nghe", "laptop", "nước giặt", "kem dưỡng da mua ở nhà thuốc", "kem dưỡng da", "sữa rửa mặt", "ao thun")),
    KeywordRule("giai_tri", ("vé phim", "xem phim", "game", "truyện", "nghe nhạc", "ve phim")),
    KeywordRule("suc_khoe", ("thuốc", "khám", "xét nghiệm", "nha khoa", "thuoc", "kham benh")),
    KeywordRule("khac", ("quà mừng cưới", "quà biếu", "phí gửi bưu kiện", "thuốc lá")),
)


def normalize_description(description: str) -> str:
    """Validate before collapsing spaces; errors never echo private text."""
    if not isinstance(description, str):
        raise ValueError("Mô tả baseline phải là chuỗi văn bản.")
    if any(unicodedata.category(character) == "Cs" for character in description):
        raise ValueError("Mô tả baseline chứa mã Unicode không hợp lệ.")
    canonical = unicodedata.normalize("NFC", description).strip()
    if not 1 <= len(canonical) <= 300 or not any(c.isalpha() for c in canonical):
        raise ValueError("Mô tả baseline cần có chữ và dài 1–300 ký tự.")
    return normalize_text(canonical)


def _descriptions(values: Sequence[str]) -> list[str]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ValueError("Cần danh sách mô tả, không phải một chuỗi hoặc metadata.")
    return [normalize_description(value) for value in values]


def _is_token_character(character: str) -> bool:
    # Some combining marks remain after NFC. Python regex \w excludes them,
    # so relying only on \b would allow substring matches inside those tokens.
    return character.isalnum() or character == "_" or unicodedata.category(character).startswith("M")


@dataclass(frozen=True)
class KeywordHit:
    category: str
    keyword: str
    start: int
    end: int


@dataclass(frozen=True)
class RulePrediction:
    predicted_category: str
    status: str
    matches: tuple[KeywordHit, ...]
    rule_version: str
    rule_sha256: str
    score: None = None
    requires_confirmation: bool = True

    @property
    def needs_review(self) -> bool:
        """Conflict/no-match need extra review; matched still needs confirmation."""
        return self.status != "matched"


class KeywordBaseline:
    """Full-label predictions for future comparison, with inspectable rule hits."""

    def __init__(self, rules: tuple[KeywordRule, ...] = DEFAULT_RULES, version: str = RULE_VERSION):
        self.version = version
        self._patterns = []
        serialized = []
        for rule in rules:
            if rule.category not in CATEGORIES or not rule.keywords:
                raise ValueError("Rule cần danh mục hợp lệ và ít nhất một keyword.")
            keywords = tuple(normalize_description(word) for word in rule.keywords)
            serialized.append({"category": rule.category, "keywords": keywords})
            for keyword in keywords:
                pattern = re.compile(re.escape(keyword))
                self._patterns.append((rule.category, keyword, pattern))
        payload = {"version": version, "policy": RULE_POLICY, "rules": serialized}
        self.sha256 = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    def explain(self, description: str) -> RulePrediction:
        text = normalize_description(description)
        hits = []
        for index, (category, keyword, pattern) in enumerate(self._patterns):
            for match in pattern.finditer(text):
                if (match.start() and _is_token_character(text[match.start() - 1])) or (
                    match.end() < len(text) and _is_token_character(text[match.end()])
                ):
                    continue
                hits.append((index, KeywordHit(category, keyword, match.start(), match.end())))
        hits.sort(key=lambda item: (-len(item[1].keyword.split()), -len(item[1].keyword), item[0], item[1].start))
        kept = []
        for _, hit in hits:
            # Equal spans from conflicting rules remain visible as conflicts.
            if any(other.start <= hit.start and hit.end <= other.end and
                   other.end - other.start > hit.end - hit.start for other in kept):
                continue
            kept.append(hit)
        categories = {hit.category for hit in kept}
        if len(categories) == 1:
            category, status = next(iter(categories)), "matched"
        elif categories:
            category, status = "khac", "conflict"
        else:
            category, status = "khac", "no_match"
        return RulePrediction(category, status, tuple(kept), self.version, self.sha256)

    def predict(self, descriptions: Sequence[str]) -> list[str]:
        return [self.explain(text).predicted_category for text in _descriptions(descriptions)]


class MostFrequentBaseline:
    """Caller supplies train descriptions/labels; probes never change the fit.

    TASK-07 only uses a synthetic fixture. TASK-10 must select these arguments
    from the locked TASK-08 manifest, rather than passing an entire dataset.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self._model = DummyClassifier(strategy="most_frequent", random_state=seed)

    def fit(self, train_descriptions: Sequence[str], train_labels: Sequence[str]) -> "MostFrequentBaseline":
        descriptions = _descriptions(train_descriptions)
        if isinstance(train_labels, (str, bytes)) or not isinstance(train_labels, Sequence):
            raise ValueError("Cần danh sách nhãn train.")
        labels = list(train_labels)
        if not descriptions or len(descriptions) != len(labels):
            raise ValueError("Train cần mô tả/nhãn không rỗng và cùng số lượng.")
        if any(not isinstance(label, str) or label not in CATEGORIES for label in labels):
            raise ValueError("Nhãn train phải thuộc bộ tám danh mục.")
        model = DummyClassifier(strategy="most_frequent", random_state=self.seed)
        model.fit([[text] for text in descriptions], labels)
        self._model = model
        return self

    @property
    def classes_(self) -> tuple[str, ...]:
        check_is_fitted(self._model)
        return tuple(str(label) for label in self._model.classes_)

    def predict(self, descriptions: Sequence[str]) -> list[str]:
        check_is_fitted(self._model)
        texts = _descriptions(descriptions)
        if not texts:
            return []
        return self._model.predict([[text] for text in texts]).tolist()

import pytest


@pytest.fixture
def transaction_fields():
    return {
        "transaction_id": "sample_1", "date": "2026-10-05",
        "transaction_type": "expense", "amount_vnd": "45000",
        "description": "Ăn trưa", "category": "an_uong",
    }

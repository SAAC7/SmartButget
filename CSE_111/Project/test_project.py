import os
import tempfile
import pytest 
from datetime import datetime
from project import (
    record_transaction, generate_summary, filter_transaction,
    save_dictionary, read_dictionary, CATEGORIES_EXPENSE
)


def test_record_transaction_income_and_expense():
    income = record_transaction("2025-08-12T12:00:00", True, "Growth", "Salary", 1500.0)
    assert income["Type"] == "Income"
    assert income["Category"] == "Growth"
    assert income["Amount"] == pytest.approx(1500,abs=0.1)

    expense = record_transaction("2025-08-13T12:00:00", False, "Essential", "Rent", 800.0)
    assert expense["Type"] == "Expense"
    assert expense["Description"] == "Rent"
    assert expense["Amount"]==pytest.approx(800,abs=0.1)


def test_filter_transactio_by_month_and_day():
    entries = [
        record_transaction("2025-08-01T08:00:00", True, "Growth", "Salary", 2000),
        record_transaction("2025-08-02T08:00:00", False, "Essential", "Food", 100),
        record_transaction("2025-07-15T08:00:00", False, "Reward", "Movie", 50)
    ]

    august_entries = filter_transaction(entries, year=2025, month=8)
    assert len(august_entries) == 2

    day_entries = filter_transaction(entries, year=2025, month=8, day=2)
    assert len(day_entries) == 1
    assert day_entries[0]["Description"] == "Food"


def test_generar_resumen_with_data():
    entries = [
        record_transaction("2025-08-01T10:00:00", True, "Growth", "Salary", 2000.0),
        record_transaction("2025-08-02T15:00:00", False, "Essential", "Rent", 800.0),
        record_transaction("2025-08-03T18:00:00", False, "Reward", "Cinema", 50.0)
    ]

    resumen = generate_summary(entries, 2025, 8)
    assert resumen["Total Income"] == 2000.0
    assert resumen["Essential"] == 800.0
    assert resumen["Reward"] == 50.0
    assert resumen[f"Alloc_Growth"] == 2000.0 * CATEGORIES_EXPENSE["Growth"]["Rate"]


def test_generar_resumen_no_income():
    entries = [
        record_transaction("2025-08-05T10:00:00", False, "Essential", "Groceries", 300.0)
    ]
    resumen = generate_summary(entries, 2025, 8)
    assert resumen["Total Income"] == 0
    assert resumen["Total Expenses"] == 300.0
    assert resumen["Essential"] == 300.0

    assert all(resumen[f"Alloc_{cat}"] == 0 for cat in CATEGORIES_EXPENSE)


def test_save_and_read_dictionary():
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        temp_filename = os.path.realpath(tmpfile.name)
        os.remove(temp_filename) 
    try:
        entry = record_transaction("2025-08-12T12:00:00", True, "Growth", "Salary", 1500.0)
        save_dictionary(entry, filename=temp_filename)

        data = read_dictionary(filename=temp_filename)
        assert len(data) == 1
        assert data[0]["Amount"] == 1500.0
        assert data[0]["Category"] == "Growth"
    finally:
        os.remove(temp_filename)

pytest.main(["-v", "--tb=long", "-rN", __file__]) 
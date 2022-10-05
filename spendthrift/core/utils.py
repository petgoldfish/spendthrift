"""
Core Utils for processing statement data.
"""
import csv
import io
from collections import defaultdict
from datetime import datetime
from typing import DefaultDict, List, Tuple

from .transaction import Category, Transaction, TransactionType


def parse_statement_file(file: io.TextIOWrapper) -> List[Transaction]:
    """Parses a statement CSV file and returns a list of Transactions."""
    return [
        Transaction(
            amount=float(row["Amount"]),
            category=Category[
                row["Category"].upper().replace("&", "AND").replace(" ", "_")
                or Category.UNCATEGORIZED.value.upper()
            ],
            description=row["Description"],
            memo=row["Memo"],
            post_date=datetime.strptime(row["Post Date"], "%m/%d/%Y"),
            transaction_date=datetime.strptime(row["Transaction Date"], "%m/%d/%Y"),
            transaction_type=TransactionType[row["Type"].upper()],
        )
        for row in csv.DictReader(file)
    ]


def filter_payments(data: List[Transaction]) -> List[Transaction]:
    """
    Filter out card payment entries from raw data.

    :param data: raw list of objects from the statement file
    :returns: filtered list of objects
    """
    return [
        item for item in data if not item.transaction_type == TransactionType.PAYMENT
    ]


def group_data_by_category(
    data: List[Transaction],
) -> DefaultDict[Category, List[Transaction]]:
    """
    Group data by category.

    :param data: list of objects
    :returns: dict of objects grouped into lists by categories
    """
    by_category: DefaultDict[Category, List[Transaction]] = defaultdict(list)

    # Category
    for item in data:
        by_category[item.category].append(item)

    return by_category


def group_data_by_month(data: List[Transaction]) -> DefaultDict[str, List[Transaction]]:
    """
    Group data by month.

    :param data: list of objects
    :returns: dict of objects grouped into lists by month
    """
    by_month: DefaultDict[str, List[Transaction]] = defaultdict(list)

    # Date
    for item in data:
        month = item.post_date.strftime("%b %y")
        by_month[month].append(item)

    return by_month


def calculate_categorical_spend(
    by_category: DefaultDict[Category, List[Transaction]]
) -> List[Tuple[str, float, int]]:
    """
    Calculate a categorical spend report.

    :param by_category: dict of objects grouped by categories
    :returns: list of tuples, with each tuple being (category_name,
    categorical_sum, categorical_count)
    """
    categorical_spend = [
        (
            category.value or "Uncategorized",
            sum(item.amount for item in by_category[category]),
            len(by_category[category]),
        )
        for category in by_category
    ]
    categorical_spend.sort(key=lambda x: x[1])
    return categorical_spend


def calculate_monthly_spend(
    by_month: DefaultDict[str, List[Transaction]]
) -> List[Tuple[str, float, int]]:
    """
    Calculate a monthly spend report.

    :param by_month: dict of objects grouped by month
    :returns: list of tuples, with each tuple being (month, monthly_sum, monthly_count)
    """
    return [
        (
            month,
            sum(item.amount for item in by_month[month]),
            len(by_month[month]),
        )
        for month in by_month
    ]


def calculate_monthly_categorical_spend(
    by_month: DefaultDict[str, List[Transaction]]
) -> List[Tuple[str, List[Tuple[str, float, int]]]]:
    """
    Calculate a monthly spend report organized by category.

    :param by_month: dict of objects grouped by month
    :returns: list of tuples, with each tuple being (month, categorical_spend_for_month)
    """
    return [
        (month, calculate_categorical_spend(group_data_by_category(by_month[month])))
        for month in by_month
    ]

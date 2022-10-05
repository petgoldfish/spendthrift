"""
Core Utils for processing statement data.
"""
from collections import defaultdict
from datetime import datetime


def filter_payments(data):
    """
    Filter out card payment entries from raw data.

    :param data: raw list of objects from the statement file
    :returns: filtered list of objects
    """
    return [item for item in data if not item["Type"] == "Payment"]


def group_data_by_category(data):
    """
    Group data by category.

    :param data: list of objects
    :returns: dict of objects grouped into lists by categories
    """
    by_category = defaultdict(list)

    # Category
    for item in data:
        if item["Category"] == "":
            item["Category"] = "Uncategorized"

        by_category[item["Category"]].append(item)

    return by_category


def group_data_by_month(data):
    """
    Group data by month.

    :param data: list of objects
    :returns: dict of objects grouped into lists by month
    """
    by_month = defaultdict(list)

    # Date
    for item in data:
        post_date = datetime.strptime(item["Post Date"], "%m/%d/%Y")
        month = post_date.strftime("%b %y")
        by_month[month].append(item)

    return by_month


def calculate_categorical_spend(by_category):
    """
    Calculate a categorical spend report.

    :param by_category: dict of objects grouped by categories
    :returns: list of tuples, with each tuple being (category_name,
    categorical_sum, categorical_count)
    """
    categorical_spend = [
        (
            category,
            sum(float(item["Amount"]) for item in by_category[category]),
            len(by_category[category]),
        )
        for category in by_category
    ]
    categorical_spend.sort(key=lambda x: x[1])
    return categorical_spend


def calculate_monthly_spend(by_month):
    """
    Calculate a monthly spend report.

    :param by_month: dict of objects grouped by month
    :returns: list of tuples, with each tuple being (month, monthly_sum, monthly_count)
    """
    return [
        (
            month,
            sum(float(item["Amount"]) for item in by_month[month]),
            len(by_month[month]),
        )
        for month in by_month
    ]


def calculate_monthly_categorical_spend(by_month):
    """
    Calculate a monthly spend report organized by category.

    :param by_month: dict of objects grouped by month
    :returns: list of tuples, with each tuple being (month, categorical_spend_for_month)
    """
    return [
        (month, calculate_categorical_spend(group_data_by_category(by_month[month])))
        for month in by_month
    ]

"""
CLI Tool that parses Chase statements and produces monthly or categorical spend reports
Author: Raghav Sai
"""

import csv
from collections import defaultdict
from datetime import datetime
from enum import Enum

import click
from tabulate import tabulate


class Kind(Enum):
    """Type of report"""

    CATEGORICAL = "categorical"
    MONTHLY = "monthly"
    MONTHLY_CATRGORICAL = "monthly_categorical"


def process_data(data):
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


def generate_report(kind: str, data):
    """
    Generate a printable report of the specified kind

    :param kind: the kind of report to generate
    :returns: a printable report of the specified kind
    """
    match kind:
        case Kind.CATEGORICAL.value:
            by_category = group_data_by_category(data)
            categorical_spend = calculate_categorical_spend(by_category)
            return tabulate(
                categorical_spend,
                headers=["Category", "Amount", "Count"],
                tablefmt="fancy_grid",
            )
        case Kind.MONTHLY.value:
            by_month = group_data_by_month(data)
            monthly_spend = calculate_monthly_spend(by_month)
            return tabulate(
                monthly_spend,
                headers=["Month", "Amount", "Count"],
                tablefmt="fancy_grid",
            )
        case Kind.MONTHLY_CATRGORICAL.value:
            by_month = group_data_by_month(data)
            monthly_categorical_spend = calculate_monthly_categorical_spend(by_month)
            return "\n\n".join(
                item[0]
                + "\n"
                + tabulate(
                    item[1],
                    headers=["Category", "Amount", "Count"],
                    tablefmt="fancy_grid",
                )
                for item in monthly_categorical_spend
            )


@click.command()
@click.argument("statement_file", type=click.File("r"))
@click.option(
    "-k",
    "--kind",
    type=click.Choice([kind.value for kind in Kind]),
    default=Kind.CATEGORICAL.value,
    show_default=True,
    help="the kind of report to generate",
)
def cli(statement_file, kind):
    """Parses STATEMENT_FILE and produces the specidfied kind of spend report"""
    raw_data = [dict(row) for row in csv.DictReader(statement_file)]

    processed_data = process_data(raw_data)

    report = generate_report(kind, processed_data)
    click.echo_via_pager(report)

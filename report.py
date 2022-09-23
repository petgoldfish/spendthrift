"""
CLI Tool that parses Chase statements and produces monthly or categorical spend reports
Author: Raghav Sai
"""

import csv
from collections import defaultdict
from datetime import datetime

import click
from tabulate import tabulate


def process_data(data):
    return [item for item in data if not item["Type"] == "Payment"]


def group_data_by_category(data):
    by_category = defaultdict(list)

    # Category
    for item in data:
        if item["Category"] == "":
            item["Category"] = "Uncategorized"

        by_category[item["Category"]].append(item)

    return by_category


def group_data_by_month(data):
    by_month = defaultdict(list)

    # Date
    for item in data:
        post_date = datetime.strptime(item["Post Date"], "%m/%d/%Y")
        month = post_date.strftime("%b %y")
        by_month[month].append(item)

    return by_month


def calculate_categorical_spend(by_category):
    # Categorical spend
    categorical_spend = [
        [
            category,
            sum(float(item["Amount"]) for item in by_category[category]),
            len(by_category[category]),
        ]
        for category in by_category
    ]
    categorical_spend.sort(key=lambda x: x[1])
    return categorical_spend


def calculate_monthly_spend(by_month):
    # Monthly spend
    return [
        [
            month,
            sum(float(item["Amount"]) for item in by_month[month]),
            len(by_month[month]),
        ]
        for month in by_month
    ]


def create_report(kind: str, data):
    if kind == "categorical":
        by_category = group_data_by_category(data)
        categorical_spend = calculate_categorical_spend(by_category)
        return tabulate(
            categorical_spend,
            headers=["Category", "Amount", "Count"],
            tablefmt="fancy_grid",
        )
    if kind == "monthly":
        by_month = group_data_by_month(data)
        monthly_spend = calculate_monthly_spend(by_month)
        return tabulate(
            monthly_spend,
            headers=["Month", "Amount", "Count"],
            tablefmt="fancy_grid",
        )


@click.command()
@click.argument("statement_file", type=click.File("r"))
@click.option("--kind", default="categorical", help="the kind of report to generate")
def cli(statement_file, kind):
    raw_data = [dict(row) for row in csv.DictReader(statement_file)]

    processed_data = process_data(raw_data)

    report = create_report(kind, processed_data)
    print(report)

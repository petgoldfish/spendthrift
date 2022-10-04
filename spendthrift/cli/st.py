"""
CLI Tool that parses Chase statements and produces monthly or categorical spend reports
Author: Raghav Sai
"""

import csv

import click
from tabulate import tabulate

from spendthrift.cli.kind import Kind

from ..core.utils import (
    calculate_categorical_spend,
    calculate_monthly_categorical_spend,
    calculate_monthly_spend,
    group_data_by_category,
    group_data_by_month,
    filter_payments,
)


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

    processed_data = filter_payments(raw_data)

    report = generate_report(kind, processed_data)
    click.echo_via_pager(report)

"""
This module holds the Kind enum, which is used to categorize the kind of
reports the CLI can generate.
"""
from enum import Enum


class Kind(Enum):
    """Type of report"""

    CATEGORICAL = "categorical"
    MONTHLY = "monthly"
    MONTHLY_CATRGORICAL = "monthly_categorical"

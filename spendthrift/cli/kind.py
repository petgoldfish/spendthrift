from enum import Enum


class Kind(Enum):
    """Type of report"""

    CATEGORICAL = "categorical"
    MONTHLY = "monthly"
    MONTHLY_CATRGORICAL = "monthly_categorical"

"""Contains necessary typings"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Category(Enum):
    """The category of the transaction"""

    BILLS_AND_UTILITIES = "Bills & Utilities"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    FEES_AND_ADJUSTMENTS = "Fees & Adjustments"
    FOOD_AND_DRINK = "Food & Drink"
    GAS = "Gas"
    GIFTS_AND_DONATIONS = "Gifts & Donations"
    GROCERIES = "Groceries"
    HEALTH_AND_WELLNESS = "Health & Wellness"
    HOME = "Home"
    PROFESSIONAL_SERVICES = "Professional Services"
    SHOPPING = "Shopping"
    TRAVEL = "Travel"
    UNCATEGORIZED = "Uncategorized"


class TransactionType(Enum):
    """The type of transaction"""

    ADJUSTMENT = "Adjustment"
    FEE = "Fee"
    PAYMENT = "Payment"
    REFUND = "Refund"
    RETURN = "Return"
    SALE = "Sale"


@dataclass
class Transaction:
    """Transaction data fields"""

    transaction_date: datetime
    post_date: datetime
    description: str
    category: Category
    transaction_type: TransactionType
    amount: float
    memo: str

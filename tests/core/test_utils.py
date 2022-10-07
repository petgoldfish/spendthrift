"""Test all the util functions."""
from datetime import datetime
from typing import List

import pytest

from spendthrift.core.transaction import Category, Transaction, TransactionType
from spendthrift.core.utils import filter_payments


class TestUtils:
    """Test all utils."""

    @pytest.fixture
    def dummy_transactions(self) -> List[Transaction]:
        """List of fake transactions to test with."""
        return [
            Transaction(
                amount=-24.99,
                category=Category.ENTERTAINMENT,
                description="Movie",
                memo="",
                post_date=datetime(2022, 10, 8),
                transaction_date=datetime(2022, 10, 7),
                transaction_type=TransactionType.SALE,
            ),
            Transaction(
                amount=50,
                category=Category.UNCATEGORIZED,
                description="Payment Thank You-Mobile",
                memo="",
                post_date=datetime(2022, 10, 10),
                transaction_date=datetime(2022, 10, 10),
                transaction_type=TransactionType.PAYMENT,
            ),
        ]

    def test_filter_payments(self, dummy_data):
        """Test payments are filtered from transactions"""
        filtered_transactions = filter_payments(dummy_data)
        assert all(
            transaction.transaction_type != TransactionType.PAYMENT
            for transaction in filtered_transactions
        )

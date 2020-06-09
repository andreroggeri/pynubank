import pytest


@pytest.fixture
def account_balance_return():
    return {'data': {'viewer': {'savingsAccount': {'currentSavingsBalance': {'netAmount': 127.33}}}}}

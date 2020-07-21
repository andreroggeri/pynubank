import pytest


@pytest.fixture()
def create_money_request_return():
    return {
        "data": {
            "createMoneyRequest": {
                "moneyRequest": {
                    "amount": 550.0,
                    "message": None,
                    "url": "https://some.tld/path1/path2",
                    "id": "123123123123"
                }
            }
        }
    }

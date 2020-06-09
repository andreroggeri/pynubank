import pytest


@pytest.fixture
def bills_return():
    return {
        "_links": {
            "future": {
                "href": "https://prod-s0-billing.nubank.com.br/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/future"
            },
            "open": {
                "href": "https://prod-s0-billing.nubank.com.br/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/open"
            }
        },
        "bills": [
            {
                "state": "future",
                "summary": {
                    "adjustments": "0",
                    "close_date": "2018-05-03",
                    "due_date": "2018-05-10",
                    "effective_due_date": "2018-05-10",
                    "expenses": "126.94",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 0,
                    "open_date": "2018-04-03",
                    "paid": 0,
                    "past_balance": 0,
                    "payments": "0",
                    "precise_minimum_payment": "0",
                    "precise_total_balance": "126.94",
                    "previous_bill_balance": "0",
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 12694,
                    "total_credits": "0",
                    "total_cumulative": 12694,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "126.94",
                    "total_payments": "0"
                }
            },
            {
                "_links": {
                    "self": {
                        "href": "https://prod-s0-billing.nubank.com.br/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/open"
                    }
                },
                "state": "open",
                "summary": {
                    "adjustments": "0",
                    "close_date": "2018-04-03",
                    "due_date": "2018-04-10",
                    "effective_due_date": "2018-04-10",
                    "expenses": "303.36",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 0,
                    "open_date": "2018-03-03",
                    "paid": 0,
                    "past_balance": 0,
                    "payments": "-285.15",
                    "precise_minimum_payment": "0",
                    "precise_total_balance": "303.362041645013",
                    "previous_bill_balance": "285.152041645013",
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 30336,
                    "total_credits": "0",
                    "total_cumulative": 30336,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "303.36",
                    "total_payments": "-285.15"
                }
            },
            {
                "_links": {
                    "self": {
                        "href": "https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
                    }
                },
                "href": "nuapp://bill/abcde-fghi-jklmn-opqrst-uvxz",
                "id": "abcde-fghi-jklmn-opqrst-uvxz",
                "state": "overdue",
                "summary": {
                    "adjustments": "-63.99106066",
                    "close_date": "2018-03-03",
                    "due_date": "2018-03-10",
                    "effective_due_date": "2018-03-12",
                    "expenses": "364.14",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 8003,
                    "open_date": "2018-02-03",
                    "paid": 28515,
                    "past_balance": -1500,
                    "payments": "-960.47",
                    "precise_minimum_payment": "480.02544320601300",
                    "precise_total_balance": "285.152041645013",
                    "previous_bill_balance": "945.473102305013",
                    "remaining_minimum_payment": 0,
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 28515,
                    "total_credits": "-64.18",
                    "total_cumulative": 30015,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "364.32893934",
                    "total_payments": "-960.47"
                }
            },
        ]
    }

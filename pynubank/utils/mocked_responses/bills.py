bills_summary = {
    "_links": {
        "future": {
            "href": "https://mocked-proxy-url/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/future"
        },
        "open": {
            "href": "https://mocked-proxy-url/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/open"
        }
    },
    "bills": [
        {
            "_links": {
                "self": {
                    "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-2512"
                }
            },
            "state": "future",
            "summary": {
                "adjustments": "0",
                "close_date": "2016-05-03",
                "due_date": "2016-05-10",
                "effective_due_date": "2016-05-10",
                "expenses": "176.94",
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
                    "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-abcd"
                }
            },
            "state": "open",
            "summary": {
                "adjustments": "0",
                "close_date": "2017-04-03",
                "due_date": "2017-04-10",
                "effective_due_date": "2017-04-10",
                "expenses": "393.36",
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
                "total_balance": 306,
                "total_credits": "0",
                "total_cumulative": 30336,
                "total_financed": "0",
                "total_international": "0",
                "total_national": "303.36",
                "total_payments": "-285.15"
            }
        }, {
            "_links": {
                "self": {
                    "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
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
        }
    ]
}

bills = {
    'bill': {
        '_links': {
            'barcode': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'},
            'boleto_email': {
                'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'},
            'invoice_email': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/'
                                      'invoice/email'},
            'self': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst'
                             ''}
        },
        'account_id': 'abcde-fghi-jklmn-opqrst-uvxz',
        'auto_debit_failed': False,
        'barcode': '',
        'id': 'abcde-fghi-jklmn-opqrst-uvxz',
        'line_items': [{
            'amount': 2390,
            'category': 'Eletrônicos',
            'charges': 1,
            'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'index': 0,
            'post_date': '2015-09-09',
            'title': 'Mercadopago Mlivre'
        }, {
            'amount': 5490,
            'category': 'Eletrônicos',
            'charges': 1,
            'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'index': 0,
            'post_date': '2015-09-09',
            'title': 'Mercadopago Mlivre'
        }],
        'linha_digitavel': '',
        'payment_method': 'boleto',
        'state': 'overdue',
        'status': 'paid',
        'summary': {
            'adjustments': '0',
            'close_date': '2015-09-25',
            'due_date': '2015-10-10',
            'effective_due_date': '2015-10-13',
            'expenses': '78.8000',
            'fees': '0',
            'interest': 0,
            'interest_charge': '0',
            'interest_rate': '0.0775',
            'interest_reversal': '0',
            'international_tax': '0',
            'late_fee': '0.02',
            'late_interest_rate': '0.0875',
            'minimum_payment': 7005,
            'open_date': '2015-07-23',
            'paid': 7880,
            'past_balance': 0,
            'payments': '0',
            'precise_minimum_payment': '70.054500',
            'precise_total_balance': '78.8000',
            'previous_bill_balance': '0',
            'tax': '0',
            'total_accrued': '0',
            'total_balance': 7880,
            'total_credits': '0',
            'total_cumulative': 7880,
            'total_financed': '0',
            'total_international': '0',
            'total_national': '78.8000',
            'total_payments': '0'
        }
    }
}

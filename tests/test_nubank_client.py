import json
import pytest

from unittest.mock import MagicMock

from requests import Response

from pynubank.nubank import Nubank, NuException


@pytest.fixture
def authentication_return():
    return {
        "access_token": "access_token_123",
        "token_type": "bearer",
        "_links": {
            "change_password": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/change_password_123"
            },
            "enabled_features": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/enabled_features_123"
            },
            "revoke_token": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/revoke_token_123"
            },
            "userinfo": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/userinfo_123"
            },
            "events_page": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_page_123"
            },
            "events": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123"
            },
            "postcode": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/post_code_123"
            },
            "app_flows": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/app_flows_123"
            },
            "revoke_all": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/revoke_all_123"
            },
            "customer": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/customer_123"
            },
            "account": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/account_123"
            },
            "bills_summary": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/bills_summary_123"
            },
            "savings_account": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/savings_account_123"
            },
            "purchases": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/purchases_123"
            },
            "ghostflame": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/ghostflame_123"
            },
            "user_change_password": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/user_change_password_123"
            }
        },
        "refresh_token": "refresh_token_123",
        "refresh_before": "2017-09-16T12:41:13Z"
    }


@pytest.fixture
def events_return():
    return {
        "events": [
            {
                "description": "Shopping Iguatemi",
                "category": "transaction",
                "amount": 700,
                "time": "2017-09-09T02:03:55Z",
                "title": "transporte",
                "details": {
                    "lat": -12.9818258,
                    "lon": -38.4652058,
                    "subcategory": "card_present"
                },
                "id": "abcde-fghi-jklmn-opqrst-uvxz",
                "_links": {
                    "self": {
                        "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123"
                    }
                },
                "href": "nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz"
            }
        ],
        "as_of": "2017-09-09T06:50:22.323Z",
        "customer_id": "abcde-fghi-jklmn-opqrst-uvxz",
        "_links": {
            "updates": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/updates_123"
            },
            "next": {
                "href": "https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/next_123"
            }
        }
    }

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

@pytest.fixture
def bill_details_return():
    return {
        'bill': {
            '_links': {
                'barcode': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'
                },
                'boleto_email': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'
                },
                'invoice_email': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/invoice/email'
                },
                'self': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'
                }
            },
            'account_id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'auto_debit_failed': False,
            'barcode': '',
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'line_items': [
                {
                    'amount': 2390,
                    'category': 'Eletrônicos',
                    'charges': 1,
                    'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                    'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                    'index': 0,
                    'post_date': '2015-09-09',
                    'title': 'Mercadopago Mlivre'
                },
                {
                    'amount': 5490,
                    'category': 'Eletrônicos',
                    'charges': 1,
                    'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                    'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                    'index': 0,
                    'post_date': '2015-09-09',
                    'title': 'Mercadopago Mlivre'
                }
            ],
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

@pytest.fixture
def account_balance_return():
    return {'data': {'viewer': {'savingsAccount': {'currentSavingsBalance': {'netAmount': 127.33}}}}}


@pytest.fixture
def account_statements_return():
    return {'data': {'viewer': {'savingsAccount': {'feed': [
		{
            'id': 'abcde-fghi-jklmn-opqrst-uvxw',
		    '__typename': 'BillPaymentEvent',
		    'title': 'Pagamento da fatura',
		    'detail': 'Cartão Nubank - R$ 50,00',
		    'postDate': '2018-03-07'
        },
    	{
		    'id': 'abcde-fghi-jklmn-opqrst-uvxy',
		    '__typename': 'TransferOutReversalEvent',
		    'title': 'Transferência devolvida',
		    'detail': 'Juquinha da Silva Sauro - R$ 20,00',
		    'postDate': '2018-03-06'
	    },
        {
            'id': 'abcde-fghi-jklmn-opqrst-uvxz', 
            '__typename': 'TransferOutEvent',
            'title': 'Transferência enviada', 
            'detail': 'Juquinha da Silva Sauro - R$ 20,00',
            'postDate': '2018-03-06',
            'amount': 20.0, 
            'destinationAccount': {
                'name': 'Juquinha da Silva Sauro'
            }
        },
        {
            'id': 'abcde-fghi-jklmn-opqrst-uvx1', 
            '__typename': 'TransferInEvent',
            'title': 'Transferência recebida', 
            'detail': 'R$127.33', 
            'postDate': '2018-03-06', 
            'amount': 127.33
        },
        {
            'id': 'abcde-fghi-jklmn-opqrst-uvx2',
            '__typename': 'WelcomeEvent',
            'title': 'Bem vindo à sua conta!',
            'detail': 'Waldisney Santos\nBanco 260 - Nu Pagamentos S.A.\nAgência 0001\nConta 000000-1',
            'postDate': '2017-12-18'
         }
    ]}}}}


def create_fake_response(dict_response, status_code=200):
    response = Response()
    response.status_code = status_code
    response._content = bytes(json.dumps(dict_response).encode('utf-8'))
    return response


@pytest.mark.parametrize("http_status", [
    100, 101, 102, 103,
    201, 202, 203, 204, 205, 206, 207, 208, 226,
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423,
    424, 426, 428, 429, 431, 440, 444, 449, 450, 451, 495, 496, 497, 498, 499,
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
])
def test_authentication_failure_raise_exception(monkeypatch, http_status):
    response = Response()
    response.status_code = http_status


    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    with pytest.raises(NuException):
        Nubank('12345678909', '12345678')


def test_authentication_succeeds(monkeypatch, authentication_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    assert nubank_client.feed_url == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123'
    assert nubank_client.headers['Authorization'] == 'Bearer access_token_123'


def test_get_card_feed(monkeypatch, authentication_return, events_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(events_return)
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))

    feed = nubank_client.get_card_feed()
    assert feed['as_of'] == '2017-09-09T06:50:22.323Z'
    assert feed['customer_id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert feed['_links']['updates']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/updates_123'
    assert feed['_links']['next']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/next_123'

    events = feed['events']
    assert len(events) == 1
    assert events[0]['description'] == 'Shopping Iguatemi'
    assert events[0]['category'] == 'transaction'
    assert events[0]['amount'] == 700
    assert events[0]['time'] == '2017-09-09T02:03:55Z'
    assert events[0]['title'] == 'transporte'
    assert events[0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert events[0]['details']['lat'] == -12.9818258
    assert events[0]['details']['lon'] == -38.4652058
    assert events[0]['details']['subcategory'] == 'card_present'
    assert events[0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert events[0]['_links']['self']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'

def test_get_bills(monkeypatch, authentication_return, bills_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(bills_return)
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))

    bills = nubank_client.get_bills()

    assert len(bills) == 3
    assert bills[2]['_links']['self']['href'] == "https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
    assert bills[2]['href'] == 'nuapp://bill/abcde-fghi-jklmn-opqrst-uvxz'
    assert bills[2]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bills[2]['state'] == 'overdue'

    summary = bills[2]['summary']
    assert summary["adjustments"] == "-63.99106066"
    assert summary["close_date"] == "2018-03-03"
    assert summary["due_date"] == "2018-03-10"
    assert summary["effective_due_date"] == "2018-03-12"
    assert summary["expenses"] == "364.14"
    assert summary["fees"] == "0"
    assert summary["interest"] == 0
    assert summary["interest_charge"] == "0"
    assert summary["interest_rate"] == "0.1375"
    assert summary["interest_reversal"] == "0"
    assert summary["international_tax"] == "0"
    assert summary["minimum_payment"] == 8003
    assert summary["open_date"] == "2018-02-03"
    assert summary["paid"] == 28515
    assert summary["past_balance"] == -1500
    assert summary["payments"] == "-960.47"
    assert summary["precise_minimum_payment"] == "480.02544320601300"
    assert summary["precise_total_balance"] == "285.152041645013"
    assert summary["previous_bill_balance"] == "945.473102305013"
    assert summary["remaining_minimum_payment"] == 0
    assert summary["tax"] == "0"
    assert summary["total_accrued"] == "0"
    assert summary["total_balance"] == 28515
    assert summary["total_credits"] == "-64.18"
    assert summary["total_cumulative"] == 30015
    assert summary["total_financed"] == "0"
    assert summary["total_international"] == "0"
    assert summary["total_national"] == "364.32893934"
    assert summary["total_payments"] == "-960.47"

def test_get_bill_details(monkeypatch, authentication_return, bill_details_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(bill_details_return)
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))

    bill_mock = {'_links':{'self':{'href':'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'}}}
    bill_response = nubank_client.get_bill_details(bill_mock)

    bill = bill_response['bill']

    assert bill['_links']['barcode']['href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'
    assert bill['_links']['boleto_email']['href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'
    assert bill['_links']['invoice_email']['href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/invoice/email'
    assert bill['_links']['self']['href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['account_id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['auto_debit_failed'] == False
    assert bill['barcode'] == ''
    assert bill['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['amount'] == 2390
    assert bill['line_items'][0]['category'] == 'Eletrônicos'
    assert bill['line_items'][0]['charges'] == 1
    assert bill['line_items'][0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['index'] == 0
    assert bill['line_items'][0]['post_date'] == '2015-09-09'
    assert bill['line_items'][0]['title'] == 'Mercadopago Mlivre'
    assert bill['linha_digitavel'] == ''
    assert bill['payment_method'] == 'boleto'
    assert bill['state'] == 'overdue'
    assert bill['status'] == 'paid'
    assert bill['summary']['adjustments'] == '0'
    assert bill['summary']['close_date'] == '2015-09-25'
    assert bill['summary']['due_date'] == '2015-10-10'
    assert bill['summary']['effective_due_date'] == '2015-10-13'
    assert bill['summary']['expenses'] == '78.8000'
    assert bill['summary']['fees'] == '0'
    assert bill['summary']['interest'] == 0
    assert bill['summary']['interest_charge'] == '0'
    assert bill['summary']['interest_rate'] == '0.0775'
    assert bill['summary']['interest_reversal'] == '0'
    assert bill['summary']['international_tax'] == '0'
    assert bill['summary']['late_fee'] == '0.02'
    assert bill['summary']['late_interest_rate'] == '0.0875'
    assert bill['summary']['minimum_payment'] == 7005
    assert bill['summary']['open_date'] == '2015-07-23'
    assert bill['summary']['paid'] == 7880
    assert bill['summary']['past_balance'] == 0
    assert bill['summary']['payments'] == '0'
    assert bill['summary']['precise_minimum_payment'] == '70.054500'
    assert bill['summary']['precise_total_balance'] == '78.8000'
    assert bill['summary']['previous_bill_balance'] == '0'
    assert bill['summary']['tax'] == '0'
    assert bill['summary']['total_accrued'] == '0'
    assert bill['summary']['total_balance'] == 7880
    assert bill['summary']['total_credits'] == '0'
    assert bill['summary']['total_cumulative'] == 7880
    assert bill['summary']['total_financed'] == '0'
    assert bill['summary']['total_international'] == '0'
    assert bill['summary']['total_national'] == '78.8000'
    assert bill['summary']['total_payments'] == '0'

def test_get_card_statements(monkeypatch, authentication_return, events_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(events_return)
    monkeypatch.setattr('requests.get', MagicMock(return_value=response))
    statements = nubank_client.get_card_statements()

    assert len(statements) == 1
    assert statements[0]['description'] == 'Shopping Iguatemi'
    assert statements[0]['category'] == 'transaction'
    assert statements[0]['amount'] == 700
    assert statements[0]['time'] == '2017-09-09T02:03:55Z'
    assert statements[0]['title'] == 'transporte'
    assert statements[0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[0]['details']['lat'] == -12.9818258
    assert statements[0]['details']['lon'] == -38.4652058
    assert statements[0]['details']['subcategory'] == 'card_present'
    assert statements[0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[0]['_links']['self']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'


def test_get_account_balance(monkeypatch, authentication_return, account_balance_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(account_balance_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    balance = nubank_client.get_account_balance()

    assert balance == 127.33


def test_get_account_feed(monkeypatch, authentication_return, account_statements_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(account_statements_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    statements = nubank_client.get_account_feed()

    assert len(statements) == 5
    assert statements[1]['id'] == 'abcde-fghi-jklmn-opqrst-uvxy'
    assert statements[1]['__typename'] == 'TransferOutReversalEvent'
    assert statements[1]['title'] == 'Transferência devolvida'
    assert statements[1]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[1]['postDate'] == '2018-03-06'
    
    assert statements[2]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[2]['__typename'] == 'TransferOutEvent'
    assert statements[2]['title'] == 'Transferência enviada'
    assert statements[2]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[2]['postDate'] == '2018-03-06'
    assert statements[2]['amount'] == 20.0
    assert statements[2]['destinationAccount']['name'] == 'Juquinha da Silva Sauro'


def test_get_account_statements(monkeypatch, authentication_return, account_statements_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(account_statements_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    statements = nubank_client.get_account_statements()

    assert len(statements) == 2
    assert statements[1]['id'] == 'abcde-fghi-jklmn-opqrst-uvx1'
    assert statements[1]['__typename'] == 'TransferInEvent'
    assert statements[1]['title'] == 'Transferência recebida'
    assert statements[1]['detail'] == 'R$127.33'
    assert statements[1]['postDate'] == '2018-03-06'
    assert statements[1]['amount'] == 127.33


@pytest.mark.parametrize("http_status", [
    100, 101, 102, 103,
    201, 202, 203, 204, 205, 206, 207, 208, 226,
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422,
    423,
    424, 426, 428, 429, 431, 440, 444, 449, 450, 451, 495, 496, 497, 498, 499,
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
])
def test_grapql_query_raises_exeption(monkeypatch, authentication_return, http_status):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = Response()
    response.status_code = http_status


    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    with pytest.raises(NuException):
        nubank_client.get_account_balance()

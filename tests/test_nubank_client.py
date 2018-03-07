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
def account_balance_return():
    return {'data': {'viewer': {'savingsAccount': {'currentSavingsBalance': {'netAmount': 127.33}}}}}


@pytest.fixture
def account_statements_return():
    return {'data': {'viewer': {'savingsAccount': {'feed': [
        {
            'id': 'abcde-fghi-jklmn-opqrst-uvxz', '__typename': 'TransferOutEvent',
            'title': 'Transferência enviada', 'detail': 'Juquinha da Silva Sauro - R$ 20,00',
            'postDate': '2018-03-06',
            'amount': 20.0, 'destinationAccount': {'name': 'Juquinha da Silva Sauro'}
        },
        {
            'id': 'abcde-fghi-jklmn-opqrst-uvx1', '__typename': 'TransferInEvent',
            'title': 'Transferência recebida', 'detail': 'R$127.33', 'postDate': '2018-03-06', 'amount': 127.33
        },
        {'id': 'abcde-fghi-jklmn-opqrst-uvx2', '__typename': 'WelcomeEvent',
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

    assert len(statements) == 3


def test_get_account_statements(monkeypatch, authentication_return, account_statements_return):
    response = create_fake_response(authentication_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    nubank_client = Nubank('12345678909', '12345678')

    response = create_fake_response(account_statements_return)
    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    statements = nubank_client.get_account_statements()

    assert len(statements) == 2


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

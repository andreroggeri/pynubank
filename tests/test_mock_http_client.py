import sys
import inspect
import pytest
from pynubank.nubank import Nubank
from pynubank.exception import NuException
from pynubank import MockHttpClient


@pytest.fixture(scope="module")
def nubank_client():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')
    return client


def test_nubank_authentication(nubank_client):
    assert nubank_client.feed_url
    assert nubank_client.client.get_header('Authorization')


def test_authenticate_with_qr_code():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')


def test_authenticate_with_cert():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_cert('12345678912', 'hunter12', 'certpath')


def test_authenticate_with_refresh_token():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_refresh_token('refreshtoken', 'certpath')


def test_get_card_statements(nubank_client):
    assert nubank_client.get_card_statements()


def test_get_card_feed(nubank_client):
    assert nubank_client.get_card_feed()


def test_get_bills(nubank_client):
    assert nubank_client.get_bills()


def test_get_bill_details(nubank_client):
    assert nubank_client.get_bill_details(nubank_client.get_bills()[1])


def test_get_account_feed(nubank_client):
    assert nubank_client.get_account_feed()


def test_get_account_statements(nubank_client):
    assert nubank_client.get_account_statements()


def test_get_account_balance(nubank_client):
    assert nubank_client.get_account_balance()


def test_get_account_investments_details(nubank_client):
    assert nubank_client.get_account_investments_details()


def test_create_boleto(nubank_client):
    assert nubank_client.create_boleto(123)


def test_create_money_request(nubank_client):
    assert nubank_client.create_money_request(456)


def test_get_qr_code(nubank_client):
    assert nubank_client.get_qr_code()


def test_get_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.get('invalid.url')


def test_post_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.post('invalid.url', {})


def test_check_not_tested_new_methods(nubank_client):
    tested_functions = []

    function_list = [(name, obj) for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(obj)]
    for name, function in function_list:
        if 'test_' in name:
            tested_functions.append(name.replace('test_', ''))

    methods = dir(nubank_client)
    for method_name in methods:
        if method_name[0] != '_':
            if callable(getattr(nubank_client, method_name)):
                assert method_name in tested_functions, 'Method not tested in MockHttpClient %s' % method_name

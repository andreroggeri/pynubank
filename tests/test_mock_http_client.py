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


def test_get_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.get('invalid.url')


def test_post_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.post('invalid.url', {})

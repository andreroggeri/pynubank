import inspect
from datetime import datetime
from uuid import uuid4

import pytest

from pynubank import MockHttpClient
from pynubank.exception import NuException
from pynubank.nubank import Nubank


@pytest.fixture(scope="module")
def nubank_client():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')
    return client


def test_get_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.get('invalid.url')


def test_post_invalid_url_should_throw_exception():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.post('invalid.url', {})


def test_check_not_tested_new_methods(nubank_client):
    default_params = {
        'get_bill_details': {
            'bill': {'_links': {'self': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz'}}}
        },
        'get_account_investments_yield': {
            'date': datetime.now(),
        },
        'get_card_statement_details': {
            'statement': {'_links': {'self': {'href': f'https://mocked-proxy-url/api/transactions/{uuid4()}'}}},
        },
        'authenticate_with_cert': {
            'cpf': '12345678912',
            'password': 'hunter12',
            'cert_data': b'cert_data',
        },
        'authenticate_with_refresh_token': {
            'refresh_token': 'refresh_token',
            'cert_data': b'cert_data',
        }
    }

    methods = dir(nubank_client)
    for method_name in methods:
        method = getattr(nubank_client, method_name)
        if method_name[0] != '_' and callable(method):

            args = list(range(get_method_arg_count(method) - 1))

            params = default_params.get(method_name)
            if params is None:
                params = inspect.signature(method).parameters

            for index, name in enumerate(params):
                args[index] = params[name].annotation() if type(params[name]) == inspect.Parameter else params[name]
            try:
                method(*args)
            except Exception as ex:
                print(f'{method_name} is missing a mock !!')
                raise ex


def get_method_arg_count(method):
    try:
        return method.__wrapped__.__code__.co_argcount
    except AttributeError:
        return method.__code__.co_argcount

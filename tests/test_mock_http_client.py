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
        }
    }

    methods = dir(nubank_client)
    for method_name in methods:
        method = getattr(nubank_client, method_name)
        if method_name[0] != '_' and callable(method):
            args = list(range(method.__code__.co_argcount - 1))

            params = default_params.get(method_name)
            if params is None:
                params = inspect.signature(method).parameters

            for index, name in enumerate(params):
                args[index] = params[name].annotation() if type(params[name]) == inspect.Parameter else params[name]

            method(*args)

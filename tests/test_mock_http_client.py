import inspect
import pytest
from pynubank.nubank import Nubank
from pynubank import MockHttpClient


@pytest.fixture(scope="module")
def nubank_client():
    client = Nubank(client=MockHttpClient())
    client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')
    return client


def test_check_not_tested_new_methods(nubank_client):
    methods = dir(nubank_client)
    for method_name in methods:
        method = getattr(nubank_client, method_name)
        if method_name[0] != '_' and callable(method):
            args = list(range(method.__code__.co_argcount - 1))
            params = inspect.signature(method).parameters
            for index, name in enumerate(params):
                args[index] = params[name].annotation()
            method(*args)

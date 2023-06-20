import json
from unittest.mock import MagicMock

import pytest
from requests import Response

from pynubank import NuException, MockHttpClient
from pynubank.utils.certificate_generator import CertificateGenerator
from pynubank.utils.discovery import Discovery

headers = {
    'WWW-Authenticate': 'device-authorization encrypted-code="abc123", sent-to="john@doe"'
}


def fake_update_proxy(self: Discovery):
    self.proxy_list_app_url = {
        'gen_certificate': 'https://some-url/gen-cert',
    }


def mock_response(content=None, return_headers=None, status_code=200):
    response = Response()
    response.status_code = status_code
    response.headers = return_headers
    if content:
        response._content = json.dumps(content).encode()

    return response


def test_request_code_fails_when_status_code_is_different_from_401(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response()))

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    with pytest.raises(NuException) as ex:
        email = generator.request_code()

        assert ex is not None
        assert email is None


def test_request_code_fails_when_there_is_no_authenticate_header(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response(None, {}, 401)))

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    with pytest.raises(NuException) as ex:
        email = generator.request_code()

        assert ex is not None
        assert email is None


def test_request_code(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response(None, headers, 401)))

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    email = generator.request_code()

    assert email == 'john@doe'
    assert generator.encrypted_code == 'abc123'


def test_exchange_certs_fails_when_called_without_request_code(monkeypatch):
    http = MockHttpClient()

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    with pytest.raises(NuException) as ex:
        cert1, cert2 = generator.exchange_certs('1234')

        assert cert1 is None
        assert cert2 is None
        assert ex is not None


def test_exchange_cert_fails_when_status_code_is_different_from_200(monkeypatch):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response(None, headers, 401)))

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    generator.request_code()

    with pytest.raises(NuException) as ex:
        cert1, cert2 = generator.exchange_certs('1234')

        assert cert1 is None
        assert cert2 is None
        assert ex is not None


def test_exchange_certs(monkeypatch, gen_certificate_return):
    http = MockHttpClient()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response(None, headers, 401)))

    generator = CertificateGenerator('123456789', 'hunter12', '1234', http_client=http)

    generator.request_code()
    monkeypatch.setattr(http, 'raw_post', MagicMock(return_value=mock_response(gen_certificate_return, headers, 200)))
    cert1, cert2 = generator.exchange_certs('1234')

    assert cert1 is not None
    assert cert2 is not None

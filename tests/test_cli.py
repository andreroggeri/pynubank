import os
from pathlib import Path
from unittest.mock import patch

import OpenSSL

import pynubank
from pynubank import NuException
from pynubank.utils.certificate_generator import CertificateGenerator
from pynubank.utils.http import HttpClient


def mock_error(_):
    raise NuException('failed')


def mock_certs(*args):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)

    return p12, p12


def clean():
    workdir = Path(os.getcwd())

    cert = workdir.joinpath('cert.p12')

    if cert.exists():
        cert.unlink()


@patch.object(pynubank.utils.certificate_generator.CertificateGenerator, 'request_code', mock_error)
@patch('builtins.input', lambda *args: '12341234')
@patch('getpass.getpass', lambda *args: '12341234')
def test_request_code_exception_should_stop_execution(monkeypatch, proxy_return):
    from pynubank import cli
    monkeypatch.setattr(HttpClient, 'get', lambda *args: proxy_return)

    clean()
    cli.main()

    workdir = Path(os.getcwd())

    cert = workdir.joinpath('cert.p12')

    assert cert.exists() is False
    clean()


@patch.object(pynubank.utils.certificate_generator.CertificateGenerator, 'exchange_certs', mock_certs)
@patch.object(pynubank.utils.certificate_generator.CertificateGenerator, 'request_code', lambda x: 'email@tld')
@patch('builtins.input', lambda *args: '12341234')
@patch('getpass.getpass', lambda *args: '12341234')
def test_should_generate_certs(monkeypatch, proxy_return):
    from pynubank import cli
    monkeypatch.setattr(HttpClient, 'get', lambda *args: proxy_return)

    clean()
    cli.main()

    workdir = Path(os.getcwd())

    cert = workdir.joinpath('cert.p12')

    assert cert.exists() is True
    clean()

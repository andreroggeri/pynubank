import os
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import OpenSSL

import pynubank
from pynubank import NuException
from pynubank.utils.certificate_generator import CertificateGenerator


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
@patch('sys.stdin', StringIO('1234\n1234\nabcabc\n'))
def test_request_code_exception_should_stop_execution():
    from pynubank import cli

    clean()
    cli.main()

    workdir = Path(os.getcwd())

    cert = workdir.joinpath('cert.p12')

    assert cert.exists() is False


@patch.object(pynubank.utils.certificate_generator.CertificateGenerator, 'exchange_certs', mock_certs)
@patch.object(pynubank.utils.certificate_generator.CertificateGenerator, 'request_code', lambda x: 'email@tld')
@patch('sys.stdin', StringIO('1234\n1234\nabcabc\n'))
def test_should_generate_certs():
    from pynubank import cli

    clean()
    cli.main()

    workdir = Path(os.getcwd())

    cert = workdir.joinpath('cert.p12')

    assert cert.exists() is True

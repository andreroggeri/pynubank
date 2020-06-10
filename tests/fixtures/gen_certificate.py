import pathlib

import pytest


@pytest.fixture
def gen_certificate_return():
    with open(pathlib.Path(__file__).absolute().parent.joinpath('cert.cer')) as f:
        cert = f.read()
    return {
        'certificate': cert,
        'certificate_crypto': cert,
    }

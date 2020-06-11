import pytest


@pytest.fixture
def proxy_return():
    return {
        'token': 'https://some-url/token',
        'login': 'https://some-url/login',
        'lift': 'https://some-url/api/proxy/B',
        'gen_certificate': 'https://some-url/gen_cert'
    }

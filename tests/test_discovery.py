from unittest.mock import MagicMock

import pytest

from pynubank import NuException
from pynubank.utils.discovery import Discovery
from pynubank.utils.http import HttpClient


def build_discovery() -> Discovery:
    http = HttpClient()
    discovery = Discovery(http)
    return discovery


def test_get_unexistent_url(monkeypatch, proxy_return):
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=proxy_return))

    discovery = build_discovery()

    with pytest.raises(NuException) as ex:
        discovery.get_url('some-url')
        assert ex is not None


def test_get_url(monkeypatch, proxy_return):
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=proxy_return))

    discovery = build_discovery()

    assert discovery.get_url('token') == proxy_return['token']


def test_get_app_url(monkeypatch, proxy_return):
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=proxy_return))

    discovery = build_discovery()

    assert discovery.get_app_url('lift') == proxy_return['lift']

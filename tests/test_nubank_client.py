from unittest.mock import MagicMock

import pytest

from requests import Response

from pynubank.nubank import Nubank, NuException


@pytest.mark.parametrize("http_status", [
    100, 101, 102, 103,
    201, 202, 203, 204, 205, 206, 207, 208, 226,
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423,
    424, 426, 428, 429, 431, 440, 444, 449, 450, 451, 495, 496, 497, 498, 499,
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
])
def test_authentication_failure_raise_exception(monkeypatch, http_status):
    response = Response()
    response.status_code = http_status

    monkeypatch.setattr('requests.post', MagicMock(return_value=response))
    with pytest.raises(NuException):
        Nubank('12345678909', '12345678')

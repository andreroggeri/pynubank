from .exception import NuRequestException, NuException
from .nubank import Nubank
from .utils.mock_http import MockHttpClient
from .utils.http import HttpClient
from .utils.discovery import DISCOVERY_URL


def is_alive(client: HttpClient = None) -> bool:
    if client is None:
        client = HttpClient()

    response = client.raw_get(DISCOVERY_URL)
    return response.status_code in [200, 201]

from pynubank.exception import NuException
from pynubank.utils.http import HttpClient

DISCOVERY_URL = 'https://prod-s0-webapp-proxy.nubank.com.br/api/discovery'
DISCOVERY_APP_URL = 'https://prod-s0-webapp-proxy.nubank.com.br/api/app/discovery'


class Discovery:
    def __init__(self, client: HttpClient):
        self.client = client
        self.proxy_list_url = {}
        self.proxy_list_app_url = {}

        self._update_proxy_urls()

    def get_url(self, name: str) -> str:
        return self._get_url(name, self.proxy_list_url)

    def get_app_url(self, name: str) -> str:
        return self._get_url(name, self.proxy_list_app_url)

    def _update_proxy_urls(self):
        self.proxy_list_url = self.client.get(DISCOVERY_URL)
        self.proxy_list_app_url = self.client.get(DISCOVERY_APP_URL)

    def _get_url(self, name: str, target: dict) -> str:
        url = target.get(name)
        if not url:
            raise NuException(f'There is no URL discovered for {name}')

        return url

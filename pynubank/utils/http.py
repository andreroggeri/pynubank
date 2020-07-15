from requests import Response
from requests_pkcs12 import get, post

from pynubank import NuRequestException


class HttpClient:

    def __init__(self):
        self._cert = None
        self._headers = {
            'Content-Type': 'application/json',
            'X-Correlation-Id': 'WEB-APP.pewW9',
            'User-Agent': 'pynubank Client - https://github.com/andreroggeri/pynubank',
        }

    def set_cert(self, cert_path: str):
        self._cert = cert_path

    def set_header(self, name, value):
        self._headers[name] = value

    def get_header(self, name):
        return self._headers.get(name)

    @property
    def _cert_args(self):
        return {'pkcs12_filename': self._cert, 'pkcs12_password': ''} if self._cert else {}

    def _handle_response(self, response: Response) -> dict:
        if response.status_code != 200:
            raise NuRequestException(response)

        return response.json()

    def get(self, url: str) -> dict:
        return self._handle_response(get(url, headers=self._headers, **self._cert_args))

    def post(self, url: str, json: dict) -> dict:
        return self._handle_response(post(url, json=json, headers=self._headers, **self._cert_args))

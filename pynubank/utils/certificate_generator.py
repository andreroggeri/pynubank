from typing import Optional

import OpenSSL
from OpenSSL.crypto import X509

from pynubank import NuException, NuRequestException
from pynubank.utils.discovery import Discovery
from pynubank.utils.http import HttpClient


class CertificateGenerator:

    def __init__(self, login, password, device_id, encrypted_code=None, http_client: Optional[HttpClient] = None):
        self.login = login
        self.password = password
        self.device_id = device_id
        self.encrypted_code = encrypted_code
        self.key1 = self._generate_key()
        self.key2 = self._generate_key()
        self.http = HttpClient() if http_client is None else http_client
        discovery = Discovery(self.http)
        self.url = discovery.get_app_url('gen_certificate')

    def request_code(self) -> str:
        response = self.http.raw_post(self.url, json=self._get_payload())

        if response.status_code != 401 or not response.headers.get('WWW-Authenticate'):
            raise NuException('Authentication code request failed.')

        parsed = self._parse_authenticate_headers(response.headers.get('WWW-Authenticate'))
        self.encrypted_code = parsed.get('device-authorization_encrypted-code')

        return parsed.get('sent-to')

    def exchange_certs(self, code: str):
        if not self.encrypted_code:
            raise NuException('No encrypted code found. Did you call `request_code` before exchanging certs ?')

        payload = self._get_payload()
        payload['code'] = code
        payload['encrypted-code'] = self.encrypted_code

        response = self.http.raw_post(self.url, json=payload)

        if response.status_code != 200:
            raise NuRequestException(response)

        data = response.json()

        cert1 = self._parse_cert(data['certificate'])
        cert2 = self._parse_cert(data['certificate_crypto'])

        return self._gen_cert(self.key1, cert1), self._gen_cert(self.key2, cert2)

    def _get_payload(self):
        return {
            'login': self.login,
            'password': self.password,
            'public_key': self._get_public_key(self.key1),
            'public_key_crypto': self._get_public_key(self.key2),
            'model': f'PyNubank Client ({self.device_id})',
            'device_id': self.device_id
        }

    def _parse_cert(self, content: str) -> X509:
        return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, content.encode())

    def _gen_cert(self, key, cert):
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_privatekey(key)
        p12.set_certificate(cert)

        return p12

    def _generate_key(self):
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

        return key

    def _get_public_key(self, key) -> str:
        return OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, key).decode()

    def _parse_authenticate_headers(self, header_content: str) -> dict:
        chunks = header_content.split(',')
        parsed = {}
        for chunk in chunks:
            key, value = chunk.split('=')
            key = key.strip().replace(' ', '_')
            value = value.replace('"', '')
            parsed[key] = value

        return parsed

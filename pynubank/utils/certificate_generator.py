from typing import Optional

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12

from pynubank import NuException, NuRequestException
from pynubank.utils.discovery import Discovery
from pynubank.utils.http import HttpClient


class PKCS12Certificate:
    """A private key and its certificate, exported as an unencrypted PKCS#12 file.

    Replaces ``OpenSSL.crypto.PKCS12``, which pyOpenSSL 24.1 removed.
    """

    def __init__(self, key: rsa.RSAPrivateKey, cert: Optional[x509.Certificate] = None):
        self.key = key
        self.cert = cert

    def export(self) -> bytes:
        return pkcs12.serialize_key_and_certificates(
            None, self.key, self.cert, None, serialization.NoEncryption())


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

    def _parse_cert(self, content: str) -> x509.Certificate:
        return x509.load_pem_x509_certificate(content.encode())

    def _gen_cert(self, key, cert) -> PKCS12Certificate:
        return PKCS12Certificate(key, cert)

    def _generate_key(self) -> rsa.RSAPrivateKey:
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def _get_public_key(self, key) -> str:
        return key.public_key().public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()

    def _parse_authenticate_headers(self, header_content: str) -> dict:
        chunks = header_content.split(',')
        parsed = {}
        for chunk in chunks:
            key, value = chunk.split('=')
            key = key.strip().replace(' ', '_')
            value = value.replace('"', '')
            parsed[key] = value

        return parsed

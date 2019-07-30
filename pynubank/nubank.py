import json
import os
import uuid
from typing import Tuple

import requests
from qrcode import QRCode
from requests import Response

PAYMENT_EVENT_TYPES = (
    'TransferOutEvent',
    'TransferInEvent',
    'TransferOutReversalEvent',
    'BarcodePaymentEvent',
    'DebitPurchaseEvent',
    'DebitPurchaseReversalEvent',
)


class NuException(Exception):

    def __init__(self, status_code, response, url):
        super().__init__()
        self.url = url
        self.status_code = status_code
        self.response = response


class Nubank:
    DISCOVERY_URL = 'https://prod-s0-webapp-proxy.nubank.com.br/api/discovery'
    DISCOVERY_APP_URL = 'https://prod-s0-webapp-proxy.nubank.com.br/api/app/discovery'
    auth_url = None
    feed_url = None
    proxy_list_url = None
    proxy_list_app_url = None
    query_url = None
    bills_url = None

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'X-Correlation-Id': 'WEB-APP.pewW9',
            'User-Agent': 'pynubank Client - https://github.com/andreroggeri/pynubank',
        }
        self._update_proxy_urls()
        self.auth_url = self.proxy_list_url['login']

    @staticmethod
    def _get_query(query_name):
        root = os.path.abspath(os.path.dirname(__file__))
        gql_file = query_name + '.gql'
        path = os.path.join(root, 'queries', gql_file)
        with open(path) as gql:
            return gql.read()

    def _update_proxy_urls(self):
        request = requests.get(self.DISCOVERY_URL, headers=self.headers)
        self.proxy_list_url = json.loads(request.content.decode('utf-8'))
        request = requests.get(self.DISCOVERY_APP_URL, headers=self.headers)
        self.proxy_list_app_url = json.loads(request.content.decode('utf-8'))

    def _make_graphql_request(self, graphql_object):
        body = {
            'query': self._get_query(graphql_object)
        }
        response = requests.post(self.query_url, json=body, headers=self.headers)

        return self._handle_response(response)

    def _password_auth(self, cpf: str, password: str):
        payload = {
            "grant_type": "password",
            "login": cpf,
            "password": password,
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
        }
        response = requests.post(self.auth_url, json=payload, headers=self.headers)
        data = self._handle_response(response)
        return data

    def _handle_response(self, response: Response) -> dict:
        if response.status_code != 200:
            raise NuException(f'The request made failed with HTTP status code {response.status_code}',
                              response.status_code, response.json())

        return response.json()

    def get_qr_code(self) -> Tuple[str, QRCode]:
        content = str(uuid.uuid4())
        qr = QRCode()
        qr.add_data(content)
        return content, qr

    def authenticate_with_qr_code(self, cpf: str, password, uuid: str):
        auth_data = self._password_auth(cpf, password)
        self.headers['Authorization'] = f'Bearer {auth_data["access_token"]}'

        payload = {
            'qr_code_id': uuid,
            'type': 'login-webapp'
        }

        response = requests.post(self.proxy_list_app_url['lift'], json=payload, headers=self.headers)

        auth_data = self._handle_response(response)
        self.headers['Authorization'] = f'Bearer {auth_data["access_token"]}'
        self.feed_url = auth_data['_links']['events']['href']
        self.query_url = auth_data['_links']['ghostflame']['href']
        self.bills_url = auth_data['_links']['bills_summary']['href']

    def get_card_feed(self):
        request = requests.get(self.feed_url, headers=self.headers)
        return json.loads(request.content.decode('utf-8'))

    def get_card_statements(self):
        feed = self.get_card_feed()
        return list(filter(lambda x: x['category'] == 'transaction', feed['events']))

    def get_bills(self):
        request = requests.get(self.bills_url, headers=self.headers)
        return json.loads(request.content.decode('utf-8'))['bills']

    def get_bill_details(self, bill):
        request = requests.get(bill['_links']['self']['href'], headers=self.headers)
        return json.loads(request.content.decode('utf-8'))

    def get_account_feed(self):
        data = self._make_graphql_request('account_feed')
        return data['data']['viewer']['savingsAccount']['feed']

    def get_account_statements(self):
        feed = self.get_account_feed()
        return list(filter(lambda x: x['__typename'] in PAYMENT_EVENT_TYPES, feed))

    def get_account_balance(self):
        data = self._make_graphql_request('account_balance')
        return data['data']['viewer']['savingsAccount']['currentSavingsBalance']['netAmount']

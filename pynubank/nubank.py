import json
import os
import uuid

import requests

from pynubank import utils


class NuException(BaseException):
    pass


class Nubank:
    headers = {
        'Content-Type': 'application/json',
        'X-Correlation-Id': 'WEB-APP.pewW9',
        'User-Agent': 'pynubank Client - https://github.com/andreroggeri/pynubank',
    }
    TOKEN_URL = None
    discovery_url = 'https://prod-s0-webapp-proxy.nubank.com.br/api/discovery'
    discovery_app_url = 'https://prod-s0-webapp-proxy.nubank.com.br/api/app/discovery'
    feed_url = None
    proxy_list_url = None
    proxy_list_app_url = None
    query_url = None
    allow_qr_code_auth = False

    def __init__(self, cpf, password, allow_qr_code_auth=False):
        self._get_proxy_urls()
        self.TOKEN_URL = self.proxy_list_url['login']
        self.allow_qr_code_auth = allow_qr_code_auth
        self.authenticate(cpf, password)

    @staticmethod
    def _get_query(query_name):
        root = os.path.abspath(os.path.dirname(__file__))
        gql_file = query_name + '.gql'
        path = os.path.join(root, 'queries', gql_file)
        with open(path) as gql:
            return gql.read()

    def _get_proxy_urls(self):
        request = requests.get(self.discovery_url, headers=self.headers)
        self.proxy_list_url = json.loads(request.content.decode('utf-8'))
        request = requests.get(self.discovery_app_url, headers=self.headers)
        self.proxy_list_app_url = json.loads(request.content.decode('utf-8'))

    def _make_graphql_request(self, graphql_object):
        body = {
            'query': self._get_query(graphql_object)
        }
        request = requests.post(self.query_url, json=body, headers=self.headers)
        if request.status_code != 200:
            message = '{} ({})'.format(request.reason, request.status_code)
            raise NuException('Something wrong with your request. Check and try again. {}'.format(message))
        return json.loads(request.content.decode('utf-8'))

    def _qr_code_auth(self):
        print('You must authenticate with your phone to be able to access your data.')
        print('Scan the QRCode below with you Nubank application on the following menu:')
        print('Nu(Seu Nome) > Perfil > Acesso pelo site')
        content = uuid.uuid4()
        utils.print_qr_code(str(content))
        input('After the scan, press enter do proceed')
        payload = {
            'qr_code_id': str(content),
            'type': 'login-webapp'
        }
        req = requests.post(self.proxy_list_app_url['lift'], json=payload, headers=self.headers)
        if req.status_code != 200:
            raise NuException('Failed to authenticate with QRCode')

        data = json.loads(req.content.decode('utf-8'))
        self.headers['Authorization'] = 'Bearer {}'.format(data['access_token'])
        self.feed_url = data['_links']['events']['href']
        self.query_url = data['_links']['ghostflame']['href']
        self.bills_url = data['_links']['bills_summary']['href']

    def authenticate(self, cpf, password):
        body = {
            "grant_type": "password",
            "login": cpf,
            "password": password,
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
        }
        request = requests.post(self.TOKEN_URL, json=body, headers=self.headers)
        if request.status_code != 200:
            message = '{} ({})'.format(request.reason, request.status_code)
            raise NuException('Authentication failed. {}'.format(message))

        data = json.loads(request.content.decode('utf-8'))
        self.headers['Authorization'] = 'Bearer {}'.format(data['access_token'])

        if data['_links'].get('events'):
            self.feed_url = data['_links']['events']['href']
            self.query_url = data['_links']['ghostflame']['href']
            self.bills_url = data['_links']['bills_summary']['href']
        else:
            if self.allow_qr_code_auth:
                self._qr_code_auth()
            else:
                raise NuException('QRCode authentication is not enabled.'
                                  ' Enable it on the Nubank constructor, passing allow_qr_code_auth=True')

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
        return list(filter(lambda x: x['__typename'] in ('TransferOutEvent', 'TransferInEvent', 'TransferOutReversalEvent', 'BarcodePaymentEvent'), feed))

    def get_account_balance(self):
        data = self._make_graphql_request('account_balance')
        return data['data']['viewer']['savingsAccount']['currentSavingsBalance']['netAmount']

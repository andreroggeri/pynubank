import json

import os
import requests


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
    feed_url = None
    proxy_list_url = None
    query_url = None
    access_token = None
    refresh_token = None
    refresh_before = None

    def __init__(self, cpf=None, password=None, refresh_token=None):
        self.proxy_list_url = self._get_proxy_urls()
        self.TOKEN_URL = self.proxy_list_url['login']
        if cpf is not None and password is not None:
            self.authenticate(cpf, password)
        elif refresh_token is not None:
            self.authenticate(cpf, password, refresh_token)
        else:
            raise NuException('Authentication failed. Login using NuBank website, make all steps of authentication and try again.')

    @staticmethod
    def _get_query(query_name):
        root = os.path.abspath(os.path.dirname(__file__))
        gql_file = query_name + '.gql'
        path = os.path.join(root, 'queries', gql_file)
        with open(path) as gql:
            return gql.read()

    def _get_proxy_urls(self):
        request = requests.get(self.discovery_url, headers=self.headers)
        return json.loads(request.content.decode('utf-8'))

    def _make_graphql_request(self, graphql_object):
        body = {
            'query': self._get_query(graphql_object)
        }
        request = requests.post(self.query_url, json=body, headers=self.headers)
        if request.status_code != 200:
            message = '{} ({})'.format(request.reason, request.status_code)
            raise NuException('Something wrong with your request. Check and try again. {}'.format(message))
        return json.loads(request.content.decode('utf-8'))

    def authenticate(self, cpf=None, password=None, refresh_token=None):
        if cpf is not None and password is not None:
            body = {
                "grant_type": "password",
                "login": cpf,
                "password": password,
                "client_id": "other.conta",
                "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
            }
        else:
            body = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": "other.conta",
                "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
            }
        request = requests.post(self.TOKEN_URL, json=body, headers=self.headers)
        if request.status_code != 200:
            message = '{} ({})'.format(request.reason, request.status_code)
            raise NuException('Authentication failed. {}'.format(message))

        data = json.loads(request.content.decode('utf-8'))
        self.headers['Authorization'] = 'Bearer {}'.format(data['access_token'])
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.refresh_before = data['refresh_before']
        self.feed_url = data.get('_links', {}).get('events', {}).get('href')
        if self.feed_url is None:
            raise NuException('Authentication failed. Login using NuBank website, make all steps of authentication and try again.')
        self.query_url = data['_links']['ghostflame']['href']
        self.bills_url = data['_links']['bills_summary']['href']

    def get_tokens(self):
        tokens = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'refresh_before': self.refresh_before
        }
        return tokens

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

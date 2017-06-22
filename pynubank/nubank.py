import json

import requests


class NuException(BaseException):
    pass


class Nubank:
    headers = {
        'Content-Type': 'application/json',
        'X-Correlation-Id': 'WEB-APP.pewW9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36',
        'Origin': 'https://conta.nubank.com.br',
        'Referer': 'https://conta.nubank.com.br/',
    }
    TOKEN_URL = 'https://prod-auth.nubank.com.br/api/token'
    feed_url = None

    def __init__(self, cpf, password):
        self.authenticate(cpf, password)

    def authenticate(self, cpf, password):
        body = {
            "grant_type": "password",
            "login": cpf,
            "password": password,
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
        }
        request = requests.post(Nubank.TOKEN_URL, json=body, headers=self.headers)
        if request.status_code != 200:
            raise NuException('Authentication failed. Check your credentials!')

        data = json.loads(request.content.decode('utf-8'))
        self.headers['Authorization'] = 'Bearer {}'.format(data['access_token'])
        self.feed_url = data['_links']['events']['href']

    def get_account_feed(self):
        request = requests.get(self.feed_url, headers=self.headers)
        return json.loads(request.content.decode('utf-8'))

    def get_account_statements(self):
        feed = self.get_account_feed()
        return list(filter(lambda x: x['category'] == 'transaction', feed['events']))

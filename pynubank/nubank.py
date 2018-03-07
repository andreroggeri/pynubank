import json

import requests


class NuException(BaseException):
    pass


class Nubank:
    headers = {
        'Content-Type': 'application/json',
        'X-Correlation-Id': 'WEB-APP.pewW9',
        'User-Agent': 'pynubank Client - https://github.com/andreroggeri/pynubank',
    }
    TOKEN_URL = 'https://prod-auth.nubank.com.br/api/token'
    feed_url = None
    query_url = None

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
        self.query_url = data['_links']['ghostflame']['href']

    def get_card_feed(self):
        request = requests.get(self.feed_url, headers=self.headers)
        return json.loads(request.content.decode('utf-8'))

    def get_card_statements(self):
        feed = self.get_card_feed()
        return list(filter(lambda x: x['category'] == 'transaction', feed['events']))

    def get_account_statements(self):
        statements_query = """
              {
                viewer {
                  savingsAccount {
                    feed {
                      id
                      __typename
                      title
                      detail
                      postDate
                      ... on TransferInEvent {
                        amount
                      }
                      ... on TransferOutEvent {
                        amount
                        destinationAccount {
                          name
                        }
                      }
                    }  
                  }
                }
              }
            """
        body = {
            'query': statements_query,
            'variables': {}
        }
        request = requests.post(self.query_url, json=body, headers=self.headers)
        data = json.loads(request.content.decode('utf-8'))

        return data['data']['viewer']['savingsAccount']['feed']

    def get_account_balance(self):
        savings_query = """
                        {
                          viewer {
                            savingsAccount {
                              currentSavingsBalance {
                                netAmount
                                }
                              }
                            }
                        }
                        """
        body = {
            'query': savings_query,
        }
        request = requests.post(self.query_url, json=body, headers=self.headers)
        data = json.loads(request.content.decode('utf-8'))
        return data['data']['viewer']['savingsAccount']['currentSavingsBalance']['netAmount']

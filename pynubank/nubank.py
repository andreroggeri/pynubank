import calendar
import datetime
import itertools
import uuid
from typing import Tuple

from qrcode import QRCode

from pynubank.exception import NuMissingCreditCard
from pynubank.utils.discovery import Discovery
from pynubank.utils.graphql import prepare_request_body
from pynubank.utils.http import HttpClient
from pynubank.utils.parsing import parse_float, parse_pix_transaction

PAYMENT_EVENT_TYPES = (
    'TransferOutEvent',
    'TransferInEvent',
    'TransferOutReversalEvent',
    'BarcodePaymentEvent',
    'DebitPurchaseEvent',
    'DebitPurchaseReversalEvent',
    'BillPaymentEvent',
    'DebitWithdrawalFeeEvent',
    'DebitWithdrawalEvent',
    'PixTransferOutEvent',
    'PixTransferInEvent',
    'PixTransferOutReversalEvent',
    'PixTransferFailedEvent',
)


class Nubank:
    def __init__(self, client: HttpClient = None):
        if client is None:
            client = HttpClient()

        self._client = client
        self._discovery = Discovery(self._client)
        self._feed_url = None
        self._query_url = None
        self._bills_url = None
        self._customer_url = None
        self._revoke_token_url = None

    def _make_graphql_request(self, graphql_object, variables=None):
        return self._client.post(self._query_url,
                                 json=prepare_request_body(graphql_object, variables))

    def _password_auth(self, cpf: str, password: str):
        payload = {
            "grant_type": "password",
            "login": cpf,
            "password": password,
            "client_id": "other.conta",
            "client_secret": "yQPeLzoHuJzlMMSAjC-LgNUJdUecx8XO"
        }
        return self._client.post(self._discovery.get_url('login'), json=payload)

    def _find_url(self, known_keys: list, links: dict) -> str:
        links_keys = links.keys()
        common_keys = [item for item in links_keys if item in known_keys]
        key = next(iter(common_keys), None)
        return links.get(key, {}).get('href', None)

    def _save_auth_data(self, auth_data: dict) -> None:
        self._client.set_header('Authorization', f'Bearer {auth_data["access_token"]}')

        links = auth_data['_links']

        feed_url_keys = ['events', 'magnitude']
        bills_url_keys = ['bills_summary']
        customer_url_keys = ['customer']

        self._feed_url = self._find_url(feed_url_keys, links)
        self._bills_url = self._find_url(bills_url_keys, links)
        self._customer_url = self._find_url(customer_url_keys, links)
        self._query_url = links['ghostflame']['href']
        self._revoke_token_url = links['revoke_token']['href']

    def get_qr_code(self) -> Tuple[str, QRCode]:
        content = str(uuid.uuid4())
        qr = QRCode()
        qr.add_data(content)
        return content, qr

    def authenticate_with_qr_code(self, cpf: str, password, uuid: str):
        auth_data = self._password_auth(cpf, password)
        self._client.set_header('Authorization', f'Bearer {auth_data["access_token"]}')

        payload = {
            'qr_code_id': uuid,
            'type': 'login-webapp'
        }

        response = self._client.post(self._discovery.get_app_url('lift'), json=payload)

        self._save_auth_data(response)

    def authenticate_with_cert(self, cpf: str, password: str, cert_path: str):
        self._client.set_cert(cert_path)
        url = self._discovery.get_app_url('token')
        payload = {
            'grant_type': 'password',
            'client_id': 'legacy_client_id',
            'client_secret': 'legacy_client_secret',
            'login': cpf,
            'password': password
        }

        response = self._client.post(url, json=payload)

        self._save_auth_data(response)

        return response.get('refresh_token')

    def authenticate_with_refresh_token(self, refresh_token: str, cert_path: str):
        self._client.set_cert(cert_path)

        url = self._discovery.get_app_url('token')
        payload = {
            'grant_type': 'refresh_token',
            'client_id': 'legacy_client_id',
            'client_secret': 'legacy_client_secret',
            'refresh_token': refresh_token,
        }

        response = self._client.post(url, json=payload)

        self._save_auth_data(response)

        return response.get('refresh_token')

    def revoke_token(self):
        self._client.post(self._revoke_token_url, {})

        self._client.remove_header('Authorization')

    def get_card_feed(self):
        return self._client.get(self._feed_url)

    def get_card_statements(self):
        feed = self.get_card_feed()
        return list(filter(lambda x: x['category'] == 'transaction', feed['events']))

    def get_card_payments(self):
        feed = self.get_card_feed()
        return list(filter(lambda x: x['category'] == 'payment', feed['events']))

    def get_bills(self):
        if self._bills_url is not None:
            request = self._client.get(self._bills_url)
            return request['bills']
        else:
            raise NuMissingCreditCard

    def get_customer(self):
        request = self._client.get(self._customer_url)
        return request['customer']

    def get_bill_details(self, bill: dict):
        return self._client.get(bill['_links']['self']['href'])

    def get_account_feed(self):
        data = self._make_graphql_request('account_feed')
        return data['data']['viewer']['savingsAccount']['feed']

    def get_account_statements(self):
        feed = self.get_account_feed()
        feed = map(parse_pix_transaction, feed)
        return list(filter(lambda x: x['__typename'] in PAYMENT_EVENT_TYPES, feed))

    def get_account_balance(self):
        data = self._make_graphql_request('account_balance')
        return data['data']['viewer']['savingsAccount']['currentSavingsBalance']['netAmount']

    def get_account_investments_details(self):
        data = self._make_graphql_request('account_investments')
        return data['data']['viewer']['savingsAccount']['redeemableDeposits']

    def get_account_investments_yield(self, date=datetime.datetime.now()) -> float:
        _, last_day = calendar.monthrange(date.year, date.month)
        last_month_day = datetime.date(date.year, date.month, last_day)

        payload = {
            "asOf": last_month_day.strftime('%Y-%m-%d')
        }

        data = self._make_graphql_request('account_investments_yield', payload)

        value = \
            data['data']['viewer']['productFeatures']['savings']['screens']['detailedBalance']['monthBalanceSection'][
                'yieldSection']['semantics']['label']

        return parse_float(value)

    def create_boleto(self, amount: float) -> str:
        customer_id_response = self._make_graphql_request('account_id')
        customer_id = customer_id_response['data']['viewer']['id']

        payload = {
            "input": {"amount": str(amount), "customerId": customer_id}
        }

        boleto_response = self._make_graphql_request('create_boleto', payload)

        barcode = boleto_response['data']['createTransferInBoleto']['boleto']['readableBarcode']

        return barcode

    def create_money_request(self, amount: float) -> str:
        account_data = self._make_graphql_request('account_feed')
        account_id = account_data['data']['viewer']['savingsAccount']['id']
        payload = {
            'input': {
                'amount': amount, 'savingsAccountId': account_id
            }
        }

        money_request_response = self._make_graphql_request('create_money_request', payload)

        return money_request_response['data']['createMoneyRequest']['moneyRequest']['url']

    def get_available_pix_keys(self):
        response = self._make_graphql_request('get_pix_keys')
        savings_acount = response['data']['viewer']['savingsAccount']

        return {'keys': savings_acount['dict']['keys'], 'account_id': savings_acount['id']}

    def create_pix_payment_qrcode(self, account_id: str, amount: float, pix_key: dict, tx_id: str = '') -> dict:
        payload = {
            'createPaymentRequestInput': {
                'amount': amount,
                'pixAlias': pix_key.get('value'),
                "savingsAccountId": account_id,
                'transactionId': tx_id,
            }
        }

        response = self._make_graphql_request('create_pix_money_request', payload)

        data = response['data']['createPaymentRequest']['paymentRequest']
        qr = QRCode()
        qr.add_data(data['brcode'])

        return {
            'payment_url': data['url'],
            'payment_code': data['brcode'],
            'qr_code': qr,
        }

    def get_pix_identifier(self, transaction_id: str):
        def find_pix_identifier(table_item: dict):
            return table_item.get('label') == 'Identificador'

        response = self._make_graphql_request('pix_receipt_screen', {'type': 'TRANSFER_IN', 'id': transaction_id})
        if 'errors' in response.keys():
            return

        screen_pieces = response['data']['viewer']['savingsAccount']['getGenericReceiptScreen']['screenPieces']
        table_items = list(itertools.chain(*[table_item.get('tableItems', []) for table_item in screen_pieces]))

        identifier_data = next(filter(find_pix_identifier, table_items), None)

        if identifier_data is None:
            return

        return identifier_data['value']

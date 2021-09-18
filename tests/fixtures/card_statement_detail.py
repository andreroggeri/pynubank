from uuid import uuid4

import pytest


@pytest.fixture
def card_statement_detail():
    id = str(uuid4())
    return {
        'transaction': {
            'category': 'outros',
            'amount': 10000,
            'tags': [],
            'card_last_four_digits': '1234',
            'time': '2021-08-12T10:56:00Z',
            'charges': 2,
            'original_merchant_name': 'Loja',
            'mcc': '1234',
            'charges_list': [
                {
                    'amount': 5000,
                    'status': 'future',
                    'index': 1,
                    'source': 'installments_merchant',
                    'extras': [],
                    'post_date': '2021-09-10',
                },
                {
                    'amount': 5000,
                    'status': 'future',
                    'index': 2,
                    'source': 'installments_merchant',
                    'extras': [],
                    'post_date': '2021-10-10',
                },
            ],
            'source': 'installments_merchant',
            'adjustments': [],
            'amount_without_iof': 10000,
            'account': str(uuid4()),
            'card': str(uuid4()),
            'status': 'settled',
            'id': id,
            'merchant_name': 'Loja',
            'event_type': 'transaction_card_not_present',
            '_links': {
                'category': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}/category'
                },
                'anticipate': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}/anticipation-with-pin-verification'
                },
                'chargeback_reasons_v4': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/removed?name=chargeback-reasons-v4'
                },
                'notify_geo': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/waypoints/transaction/{id}'
                },
                'categories': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}/category'
                },
                'chargeback': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/removed?name=chargeback'
                },
                'create_tag': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}/tags'
                },
                'tx_financing': {
                    'href': 'nuapp://informative-bottom-sheet?title=Esta+compra+n%C3%A3o+pode+ser+parcelada'
                },
                'chargeback_flow': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/chargeback-requests'
                },
                'complaint_flow': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/complaint-requests'
                },
                'chargeback_reasons': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/removed?name=chargeback-reasons'
                },
                'merchant': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}/merchant'
                },
                'self': {
                    'href': f'https://prod-s0-facade.nubank.com.br/api/transactions/{id}'
                },
                'get_static_map_bytes': {
                    'href': 'https://prod-s0-facade.nubank.com.br/api/static-map-bytes'
                },
            },
            'country': 'BRA',
            'card_type': 'credit_card_virtual',
        }
    }

import pytest


@pytest.fixture
def bill_details_return():
    return {
        'bill': {
            '_links': {
                'barcode': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'
                },
                'boleto_email': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'
                },
                'invoice_email': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/invoice/email'
                },
                'self': {
                    'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'
                }
            },
            'account_id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'auto_debit_failed': False,
            'barcode': '',
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'line_items': [
                {
                    'amount': 2390,
                    'category': 'Eletrônicos',
                    'charges': 1,
                    'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                    'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                    'index': 0,
                    'post_date': '2015-09-09',
                    'title': 'Mercadopago Mlivre'
                },
                {
                    'amount': 5490,
                    'category': 'Eletrônicos',
                    'charges': 1,
                    'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                    'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                    'index': 0,
                    'post_date': '2015-09-09',
                    'title': 'Mercadopago Mlivre'
                }
            ],
            'linha_digitavel': '',
            'payment_method': 'boleto',
            'state': 'overdue',
            'status': 'paid',
            'summary': {
                'adjustments': '0',
                'close_date': '2015-09-25',
                'due_date': '2015-10-10',
                'effective_due_date': '2015-10-13',
                'expenses': '78.8000',
                'fees': '0',
                'interest': 0,
                'interest_charge': '0',
                'interest_rate': '0.0775',
                'interest_reversal': '0',
                'international_tax': '0',
                'late_fee': '0.02',
                'late_interest_rate': '0.0875',
                'minimum_payment': 7005,
                'open_date': '2015-07-23',
                'paid': 7880,
                'past_balance': 0,
                'payments': '0',
                'precise_minimum_payment': '70.054500',
                'precise_total_balance': '78.8000',
                'previous_bill_balance': '0',
                'tax': '0',
                'total_accrued': '0',
                'total_balance': 7880,
                'total_credits': '0',
                'total_cumulative': 7880,
                'total_financed': '0',
                'total_international': '0',
                'total_national': '78.8000',
                'total_payments': '0'
            }
        }
    }

import fnmatch
from pynubank.utils.http import HttpClient
from pynubank.utils.discovery import DISCOVERY_URL, DISCOVERY_APP_URL
from pynubank.utils.graphql import prepare_request_body
from pynubank import NuException


class MockHttpClient(HttpClient):
    def get(self, url: str) -> dict:
        result = self._find(url)
        if result is None:
            raise NuException(f'There is no result expected for {url}')
        return result

    def post(self, url: str, json: dict) -> dict:
        result = self._find(url, json)
        if result is None:
            json['variables'] = {}
            result = self._find(url, json)

            if result is None:
                raise NuException(f'There is no result expected for {url}')
        return result

    def _find(self, url: str, json: dict = None):
        result = self._results.get(url)
        if result:
            return result

        for k in self._results.keys():
            if type(k) == str:
                if fnmatch.fnmatch(url, k):
                    return self._results[k]

            if type(k) == tuple and json is not None:
                if fnmatch.fnmatch(url, k[0]):
                    return self._results.get((k[0], str(json)))

        return self._results.get((url, str(json)))

    _results = {}
    _results['https://*/api/discovery'] = {
        'register_prospect_savings_web': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_web',
        'register_prospect_savings_mgm': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_mgm',
        'pusher_auth_channel': 'https://mocked-proxy-url/api/proxy/pusher_auth_channel',
        'register_prospect_debit': 'https://mocked-proxy-url/api/proxy/register_prospect_debit',
        'reset_password': 'https://mocked-proxy-url/api/proxy/reset_password',
        'register_prospect': 'https://mocked-proxy-url/api/proxy/register_prospect',
        'register_prospect_savings_request_money': 'https://mocked-proxy-url/api/proxy/register_prospect_savings_request_money',
        'register_prospect_global_web': 'https://mocked-proxy-url/api/proxy/register_prospect_global_web',
        'register_prospect_c': 'https://mocked-proxy-url/api/proxy/register_prospect_c',
        'request_password_reset': 'https://mocked-proxy-url/api/proxy/request_password_reset',
        'auth_gen_certificates': 'https://mocked-proxy-url/api/proxy/auth_gen_certificates',
        'login': 'https://mocked-proxy-url/api/proxy/login',
        'email_verify': 'https://mocked-proxy-url/api/proxy/email_verify',
        'auth_device_resend_code': 'https://mocked-proxy-url/api/proxy/auth_device_resend_code',
        'msat': 'https://mocked-proxy-url/api/proxy/msat'
    }
    _results['https://*/api/app/discovery'] = {
        'scopes': 'https://mocked-proxy-url/api/admin/scope',
        'creation': 'https://mocked-proxy-url/api/creation',
        'change_password': 'https://mocked-proxy-url/api/change-password',
        'smokejumper': 'https://prod-cdn.nubank.com.br/mobile/fire-station/smokejumper.json',
        'block': 'https://mocked-proxy-url/api/admin/block',
        'lift': 'https://mocked-proxy-url/api/proxy/lift',
        'shard_mapping_id': 'https://mocked-proxy-url/api/mapping/:kind/:id',
        'force_reset_password': 'https://mocked-proxy-url/api/admin/force-reset-password',
        'revoke_token': 'https://mocked-proxy-url/api/proxy/revoke_token',
        'userinfo': 'https://mocked-proxy-url/api/userinfo',
        'reset_password': 'https://mocked-proxy-url/api/proxy/reset_password',
        'unblock': 'https://mocked-proxy-url/api/admin/unblock',
        'shard_mapping_cnpj': 'https://mocked-proxy-url/api/proxy/shard_mapping_cnpj',
        'shard_mapping_cpf': 'https://mocked-proxy-url/api/mapping/shard_mapping_cpf',
        'register_prospect': 'https://mocked-proxy-url/api/proxy/register_prospect',
        'engage': 'https://mocked-proxy-url/api/proxy/engage',
        'account_recovery_job': 'https://mocked-proxy-url/api/proxy/account_recovery_job',
        'account_recovery_confirm': 'https://mocked-proxy-url/api/proxy/account_recovery_confirm',
        'magnitude': 'https://prod-s0-magnitude.nubank.com.br/api/events',
        'revoke_all': 'https://mocked-proxy-url/api/proxy/revoke_all',
        'user_hypermedia': 'https://mocked-proxy-url/api/admin/users/:id/hypermedia',
        'gen_certificate': 'https://mocked-proxy-url/api/proxy/gen_certificate',
        'email_verify': 'https://mocked-proxy-url/api/proxy/email_verify',
        'prospect_location': 'https://mocked-proxy-url/api/proxy/prospect_location',
        'token': 'https://mocked-proxy-url/api/token',
        'account_recovery': 'https://mocked-proxy-url/api/proxy/account_recovery',
        'start_screen_v2': 'https://mocked-proxy-url/api/proxy/start_screen_v2',
        'scopes_remove': 'https://mocked-proxy-url/api/admin/scope/:admin-id',
        'approved_products': 'https://mocked-proxy-url/api/proxy/approved_products',
        'admin_revoke_all': 'https://mocked-proxy-url/api/proxy/admin_revoke_all',
        'faq': {'ios': 'https://ajuda.nubank.com.br/ios', 'android': 'https://ajuda.nubank.com.br/android',
                'wp': 'https://ajuda.nubank.com.br/windows-phone'},
        'scopes_add': 'https://mocked-proxy-url/api/admin/scope/:admin-id',
        'registration': 'https://mocked-proxy-url/api/proxy/registration',
        'global_services': 'https://mocked-proxy-url/api/mapping/global-services',
        'start_screen': 'https://mocked-proxy-url/api/proxy/start_screen',
        'user_change_password': 'https://mocked-proxy-url/api/user/:user-id/password',
        'account_recovery_token': 'https://mocked-proxy-url/api/proxy/account_recovery_token',
        'user_status': 'https://mocked-proxy-url/api/admin/user-status',
        'engage_and_create_credentials': 'https://mocked-proxy-url/api/proxy/engage_and_create_credentials'
    }

    _results['https://mocked-proxy-url/api/proxy/login'] = {
        'access_token': 'access_token_123',
        'token_type': 'bearer',
        '_links': {
            'change_password': {'href': 'https://mocked-proxy-url/api/proxy/change_password_123'},
            'enabled_features': {'href': 'https://mocked-proxy-url/api/proxy/enabled_features_123'},
            'revoke_token': {'href': 'https://mocked-proxy-url/api/proxy/revoke_token_123'},
            'userinfo': {'href': 'https://mocked-proxy-url/api/proxy/userinfo_123'},
            'events_page': {'href': 'https://mocked-proxy-url/api/proxy/events_page_123'},
            'events': {'href': 'https://mocked-proxy-url/api/proxy/events_123'},
            'postcode': {'href': 'https://mocked-proxy-url/api/proxy/post_code_123'},
            'app_flows': {'href': 'https://mocked-proxy-url/api/proxy/app_flows_123'},
            'revoke_all': {'href': 'https://mocked-proxy-url/api/proxy/revoke_all_123'},
            'customer': {'href': 'https://mocked-proxy-url/api/proxy/customer_123'},
            'account': {'href': 'https://mocked-proxy-url/api/proxy/account_123'},
            'bills_summary': {'href': 'https://mocked-proxy-url/api/proxy/bills_summary_123'},
            'savings_account': {'href': 'https://mocked-proxy-url/api/proxy/savings_account_123'},
            'purchases': {'href': 'https://mocked-proxy-url/api/proxy/purchases_123'},
            'ghostflame': {'href': 'https://mocked-proxy-url/api/proxy/ghostflame_123'},
            'user_change_password': {'href': 'https://mocked-proxy-url/api/proxy/user_change_password_123'}
        }
    }

    _results['https://mocked-proxy-url/api/proxy/lift'] = {
        'access_token': 'access_token_123',
        'token_type': 'bearer',
        '_links': {
            'change_password': {'href': 'https://mocked-proxy-url/api/proxy/change_password_123'},
            'enabled_features': {'href': 'https://mocked-proxy-url/api/proxy/enabled_features_123'},
            'revoke_token': {'href': 'https://mocked-proxy-url/api/proxy/revoke_token_123'},
            'userinfo': {'href': 'https://mocked-proxy-url/api/proxy/userinfo_123'},
            'events_page': {'href': 'https://mocked-proxy-url/api/proxy/events_page_123'},
            'events': {'href': 'https://mocked-proxy-url/api/proxy/events_123'},
            'postcode': {'href': 'https://mocked-proxy-url/api/proxy/post_code_123'},
            'app_flows': {'href': 'https://mocked-proxy-url/api/proxy/app_flows_123'},
            'revoke_all': {'href': 'https://mocked-proxy-url/api/proxy/revoke_all_123'},
            'customer': {'href': 'https://mocked-proxy-url/api/proxy/customer_123'},
            'account': {'href': 'https://mocked-proxy-url/api/proxy/account_123'},
            'bills_summary': {'href': 'https://mocked-proxy-url/api/proxy/bills_summary_123'},
            'savings_account': {'href': 'https://mocked-proxy-url/api/proxy/savings_account_123'},
            'purchases': {'href': 'https://mocked-proxy-url/api/proxy/purchases_123'},
            'ghostflame': {'href': 'https://mocked-proxy-url/api/proxy/ghostflame_123'},
            'user_change_password': {'href': 'https://mocked-proxy-url/api/proxy/user_change_password_123'}
        }
    }

    _results['https://mocked-proxy-url/api/token'] = {
        'access_token': 'access_token_123',
        'token_type': 'bearer',
        '_links': {
            'change_password': {'href': 'https://mocked-proxy-url/api/proxy/change_password_123'},
            'enabled_features': {'href': 'https://mocked-proxy-url/api/proxy/enabled_features_123'},
            'revoke_token': {'href': 'https://mocked-proxy-url/api/proxy/revoke_token_123'},
            'userinfo': {'href': 'https://mocked-proxy-url/api/proxy/userinfo_123'},
            'events_page': {'href': 'https://mocked-proxy-url/api/proxy/events_page_123'},
            'events': {'href': 'https://mocked-proxy-url/api/proxy/events_123'},
            'postcode': {'href': 'https://mocked-proxy-url/api/proxy/post_code_123'},
            'app_flows': {'href': 'https://mocked-proxy-url/api/proxy/app_flows_123'},
            'revoke_all': {'href': 'https://mocked-proxy-url/api/proxy/revoke_all_123'},
            'customer': {'href': 'https://mocked-proxy-url/api/proxy/customer_123'},
            'account': {'href': 'https://mocked-proxy-url/api/proxy/account_123'},
            'bills_summary': {'href': 'https://mocked-proxy-url/api/proxy/bills_summary_123'},
            'savings_account': {'href': 'https://mocked-proxy-url/api/proxy/savings_account_123'},
            'purchases': {'href': 'https://mocked-proxy-url/api/proxy/purchases_123'},
            'ghostflame': {'href': 'https://mocked-proxy-url/api/proxy/ghostflame_123'},
            'user_change_password': {'href': 'https://mocked-proxy-url/api/proxy/user_change_password_123'}
        }
    }

    _results['https://mocked-proxy-url/api/proxy/events_123'] = {
        'events': [{
            'description': 'Shopping Iguatemi', 'category': 'transaction', 'amount': 700,
            'time': '2017-09-09T02:03:55Z', 'title': 'transporte',
            'details': {'lat': -12.9818258, 'lon': -38.4652058, 'subcategory': 'card_present'},
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            '_links': {'self': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'}},
            'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
        }],
        'as_of': '2017-09-09T06:50:22.323Z',
        'customer_id': 'abcde-fghi-jklmn-opqrst-uvxz',
        '_links': {
            'updates': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/updates_123'},
            'next': {'href': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/next_123'}
        }
    }

    _results['https://mocked-proxy-url/api/proxy/bills_summary_123'] = {
        "_links": {
            "future": {
                "href": "https://mocked-proxy-url/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/future"
            },
            "open": {
                "href": "https://mocked-proxy-url/api/accounts/abcde-fghi-jklmn-opqrst-uvxz/bills/open"
            }
        },
        "bills": [
            {
                "_links": {
                    "self": {
                        "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
                    }
                },
                "state": "future",
                "summary": {
                    "adjustments": "0",
                    "close_date": "2018-05-03",
                    "due_date": "2018-05-10",
                    "effective_due_date": "2018-05-10",
                    "expenses": "126.94",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 0,
                    "open_date": "2018-04-03",
                    "paid": 0,
                    "past_balance": 0,
                    "payments": "0",
                    "precise_minimum_payment": "0",
                    "precise_total_balance": "126.94",
                    "previous_bill_balance": "0",
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 12694,
                    "total_credits": "0",
                    "total_cumulative": 12694,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "126.94",
                    "total_payments": "0"
                }
            },
            {
                "_links": {
                    "self": {
                        "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
                    }
                },
                "state": "open",
                "summary": {
                    "adjustments": "0",
                    "close_date": "2018-04-03",
                    "due_date": "2018-04-10",
                    "effective_due_date": "2018-04-10",
                    "expenses": "303.36",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 0,
                    "open_date": "2018-03-03",
                    "paid": 0,
                    "past_balance": 0,
                    "payments": "-285.15",
                    "precise_minimum_payment": "0",
                    "precise_total_balance": "303.362041645013",
                    "previous_bill_balance": "285.152041645013",
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 30336,
                    "total_credits": "0",
                    "total_cumulative": 30336,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "303.36",
                    "total_payments": "-285.15"
                }
            }, {
                "_links": {
                    "self": {
                        "href": "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
                    }
                },
                "href": "nuapp://bill/abcde-fghi-jklmn-opqrst-uvxz",
                "id": "abcde-fghi-jklmn-opqrst-uvxz",
                "state": "overdue",
                "summary": {
                    "adjustments": "-63.99106066",
                    "close_date": "2018-03-03",
                    "due_date": "2018-03-10",
                    "effective_due_date": "2018-03-12",
                    "expenses": "364.14",
                    "fees": "0",
                    "interest": 0,
                    "interest_charge": "0",
                    "interest_rate": "0.1375",
                    "interest_reversal": "0",
                    "international_tax": "0",
                    "minimum_payment": 8003,
                    "open_date": "2018-02-03",
                    "paid": 28515,
                    "past_balance": -1500,
                    "payments": "-960.47",
                    "precise_minimum_payment": "480.02544320601300",
                    "precise_total_balance": "285.152041645013",
                    "previous_bill_balance": "945.473102305013",
                    "remaining_minimum_payment": 0,
                    "tax": "0",
                    "total_accrued": "0",
                    "total_balance": 28515,
                    "total_credits": "-64.18",
                    "total_cumulative": 30015,
                    "total_financed": "0",
                    "total_international": "0",
                    "total_national": "364.32893934",
                    "total_payments": "-960.47"
                }
            }
        ]
    }

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123', str(prepare_request_body('account_balance')))] = {
        'data': {'viewer': {'savingsAccount': {'currentSavingsBalance': {'netAmount': 127.33}}}}
    }

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123', str(prepare_request_body('account_feed')))] = {
        'data': {
            'viewer': {
                'savingsAccount': {
                    'id': 'abc123123',
                    'feed': [{
                        'id': 'abcde-fghi-jklmn-opqrst-uvxw', '__typename': 'BillPaymentEvent',
                        'title': 'Pagamento da fatura',
                        'detail': 'Cartão Nubank - R$ 50,00', 'postDate': '2018-03-07'
                    }, {
                        'id': 'abcde-fghi-jklmn-opqrst-uvxy', '__typename': 'TransferOutReversalEvent',
                        'title': 'Transferência devolvida', 'detail': 'Juquinha da Silva Sauro - R$ 20,00',
                        'postDate': '2018-03-06'
                    }, {
                        'id': 'abcde-fghi-jklmn-opqrst-uvxz', '__typename': 'TransferOutEvent',
                        'title': 'Transferência enviada',
                        'detail': 'Juquinha da Silva Sauro - R$ 20,00', 'postDate': '2018-03-06', 'amount': 20.0,
                        'destinationAccount': {'name': 'Juquinha da Silva Sauro'}
                    }, {
                        'id': 'abcde-fghi-jklmn-opqrst-uvx1', '__typename': 'TransferInEvent',
                        'title': 'Transferência recebida',
                        'detail': 'R$127.33', 'postDate': '2018-03-06', 'amount': 127.33
                    }, {
                        'id': 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123', '__typename': 'BarcodePaymentEvent',
                        'title': 'Pagamento efetuado', 'detail': 'AES ELETROPAULO', 'postDate': '2018-02-05',
                        'amount': 169.2
                    }, {
                        'id': 'abcde-fghi-jklmn-opqrst-uvx2', '__typename': 'WelcomeEvent',
                        'title': 'Bem vindo à sua conta!',
                        'detail': 'Waldisney Santos\nBanco 260 - Nu Pagamentos S.A.\nAgência 0001\nConta 000000-1',
                        'postDate': '2017-12-18'
                    }]
                }
            }
        }
    }

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123',
              str(prepare_request_body('account_investments')))] = {
        'data': {
            'viewer': {
                'savingsAccount': {
                    'redeemableDeposits': [{
                        'id': 'vjdhausd-asdg-bgfs-vfsg-jrthfuv', 'rate': 1, 'vehicle': 'RECEIPT_DEPOSIT',
                        'openDate': '2020-07-13', 'maturityDate': '2022-07-05', 'principal': 156.52,
                        'redeemedBalance': {
                            'netAmount': 0, 'yield': 0, 'incomeTax': 0, 'iofTax': 0,
                            'id': 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123'
                        }
                    }, {
                        'id': 'abcdefhi-jklm-opqr-stuv-wyasdx', 'rate': 1, 'vehicle': 'RECEIPT_DEPOSIT',
                        'openDate': '2020-07-10', 'maturityDate': '2022-07-04', 'principal': 104.95,
                        'redeemedBalance': {
                            'netAmount': 0, 'yield': 0, 'incomeTax': 0, 'iofTax': 0,
                            'id': 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123'
                        }
                    }, {
                        'id': 'ffghjyu-ktyu-dfgn-nfgh-asdgre', 'rate': 1, 'vehicle': 'RECEIPT_DEPOSIT',
                        'openDate': '2020-08-11', 'maturityDate': '2022-08-03', 'principal': 77.77,
                        'redeemedBalance': {
                            'netAmount': 39.99, 'yield': 0.05, 'incomeTax': 0.01, 'iofTax': 0.01,
                            'id': 'sdfgehhdf-jkre-thre-nghh-kuvsnjue633'
                        }
                    }]
                }
            }
        }
    }

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123', str(prepare_request_body('account_id')))] = {
        'data': {
            'viewer': {'id': '123123123'},
            'createTransferInBoleto': {
                'boleto': {
                    'id': '123123123', 'dueDate': '2020-06-16', 'barcode': '123123132123123123123',
                    'readableBarcode': '123131321231231.2313212312.2131231.21332123', 'amount': 1231.23
                }
            }
        }
    }

    _results[('https://mocked-proxy-url/api/proxy/ghostflame_123', str(prepare_request_body('create_boleto')))] = {
        'data': {
            'viewer': {'id': '123123123'},
            'createTransferInBoleto': {
                'boleto': {
                    'id': '123123123', 'dueDate': '2020-06-16', 'barcode': '123123132123123123123',
                    'readableBarcode': '123131321231231.2313212312.2131231.21332123', 'amount': 200.5
                }
            }
        }
    }

    _results[
        ('https://mocked-proxy-url/api/proxy/ghostflame_123', str(prepare_request_body('create_money_request')))] = {
        "data": {
            "createMoneyRequest": {
                "moneyRequest": {
                    "amount": 550.0,
                    "message": None,
                    "url": "https://some.tld/path1/path2",
                    "id": "123123123123"
                }
            }
        }
    }

    _results['https://*/api/bills/*'] = {
        'bill': {
            '_links': {
                'barcode': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'},
                'boleto_email': {
                    'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'},
                'invoice_email': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/'
                                          'invoice/email'},
                'self': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst'
                                 ''}
            },
            'account_id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'auto_debit_failed': False,
            'barcode': '',
            'id': 'abcde-fghi-jklmn-opqrst-uvxz',
            'line_items': [{
                'amount': 2390,
                'category': 'Eletrônicos',
                'charges': 1,
                'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                'index': 0,
                'post_date': '2015-09-09',
                'title': 'Mercadopago Mlivre'
            }, {
                'amount': 5490,
                'category': 'Eletrônicos',
                'charges': 1,
                'href': 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz',
                'id': 'abcde-fghi-jklmn-opqrst-uvxz',
                'index': 0,
                'post_date': '2015-09-09',
                'title': 'Mercadopago Mlivre'
            }],
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

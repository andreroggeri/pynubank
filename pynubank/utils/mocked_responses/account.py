def account_balance():
    return {
        'data': {'viewer': {'savingsAccount': {'currentSavingsBalance': {'netAmount': 127.33}}}}
    }


def feed():
    return {
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


def investments():
    return {
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

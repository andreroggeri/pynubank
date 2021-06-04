from pynubank.utils.parsing import parse_pix_transaction

base_transaction = {
    "id": "12c77a49-21c2-427d-8662-beba354e8356",
    "__typename": "GenericFeedEvent",
    "title": "Transferência enviada",
    "detail": "Waldisney da Silva\nR$ 3.668,40",
    "postDate": "2021-03-24"
}


def test_should_do_nothing_with_transactions_that_arent_pix():
    transaction = base_transaction.copy()
    transaction['__typename'] = 'TransferInEvent'
    transaction['amount'] = 3429

    parsed = parse_pix_transaction(transaction)

    assert parsed['__typename'] == transaction['__typename']
    assert parsed['amount'] == transaction['amount']


def test_should_parse_inflow_pix_transaction():
    transaction = base_transaction.copy()
    transaction['title'] = 'Transferência recebida'

    parsed = parse_pix_transaction(transaction)

    assert parsed['__typename'] == 'PixTransferInEvent'
    assert parsed['amount'] == 3668.40


def test_should_parse_outflow_pix_transaction():
    transaction = base_transaction.copy()
    transaction['title'] = 'Transferência enviada'

    parsed = parse_pix_transaction(transaction)

    assert parsed['__typename'] == 'PixTransferOutEvent'
    assert parsed['amount'] == 3668.40


def test_should_parse_reversal_pix_transaction():
    transaction = base_transaction.copy()
    transaction['title'] = 'Reembolso enviado'

    parsed = parse_pix_transaction(transaction)

    assert parsed['__typename'] == 'PixTransferOutReversalEvent'
    assert parsed['amount'] == 3668.40


def test_should_parse_failed_pix_transaction():
    transaction = base_transaction.copy()
    transaction['title'] = 'Transferência falhou'

    parsed = parse_pix_transaction(transaction)

    assert parsed['__typename'] == 'PixTransferFailedEvent'
    assert parsed['amount'] == 3668.40

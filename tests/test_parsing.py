import pytest

from pynubank.utils.parsing import parse_pix_transaction, parse_float

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


@pytest.mark.parametrize(['test_value', 'expected'], [
    ('R$1,00', 1.0),
    ('R$0,01', 0.01),
    ('R$0,1', 0.1),
    ('R$1.000,20', 1000.20),
    ('R$83.120,11', 83120.11),
    ('R$9.183.120,11', 9183120.11),
    ('Projeção aproximada para 31 de Agosto de 2021, seu dinheiro renderá R$ 0,18', 0.18)
])
def test_parse_float(test_value: str, expected: float):
    result = parse_float(test_value)

    assert result == expected

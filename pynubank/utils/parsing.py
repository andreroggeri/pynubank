import re

TITLE_INFLOW_PIX = 'Transferência recebida'
TITLE_OUTFLOW_PIX = 'Transferência enviada'
TITLE_REVERSAL_PIX = 'Reembolso enviado'
TITLE_FAILED_PIX = 'Transferência falhou'

PIX_TRANSACTION_MAP = {
    TITLE_INFLOW_PIX: 'PixTransferInEvent',
    TITLE_OUTFLOW_PIX: 'PixTransferOutEvent',
    TITLE_REVERSAL_PIX: 'PixTransferOutReversalEvent',
    TITLE_FAILED_PIX: 'PixTransferFailedEvent',
}


def parse_float(value: str):
    return float(re.search(r'(?:\d*\.)*\d+,\d{1,2}', value).group().replace('.', '').replace(',', '.'))


def parse_pix_transaction(transaction: dict) -> dict:
    if transaction['__typename'] != 'GenericFeedEvent':
        return transaction

    if transaction['title'] in PIX_TRANSACTION_MAP.keys():
        transaction['__typename'] = PIX_TRANSACTION_MAP[transaction['title']]
        transaction['amount'] = parse_float(transaction['detail'])

    return transaction

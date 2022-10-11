import re

TITLE_INFLOW_PIX = 'Transferência recebida'
TITLE_OUTFLOW_PIX = 'Transferência enviada'
TITLE_REVERSAL_PIX = 'Reembolso enviado'
TITLE_FAILED_PIX = 'Transferência falhou'
TITLE_SCHEDULED_PIX = 'Transferência agendada'
TITLE_INFLOW_TED_DOC = 'Transferência recebida em processamento'

TRANSACTION_MAP = {
    TITLE_INFLOW_PIX: 'PixTransferInEvent',
    TITLE_OUTFLOW_PIX: 'PixTransferOutEvent',
    TITLE_REVERSAL_PIX: 'PixTransferOutReversalEvent',
    TITLE_FAILED_PIX: 'PixTransferFailedEvent',
    TITLE_SCHEDULED_PIX: 'PixTransferScheduledEvent',
    TITLE_INFLOW_TED_DOC: 'TransferInEvent',
}


def parse_float(value: str):
    return float(re.search(r'(?:\d*\.)*\d+,\d{1,2}', value).group().replace('.', '').replace(',', '.'))

def parse_transaction(transaction: dict) -> dict:
    if transaction['__typename'] != 'GenericFeedEvent':
        return transaction

    if transaction['title'] in TRANSACTION_MAP.keys():
        transaction['__typename'] = TRANSACTION_MAP[transaction['title']]
        transaction['amount'] = parse_float(transaction['detail'])
        if "\n" in transaction['detail']:
            split_details = transaction['detail'].split('\n')
            transaction['originAccount'] = {"name": split_details[0]}
            transaction['detail'] = split_details[1]

    return transaction

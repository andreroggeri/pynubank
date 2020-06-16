from unittest.mock import MagicMock

from qrcode import QRCode

from pynubank.nubank import Nubank
from pynubank.utils.discovery import Discovery
from pynubank.utils.http import HttpClient


def fake_update_proxy(self: Discovery):
    self.proxy_list_app_url = {
        'token': 'https://some-url/token',
        'lift': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/B'
    }
    self.proxy_list_url = {
        'login': 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/A',
    }


def test_authenticate_with_qr_code_succeeds(monkeypatch, authentication_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))

    nubank_client = Nubank()
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    assert nubank_client.feed_url == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_authenticate_with_cert(monkeypatch, authentication_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))

    nubank_client = Nubank()

    nubank_client.authenticate_with_cert('1234', 'hunter12', 'some-file.p12')

    assert nubank_client.feed_url == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_authenticate_with_refresh_token(monkeypatch, authentication_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))

    nubank_client = Nubank()

    nubank_client.authenticate_with_refresh_token('token', 'some-file.p12')

    assert nubank_client.feed_url == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_get_card_feed(monkeypatch, authentication_return, events_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=events_return))
    nubank_client = Nubank()

    feed = nubank_client.get_card_feed()
    assert feed['as_of'] == '2017-09-09T06:50:22.323Z'
    assert feed['customer_id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert feed['_links']['updates']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/updates_123'
    assert feed['_links']['next']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/next_123'

    events = feed['events']
    assert len(events) == 1
    assert events[0]['description'] == 'Shopping Iguatemi'
    assert events[0]['category'] == 'transaction'
    assert events[0]['amount'] == 700
    assert events[0]['time'] == '2017-09-09T02:03:55Z'
    assert events[0]['title'] == 'transporte'
    assert events[0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert events[0]['details']['lat'] == -12.9818258
    assert events[0]['details']['lon'] == -38.4652058
    assert events[0]['details']['subcategory'] == 'card_present'
    assert events[0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert events[0]['_links']['self']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'


def test_get_bills(monkeypatch, authentication_return, bills_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=bills_return))
    nubank_client = Nubank()

    bills = nubank_client.get_bills()

    assert len(bills) == 3
    assert bills[2]['_links']['self'][
               'href'] == "https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
    assert bills[2]['href'] == 'nuapp://bill/abcde-fghi-jklmn-opqrst-uvxz'
    assert bills[2]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bills[2]['state'] == 'overdue'

    summary = bills[2]['summary']
    assert summary["adjustments"] == "-63.99106066"
    assert summary["close_date"] == "2018-03-03"
    assert summary["due_date"] == "2018-03-10"
    assert summary["effective_due_date"] == "2018-03-12"
    assert summary["expenses"] == "364.14"
    assert summary["fees"] == "0"
    assert summary["interest"] == 0
    assert summary["interest_charge"] == "0"
    assert summary["interest_rate"] == "0.1375"
    assert summary["interest_reversal"] == "0"
    assert summary["international_tax"] == "0"
    assert summary["minimum_payment"] == 8003
    assert summary["open_date"] == "2018-02-03"
    assert summary["paid"] == 28515
    assert summary["past_balance"] == -1500
    assert summary["payments"] == "-960.47"
    assert summary["precise_minimum_payment"] == "480.02544320601300"
    assert summary["precise_total_balance"] == "285.152041645013"
    assert summary["previous_bill_balance"] == "945.473102305013"
    assert summary["remaining_minimum_payment"] == 0
    assert summary["tax"] == "0"
    assert summary["total_accrued"] == "0"
    assert summary["total_balance"] == 28515
    assert summary["total_credits"] == "-64.18"
    assert summary["total_cumulative"] == 30015
    assert summary["total_financed"] == "0"
    assert summary["total_international"] == "0"
    assert summary["total_national"] == "364.32893934"
    assert summary["total_payments"] == "-960.47"


def test_get_bill_details(monkeypatch, authentication_return, bill_details_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=authentication_return))
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=bill_details_return))
    nubank_client = Nubank()

    bill_mock = {
        '_links': {'self': {'href': 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'}}}
    bill_response = nubank_client.get_bill_details(bill_mock)

    bill = bill_response['bill']

    assert bill['_links']['barcode'][
               'href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'
    assert bill['_links']['boleto_email'][
               'href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'
    assert bill['_links']['invoice_email'][
               'href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz/invoice/email'
    assert bill['_links']['self'][
               'href'] == 'https://prod-s0-billing.nubank.com.br/api/bills/abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['account_id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['auto_debit_failed'] == False
    assert bill['barcode'] == ''
    assert bill['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['amount'] == 2390
    assert bill['line_items'][0]['category'] == 'Eletrônicos'
    assert bill['line_items'][0]['charges'] == 1
    assert bill['line_items'][0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['index'] == 0
    assert bill['line_items'][0]['post_date'] == '2015-09-09'
    assert bill['line_items'][0]['title'] == 'Mercadopago Mlivre'
    assert bill['linha_digitavel'] == ''
    assert bill['payment_method'] == 'boleto'
    assert bill['state'] == 'overdue'
    assert bill['status'] == 'paid'
    assert bill['summary']['adjustments'] == '0'
    assert bill['summary']['close_date'] == '2015-09-25'
    assert bill['summary']['due_date'] == '2015-10-10'
    assert bill['summary']['effective_due_date'] == '2015-10-13'
    assert bill['summary']['expenses'] == '78.8000'
    assert bill['summary']['fees'] == '0'
    assert bill['summary']['interest'] == 0
    assert bill['summary']['interest_charge'] == '0'
    assert bill['summary']['interest_rate'] == '0.0775'
    assert bill['summary']['interest_reversal'] == '0'
    assert bill['summary']['international_tax'] == '0'
    assert bill['summary']['late_fee'] == '0.02'
    assert bill['summary']['late_interest_rate'] == '0.0875'
    assert bill['summary']['minimum_payment'] == 7005
    assert bill['summary']['open_date'] == '2015-07-23'
    assert bill['summary']['paid'] == 7880
    assert bill['summary']['past_balance'] == 0
    assert bill['summary']['payments'] == '0'
    assert bill['summary']['precise_minimum_payment'] == '70.054500'
    assert bill['summary']['precise_total_balance'] == '78.8000'
    assert bill['summary']['previous_bill_balance'] == '0'
    assert bill['summary']['tax'] == '0'
    assert bill['summary']['total_accrued'] == '0'
    assert bill['summary']['total_balance'] == 7880
    assert bill['summary']['total_credits'] == '0'
    assert bill['summary']['total_cumulative'] == 7880
    assert bill['summary']['total_financed'] == '0'
    assert bill['summary']['total_international'] == '0'
    assert bill['summary']['total_national'] == '78.8000'
    assert bill['summary']['total_payments'] == '0'


def test_get_card_statements(monkeypatch, events_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'get', MagicMock(return_value=events_return))
    nubank_client = Nubank()

    statements = nubank_client.get_card_statements()

    assert len(statements) == 1
    assert statements[0]['description'] == 'Shopping Iguatemi'
    assert statements[0]['category'] == 'transaction'
    assert statements[0]['amount'] == 700
    assert statements[0]['time'] == '2017-09-09T02:03:55Z'
    assert statements[0]['title'] == 'transporte'
    assert statements[0]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[0]['details']['lat'] == -12.9818258
    assert statements[0]['details']['lon'] == -38.4652058
    assert statements[0]['details']['subcategory'] == 'card_present'
    assert statements[0]['href'] == 'nuapp://transaction/abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[0]['_links']['self']['href'] == 'https://prod-s0-webapp-proxy.nubank.com.br/api/proxy/_links_123'


def test_get_account_balance(monkeypatch, account_balance_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=account_balance_return))
    nubank_client = Nubank()

    balance = nubank_client.get_account_balance()

    assert balance == 127.33


def test_get_account_feed(monkeypatch, account_statements_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=account_statements_return))
    nubank_client = Nubank()

    statements = nubank_client.get_account_feed()

    assert len(statements) == 6
    assert statements[1]['id'] == 'abcde-fghi-jklmn-opqrst-uvxy'
    assert statements[1]['__typename'] == 'TransferOutReversalEvent'
    assert statements[1]['title'] == 'Transferência devolvida'
    assert statements[1]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[1]['postDate'] == '2018-03-06'

    assert statements[2]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[2]['__typename'] == 'TransferOutEvent'
    assert statements[2]['title'] == 'Transferência enviada'
    assert statements[2]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[2]['postDate'] == '2018-03-06'
    assert statements[2]['amount'] == 20.0
    assert statements[2]['destinationAccount']['name'] == 'Juquinha da Silva Sauro'


def test_get_account_statements(monkeypatch, account_statements_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=account_statements_return))
    nubank_client = Nubank()

    statements = nubank_client.get_account_statements()

    assert len(statements) == 5
    assert statements[3]['id'] == 'abcde-fghi-jklmn-opqrst-uvx1'
    assert statements[3]['__typename'] == 'TransferInEvent'
    assert statements[3]['title'] == 'Transferência recebida'
    assert statements[3]['detail'] == 'R$127.33'
    assert statements[3]['postDate'] == '2018-03-06'
    assert statements[3]['amount'] == 127.33

    assert statements[4]['id'] == 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123'
    assert statements[4]['__typename'] == 'BarcodePaymentEvent'
    assert statements[4]['title'] == 'Pagamento efetuado'
    assert statements[4]['detail'] == 'AES ELETROPAULO'
    assert statements[4]['postDate'] == '2018-02-05'
    assert statements[4]['amount'] == 169.2


def test_get_qr_code(monkeypatch):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    client = Nubank()
    uid, qr = client.get_qr_code()

    assert uid != ''
    assert isinstance(qr, QRCode)


def test_should_generate_boleto(monkeypatch, create_boleto_return):
    monkeypatch.setattr(Discovery, '_update_proxy_urls', fake_update_proxy)
    monkeypatch.setattr(HttpClient, 'post', MagicMock(return_value=create_boleto_return))
    client = Nubank()

    boleto = client.create_boleto(200.50)

    assert boleto == create_boleto_return['data']['createTransferInBoleto']['boleto']['readableBarcode']

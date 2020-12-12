import pytest
from qrcode import QRCode
from pynubank.nubank import Nubank
from pynubank import MockHttpClient
from pynubank.exception import NuMissingCreditCard


def test_authenticate_with_qr_code_succeeds():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    assert nubank_client.feed_url == 'https://mocked-proxy-url/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_authenticate_with_cert():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_cert('1234', 'hunter12', 'some-file.p12')

    assert nubank_client.feed_url == 'https://mocked-proxy-url/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_authenticate_with_refresh_token():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_refresh_token('token', 'some-file.p12')

    assert nubank_client.feed_url == 'https://mocked-proxy-url/api/proxy/events_123'
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_authenticate_with_cert_missing_credit_card():
    mock_client = MockHttpClient()
    mock_client.remove_mock_url(('https://mocked-proxy-url/api/proxy/events_123', ''))
    mock_client.remove_mock_url(('https://mocked-proxy-url/api/token', ''))

    mock_client.add_mock_url('https://mocked-proxy-url/api/proxy/magnitude_123', '', 'proxy_events')
    mock_client.add_mock_url('https://mocked-proxy-url/api/token', '', 'discovery_login_alternative')

    nubank_client = Nubank(client=mock_client)
    nubank_client.authenticate_with_cert('1234', 'hunter12', 'some-file.p12')

    assert nubank_client.feed_url == 'https://mocked-proxy-url/api/proxy/magnitude_123'
    assert nubank_client.bills_url is None
    assert nubank_client.client.get_header('Authorization') == 'Bearer access_token_123'


def test_get_card_feed():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

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


def test_get_bills_missing_credit_card():
    mock_client = MockHttpClient()
    mock_client.remove_mock_url(('https://mocked-proxy-url/api/proxy/events_123', ''))
    mock_client.remove_mock_url(('https://mocked-proxy-url/api/token', ''))

    mock_client.add_mock_url('https://mocked-proxy-url/api/proxy/magnitude_123', '', 'proxy_events')
    mock_client.add_mock_url('https://mocked-proxy-url/api/token', '', 'discovery_login_alternative')

    nubank_client = Nubank(client=mock_client)
    nubank_client.authenticate_with_cert('1234', 'hunter12', 'some-file.p12')

    with pytest.raises(NuMissingCreditCard):
        nubank_client.get_bills()


def test_get_bills():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    bills = nubank_client.get_bills()

    assert len(bills) == 3
    assert bills[2]['_links']['self'][
               'href'] == "https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz"
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


def test_get_bill_details():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    bill_mock = {
        '_links': {'self': {'href': 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz'}}}
    bill_response = nubank_client.get_bill_details(bill_mock)

    bill = bill_response['bill']

    assert bill['_links']['barcode'][
               'href'] == 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/barcode'
    assert bill['_links']['boleto_email'][
               'href'] == 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/boleto/email'
    assert bill['_links']['invoice_email'][
               'href'] == 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst-uvxz/invoice/email'
    assert bill['_links']['self'][
               'href'] == 'https://mocked-proxy-url/api/bills/abcde-fghi-jklmn-opqrst'
    assert bill['account_id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['auto_debit_failed'] == False
    assert bill['barcode'] == ''
    assert bill['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert bill['line_items'][0]['amount'] == 2390
    assert bill['line_items'][0]['category'] == 'Eletronicos'
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


def test_get_card_statements():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

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


def test_get_account_balance():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    balance = nubank_client.get_account_balance()

    assert balance == 127.33


def test_get_account_feed():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    statements = nubank_client.get_account_feed()

    assert len(statements) == 6
    assert statements[1]['id'] == 'abcde-fghi-jklmn-opqrst-uvxy'
    assert statements[1]['__typename'] == 'TransferOutReversalEvent'
    assert statements[1]['title'] == 'Transferencia devolvida'
    assert statements[1]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[1]['postDate'] == '2018-03-06'

    assert statements[2]['id'] == 'abcde-fghi-jklmn-opqrst-uvxz'
    assert statements[2]['__typename'] == 'TransferOutEvent'
    assert statements[2]['title'] == 'Transferencia enviada'
    assert statements[2]['detail'] == 'Juquinha da Silva Sauro - R$ 20,00'
    assert statements[2]['postDate'] == '2018-03-06'
    assert statements[2]['amount'] == 20.0
    assert statements[2]['destinationAccount']['name'] == 'Juquinha da Silva Sauro'


def test_get_account_statements():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    statements = nubank_client.get_account_statements()

    assert len(statements) == 5
    assert statements[3]['id'] == 'abcde-fghi-jklmn-opqrst-uvx1'
    assert statements[3]['__typename'] == 'TransferInEvent'
    assert statements[3]['title'] == 'Transferencia recebida'
    assert statements[3]['detail'] == 'R$127.33'
    assert statements[3]['postDate'] == '2018-03-06'
    assert statements[3]['amount'] == 127.33

    assert statements[4]['id'] == 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123'
    assert statements[4]['__typename'] == 'BarcodePaymentEvent'
    assert statements[4]['title'] == 'Pagamento efetuado'
    assert statements[4]['detail'] == 'AES ELETROPAULO'
    assert statements[4]['postDate'] == '2018-02-05'
    assert statements[4]['amount'] == 169.2


def test_get_account_investments_details():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    statements = nubank_client.get_account_investments_details()

    assert len(statements) == 3
    assert statements[0]['id'] == 'vjdhausd-asdg-bgfs-vfsg-jrthfuv'
    assert statements[0]['rate'] == 1
    assert statements[0]['vehicle'] == 'RECEIPT_DEPOSIT'
    assert statements[0]['openDate'] == '2020-07-13'
    assert statements[0]['maturityDate'] == '2022-07-05'
    assert statements[0]['principal'] == 156.52
    assert statements[0]['redeemedBalance']['netAmount'] == 0
    assert statements[0]['redeemedBalance']['yield'] == 0
    assert statements[0]['redeemedBalance']['incomeTax'] == 0
    assert statements[0]['redeemedBalance']['iofTax'] == 0
    assert statements[0]['redeemedBalance']['id'] == 'abcdefgh-ijkl-mnop-qrst-uvwxyz0123'

    assert statements[2]['id'] == 'ffghjyu-ktyu-dfgn-nfgh-asdgre'
    assert statements[2]['rate'] == 1
    assert statements[2]['vehicle'] == 'RECEIPT_DEPOSIT'
    assert statements[2]['openDate'] == '2020-08-11'
    assert statements[2]['maturityDate'] == '2022-08-03'
    assert statements[2]['principal'] == 77.77
    assert statements[2]['redeemedBalance']['netAmount'] == 39.99
    assert statements[2]['redeemedBalance']['yield'] == 0.05
    assert statements[2]['redeemedBalance']['incomeTax'] == 0.01
    assert statements[2]['redeemedBalance']['iofTax'] == 0.01
    assert statements[2]['redeemedBalance']['id'] == 'sdfgehhdf-jkre-thre-nghh-kuvsnjue633'


def test_get_customer():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    customer = nubank_client.get_customer()

    assert len(customer) == 39
    assert customer['cpf'] == '12312312312'
    assert customer['email'] == 'this.fake@email.com'
    assert customer['phone'] == '1122334455678'
    assert customer['name'] == 'John Doe Mary Doe'
    assert customer['billing_address_number'] == '123'
    assert customer['billing_address_line1'] == "Paulista Avenue"
    assert customer['billing_address_city'] == "São Paulo"
    assert customer['billing_address_locality'] == "Bebedouro"
    assert customer['billing_address_state'] == "SP"
    assert customer['billing_address_postcode'] == "01234567"
    assert customer['billing_address_country'] == "Brasil"


def test_get_qr_code(monkeypatch):
    nubank_client = Nubank(client=MockHttpClient())
    uid, qr = nubank_client.get_qr_code()

    assert uid != ''
    assert isinstance(qr, QRCode)


def test_should_generate_boleto():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    assert nubank_client.create_boleto(200.50) == '123131321231231.2313212312.2131231.21332123'


def test_should_create_money_request():
    nubank_client = Nubank(client=MockHttpClient())
    nubank_client.authenticate_with_qr_code('12345678912', 'hunter12', 'some-uuid')

    assert nubank_client.create_money_request(200) == 'https://some.tld/path1/path2'

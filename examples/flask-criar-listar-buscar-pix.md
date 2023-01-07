# Criar, listar e buscar pela chave utilizando Flask

Criei uma API de exemplo utilizando Flask em que é possível criar, listar e buscar a transação PIX pela chave e retornar os dados em JSON.

`pip install -U Flask`

# Como funciona?

Acesse pela url local http://127.0.0.1:5000/ e utilize os seguintes endpoints:

`/list` - Lista todas as transações.

`/create?code=123&valor=10` - Cria uma cobrança pix fornecendo o código e o valor cobrado.

`/find?code=123` - Busca a transação pela chave fornecida no create. Implementada de forma performática utilizando paginador. Se não encontrar vai até a última página e retornará vazio.

`/feed` - Lista todas as transações de forma paginada.

`/feed?cursor=ezpwcmlvcml0eSAwLCA6dGltZ...` - Lista todas as transações de forma paginada informando o cursor da última transação. Isso irá retornar os próximos registros.

Obs: Tomar cuidado com os endpoints `/list` e `/find?code=123` em contas com muitas transações. Necessário melhorias.

```python
from pynubank import Nubank
import flask
from flask import request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True

nu = Nubank()

refresh_token = nu.authenticate_with_cert('cpf', 'password', 'cert.p12')
nu.authenticate_with_refresh_token(refresh_token, 'cert.p12')

@app.route('/create', methods=['GET'])
def create():
    code = request.args.get('code')
    valor = request.args.get('valor')
    if code is None or valor is None:
        return jsonify(error="Digite o código e o valor.")
    data = nu.get_available_pix_keys()
    money_request = nu.create_pix_payment_qrcode(data['account_id'], valor, data['keys'][0], code)
    qr = money_request['qr_code']
    img = qr.make_image()
    img.save('/var/www/nubankpy/images/'+code+'.png')
    return jsonify(payment_url=money_request['payment_url'],payment_code=money_request['payment_code'])

@app.route('/list', methods=['GET'])
def list():
    transactions = nu.get_account_statements()
    newTransactions = []
    for idx,transaction in enumerate(transactions):
        tx_status = nu.get_pix_identifier(transaction['id'])
        if tx_status:
            transaction['identificador'] = tx_status
            newTransactions.append(transaction)
    return jsonify(newTransactions)

@app.route('/find', methods=['GET'])
def find():
    code = request.args.get('code')
    feed = nu.get_account_feed_paginated()
    has_next_page = feed['pageInfo']['hasNextPage']
    response = {}     

    for idx,transaction in enumerate(feed['edges']):
        tx_status = nu.get_pix_identifier(transaction['node']['id'])
        if tx_status == code:
            has_next_page = False
            response = transaction['node']
            break
    if has_next_page:
        cursor = feed['edges'][-1]['cursor']
        more_feed = nu.get_account_feed_paginated(cursor)
    return jsonify(response)

@app.route('/feed', methods=['GET'])
def feed():
    page = request.args.get('page')
    feed = nu.get_account_feed_paginated(page)    
    return jsonify(feed)
app.run()

```

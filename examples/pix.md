# Pix
Está implementado o suporte a consulta de chaves do Pix e solicitação de cobrança (QRCode).

## Solicitando um pagamento
```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_qr_code('some-cpf', 'some-password', 'some-uuid')

data = nu.get_available_pix_keys()

code = '123' #Código único da tansação é necessário para o get_pix_identifier

print(data['keys']) # Retorna lista de chaves cadastradas no Pix

print(data['account_id']) # Retorna id da sua conta

# No exemplo abaixo solicitamos uma cobrança de R$ 50,25 utilizando a primeira chave cadastrada
money_request = nu.create_pix_payment_qrcode(data['account_id'], 50.25, data['keys'][0], code)

# Irá printar o QRCode no terminal
money_request['qr_code'].print_ascii()

# Também é possível gerar uma imagem para ser enviada através de algum sistema
# Nesse caso irá salvar um arquivo qr_code.png que pode ser escaneado pelo app do banco para ser pago
# Salva o nome do arquivo com o código do identifier
qr = money_request['qr_code']
img = qr.make_image()
img.save(code+'.png')

# Além do QRCode também há uma URL para pagamento
print(money_request['payment_url'])
```

## Obtendo o identificador de uma transação

```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_qr_code('some-cpf', 'some-password', 'some-uuid')

transactions = nu.get_account_statements()

for transaction in transactions[:100]:
    tx_status = nu.get_pix_identifier(transaction['id'])
    # Poderá retornar None caso a transação não seja Pix ou não tiver identificador
    # Caso contrário retorna o identificador único que foi cadastrado no QRCode
    print(tx_status) 
```

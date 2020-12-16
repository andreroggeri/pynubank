# Pix
Está implementado o suporte a consulta de chaves do Pix e solicitação de cobrança (QRCode).

## Solicitando um pagamento
```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())

data = nu.get_available_pix_keys()

print(data['keys']) # Retorna lista de chaves cadastradas no Pix

print(data['account_id']) # Retorna id da sua conta

# No exemplo abaixo solicitamos uma cobrança de R$ 50,25 utilizando a primeira chave cadastrada
money_request = nu.create_pix_payment_qrcode(data['account_id'], 50.25, data['keys'][0])

# Irá printar o QRCode no terminal
money_request['qr_code'].print_ascii()

# Também é possível gerar uma imagem para ser enviada através de algum sistema
# Nesse caso irá salvar um arquivo qr_code.png que pode ser escaneado pelo app do banco para ser pago
qr = money_request['qr_ocde']
img = qr.make_image()
img.save('qr_code.png')

# Além do QRCode também há uma URL para pagamento
print(money_request['payment_url'])

```
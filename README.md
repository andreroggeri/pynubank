# pynubank
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynubank)
[![PyPI version](https://badge.fury.io/py/pynubank.svg)](https://badge.fury.io/py/pynubank)
[![Coverage Status](https://coveralls.io/repos/github/andreroggeri/pynubank/badge.svg?branch=master)](https://coveralls.io/github/andreroggeri/pynubank?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e550387e85d315a212af/maintainability)](https://codeclimate.com/github/andreroggeri/pynubank/maintainability)

Acesse seus extratos do Nubank pelo Python ([Baseado na versão js](https://github.com/Astrocoders/nubank-api))

## Instalação
Disponível via pip

`pip install pynubank`

## Utilizando

### Atenção !
O Nubank pode bloquear a sua conta por 72 horas caso detecte algum comportamento anormal !
Por conta disso, evite enviar muitas requisições. Se for necessário, faça um mock da resposta ou utilize o Jupyter durante o desenvolvimento para que o bloqueio não ocorra.

### Cartão de Crédito
```python
from pynubank import Nubank

nu = Nubank()
uuid, qr_code = nu.get_qr_code()
# Utilize o CPF sem pontos ou traços
nu.authenticate_with_qr_code('123456789', 'senha', uuid)

# Lista de dicionários contendo todas as transações de seu cartão de crédito
card_statements = nu.get_card_statements()

# Soma de todas as compras
print(sum([t['amount'] for t in card_statements]))

# Lista de dicionários contendo todas as faturas do seu cartão de crédito
bills = nu.get_bills()

# Retorna um dicionário contendo os detalhes de uma fatura retornada por get_bills()
bill_details = nu.get_bill_details(bills[1])
```

### NuConta
```python
from pynubank import Nubank

nu = Nubank()
uuid, qr_code = nu.get_qr_code()
# Utilize o CPF sem pontos ou traços
nu.authenticate_with_qr_code('123456789', 'senha', uuid)

# Lista de dicionários contendo todas as transações de seu cartão de crédito
account_statements = nu.get_account_statements()

# Soma de todas as transações na NuConta
# Observacão: As transações de saída não possuem o valor negativo, então deve-se olhar a propriedade "__typename".
# TransferInEvent = Entrada
# TransferOutEvent = Saída
# TransferOutReversalEvent = Devolução
print(sum([t['amount'] for t in account_statements]))

# Saldo atual
print(nu.get_account_balance())
```
### Mais exemplos
A pasta [examples](./examples/) possui mais referencias de uso com autenticação e visualização dos dados

## Testes
1. Instale os requirements
1. Execute o comando pytest

```
$ pip install -r requirements.txt
$ pip install -r requirements-test.txt

$ pytest
```

## Contribuindo

Envie sua PR para melhorar esse projeto ! 😋

# pynubank
[![Python package](https://github.com/andreroggeri/pynubank/actions/workflows/build.yml/badge.svg)](https://github.com/andreroggeri/pynubank/actions/workflows/build.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynubank)
[![PyPI version](https://badge.fury.io/py/pynubank.svg)](https://badge.fury.io/py/pynubank)
[![Coverage Status](https://coveralls.io/repos/github/andreroggeri/pynubank/badge.svg?branch=master)](https://coveralls.io/github/andreroggeri/pynubank?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e550387e85d315a212af/maintainability)](https://codeclimate.com/github/andreroggeri/pynubank/maintainability) [![Join the chat at https://gitter.im/pynubank/pynubank](https://badges.gitter.im/pynubank/pynubank.svg)](https://gitter.im/pynubank/pynubank?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Acesse seus extratos do Nubank pelo Python ([Baseado na versão js](https://github.com/Astrocoders/nubank-api))

## Instalação
Disponível via pip

`pip install pynubank`


## Autenticação
Primeiro de tudo, precisamos nos autenticar. 

Para isso, além do seu CPF e senha usuais, precisamos de um fator extra de autenticação.

Temos 3 opções disponíveis, com seus respectivos exemplos:
- [QR Code](https://github.com/andreroggeri/pynubank/blob/master/examples/login-qrcode.md) (assim como é feito no app web. Obs: permite somente acesso aos dados do cartão de crédito) 
- [Certificado](https://github.com/andreroggeri/pynubank/blob/master/examples/login-certificate.md) (assim como é feito no app mobile)
- [Certificado e Refresh Token](https://github.com/andreroggeri/pynubank/blob/master/examples/login-refresh-token.md)

Tendo seguido com sucesso uma das opções, você pode tentar um dos exemplos a seguir!

## Exemplos

> :warning:  **Atenção**: O Nubank pode bloquear a sua conta por 72 horas caso detecte algum comportamento anormal !
Por conta disso, **evite enviar muitas requisições**. Você também pode utilizar o MockHttpClient descrito abaixo.

### Realizando testes com dados falsos
Você pode utilizar este recurso para receber dados falsos para testar a sua solução sem correr riscos de ser bloqueado pelo Nubank e com tempo de resposta instantâneo. Para isso, utilize o exemplo a seguir:

```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_cert("qualquer-cpf", "qualquer-senha", "caminho/do_certificado.p12") # Essa linha funciona porque não estamos chamando o servidor do Nubank ;)

# Qualquer método chamado não passará pelo Nubank e terá o retorno instantâneo.
```


### Cartão de Crédito
```python
from pynubank import Nubank

nu = Nubank()

# Insira aqui o código para se autenticar!
# Veja a seção acima sobre autenticação para mais detalhes ;)

# Lista de dicionários contendo todas as transações de seu cartão de crédito
card_statements = nu.get_card_statements()

# Retorna um dicionário contendo os detalhes de uma transação retornada por get_card_statements()
# Contém as parcelas da transação
card_statement_details = nu.get_card_statement_details(card_statements[0])

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

# Insira aqui o código para se autenticar!
# Veja a seção acima sobre autenticação para mais detalhes ;)

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
A pasta [examples](./examples/) possui mais referencias de uso com autenticação e visualização dos dados.

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

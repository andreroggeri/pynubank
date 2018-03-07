# pynubank
[![PyPI version](https://badge.fury.io/py/pynubank.svg)](https://badge.fury.io/py/pynubank)
[![Coverage Status](https://coveralls.io/repos/github/andreroggeri/pynubank/badge.svg?branch=add-coverage-check)](https://coveralls.io/github/andreroggeri/pynubank?branch=add-coverage-check)

Acesse seus extratos do Nubank pelo Python ([Baseado na versão js](https://github.com/Astrocoders/nubank-api))

## Instalação
Disponível via pip

`pip install pynubank`

## Utilizando


#### Cartão de Crédito
```
from pynubank import Nubank

# Utilize o CPF sem pontos ou traços
nu = Nubank('123456789', 'senha') 

# Lista de dicionários contendo todas as transações de seu cartão de crédito
card_statements = nu.get_card_statements()

# Soma de todas as compras
print(sum([t['amount'] for t in card_statements])) 
```

### NuConta
```
from pynubank import Nubank

# Utilize o CPF sem pontos ou traços
nu = Nubank('123456789', 'senha') 

# Lista de dicionários contendo todas as transações de seu cartão de crédito
account_statements = nu.get_account_statements() 

# Soma de todas as transações na NuConta
# Observacão: As transações de saída não possuem o valor negativo, então deve-se olhar a propiedade "__typename".
# TransferInEvent = Entrada
# TransferOutEvent = Saída
print(sum([t['amount'] for t in account_statements])) 

# Saldo atual
print(nu.get_account_balance())
```


#### Utilizando com Pandas
```
>>> import pandas as pd
>>> from pynubank import Nubank

>>> nu = Nubank('123456789', 'senha')

>>> transactions = nu.get_account_statements()

>>> df = pd.DataFrame(transactions, columns=['time', 'amount'])
>>> df['time'] = pd.to_datetime(df['time'])
>>> df.groupby([df.time.dt.year, df.time.dt.month]).sum() # Agrupado por Ano/Mês
Year Month  Amount   
2016 6      20000
     7      20000
     8      20000
     9      20000
     10     20000
     11     40000
     12     40000
     
2017 1     100000
     2      20000
     3      30000
     4      35000
     5      12000
     6      22000
     
>>> df.groupby([df.title]).sum() # Agrupado por categoria
title         amount
casa           13000
eletrônicos   123000
lazer          32800
outros        100000
restaurante    98505
saúde           3435
serviços      456785
supermercado   45621
transporte    489152
vestuário      45612
viagem         78456

```

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
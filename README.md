# pynubank
Acesse seus extratos do Nubank pelo Python ([Baseado na versão js](https://github.com/Astrocoders/nubank-api))

## Instalação
Disponível via pip

`pip install pynubank`

## Utilizando


#### Básico
```
from pynubank import Nubank

nu = Nubank('123456789', 'senha') # Utilize o CPF sem pontos ou traços
stmts = nu.get_account_statements() # Retorna uma lista de dicionários contendo todas as transações

sum([stmt['amount'] for stmt in stmts['transactions']]) # Soma de todas as compras
```

#### Utilizando com Pandas
```
import pandas as pd
from pynubank import Nubank

nu = Nubank('123456789', 'senha')
transactions = nu.get_account_statements()['transactions']

df = pd.DataFrame(transactions, columns=['time', 'amount'])
df['time'] = pd.to_datetime(df['time'])
df.groupby([df.time.dt.year, df.time.dt.month]).sum() # Agrupado por Ano/Mês
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

```


## Contribuindo

Envie sua PR para melhorar esse projeto ! 😋
# Análisando os dados
O Nubank retorna todos os dados em formato JSON, para visualizar as informações disponíveis basta printar o resultado de algum método.

Os exemplos abaixo utilizam as bibliotecas `pandas` e `matplotlib` para fazer a visualização dos dados.

```python
from pynubank import Nubank

nu = Nubank()
# Assumindo que você já fez a autenticação aqui

# Assim é possível ver todos os dados
print(nu.get_card_statements())
```

## Gastos por categoria
O Nubank faz uma categorização dos gastos, sendo possível agrupar essas informações e gerar um gráfico com a biblioteca `matplotlib`

```python
from pynubank import Nubank
import pandas as pd
nu = Nubank()
# Assumindo que você já fez a autenticação aqui

# Recupera as compras feitas no cartão
transactions = nu.get_card_statements()

# Agrupa pelo campo "title" que é a categoria e soma os valores
df = pd.read_json(transactions).groupby(['title']).sum()

# Plota o gráfico baseado no campo amount
df['amount'].plot.pie(figsize=(6, 6), autopct='%.2f')
```

Resultado:

![Gráfico de Gasto por Categoria](./img/category-chart.PNG)

## Evolução do Saldo da Nuconta
Podemos fazer o acompanhamento da evolução do saldo da NuConta somando o campo amount.

```python
from pynubank import Nubank
import pandas as pd
nu = Nubank()
# Assumindo que você já fez a autenticação aqui

# Recupera as transações da NuConta
transactions = nu.get_account_statements()

IN_EVENT = 'TransferInEvent'

# Transformamos os valores que não são TransferInEvent em negativo
# Para que a soma seja feita corretamente
def transform_value(transaction):
    if transaction.get('__typename') != IN_EVENT:
        transaction['amount'] = transaction['amount'] * -1
    return transaction

transactions = list(map(transform_value, transactions))

# Transforma as transações num DataFrame
df = pd.DataFrame(transactions)

# Faz parse do campo postDate para podermos agrupar por mês
df['postDate'] = pd.to_datetime(df['postDate'])
df.index = df.postDate

# Inverte a ordem do DataFrame para que fique na ordem crescente
df = df.iloc[::-1]

# Agrupa por mês e faz a soma cumulativa dos dados
df.groupby(pd.Grouper(freq='M')).cumsum().plot()
```

Resultado:

![Gráfico de Gasto por Categoria](./img/balance-evolution.PNG)
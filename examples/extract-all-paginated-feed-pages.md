# Feed paginado

O Nubank fez uma nova implementação do feed da NuConta onde é possível obter as transações e eventos de forma paginada.

Isso foi feito por motivos de performance. Algumas contas com milhares de transações estavam lentas ou falhavam na hora
de obter os registros.

Essa implementação está no método `get_account_feed_paginated`.

## Utilização

```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_cert('some-cpf', 'some-pass', 'cert-path')

# A variável feed conterá a página atual com as transações
feed = nu.get_account_feed_paginated()
```

## Buscando mais páginas

```python
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_cert('some-cpf', 'some-pass', 'cert-path')

# A variável feed conterá a página atual 
feed = nu.get_account_feed_paginated()

# hasNextPage contém um boleano indicando se há uma nova página
has_next_page = feed['pageInfo']['hasNextPage']

if has_next_page:
    # Toda transação retorna um "cursor"
    # Esse cursor pode ser passado como parâmetro para a função para recuperar mais transações após o cursor
    # Aqui estamos recuperando o cursor da última transação retornada
    cursor = feed['edges'][-1]['cursor']

    # Aqui recuperamos a próxima página
    more_feed = nu.get_account_feed_paginated(cursor)
```

## Buscando todas as páginas

```python
import json
from pynubank import Nubank, MockHttpClient

nu = Nubank(MockHttpClient())
nu.authenticate_with_cert('some-cpf', 'some-pass', 'cert-path')

has_next_page = True
current_page_number = 1
cursor = None

# A lógica abaixo irá recuperar todas as páginas
# E salvar em arquivos sequenciais como feed_1.json, feed_2.json, etc
while has_next_page:
    feed = nu.get_account_feed_paginated(cursor)

    with open(f'feed_{current_page_number}.json', 'w') as f:
        json.dump(feed, f)

    has_next_page = feed['pageInfo']['hasNextPage']
    cursor = feed['edges'][-1]['cursor']
    current_page_number += 1
```
# Autenticação por Token com certificado
Uma vez gerado o certificado e feito o login uma vez o login com usuário e senha, é possível utilizar o próprio token para fazer login no Nubank

```python
from pynubank import Nubank

nu = Nubank()

# O Refresh token pode ser utilizado para fazer logins futuros (Sem senha)
refresh_token = nu.authenticate_with_cert('123456789', 'senha', 'caminho/do_certificado.p12')

# Numa futura utilização é possível fazer o login só com o token
nu.authenticate_with_refresh_token(refresh_token, 'caminho/do_certificado.p12')

print(nu.get_account_balance())
```
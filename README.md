# Entra ID Attribute Pipeline

Automatize a extração, análise e aplicação de atributos personalizados no Entra ID com Microsoft Graph API.

## Pré-requisitos

- Python 3.10+
- Service Principal com permissões para custom security attributes
- Registro da aplicação com `client_id`, `client_secret`, `tenant_id`

## Execução Local

1. Clone o repositório
2. Crie `.env` com base no `.env.template`
3. Instale dependências: `pip install -r requirements.txt`
4. Execute: `python main.py`

## Execução via GitHub Actions

Configure os segredos:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `TENANT_ID`

E dispare o workflow `Executar Pipeline`.

## Scripts

| Script | Função |
|--------|--------|
| 01 | Extrai usuários e SPs com atributos para CSV |
| 02 | Extrai definição dos atributos customizados |
| 03 | Faz match entre SPs e atributos |
| 04 | Aplica os atributos com PATCH |

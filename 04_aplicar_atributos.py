import json
import requests
import msal
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env


# Config
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://graph.microsoft.com/.default']

def obter_token():
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )
    token_result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in token_result:
        raise Exception(f"Erro ao obter token: {token_result.get('error_description')}")
    return token_result["access_token"]

access_token = obter_token()
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Carregar matches
with open("matches_sp_atributos.json", encoding="utf-8") as f:
    matches = json.load(f)

# Carregar SPs que já possuem atributos
with open("sps_with_attrs.csv", encoding="utf-8") as f:
    sp_com_atributos_ids = [linha.split(",")[0].strip('"') for linha in f.read().splitlines()[1:]]

# Carregar atributos customizados e montar dicionário de referência
with open("atributos_customizados.json", encoding="utf-8") as f:
    atributos_raw = json.load(f)[0]  # Lista dentro de lista
    mapa_atributos = {attr["name"]: attr["attributeSet"] for attr in atributos_raw}

# Função para aplicar PATCH
def aplicar_atributo(sp_id, attribute_set, nome_atributo):
    url = f"https://graph.microsoft.com/beta/servicePrincipals/{sp_id}"
    body = {
        "customSecurityAttributes": {
            attribute_set: {
                "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
                nome_atributo: [nome_atributo]
            }
        }
    }
    response = requests.patch(url, headers=headers, json=body)
    return response.status_code, response.text

# Aplicar atributos
aplicados = 0
for match in matches:
    sp_nome = match["servicePrincipal"]
    nome_atributo = match["atributoEncontrado"]

    attribute_set = mapa_atributos.get(nome_atributo)
    if not attribute_set:
        print(f"[✗] Atributo '{nome_atributo}' não encontrado no dicionário. Ignorando.")
        continue

    # Buscar SP
    query = f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=displayName eq '{sp_nome}'&$select=id"
    res = requests.get(query, headers=headers)
    if res.status_code == 200 and res.json()["value"]:
        sp_id = res.json()["value"][0]["id"]
        if sp_id not in sp_com_atributos_ids:
            status, texto = aplicar_atributo(sp_id, attribute_set, nome_atributo)
            if status == 204:
                print(f"[¬] '{nome_atributo}' aplicado à SP '{sp_nome}' (Set: {attribute_set})")
                aplicados += 1
            else:
                print(f"[X] Erro aplicando '{nome_atributo}' em '{sp_nome}': {status} - {texto}")
        else:
            print(f"[~] SP '{sp_nome}' já possui atributo(s), ignorando.")
    else:
        print(f"[!] SP '{sp_nome}' não encontrada.")

print(f"\n Total de atributos aplicados: {aplicados}")

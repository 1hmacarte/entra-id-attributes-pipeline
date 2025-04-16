
import requests
import json
import csv
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env


# Config
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")

authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://graph.microsoft.com/.default']
graph_endpoint = 'https://graph.microsoft.com/v1.0'

# AUTH
app = ConfidentialClientApplication(
    client_id=client_id,
    authority=authority,
    client_credential=client_secret
)

token_result = app.acquire_token_for_client(scopes=scope)

if "access_token" not in token_result:
    print("Erro ao obter token:")
    print(token_result.get("error_description"))
    exit()

access_token = token_result['access_token']
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

with open("token.txt", "w") as f:
    f.write(access_token)


# Get attributes name
print("Obtendo definições de atributos personalizados...")

attr_url = f'{graph_endpoint}/directory/customSecurityAttributeDefinitions'
attr_response = requests.get(attr_url, headers=headers)

if attr_response.status_code != 200:
    print("Erro ao extrair atributos:", attr_response.status_code)
    print(attr_response.text)
    exit()

definitions = attr_response.json().get('value', [])

# Mapeia atributos por nome_lower → nome_original
atributos_dict = {}

for atributo in definitions:
    nome_original = atributo.get('name', '')
    nome_lower = nome_original.lower()
    if nome_original:
        atributos_dict[nome_lower] = nome_original

print(f"Atributos coletados: {list(atributos_dict.values())}")

# Get SERVICE PRINCIPALS
print("Buscando Service Principals...")

sp_url = f"{graph_endpoint}/servicePrincipals?$select=id,displayName&$top=100"
service_principals = []

while sp_url:
    sp_response = requests.get(sp_url, headers=headers)
    if sp_response.status_code != 200:
        print("Erro ao obter SPs:", sp_response.status_code)
        break
    data = sp_response.json()
    service_principals.extend(data.get('value', []))
    sp_url = data.get('@odata.nextLink')

# Verifica correspondências entre nomes de SP e atributos
print("Verificando correspondências entre nomes de SP e atributos...")

matches = []

for sp in service_principals:
    nome_sp = sp.get("displayName", "").lower()
    for atributo_lower, nome_original in atributos_dict.items():
        if atributo_lower in nome_sp:
            matches.append({
                "servicePrincipal": sp["displayName"],
                "atributoEncontrado": nome_original  # Agora transmitindo para o nome correto
            })

# Salvar resultados
with open("matches_sp_atributos.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=2, ensure_ascii=False)

with open("matches_sp_atributos.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ['servicePrincipal', 'atributoEncontrado']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in matches:
        writer.writerow(row)

print(f"\n{len(matches)} correspondências encontradas. Salvo em 'matches_sp_atributos.json' e .csv.")






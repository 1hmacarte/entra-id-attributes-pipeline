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
user_id = client_id  # or user object id

authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://graph.microsoft.com/.default']
graph_endpoint = 'https://graph.microsoft.com/v1.0'


#Auth
app = ConfidentialClientApplication(
    client_id=client_id,
    authority=authority,
    client_credential=client_secret
)

token_result = app.acquire_token_for_client(scopes=scope)

if "access_token" not in token_result:
    print(" Erro ao obter token:")
    print(token_result.get("error_description"))
    exit()

access_token = token_result['access_token']
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}


# attributes set extract
print("Extraindo definições de atributos personalizados...")

url = f'{graph_endpoint}/directory/customSecurityAttributeDefinitions'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    definitions = response.json().get('value', [])

    atributos_extraidos = [definitions] #before set [definitions] the result was null

    for attr_set in definitions:
        conjunto_nome = attr_set['id']
        print(f"\n Conjunto: {conjunto_nome}")

        for atributo in attr_set.get('attributes', []):
            nome = atributo['name']
            tipo = atributo['type']
            valores_permitidos = atributo.get('use_pre_defined_values_only', [])
            required = atributo.get('isRequired', False)

            print(f" - Atributo: {nome}")
            print(f"   Tipo: {tipo}")
            print(f"   Obrigatório: {required}")
            if valores_permitidos:
                print(f"   Valores permitidos: {valores_permitidos}")

            atributos_extraidos.append({
                "conjunto": conjunto_nome,
                "nome": nome,
                "tipo": tipo,
                "obrigatorio": required,
                "valores_permitidos": valores_permitidos
            })

    # Json save
    with open('atributos_customizados.json', 'w', encoding='utf-8') as f:
        json.dump(atributos_extraidos, f, indent=2, ensure_ascii=False)
    print("\n Extração concluída e salva em 'atributos_customizados.json'.")


else:
    print(f" Erro ao extrair atributos: {response.status_code}")
    print(response.text)
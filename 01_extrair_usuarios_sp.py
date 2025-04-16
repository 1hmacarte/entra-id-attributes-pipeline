import requests
import json
import msal
from msal import ConfidentialClientApplication
import csv
import io
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env


# Config
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]


# Auth
app = ConfidentialClientApplication(
   client_id,
   authority=authority,
   client_credential=client_secret
)
token = app.acquire_token_for_client(scopes=scopes)

# Check if authentication was successful
if "access_token" in token:
   access_token = token["access_token"]
   headers = {
       "Authorization": f"Bearer {access_token}",#declaração de tipo de token oauth2
       "Content-Type": "application/json"
   }
else:
   print(f"Authentication failed: {token.get('error_description')}")

   exit()

print(token)




# Helper to get all pages
def get_all_pages(url):
    results = []
    while url:
        res = requests.get(url, headers=headers)
        data = res.json()
        results.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return results


# Query users (include aboutMe or description)
print("Fetching users...")
user_url = "https://graph.microsoft.com/beta/users?$select=id,displayName,customSecurityAttributes"
users = get_all_pages(user_url)
users_with_attrs = [u for u in users if "customSecurityAttributes" in u and u["customSecurityAttributes"]]
# Query service principals (include notes)
print("Fetching service principals...")
sp_url = "https://graph.microsoft.com/beta/servicePrincipals?$select=id,displayName,customSecurityAttributes,notes"
sps = get_all_pages(sp_url)
sps_with_attrs = [sp for sp in sps if "customSecurityAttributes" in sp and sp["customSecurityAttributes"]]
# Output
print("\n[+] Users with custom security attributes:")
for u in users_with_attrs:
   print(f" - {u['displayName']} ({u['id']})")
   print(f"    Custom Attrs: {u['customSecurityAttributes']}")
   print(f"    AboutMe: {u.get('aboutMe', 'N/A')}")
print("\n[+] Service Principals with custom security attributes:")
for sp in sps_with_attrs:
   print(f" - {sp['displayName']} ({sp['id']})")
   print(f"    Custom Attrs: {sp['customSecurityAttributes']}")
   print(f"    Notes: {sp.get('notes', 'N/A')}")
# Export Users to CSV
with open("users_with_attrs.csv", mode="w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["id", "displayName", "customSecurityAttributes", "aboutMe"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user in users_with_attrs:
        writer.writerow({
            "id": user["id"],
            "displayName": user["displayName"],
            "customSecurityAttributes": json.dumps(user.get("customSecurityAttributes", {})),
            "aboutMe": user.get("aboutMe", "")
        })

# Export Service Principals to CSV
with open("sps_with_attrs.csv", mode="w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["id", "displayName", "customSecurityAttributes", "notes"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for sp in sps_with_attrs:
        writer.writerow({
            "id": sp["id"],
            "displayName": sp["displayName"],
            "customSecurityAttributes": json.dumps(sp.get("customSecurityAttributes", {})),
            "notes": sp.get("notes", "")
        })

print("\n[-] Dados exportados para CSV.")

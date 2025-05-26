import msal
import requests
import time

CLIENT_ID = 'db8114f1-02f2-40ae-a325-53dd5048df94'
TENANT_ID = 'e9d15e4b-1505-4712-b677-9ae67f2592d5'

SCOPES = ["Files.ReadWrite.All"]

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

token_cache = None
access_token = None
token_expiry = 0

def get_access_token():
    global token_cache, access_token, token_expiry

    # Se o token ainda for válido, retorna ele
    if access_token and time.time() < token_expiry - 60:
        return access_token

    # Inicia o device flow para login (uma vez)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Não conseguiu iniciar o fluxo de device code")

    print(flow["message"])  # instruções para o usuário entrar no link e usar o código

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        access_token = result["access_token"]
        # Expira em result['expires_in'] segundos (normalmente 3600)
        token_expiry = time.time() + int(result['expires_in'])
        return access_token
    else:
        raise Exception(f"Erro ao adquirir token: {result.get('error')} - {result.get('error_description')}")

def upload_onedrive(file_content, nome_arquivo):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{nome_arquivo}:/content"

    response = requests.put(upload_url, headers=headers, data=file_content)

    if response.status_code in (200, 201):
        # Retorna True e a URL do arquivo no OneDrive
        return True, response.json().get('webUrl', '')
    else:
        return False, response.text
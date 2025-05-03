import requests
import base64
from urllib.parse import urlencode
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, SCOPES

def get_authorization_url(state_token):
    query_params = urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state_token,
    })
    print(f"{AUTH_URL}?{query_params}")
    return f"{AUTH_URL}?{query_params}"

def get_token(code, company):
    # Construct the Basic Auth header
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    basic_auth = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(f"https://{company}{TOKEN_URL}", headers=headers, data=data)
    response.raise_for_status()
    return response.json()

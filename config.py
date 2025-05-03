from dotenv import load_dotenv
load_dotenv()
import os

CLIENT_ID = os.getenv("NETSUITE_CLIENT_ID")
CLIENT_SECRET = os.getenv("NETSUITE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://system.netsuite.com/app/login/oauth2/authorize.nl"
TOKEN_URL = ".suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
SCOPES = "rest_webservices"

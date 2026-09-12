import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MS_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
TENANT = os.getenv("MS_TENANT", "organizations")
SESSION_SECRET = os.getenv("SESSION_SECRET")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN", "mymail.mapua.edu.ph")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Microsoft publishes its login endpoints at this URL — Authlib reads it automatically
METADATA_URL = f"https://login.microsoftonline.com/{TENANT}/v2.0/.well-known/openid-configuration"
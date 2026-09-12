from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from app import config

oauth = OAuth()
oauth.register(
    name="microsoft",
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    server_metadata_url=config.METADATA_URL,
    client_kwargs={"scope": "openid email profile"},
)


def is_mapua_account(email: str) -> bool:
    """Only allow official Mapua student/staff accounts."""
    return bool(email) and email.lower().endswith("@" + config.ALLOWED_DOMAIN.lower())


def get_current_user(request: Request):
    """Returns the logged-in user dict, or None if not logged in."""
    return request.session.get("user")

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app import config
from app.auth import oauth, is_mapua_account, get_current_user

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.SESSION_SECRET)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    if get_current_user(request):
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.get("/auth/login")
async def login(request: Request):
    # Sends the user to Microsoft's sign-in page
    return await oauth.microsoft.authorize_redirect(request, config.REDIRECT_URI)


@app.get("/auth/callback")
async def callback(request: Request):
    # Microsoft sends the user back here after they sign in
    try:
        token = await oauth.microsoft.authorize_access_token(request)
    except Exception:
        return templates.TemplateResponse(
            request, "login.html", {"error": "Sign-in failed. Please try again."}
        )

    claims = token.get("userinfo") or {}
    email = claims.get("email") or claims.get("preferred_username", "")

    # THE DOMAIN GATE — this is what restricts access to Mapua accounts
    if not is_mapua_account(email):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": f"Only @{config.ALLOWED_DOMAIN} accounts are allowed."},
        )

    request.session["user"] = {"email": email, "name": claims.get("name", email)}
    return RedirectResponse("/dashboard")


@app.get("/dashboard")
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/")   # protected route
    return templates.TemplateResponse(request, "dashboard.html", {"user": user})


@app.get("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


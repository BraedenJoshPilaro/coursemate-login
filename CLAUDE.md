# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows (source .venv/bin/activate elsewhere)
pip install -r requirements.txt
cp .env.example .env              # then fill in MS_CLIENT_ID, MS_CLIENT_SECRET, SESSION_SECRET

uvicorn app.main:app --reload     # serves on http://localhost:8000
```

Run from the repo root: `app/main.py` mounts `app/static` and `app/templates` via relative paths. The README's `python -m app.main` won't start a server, because `main.py` has no `uvicorn.run` entry point.

There are no tests, linter, or build step configured.

## Architecture

A small FastAPI app that signs users in with Microsoft Entra ID (OAuth2/OIDC via Authlib) and only lets in accounts from the Mapua email domain.

- `app/config.py` loads `.env` with python-dotenv and exposes module-level constants. `METADATA_URL` is built from `MS_TENANT` (default `organizations`, meaning any work/school tenant). Authlib uses it to discover Microsoft's endpoints.
- `app/auth.py` registers the `oauth.microsoft` client (scopes `openid email profile`) and holds `is_mapua_account` (suffix check against `ALLOWED_DOMAIN`, default `mymail.mapua.edu.ph`) and `get_current_user`.
- `app/main.py` has the routes. Flow: `/` → `/auth/login` (redirect to Microsoft) → `/auth/callback` (exchange the code, read `email` or `preferred_username` from the ID token's `userinfo`, apply the domain gate) → `/dashboard`. `/auth/logout` clears the session.

Key points:
- **Session state lives in Starlette's `SessionMiddleware`**, a signed cookie keyed by `SESSION_SECRET`. The logged-in user is `request.session["user"] = {"email", "name"}`. Authlib also keeps the OAuth state/nonce in this session between login and callback, so the middleware is required for the OAuth flow itself.
- **Access control is enforced only by the domain gate in `/auth/callback`**, plus per-route `get_current_user` checks that redirect to `/`. There is no dependency/decorator. New protected routes must do this check themselves.
- `REDIRECT_URI` must match the redirect URI registered in the Azure app registration exactly.
- Errors are shown by re-rendering `login.html` with an `error` context variable. Templates extend `base.html`.

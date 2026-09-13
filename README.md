# Mapua Chat Login

A FastAPI web app that lets users sign in with their Microsoft account. Only official Mapua accounts (`@mymail.mapua.edu.ph` by default) are allowed in.

## Features

- Microsoft sign-in (OAuth 2.0 / OpenID Connect) using Authlib
- Only accounts from the allowed email domain can sign in; anyone else sees an error on the login page
- Signed session cookie that keeps users logged in
- Protected dashboard page and a logout route

## Tech Stack

- Python, FastAPI, Uvicorn
- Authlib (Microsoft identity platform)
- Starlette `SessionMiddleware`
- Jinja2 templates

## Prerequisites

- Python 3
- An app registration in Microsoft Entra ID (Azure portal) with:
  - A client ID and client secret
  - A web redirect URI that matches `REDIRECT_URI` (e.g. `http://localhost:8000/auth/callback`)

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate it:
   ```bash
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in the values (see below).
5. Run the app from the project root:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Open http://localhost:8000.

## Environment Variables

| Variable           | Description                                                        | Default               |
| ------------------ | ------------------------------------------------------------------ | --------------------- |
| `MS_CLIENT_ID`     | Application (client) ID from the Azure app registration            | —                     |
| `MS_CLIENT_SECRET` | Client secret from the Azure app registration                      | —                     |
| `MS_TENANT`        | Tenant used for sign-in (`organizations` = any work/school account) | `organizations`       |
| `SESSION_SECRET`   | Random string used to sign the session cookie                      | —                     |
| `ALLOWED_DOMAIN`   | Email domain allowed to sign in                                    | `mymail.mapua.edu.ph` |
| `REDIRECT_URI`     | OAuth callback URL; must match the Azure registration exactly      | —                     |

## Routes

| Route            | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| `/`              | Login page (redirects to `/dashboard` if already signed in)         |
| `/auth/login`    | Redirects to Microsoft's sign-in page                               |
| `/auth/callback` | Handles Microsoft's response, checks the email domain, starts the session |
| `/dashboard`     | Protected page for signed-in users                                  |
| `/auth/logout`   | Clears the session and returns to `/`                               |

## Project Structure

```
mapua-chat-login/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app, middleware, and routes
│   ├── auth.py            # Microsoft OAuth client and domain check
│   ├── config.py          # Loads settings from .env
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── login.html
│       └── dashboard.html
├── .env.example
├── requirements.txt
├── CLAUDE.md
└── README.md
```

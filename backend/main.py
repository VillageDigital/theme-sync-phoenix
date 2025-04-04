from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import os
from dotenv import load_dotenv

# ✅ Firestore
from google.cloud import firestore

# ✅ Load .env variables (Shopify credentials)
load_dotenv()

# ✅ Use absolute path to Firestore key in root directory
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("firestore-key.json")

# ✅ Initialize FastAPI and Firestore
app = FastAPI()
db = firestore.Client()

# 🔑 Shopify credentials
SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "28e9c04efaacc63a04075ed0fcfe8918")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "91ae31c88d82aed57030e1dee76fd895")

@app.get("/")
def root():
    return RedirectResponse(url="/app")

@app.get("/auth")
def auth(shop: str):
    redirect_uri = "https://village-digital-themesync.ngrok.app/api/auth/callback"

    install_url = (
        f"https://{shop}/admin/oauth/authorize?"
        f"client_id={SHOPIFY_CLIENT_ID}&scope=read_themes,write_themes,read_products&"
        f"redirect_uri={redirect_uri}&state=123456&grant_options[]=per-user"
    )
    return RedirectResponse(url=install_url)

@app.get("/api/auth/callback")
async def auth_callback(request: Request):
    params = dict(request.query_params)
    code = params.get("code")
    hmac = params.get("hmac")
    shop = params.get("shop")
    state = params.get("state")

    if not code or not shop:
        return {"error": "Missing code or shop."}

    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": SHOPIFY_CLIENT_ID,
        "client_secret": SHOPIFY_CLIENT_SECRET,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, json=payload)
        token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "Token exchange failed.", "details": token_data}

    # ✅ Save to Firestore under "sessions" collection
    db.collection("sessions").document(shop).set({
        "access_token": access_token
    })

    return {
        "message": "✅ Access token received and stored!",
        "shop": shop,
        "access_token": access_token
    }
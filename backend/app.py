from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret key in production

# Onshape OAuth settings
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "http://localhost:5000/callback"  # Change when hosting externally
AUTH_URL = "https://oauth.onshape.com/oauth/authorize"
TOKEN_URL = "https://oauth.onshape.com/oauth/token"

@app.route("/")
def home():
    return redirect("index.html")  # Redirect to your hosted GitHub Pages

@app.route("/login")
def login():
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "read"  # Adjust scope as needed
    }
    return redirect(f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=read")

@app.route("/callback")
def callback():
    if "error" in request.args:
        return f"Error: {request.args['error']}"

    auth_code = request.args.get("code")
    if not auth_code:
        return "Missing authorization code"

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code == 200:
        session["access_token"] = response.json()["access_token"]
        return "Login successful! You can now use the API."
    else:
        return f"Token request failed: {response.text}"

if __name__ == "__main__":
    app.run(debug=True, port=5000)

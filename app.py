from flask import Flask, session, redirect, request, render_template, url_for
import secrets
from auth import get_authorization_url, get_token

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def home():
    if "access_token" in session:
        return f"""
            <h2>You're logged in via NetSuite!</h2>
            <p>Access Token (partial): {session['access_token'][:10]}...</p>
            <a href='/logout'>Logout</a>
        """
    return render_template("home.html")

@app.route("/login")
def login():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state
    return redirect(get_authorization_url(state))

@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"OAuth Error: {error}"

    code = request.args.get("code")
    state = request.args.get("state")
    company = request.args.get("company")

    if state != session.get("oauth_state"):
        return "Invalid state parameter", 400

    try:
        token_data = get_token(code, company)
        session["access_token"] = token_data["access_token"]
        session["refresh_token"] = token_data.get("refresh_token")
        session["token_type"] = token_data["token_type"]
        session["expires_in"] = token_data["expires_in"]
        return redirect(url_for("home"))
    except Exception as e:
        return f"Token exchange failed: {e}", 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)

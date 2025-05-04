from flask import Flask, session, redirect, request, render_template, url_for
import secrets
from auth import get_authorization_url, get_token
from database import get_lessons
import json
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def home():
    if "access_token" in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    lessons = get_lessons()
    return render_template("dashboard.html", lessons=lessons)

@app.route("/login", methods=["GET", "POST"])
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
        session["suiteql_endpoint"] = f"https://{company}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"
        return redirect(url_for("home"))
    except Exception as e:
        return f"Token exchange failed: {e}", 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    lesson = get_lessons(lesson_id)
    if len(lesson) == 0:
        return render_template("404.html"), 404
    lesson = lesson[0]
    if not lesson["id"] == 1 and "access_token" in session:
        lesson.update({"show_editor": True})
    return render_template("lesson.html", lesson=lesson)

@app.route("/run-query", methods=["POST"])
def run_query():
    user_query = request.json.get("query", "")
    headers = {
        "Authorization": f"Bearer {session.get("access_token")}",
        "Content-Type": "application/json",
        "Prefer": "transient"
    }
    payload = { "q": user_query }
    try:
        response = requests.post(session.get("suiteql_endpoint"), headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        results = [{k: v for k, v in item.items() if k != 'links'} for item in response.json()["items"]]
        print(results)
        return {"success": True, "results": results}
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
            "details": getattr(e.response, "text", None)
        }

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html") , 404
    
if __name__ == "__main__":
    app.run(debug=True)

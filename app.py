from flask import Flask, session, redirect, request, render_template, url_for
import secrets
from auth import get_authorization_url, get_token
from database import get_lessons

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def home():
    if "access_token" in session:
        lessons = get_lessons()
        return redirect(render_template("dashboard.html", lessons=lessons))
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
    if not lesson["id"] == 1:
        lesson.update({"show_editor": True})
    return render_template("lesson.html", lesson=lesson)

@app.route("/run-query/<int:lesson_id>", methods=["POST"])
def run_query(lesson_id):
    #TODO: Query Netsuite with SuiteQL
    return {"success": False, "error": "Not implemented"}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html") , 404
    
if __name__ == "__main__":
    app.run(debug=True)

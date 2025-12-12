from flask import Flask, request, redirect, url_for
from Controls.BaseControl import BaseController
from Controls.AdminControl import admin_bp
from Controls.UserControl import user_bp

app = Flask(__name__, template_folder="Design")
app.secret_key = "supersecret"

base_ctrl = BaseController()

# ---------------- Register Blueprints ----------------
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

# ---------------- HOME / LOGIN & SIGNUP ----------------
@app.route("/", methods=["GET"])
def index():
    if base_ctrl.is_logged_in():
        user_type = base_ctrl.get_user_type()
        if user_type == "admin":
            return redirect(url_for("admin.dashboard"))
        elif user_type == "user":
            return redirect(url_for("user.user_dashboard"))

    show_signup = request.args.get("signup") == "1"
    return base_ctrl.render("Login.html", signup=show_signup)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    return base_ctrl.handle_login()

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    return base_ctrl.handle_signup()

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    base_ctrl.logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

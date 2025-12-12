from flask import Blueprint, session
from Controls.BaseControl import BaseController
from functools import wraps

user_controller = BaseController()
user_bp = Blueprint("user", __name__, url_prefix="/user")

# --- User login required decorator ---
def user_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not user_controller.is_logged_in() or user_controller.get_user_type() != "user":
            return redirect("/")
        return f(*args, **kwargs)
    return decorated

@user_bp.route("/dashboard")
@user_login_required
def user_dashboard():
    username = session["user"]["username"]
    return user_controller.render("UserDashboard.html", username=username)

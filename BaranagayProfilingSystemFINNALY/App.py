from flask import Flask, request, redirect, session, flash
from Controls.BaseControl import BaseController
from Controls.BarangayProfileBE import user_bp  # Blueprint for user routes

# ------------------- App Setup -------------------
app = Flask(
    __name__,
    template_folder="Design",  # Templates folder
    static_folder="static"     # Static folder
)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret key

# Base controller instance
base = BaseController()

# ------------------- Register Blueprint -------------------
app.register_blueprint(user_bp)  # Registers all /user routes

# ------------------- Routes -------------------

@app.route("/", methods=["GET", "POST"])
def login():
    """
    Handle login page and signup page display.
    Redirect already logged-in users to dashboard.
    """
    # Redirect if already logged in
    if base.is_logged_in():
        return redirect("/user/dashboard")

    signup = request.args.get("signup", "0") == "1"

    if request.method == "POST":
        if signup:
            # Handle user signup
            return base.handle_signup()
        else:
            # Handle user login
            return base.handle_login()

    # Render login page
    return base.render("Login.html", signup=signup)


@app.route("/logout")
def logout():
    """
    Logs out the current user and redirects to login page.
    """
    base.logout_user()
    flash("Logged out successfully.", "success")
    return redirect("/")


# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True)

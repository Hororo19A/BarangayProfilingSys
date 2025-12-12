from flask import render_template, session, request, redirect, url_for, flash
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="temporary"
    )

class BaseController:

    # ---------- RENDER ----------
    def render(self, template_name, **kwargs):
        return render_template(template_name, **kwargs)

    # ---------- SESSION ----------
    def is_logged_in(self):
        return "user" in session

    def get_user_type(self):
        return session.get("user", {}).get("type")

    def login_user(self, username, user_type):
        session["user"] = {"username": username, "type": user_type}

    def logout_user(self):
        session.clear()

    # ---------- LOGIN ----------
    def validate_login(self, username, password):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # --- Check adminacc table ---
        cursor.execute(
            "SELECT * FROM adminacc WHERE Username=%s AND Password=%s",
            (username, password)
        )
        admin = cursor.fetchone()
        if admin:
            cursor.close()
            db.close()
            return "admin"

        # --- Check useracc table ---
        cursor.execute(
            "SELECT * FROM useracc WHERE Username=%s AND Password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user:
            return "user"

        return None

    def handle_login(self):
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect("/")

        user_type = self.validate_login(username, password)

        if not user_type:
            flash("Invalid username or password.", "danger")
            return redirect("/")

        self.login_user(username, user_type)

        if user_type == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("user.user_dashboard"))

    # ---------- SIGNUP ----------
    def handle_signup(self):
        fname = request.form.get("firstname")
        mname = request.form.get("middlename")
        lname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")

        if not fname or not lname or not username or not password:
            flash("All required fields must be filled.", "danger")
            return redirect("/?signup=1")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Check if username exists in useracc
        cursor.execute("SELECT * FROM useracc WHERE Username=%s", (username,))
        exist = cursor.fetchone()
        if exist:
            flash("Username already taken.", "danger")
            cursor.close()
            db.close()
            return redirect("/?signup=1")

        # Insert new user
        cursor.execute(
            "INSERT INTO useracc (FirstName, MiddleName, LastName, Username, Password) "
            "VALUES (%s, %s, %s, %s, %s)",
            (fname, mname, lname, username, password)
        )
        db.commit()
        cursor.close()
        db.close()

        flash("Account created successfully! Please log in.", "success")
        return redirect("/")

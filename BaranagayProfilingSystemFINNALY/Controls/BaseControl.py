from flask import render_template, session, request, redirect, flash
import mysql.connector

# ---------- Base Controller ----------
class BaseController:

    def __init__(self, template_folder="Design"):
        self.template_folder = template_folder

    # ---------- Database Connection ----------
    def db_connect(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="temporary1"
        )

    # ---------- Render ----------
    def render(self, template_name, **kwargs):
        return render_template(template_name, **kwargs)

    # ---------- Session Management ----------
    def is_logged_in(self):
        return "user" in session

    def get_user_type(self):
        return session.get("user", {}).get("Type")

    def get_username(self):
        return session.get("user", {}).get("Username")

    def login_user(self, user_dict):
        # Store safe user info in session
        session["user"] = {
            "FirstName": user_dict.get("FirstName"),
            "MiddleName": user_dict.get("MiddleName"),
            "LastName": user_dict.get("LastName"),
            "Username": user_dict.get("Username"),
            "Type": user_dict.get("Type", "user")
        }

    def logout_user(self):
        session.clear()

    # ---------- Login ----------
    def handle_login(self):
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect("/")

        db = self.db_connect()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM useracc WHERE Username=%s AND Password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user:
            flash("Invalid username or password.", "danger")
            return redirect("/")

        # Login user (without password)
        self.login_user({
            "FirstName": user["FirstName"],
            "MiddleName": user["MiddleName"],
            "LastName": user["LastName"],
            "Username": user["Username"],
            "Type": "user"
        })

        return redirect("/user/dashboard")

    # ---------- Signup ----------
    def handle_signup(self):
        fname = request.form.get("firstname", "").strip()
        mname = request.form.get("middlename", "").strip()
        lname = request.form.get("lastname", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not fname or not lname or not username or not password:
            flash("All required fields must be filled.", "danger")
            return redirect("/?signup=1")

        db = self.db_connect()
        cursor = db.cursor(dictionary=True)

        # Check if username already exists
        cursor.execute("SELECT * FROM useracc WHERE Username=%s", (username,))
        if cursor.fetchone():
            flash("Username already taken.", "danger")
            cursor.close()
            db.close()
            return redirect("/?signup=1")

        # Insert new user with plain password
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

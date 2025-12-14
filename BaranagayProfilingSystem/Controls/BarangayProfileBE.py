from flask import Blueprint, session, request, redirect, flash, url_for, current_app
from Controls.BaseControl import BaseController
import mysql.connector
from functools import wraps
import os

# ---------------- Resident Model ----------------
class ResidentModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="temporary1"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    # --- Resident CRUD ---
    def get_all_residents(self):
        self.cursor.execute("SELECT * FROM admin")
        return self.cursor.fetchall() or []

    def get_resident(self, ref_id):
        self.cursor.execute("SELECT * FROM admin WHERE RefId=%s", (ref_id,))
        return self.cursor.fetchone() or {}

    def add_resident(self, data):
        sql = """
        INSERT INTO admin 
        (RefId, Name, MI, LastName, Birthday, Age, Sex, Address, CivilStatus,
         Occupation, Nationality, Zone, HouseholdID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        vals = (
            data["RefId"], data["Name"], data["MI"], data["LastName"], data["Birthday"],
            data["Age"], data["Sex"], data["Address"], data["CivilStatus"],
            data["Occupation"], data["Nationality"], data["Zone"], data["HouseholdID"]
        )
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def update_resident(self, ref_id, data):
        sql = """
        UPDATE admin SET 
        Name=%s, MI=%s, LastName=%s, Birthday=%s, Age=%s, Sex=%s,
        Address=%s, CivilStatus=%s, Occupation=%s, Nationality=%s, Zone=%s
        WHERE RefId=%s
        """
        vals = (
            data["Name"], data["MI"], data["LastName"], data["Birthday"], data["Age"],
            data["Sex"], data["Address"], data["CivilStatus"], data["Occupation"],
            data["Nationality"], data["Zone"], ref_id
        )
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def delete_resident(self, ref_id):
        self.cursor.execute("DELETE FROM admin WHERE RefId=%s", (ref_id,))
        self.conn.commit()

    # --- Households ---
    def get_households(self):
        self.cursor.execute(
            "SELECT HouseholdID, Name FROM admin WHERE HouseholdID IS NOT NULL AND HouseholdID != 'None'"
        )
        rows = self.cursor.fetchall()
        households = {}
        for r in rows:
            households.setdefault(r["HouseholdID"], []).append(r["Name"])
        return households

    def create_household(self, member_ids):
        self.cursor.execute(
            "SELECT HouseholdID FROM admin WHERE HouseholdID IS NOT NULL AND HouseholdID != 'None'"
        )
        existing = [row["HouseholdID"] for row in self.cursor.fetchall()]
        i = 1
        while f"HH{i}" in existing:
            i += 1
        hh_id = f"HH{i}"
        for mid in member_ids:
            self.cursor.execute(
                "UPDATE admin SET HouseholdID=%s WHERE RefId=%s", (hh_id, mid)
            )
        self.conn.commit()
        return hh_id

    def add_to_household(self, hh_id, member_ids):
        for mid in member_ids:
            self.cursor.execute(
                "UPDATE admin SET HouseholdID=%s WHERE RefId=%s", (hh_id, mid)
            )
        self.conn.commit()

    def remove_household(self, hh_id):
        self.cursor.execute(
            "UPDATE admin SET HouseholdID='None' WHERE HouseholdID=%s", (hh_id,)
        )
        self.conn.commit()

    # --- Zones ---
    def zone_counts(self):
        self.cursor.execute("SELECT Zone, COUNT(*) AS count FROM admin GROUP BY Zone")
        return {row["Zone"]: row["count"] for row in self.cursor.fetchall()} or {}

    # --- RefID ---
    def generate_next_refid(self):
        self.cursor.execute("SELECT RefId FROM admin ORDER BY RefId DESC LIMIT 1")
        last = self.cursor.fetchone()
        if last:
            return f"R{int(last['RefId'][1:]) + 1}"
        return "R1"


# ---------------- User Controller ----------------
class UserController(BaseController, ResidentModel):
    def __init__(self):
        BaseController.__init__(self)
        ResidentModel.__init__(self)

    def get_user(self):
        return session.get("user", {})

    def is_logged_in(self):
        return "user" in session

    def get_username(self):
        user = session.get("user", {})
        return user.get("Username") if user else None


# ---------------- Blueprint ----------------
user_ctrl = UserController()
user_bp = Blueprint("user", __name__, url_prefix="/user", template_folder="Design")


# --- Login required decorator ---
def user_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not user_ctrl.is_logged_in():
            return redirect("/")
        return f(*args, **kwargs)
    return decorated


# --- Render helper ---
def render_user(page, **kwargs):
    residents = user_ctrl.get_all_residents()
    households = user_ctrl.get_households()
    zones = user_ctrl.zone_counts()
    defaults = {
        "active_page": page,
        "residents": residents,
        "households": households,
        "zones": zones,
        "total_residents": len(residents),
        "total_households": len(households),
        "user": user_ctrl.get_user()
    }
    defaults.update(kwargs)
    return user_ctrl.render("BarangayProfileINT.html", **defaults)


# ---------------- Blueprint Routes ----------------
@user_bp.route("/dashboard")
@user_login_required
def dashboard():
    search_zone = request.args.get("search_zone", "").strip()
    search_household = request.args.get("search_household", "").strip()

    # Filter zones
    zones = user_ctrl.zone_counts()
    if search_zone:
        zones = {z: count for z, count in zones.items() if search_zone.lower() in z.lower()}

    # Filter households
    households = user_ctrl.get_households()
    if search_household:
        households = {k: v for k, v in households.items() if search_household.lower() in k.lower()}

    return render_user(
        "dashboard",
        zones=zones,
        search_zone=search_zone,
        households=households,
        search_household=search_household
    )


@user_bp.route("/manage_residents", methods=["GET", "POST"])
@user_login_required
def manage_residents():
    if request.method == "POST":
        try:
            age = int(request.form.get("age", 0))
        except ValueError:
            flash("Invalid age!", "danger")
            return redirect(url_for("user.manage_residents"))

        data = {
            "RefId": user_ctrl.generate_next_refid(),
            "Name": request.form.get("name", "").strip(),
            "MI": request.form.get("mi", "").strip(),
            "LastName": request.form.get("lname", "").strip(),
            "Birthday": request.form.get("birthday", ""),
            "Age": age,
            "Sex": request.form.get("sex", "Select"),
            "Address": request.form.get("address", "").strip(),
            "CivilStatus": request.form.get("civil_status", "Select"),
            "Occupation": request.form.get("occupation", "").strip(),
            "Nationality": request.form.get("nationality", "").strip(),
            "Zone": request.form.get("zone", "Unassigned").strip(),
            "HouseholdID": "None"
        }
        user_ctrl.add_resident(data)
        flash(f"Resident {data['Name']} added!", "success")
        return redirect(url_for("user.manage_residents"))

    search_query = request.args.get("search", "").lower().strip()
    residents = user_ctrl.get_all_residents()
    if search_query:
        residents = [
            r for r in residents
            if search_query in r["RefId"].lower()
            or search_query in r["Name"].lower()
            or search_query in r["LastName"].lower()
        ]
    return render_user("residents", residents=residents, search_query=search_query)


@user_bp.route("/update_resident/<ref_id>", methods=["POST"])
@user_login_required
def update_resident(ref_id):
    try:
        age = int(request.form.get("age", 0))
    except ValueError:
        flash("Invalid age!", "danger")
        return redirect(url_for("user.manage_residents"))

    data = {
        "Name": request.form.get("name", "").strip(),
        "MI": request.form.get("mi", "").strip(),
        "LastName": request.form.get("lname", "").strip(),
        "Birthday": request.form.get("birthday", ""),
        "Age": age,
        "Sex": request.form.get("sex", "Select"),
        "Address": request.form.get("address", "").strip(),
        "CivilStatus": request.form.get("civil_status", "Select"),
        "Occupation": request.form.get("occupation", "").strip(),
        "Nationality": request.form.get("nationality", "").strip(),
        "Zone": request.form.get("zone", "Unassigned").strip()
    }
    user_ctrl.update_resident(ref_id, data)
    flash(f"Resident {data['Name']} updated!", "success")
    return redirect(url_for("user.manage_residents"))


@user_bp.route("/delete_resident/<ref_id>", methods=["POST"])
@user_login_required
def delete_resident(ref_id):
    user_ctrl.delete_resident(ref_id)
    flash("Resident deleted!", "success")
    return redirect(url_for("user.manage_residents"))


@user_bp.route("/manage_households", methods=["GET"])
@user_login_required
def manage_households():
    search_hh = request.args.get("search_hh", "").strip()
    households = user_ctrl.get_households()
    if search_hh:
        households = {k: v for k, v in households.items() if search_hh.lower() in k.lower()}
    return render_user("households", households=households, search_hh=search_hh)


@user_bp.route("/create_household", methods=["POST"])
@user_login_required
def create_household():
    member_ids = request.form.getlist("members[]")
    if not member_ids:
        flash("Select at least one member", "danger")
        return redirect(url_for("user.manage_households"))
    hh_id = user_ctrl.create_household(member_ids)
    flash(f"Household {hh_id} created!", "success")
    return redirect(url_for("user.manage_households"))


@user_bp.route("/add_to_household/<hh_id>", methods=["POST"])
@user_login_required
def add_to_household(hh_id):
    member_ids = request.form.getlist("new_members")
    if not member_ids:
        flash("No member selected", "danger")
        return redirect(url_for("user.manage_households"))
    user_ctrl.add_to_household(hh_id, member_ids)
    flash(f"Members added to {hh_id}!", "success")
    return redirect(url_for("user.manage_households"))


@user_bp.route("/remove_household/<hh_id>", methods=["POST"])
@user_login_required
def remove_household(hh_id):
    user_ctrl.remove_household(hh_id)
    flash(f"Household {hh_id} removed!", "success")
    return redirect(url_for("user.manage_households"))


@user_bp.route("/settings", methods=["GET", "POST"])
@user_login_required
def settings():
    system_info = {
        "version": "1.0",
        "database": "MySQL Temporary1",
        "framework": "Flask",
        "last_update": "2025-12-12"
    }
    current_username = user_ctrl.get_username() or "User"

    if request.method == "POST":
        new_username = request.form.get("username", "").strip()
        new_password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        logo_file = request.files.get("logo")

        if new_password and new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("user.settings"))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="temporary1"
        )
        cursor = conn.cursor()

        if new_username:
            cursor.execute(
                "UPDATE useracc SET Username=%s WHERE Username=%s",
                (new_username, current_username)
            )
            session["user"]["Username"] = new_username
            current_username = new_username

        if new_password:
            cursor.execute(
                "UPDATE useracc SET Password=%s WHERE Username=%s",
                (new_password, current_username)
            )

        if logo_file and logo_file.filename:
            logo_file.save(os.path.join(current_app.static_folder, "barangaypic.png"))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Account updated successfully!", "success")
        return redirect(url_for("user.settings"))

    return render_user("settings", system_info=system_info)

from flask import Blueprint, session, request, redirect, flash, url_for
from Controls.BaseControl import BaseController
import mysql.connector
from functools import wraps

# ---------------- Resident Model ----------------
class ResidentModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="temporary"
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
        sql = """INSERT INTO admin 
        (RefId, Name, MI, LastName, Birthday, Age, Sex, Address, CivilStatus,
         Occupation, Nationality, Zone, HouseholdID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        vals = (
            data["RefId"], data["Name"], data["MI"], data["LastName"], data["Birthday"],
            data["Age"], data["Sex"], data["Address"], data["CivilStatus"],
            data["Occupation"], data["Nationality"], data["Zone"], data["HouseholdID"]
        )
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def update_resident(self, ref_id, data):
        sql = """UPDATE admin SET 
        Name=%s, MI=%s, LastName=%s, Birthday=%s, Age=%s, Sex=%s,
        Address=%s, CivilStatus=%s, Occupation=%s, Nationality=%s, Zone=%s,
        HouseholdID=%s
        WHERE RefId=%s"""
        vals = (
            data["Name"], data["MI"], data["LastName"], data["Birthday"], data["Age"],
            data["Sex"], data["Address"], data["CivilStatus"], data["Occupation"],
            data["Nationality"], data["Zone"], data["HouseholdID"], ref_id
        )
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def delete_resident(self, ref_id):
        self.cursor.execute("DELETE FROM admin WHERE RefId=%s", (ref_id,))
        self.conn.commit()

    # --- Households ---
    def available_for_household(self):
        self.cursor.execute("SELECT * FROM admin WHERE HouseholdID IS NULL OR HouseholdID='None'")
        return self.cursor.fetchall() or []

    def create_household(self, member_ids):
        self.cursor.execute("SELECT HouseholdID FROM admin WHERE HouseholdID IS NOT NULL AND HouseholdID!='None'")
        existing = [row["HouseholdID"] for row in self.cursor.fetchall()]
        i = 1
        while f"HH{i}" in existing:
            i += 1
        hh_id = f"HH{i}"
        for mid in member_ids:
            self.cursor.execute("UPDATE admin SET HouseholdID=%s WHERE RefId=%s", (hh_id, mid))
        self.conn.commit()
        return hh_id

    def add_to_household(self, hh_id, member_id):
        self.cursor.execute("UPDATE admin SET HouseholdID=%s WHERE RefId=%s", (hh_id, member_id))
        self.conn.commit()

    def remove_household(self, hh_id):
        self.cursor.execute("UPDATE admin SET HouseholdID='None' WHERE HouseholdID=%s", (hh_id,))
        self.conn.commit()

    def get_households(self):
        self.cursor.execute("SELECT HouseholdID, Name FROM admin WHERE HouseholdID IS NOT NULL AND HouseholdID!='None'")
        rows = self.cursor.fetchall()
        households = {}
        for r in rows:
            hh = r["HouseholdID"]
            households.setdefault(hh, []).append(r["Name"])
        return households

    # --- Zones ---
    def zone_counts(self):
        self.cursor.execute("SELECT Zone, COUNT(*) AS count FROM admin GROUP BY Zone")
        return {row["Zone"]: row["count"] for row in self.cursor.fetchall()} or {}

    # --- RefID Generation ---
    def generate_next_refid(self):
        self.cursor.execute("SELECT RefId FROM admin ORDER BY RefId DESC LIMIT 1")
        last = self.cursor.fetchone()
        if last:
            last_num = int(last["RefId"][1:])
            return f"R{last_num + 1}"
        return "R1"

# ---------------- Admin Controller ----------------
class AdminController(BaseController, ResidentModel):
    def __init__(self):
        BaseController.__init__(self)
        ResidentModel.__init__(self)

admin_ctrl = AdminController()
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- Login required decorator ---
def admin_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not admin_ctrl.is_logged_in() or admin_ctrl.get_user_type() != "admin":
            return redirect("/")
        return f(*args, **kwargs)
    return decorated

# --- Render helper with search, highest/lowest ---
def render_admin(page, **kwargs):
    residents = admin_ctrl.get_all_residents()
    households = admin_ctrl.get_households()
    zones = admin_ctrl.zone_counts()

    # Highest/lowest calculations
    household_sizes = {hh: len(members) for hh, members in households.items()}
    hh_highest = max(household_sizes.items(), key=lambda x: x[1])[0] if household_sizes else None
    hh_lowest = min(household_sizes.items(), key=lambda x: x[1])[0] if household_sizes else None

    zone_highest = max(zones.items(), key=lambda x: x[1])[0] if zones else None
    zone_lowest = min(zones.items(), key=lambda x: x[1])[0] if zones else None

    defaults = {
        "active_page": page,
        "residents": residents,
        "households": households,
        "zones": zones,
        "total_residents": len(residents),
        "total_households": len(households),
        "household_highest": hh_highest,
        "household_lowest": hh_lowest,
        "zone_highest": zone_highest,
        "zone_lowest": zone_lowest,
        "search_query": "",
        "search_hh": "",
        "search_zone": ""
    }
    defaults.update(kwargs)
    return admin_ctrl.render("AdminBase.html", **defaults)

# ---------------- Routes ----------------
@admin_bp.route("/dashboard")
@admin_login_required
def dashboard():
    return render_admin("dashboard")

@admin_bp.route("/manage_residents", methods=["GET", "POST"])
@admin_login_required
def manage_residents():
    if request.method == "POST":
        ref_id = admin_ctrl.generate_next_refid()
        data = {
            "RefId": ref_id,
            "Name": request.form["name"],
            "MI": request.form.get("mi", ""),
            "LastName": request.form.get("lname", ""),
            "Birthday": request.form.get("birthday", ""),
            "Age": request.form.get("age", ""),
            "Sex": request.form.get("sex", "Select"),
            "Address": request.form.get("address", ""),
            "CivilStatus": request.form.get("civil_status", "Select"),
            "Occupation": request.form.get("occupation", ""),
            "Nationality": request.form.get("nationality", ""),
            "Zone": request.form.get("zone", "Unassigned"),
            "HouseholdID": "None"
        }
        admin_ctrl.add_resident(data)
        flash(f"Resident {data['Name']} added!", "success")
        return redirect("/admin/manage_residents")

    search_query = request.args.get("search", "").lower().strip()
    residents = admin_ctrl.get_all_residents()
    if search_query:
        residents = [
            r for r in residents
            if search_query in r["RefId"].lower()
               or search_query in r["Name"].lower()
               or search_query in r["LastName"].lower()
        ]
    return render_admin("residents", residents=residents, search_query=search_query)

@admin_bp.route("/update_resident/<ref_id>", methods=["POST"])
@admin_login_required
def update_resident(ref_id):
    updated = {
        "Name": request.form["name"],
        "MI": request.form.get("mi", ""),
        "LastName": request.form.get("lname", ""),
        "Birthday": request.form.get("birthday", ""),
        "Age": request.form.get("age", ""),
        "Sex": request.form.get("sex", "Select"),
        "Address": request.form.get("address", ""),
        "CivilStatus": request.form.get("civil_status", "Select"),
        "Occupation": request.form.get("occupation", ""),
        "Nationality": request.form.get("nationality", ""),
        "Zone": request.form.get("zone", "Unassigned"),
        "HouseholdID": request.form.get("household_id", "None")
    }
    admin_ctrl.update_resident(ref_id, updated)
    flash(f"Resident {updated['Name']} updated!", "success")
    return redirect("/admin/manage_residents")

@admin_bp.route("/delete_resident/<ref_id>")
@admin_login_required
def delete_resident(ref_id):
    admin_ctrl.delete_resident(ref_id)
    flash("Resident deleted!", "success")
    return redirect("/admin/manage_residents")

# ---------------- Households ----------------
@admin_bp.route("/manage_households")
@admin_login_required
def manage_households():
    available_residents = admin_ctrl.available_for_household()
    all_households = admin_ctrl.get_households()
    zones = admin_ctrl.zone_counts()

    # --- Search functionality ---
    search_hh = request.args.get("search_hh", "").lower().strip()
    search_zone = request.args.get("search_zone", "").lower().strip()

    if search_hh:
        filtered_households = {hh_id: members for hh_id, members in all_households.items() if search_hh in hh_id.lower()}
    else:
        filtered_households = all_households

    if search_zone:
        filtered_zones = {zone: count for zone, count in zones.items() if search_zone in zone.lower()}
    else:
        filtered_zones = zones

    return render_admin(
        "households",
        residents=available_residents,
        households=filtered_households,
        zones=filtered_zones,
        search_hh=search_hh,
        search_zone=search_zone
    )

@admin_bp.route("/create_household", methods=["POST"])
@admin_login_required
def create_household():
    member_ids = request.form.getlist("members[]")
    if not member_ids:
        flash("Select at least one member!", "danger")
        return redirect("/admin/manage_households")
    hh_id = admin_ctrl.create_household(member_ids)
    flash(f"Household {hh_id} created!", "success")
    return redirect("/admin/manage_households")

@admin_bp.route("/add_members/<hh_id>", methods=["POST"])
@admin_login_required
def add_members(hh_id):
    member_ids = request.form.getlist("new_members")
    if not member_ids:
        flash("Select at least one member to add!", "danger")
        return redirect("/admin/manage_households")
    for mid in member_ids:
        admin_ctrl.add_to_household(hh_id, mid)
    flash(f"Added {len(member_ids)} member(s) to {hh_id}!", "success")
    return redirect("/admin/manage_households")

@admin_bp.route("/delete_household/<hh_id>", methods=["POST"])
@admin_login_required
def delete_household(hh_id):
    admin_ctrl.remove_household(hh_id)
    flash(f"Household {hh_id} deleted!", "success")
    return redirect("/admin/manage_households")

# ---------------- Settings ----------------
@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_login_required
def settings():
    system_info = {
        "version": "1.0",
        "developer": "Your Name",
        "database": "MySQL Temporary",
        "framework": "Flask",
        "last_update": "2025-12-11"
    }

    current_username = session.get("username", "Admin")

    if request.method == "POST":
        new_username = request.form.get("username", "").strip()
        new_password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        logo_file = request.files.get("logo")

        # Password mismatch
        if new_password and new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect("/admin/settings")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="temporary"
            )
            cursor = conn.cursor()

            # Update username
            if new_username:
                cursor.execute(
                    "UPDATE adminacc SET Username=%s WHERE Username=%s",
                    (new_username, current_username)
                )
                session["username"] = new_username
                current_username = new_username

            # Update password
            if new_password:
                cursor.execute(
                    "UPDATE adminacc SET Password=%s WHERE Username=%s",
                    (new_password, current_username)
                )

            # Update logo
            if logo_file and logo_file.filename != "":
                logo_path = "static/barangaypic.png"
                logo_file.save(logo_path)
                flash("Logo updated successfully!", "success")

            conn.commit()
            cursor.close()
            conn.close()
            flash("Account updated successfully!", "success")
        except mysql.connector.Error as e:
            flash(f"Database error: {str(e)}", "danger")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

        return redirect("/admin/settings")

    return render_admin("settings", system_info=system_info, current_username=current_username)


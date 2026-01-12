from flask import Flask, render_template, request, redirect, session,url_for,abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # needed for sessions

# ---------- Database ----------
def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user"] = username

            # ADMIN CHECK
            if username == "admin":
                session["is_admin"] = True
            else:
                session["is_admin"] = False

            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route('/gallery')
def gallery():
    if "user" not in session:
        return redirect(url_for('login'))

    if session.get('is_admin') != True:
        abort(403)

    return render_template('gallery.html')
@app.route("/logout")

def logout():
    session.pop("user", None)
    return redirect("/")

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

if __name__ == "__main__":
    app.run(debug=True)
import os
import sqlite3
import hashlib
import ast
from flask import Flask, request, render_template

app = Flask(__name__)

# -----------------------------------------
# 1) API KEY — corregido (uso de variable de entorno)
# -----------------------------------------
API_KEY = os.getenv("API_KEY", "no-key-provided")


# -----------------------------------------
# 2) Password hashing — corregido (SHA256)
# -----------------------------------------
def secure_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------------------
# 3) SQL Injection — corregido (query parametrizada)
# -----------------------------------------
def get_user_by_name(name):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    results = cursor.fetchall()
    conn.close()
    return results


# -----------------------------------------
# 4) XSS — corregido (uso de template seguro)
# -----------------------------------------
@app.route("/search")
def search():
    term = request.args.get("q", "")
    results = get_user_by_name(term)
    return render_template("search.html", term=term, results=results)


# -----------------------------------------
# 5) Command Injection — corregido (sin shell)
# -----------------------------------------
def list_directory(path):
    if not os.path.isdir(path):
        return []
    return os.listdir(path)


# -----------------------------------------
# 6) eval() — corregido (reemplazado por literal_eval)
# -----------------------------------------
def evaluate_user_input(code): 
    try:
        return ast.literal_eval(code) # parser seguro, no ejecuta codigo
    except Exception:
        return "Invalid input" 


if __name__ == "__main__":
    app.run()
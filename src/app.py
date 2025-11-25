import os
import sqlite3
import hashlib
from flask import Flask, request, render_template_string

app = Flask(__name__)

# -----------------------------------------
# 1) API KEY — corregido: ya no está hardcodeada
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
    return cursor.fetchall()


# -----------------------------------------
# 4) XSS — corregido (sanitización automática con template)
# -----------------------------------------
@app.route("/search")
def search():
    term = request.args.get("q", "")
    return render_template_string("<h1>Resultados para: {{ term }}</h1>", term=term)


# -----------------------------------------
# 5) Command Injection — corregido (sin shell=True)
# -----------------------------------------
def list_directory(path):
    if not os.path.isdir(path):
        return []
    return os.listdir(path)


# -----------------------------------------
# 6) eval() — corregido (reemplazado por literal_eval)
# -----------------------------------------
import ast

def evaluate_user_input(code):
    try:
        return ast.literal_eval(code)
    except Exception:
        return "Invalid input"

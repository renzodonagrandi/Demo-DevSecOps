import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Hardcoded secret (detectado por Semgrep) 
API_KEY = "SECRET-12345-FAKE"

# Insecure hash (detectado)  
import hashlib

def insecure_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


# SQL Injection (detectado)
def get_user_by_name(name):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)
    return cursor.fetchall()


# XSS (detectado)
@app.route("/search")
def search():
    term = request.args.get("q")
    return f"<h1>Resultados para: {term}</h1>"


# Command injection (detectado)
def list_directory(path):
    os.system("ls " + path)


# Dangerous eval (detectado)
def evaluate_user_input(code):
    return eval(code)
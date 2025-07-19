from flask import Flask, request, render_template_string
import os
import sqlite3

app = Flask(__name__)

# Connect to SQLite DB (no auth, no sanitation)
def get_db_connection():
    conn = sqlite3.connect('vuln.db')
    return conn

# Route vulnerable to SQL Injection
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return "Logged in!"
        else:
            return "Invalid credentials"
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit">
        </form>
    '''

# Route vulnerable to Remote Code Execution (RCE)
@app.route("/rce")
def rce():
    cmd = request.args.get("cmd")
    output = os.popen(cmd).read()
    return f"<pre>{output}</pre>"

# Route vulnerable to Cross-Site Scripting (XSS)
@app.route("/xss")
def xss():
    name = request.args.get("name", "World")
    return render_template_string(f"<h1>Hello {name}</h1>")

if __name__ == "__main__":
    app.run(debug=True)

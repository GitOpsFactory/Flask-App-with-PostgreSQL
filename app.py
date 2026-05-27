from flask import Flask, request
import psycopg2
import os
import socket
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.route("/", methods=["GET", "POST"])
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    users = []

    if request.method == "POST":

        action = request.form.get("action")

        # SAVE USER
        if action == "save":

            username = request.form.get("username")

            if username:

                cur.execute(
                    "INSERT INTO users (username) VALUES (%s)",
                    (username,)
                )

                conn.commit()

        # FETCH USERS
        elif action == "fetch":

            cur.execute("""
                SELECT id, username, created_at
                FROM users
                ORDER BY id DESC
            """)

            users = cur.fetchall()

    hostname = socket.gethostname()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ""

    for user in users:

        rows += f"""
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
        </tr>
        """

    cur.close()
    conn.close()

    html = f"""

    <html>

    <head>

        <title>DevOps Dashboard</title>

        <style>

            body {{
                background-color: #0f172a;
                color: white;
                font-family: Arial;
                text-align: center;
                padding: 20px;
            }}

            .card {{
                background: #1e293b;
                width: 900px;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}

            h1 {{
                color: #38bdf8;
            }}

            input {{
                padding: 10px;
                width: 250px;
                border-radius: 5px;
                border: none;
                margin-right: 10px;
            }}

            button {{
                padding: 10px 20px;
                margin: 5px;
                background-color: #38bdf8;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }}

            button:hover {{
                background-color: #0ea5e9;
            }}

            table {{
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
            }}

            th, td {{
                border: 1px solid #334155;
                padding: 12px;
            }}

            th {{
                background-color: #334155;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>🚀 Kubernetes DevOps Dashboard</h1>

            <p>📦 Pod Name: <b>{hostname}</b></p>

            <p>🕒 Current Time: <b>{current_time}</b></p>

            <p>🗄 PostgreSQL Status: <b>Connected ✅</b></p>

            <form method="POST">

                <input
                    type="text"
                    name="username"
                    placeholder="Enter Username"
                >

                <button
                    type="submit"
                    name="action"
                    value="save"
                >
                    Save User
                </button>

                <button
                    type="submit"
                    name="action"
                    value="fetch"
                >
                    Fetch Users
                </button>

            </form>

            <table>

                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Created At</th>
                </tr>

                {rows}

            </table>

        </div>

    </body>

    </html>

    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
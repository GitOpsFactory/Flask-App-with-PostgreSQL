from flask import Flask
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


@app.route("/")
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert visit
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()

    # Get total visits
    cur.execute("SELECT COUNT(*) FROM visits")
    total_visits = cur.fetchone()[0]

    # PostgreSQL version
    cur.execute("SELECT version()")
    pg_version = cur.fetchone()[0]

    cur.close()
    conn.close()

    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>DevOps Dashboard</title>

        <meta http-equiv="refresh" content="5">

        <style>
            body {{
                background-color: #0f172a;
                color: white;
                font-family: Arial;
                text-align: center;
                padding-top: 50px;
            }}

            .card {{
                background: #1e293b;
                width: 600px;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 15px rgba(0,0,0,0.5);
            }}

            h1 {{
                color: #38bdf8;
            }}

            .metric {{
                font-size: 24px;
                margin: 20px;
            }}
        </style>
    </head>

    <body>

        <div class="card">

            <h1>🚀 Kubernetes DevOps Dashboard</h1>

            <div class="metric">
                📦 Pod Name: <b>{hostname}</b>
            </div>

            <div class="metric">
                👥 Total Visits: <b>{total_visits}</b>
            </div>

            <div class="metric">
                🕒 Current Time: <b>{current_time}</b>
            </div>

            <div class="metric">
                🗄 PostgreSQL Status: <b>Connected ✅</b>
            </div>

            <div class="metric">
                🐘 PostgreSQL Version:
                <br><br>
                <small>{pg_version}</small>
            </div>

        </div>

    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
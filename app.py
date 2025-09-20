# app.py
from flask import Flask
from sqlalchemy import create_engine, text
import os, socket, traceback, urllib.parse

app = Flask(__name__)

user = os.environ.get("DATABASE_USER")
password = urllib.parse.quote_plus(os.environ["DATABASE_PASSWORD"])
host = os.environ.get("DATABASE_HOST")
db = os.environ.get("DATABASE_NAME")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db}?sslmode=require"
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

@app.route("/")
def hello():
    host = socket.gethostname()
    if not engine:
        return "DATABASE_URL manquante dans les App Settings", 500
    try:
        with engine.connect() as conn:
            (today,) = conn.execute(text("SELECT current_date")).fetchone()
        return f"Hello from Azure! Host: {host} — DB Date: {today}"
    except Exception as e:
        # logge la stacktrace dans les logs App Service
        traceback.print_exc()
        return f"Erreur DB: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

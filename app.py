from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import os, socket

app = Flask(__name__)

# 🔑 Récupère l’URL de connexion depuis les App Settings d’Azure
# Exemple attendu : postgresql://user:password@host:5432/dbname?sslmode=require
DATABASE_URL = os.environ.get("DATABASE_URL")

# Crée un moteur SQLAlchemy (pool de connexions)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@app.route("/")
def hello():
    hostname = socket.gethostname()

    # Exemple de requête : date actuelle côté DB
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_date;"))
        (today,) = result.fetchone()

    return f"Hello from Azure! Host: {hostname} — DB Date: {today}"

if __name__ == "__main__":
    # Exécution locale pour tests
    app.run(host="0.0.0.0", port=8000)


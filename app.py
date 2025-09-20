# app.py
from flask import Flask, request, jsonify, render_template
import socket
from sqlalchemy.exc import SQLAlchemyError

from db import engine, SessionLocal
from models import Base, Message, db_now

app = Flask(__name__)

#  Crée le schéma si absent (idempotent)
with engine.begin() as conn:
    Base.metadata.create_all(bind=conn)

@app.teardown_appcontext
def remove_session(_exc=None):
    # Nettoyage de session à la fin de la requête
    SessionLocal.remove()

@app.get("/healthz")
def healthz():
    try:
        with SessionLocal() as s:
            _ = db_now(s)
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "down", "error": str(e)}, 500

@app.get("/")
def index():
    hostname = socket.gethostname()
    # Rend un template simple avec un formulaire JS
    return render_template("index.html", hostname=hostname)

# -------- API JSON --------

@app.get("/api/messages")
def list_messages():
    with SessionLocal() as s:
        rows = s.query(Message).order_by(Message.id.desc()).limit(100).all()
        return jsonify([
            {"id": m.id, "content": m.content, "created_at": m.created_at.isoformat()}
            for m in rows
        ])

@app.post("/api/messages")
def create_message():
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return {"error": "content is required"}, 400

    try:
        with SessionLocal() as s:
            m = Message(content=content)
            s.add(m)
            s.commit()
            s.refresh(m)
            return {"id": m.id, "content": m.content, "created_at": m.created_at.isoformat()}, 201
    except SQLAlchemyError as e:
        return {"error": str(e)}, 500

@app.delete("/api/messages/<int:msg_id>")
def delete_message(msg_id: int):
    with SessionLocal() as s:
        m = s.get(Message, msg_id)
        if not m:
            return {"error": "not found"}, 404
        s.delete(m)
        s.commit()
        return {"status": "deleted"}, 200

if __name__ == "__main__":
    # Run local (dev)
    app.run(host="0.0.0.0", port=8000, debug=True)

































# from flask import Flask
# from sqlalchemy import create_engine, text
# import os, socket, traceback, urllib.parse

# app = Flask(__name__)

# user = os.environ.get("DATABASE_USER")
# password = urllib.parse.quote_plus(os.environ["DATABASE_PASSWORD"])
# host = os.environ.get("DATABASE_HOST")
# db = os.environ.get("DATABASE_NAME")

# DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db}?sslmode=require"
# engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

# @app.route("/")
# def hello():
#     host = socket.gethostname()
#     if not engine:
#         return "DATABASE_URL manquante dans les App Settings", 500
#     try:
#         with engine.connect() as conn:
#             (today,) = conn.execute(text("SELECT current_date")).fetchone()
#         return f"Hello from Azure! Host: {host} — DB Date: {today}"
#     except Exception as e:
#         # logge la stacktrace dans les logs App Service
#         traceback.print_exc()
#         return f"Erreur DB: {e}", 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)


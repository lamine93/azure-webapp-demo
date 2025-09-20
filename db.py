from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os, socket, traceback, urllib.parse


user = os.environ.get("DATABASE_USER")
password = urllib.parse.quote_plus(os.environ["DATABASE_PASSWORD"])
host = os.environ.get("DATABASE_HOST")
db = os.environ.get("DATABASE_NAME")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db}?sslmode=require"

# pool_pre_ping évite les connexions mortes, utile sur PaaS
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

# Session thread-safe
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

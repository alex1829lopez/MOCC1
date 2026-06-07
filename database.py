import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 📌 DB en Streamlit (escribible)
DB_PATH = "/tmp/academy.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# 🔥 IMPORTANTE: importar modelos para que SQLAlchemy los vea
from models import User  # 👈 CLAVE

def init_db():
    Base.metadata.create_all(bind=engine)

# 🔥 crear tablas al iniciar
init_db()
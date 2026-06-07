import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================
# 📦 BASE DE DATOS (FIX STREAMLIT)
# =========================

# Ruta escribible en Streamlit Cloud
DB_PATH = os.path.join("/tmp", "academy.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Sesión de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos
Base = declarative_base()


# =========================
# 🧱 IMPORTANTE: CREAR TABLAS
# =========================
def init_db():
    Base.metadata.create_all(bind=engine)


# Llamar esto una sola vez al iniciar la app
init_db()
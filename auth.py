import bcrypt
from database import SessionLocal
from models import User


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


# =========================
# REGISTRO (FIXED)
# =========================
def register_user(name, email, password):

    db = SessionLocal()

    try:
        existing = db.query(User).filter(
            User.email == email
        ).first()

        if existing:
            return False, "❌ El correo ya está registrado"

        user = User(
            name=name,
            email=email,
            password=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.close()

        return True, "✅ Usuario creado correctamente"

    except Exception as e:
        db.rollback()
        db.close()
        return False, f"Error: {str(e)}"


# =========================
# LOGIN (FIXED)
# =========================
def login_user(email, password):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == email
        ).first()

        db.close()

        if not user:
            return None

        if verify_password(password, user.password):
            return user

        return None

    except Exception:
        db.close()
        return None
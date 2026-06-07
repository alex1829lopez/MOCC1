from database import SessionLocal
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# REGISTRO
# =========================
def register_user(name, email, password):

    db = SessionLocal()

        try:
                user_exists = db.query(User).filter(User.email == email).first()

                        if user_exists:
                                    return False, "El usuario ya existe"

                                            hashed_password = generate_password_hash(password)

                                                    new_user = User(
                                                                name=name,
                                                                            email=email,
                                                                                        password=hashed_password
                                                                                                )

                                                                                                        db.add(new_user)
                                                                                                                db.commit()
                                                                                                                        db.refresh(new_user)

                                                                                                                                return True, "Usuario registrado correctamente"

                                                                                                                                    except Exception as e:
                                                                                                                                            db.rollback()
                                                                                                                                                    return False, str(e)

                                                                                                                                                        finally:
                                                                                                                                                                db.close()


                                                                                                                                                                # =========================
                                                                                                                                                                # LOGIN
                                                                                                                                                                # =========================
                                                                                                                                                                def login_user(email, password):

                                                                                                                                                                    db = SessionLocal()

                                                                                                                                                                        try:
                                                                                                                                                                                user = db.query(User).filter(User.email == email).first()

                                                                                                                                                                                        if not user:
                                                                                                                                                                                                    return None

                                                                                                                                                                                                            if check_password_hash(user.password, password):
                                                                                                                                                                                                                        return user

                                                                                                                                                                                                                                return None

                                                                                                                                                                                                                                    finally:
                                                                                                                                                                                                                                            db.close()
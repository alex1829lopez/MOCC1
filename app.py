from database import engine, Base
from models import User

Base.metadata.create_all(bind=engine)
from database import init_db
init_db()
import streamlit as st
import base64

from auth import register_user, login_user
from quiz_bank import QUIZ_BANK
from certificate import generar_certificado


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="SkillForge Academy",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================
# FONDO + ESTILO CRISTAL LIMPIO
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>

    /* FONDO PRINCIPAL */
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* 🧊 CRISTAL LIMPIO (SIN BLUR) */
    .block-container {{
        padding: 2rem;
        max-width: 900px;

        background: rgba(255, 255, 255, 0.10); /* transparente */
        border-radius: 22px;
        border: 1px solid rgba(255, 255, 255, 0.40);

        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.30);
    }}

    /* TEXTO LEGIBLE */
    p, label, h1, h2, h3, div {{
        color: white !important;
        text-shadow: 0px 2px 8px rgba(0,0,0,0.75);
    }}

    /* BOTONES */
    button {{
        width: 100%;
        border-radius: 14px;
        font-size: 16px;
        padding: 0.75rem;

        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: white;

        transition: 0.25s ease-in-out;
    }}

    button:hover {{
        background: rgba(255, 255, 255, 0.22);
        transform: scale(1.02);
    }}

    /* RADIO */
    .stRadio > div {{
        gap: 12px;
    }}

    </style>
    """, unsafe_allow_html=True)


# ACTIVAR FONDO
set_bg("fondo.jpg")


st.title("🎓 SkillForge Academy")


# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["name"] = None

if "nivel" not in st.session_state:
    st.session_state["nivel"] = 1

if "video_completado" not in st.session_state:
    st.session_state["video_completado"] = False


# =========================
# LOGIN / REGISTRO
# =========================
def auth_page():

    st.subheader("🔐 Acceso")

    tab1, tab2 = st.tabs(["Login", "Registro"])

    with tab1:
        email = st.text_input("Correo", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        if st.button("Entrar", use_container_width=True):
            user = login_user(email, password)

            if user:
                st.session_state["user"] = user.email
                st.session_state["name"] = user.name
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    with tab2:
        name = st.text_input("Nombre", key="reg_name")
        email2 = st.text_input("Correo", key="reg_email")
        password2 = st.text_input("Contraseña", key="reg_pass")

        if st.button("Registrarme", use_container_width=True):
            ok, msg = register_user(name, email2, password2)

            if ok:
                st.success(msg)
            else:
                st.error(msg)


# =========================
# CURSO
# =========================
def curso_page():

    user = st.session_state["name"]
    nivel = st.session_state["nivel"]

    st.success(f"Bienvenido {user} 🎓")
    st.markdown("---")


    if nivel == 1:
        st.subheader("📺 Módulo 1")
        st.video("limon.mp4")

    elif nivel == 2:
        st.subheader("📺 Módulo 2")
        st.video("Limon2.mp4")

    elif nivel == 3:
        st.subheader("📺 Módulo 3")
        st.video("limon3.mp4")

    else:
        st.success("🎓 Curso completado")
        return


    if not st.session_state["video_completado"]:
        if st.button("✔ Marcar video como visto", use_container_width=True):
            st.session_state["video_completado"] = True
            st.success("Video completado")

    st.markdown("---")


    if not st.session_state["video_completado"]:
        st.warning("⚠️ Debes ver el video antes del examen")

    else:
        if st.button("📥 Iniciar examen", use_container_width=True):
            st.session_state["quiz"] = QUIZ_BANK[nivel]


    if "quiz" in st.session_state:

        respuestas = []

        for i, q in enumerate(st.session_state["quiz"]):

            r = st.radio(
                q["pregunta"],
                q["opciones"],
                key=f"{nivel}_{i}"
            )

            respuestas.append(r)

        if st.button("Calificar", use_container_width=True):

            correctas = 0

            for i, q in enumerate(st.session_state["quiz"]):
                if respuestas[i] == q["respuesta"]:
                    correctas += 1

            score = (correctas / len(st.session_state["quiz"])) * 100
            st.session_state["score"] = score

            st.success(f"Resultado: {score:.0f}%")


    if "score" in st.session_state:

        if st.session_state["score"] >= 80:

            if st.session_state["nivel"] == 1:

                if st.button("➡️ Ir al Módulo 2", use_container_width=True):
                    st.session_state["nivel"] = 2
                    st.session_state["video_completado"] = False
                    st.session_state.pop("quiz", None)
                    st.session_state.pop("score", None)
                    st.rerun()

            elif st.session_state["nivel"] == 2:

                if st.button("➡️ Ir al Módulo 3", use_container_width=True):
                    st.session_state["nivel"] = 3
                    st.session_state["video_completado"] = False
                    st.session_state.pop("quiz", None)
                    st.session_state.pop("score", None)
                    st.rerun()

            else:

                if st.button("🎓 Finalizar curso", use_container_width=True):

                    st.balloons()
                    st.success("Curso completado")

                    cert = generar_certificado(
                        user,
                        "MOUSSE DE OREO",
                        st.session_state["score"]
                    )

                    with open(cert, "rb") as f:
                        st.download_button(
                            "📥 Descargar certificado",
                            f,
                            file_name="certificado.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

        else:
            st.error("❌ Necesitas mínimo 80%")


# =========================
# ROUTER
# =========================
if st.session_state["user"]:
    curso_page()
else:
    auth_page()
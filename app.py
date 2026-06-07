import streamlit as st
import base64

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
# DATOS DEL USUARIO
# =========================
if "nombre" not in st.session_state:
    st.session_state["nombre"] = ""

if "apellidos" not in st.session_state:
    st.session_state["apellidos"] = ""

if "datos_completos" not in st.session_state:
    st.session_state["datos_completos"] = False


# =========================
# PROGRESO CURSO
# =========================
if "nivel" not in st.session_state:
    st.session_state["nivel"] = 1

if "video_completado" not in st.session_state:
    st.session_state["video_completado"] = False


# =========================
# FONDO + ESTILO CRISTAL
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .block-container {{
        padding: 2rem;
        max-width: 900px;
        background: rgba(255, 255, 255, 0.10);
        border-radius: 22px;
        border: 1px solid rgba(255, 255, 255, 0.40);
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.30);
    }}

    p, label, h1, h2, h3, div {{
        color: white !important;
        text-shadow: 0px 2px 8px rgba(0,0,0,0.75);
    }}

    button {{
        width: 100%;
        border-radius: 14px;
        font-size: 16px;
        padding: 0.75rem;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: white;
    }}

    button:hover {{
        background: rgba(255, 255, 255, 0.22);
    }}
    </style>
    """, unsafe_allow_html=True)


set_bg("fondo.jpg")


# =========================
# CURSO
# =========================
def curso_page():

    # =========================
    # PEDIR NOMBRE Y APELLIDOS
    # =========================
    if not st.session_state["datos_completos"]:

        st.title("🎓 Antes de iniciar el curso")

        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")

        if st.button("Continuar"):

            if nombre.strip() == "" or apellidos.strip() == "":
                st.error("Debes completar nombre y apellidos")
            else:
                st.session_state["nombre"] = nombre
                st.session_state["apellidos"] = apellidos
                st.session_state["datos_completos"] = True

                # RESET CURSO
                st.session_state["nivel"] = 1
                st.session_state["video_completado"] = False
                st.session_state.pop("quiz", None)
                st.session_state.pop("score", None)

                st.rerun()

        return


    # =========================
    # CURSO PRINCIPAL
    # =========================
    nombre = st.session_state["nombre"]

    st.title(f"🎓 SkillForge Academy - {nombre}")

    nivel = st.session_state["nivel"]

    st.markdown("### 📚 Curso en progreso")
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


    # =========================
    # VIDEO COMPLETADO
    # =========================
    if not st.session_state["video_completado"]:
        if st.button("✔ Marcar video como visto"):
            st.session_state["video_completado"] = True
            st.success("Video completado")

    st.markdown("---")

    if not st.session_state["video_completado"]:
        st.warning("⚠️ Debes ver el video antes del examen")

    else:
        if st.button("📥 Iniciar examen"):
            st.session_state["quiz"] = QUIZ_BANK[nivel]


    # =========================
    # QUIZ
    # =========================
    if "quiz" in st.session_state:

        respuestas = []

        for i, q in enumerate(st.session_state["quiz"]):

            r = st.radio(
                q["pregunta"],
                q["opciones"],
                key=f"{nivel}_{i}"
            )

            respuestas.append(r)

        if st.button("Calificar"):

            correctas = 0

            for i, q in enumerate(st.session_state["quiz"]):
                if respuestas[i] == q["respuesta"]:
                    correctas += 1

            score = (correctas / len(st.session_state["quiz"])) * 100
            st.session_state["score"] = score

            st.success(f"Resultado: {score:.0f}%")


    # =========================
    # AVANCE / CERTIFICADO
    # =========================
    if "score" in st.session_state:

        if st.session_state["score"] >= 80:

            if st.session_state["nivel"] == 1:

                if st.button("➡️ Ir al Módulo 2"):
                    st.session_state["nivel"] = 2
                    st.session_state["video_completado"] = False
                    st.session_state.pop("quiz", None)
                    st.session_state.pop("score", None)
                    st.rerun()

            elif st.session_state["nivel"] == 2:

                if st.button("➡️ Ir al Módulo 3"):
                    st.session_state["nivel"] = 3
                    st.session_state["video_completado"] = False
                    st.session_state.pop("quiz", None)
                    st.session_state.pop("score", None)
                    st.rerun()

            else:

                st.markdown("---")
                st.subheader("🎓 Final del curso")

                if st.button("🎓 Finalizar y generar certificado"):

                    st.balloons()
                    st.success("Curso completado")

                    nombre_completo = st.session_state["nombre"] + " " + st.session_state["apellidos"]

                    cert = generar_certificado(
                        nombre_completo,
                        "SKILLFORGE ACADEMY",
                        st.session_state["score"]
                    )

                    with open(cert, "rb") as f:
                        st.download_button(
                            "📥 Descargar certificado",
                            f,
                            file_name="certificado.pdf",
                            mime="application/pdf"
                        )


# =========================
# EJECUCIÓN
# =========================
curso_page()
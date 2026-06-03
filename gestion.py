import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="Gestor Estudiantil", layout="wide")

# =========================
# BASE DE DATOS SQLITE
# =========================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    actividad TEXT,
    materia TEXT,
    prioridad TEXT,
    fecha TEXT
)
""")

conn.commit()

# =========================
# SESIÓN
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# FUNCIONES BASE DE DATOS
# =========================
def guardar_tarea(usuario, actividad, materia, prioridad, fecha):
    cursor.execute("""
        INSERT INTO tareas (usuario, actividad, materia, prioridad, fecha)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario, actividad, materia, prioridad, str(fecha)))
    conn.commit()


def cargar_tareas(usuario):
    cursor.execute("""
        SELECT id, actividad, materia, prioridad, fecha
        FROM tareas
        WHERE usuario=?
    """, (usuario,))
    return cursor.fetchall()


def eliminar_tarea(tarea_id):
    cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
    conn.commit()

# =========================
# LOGIN
# =========================
if st.session_state.user is None:

    st.title("🔐 Login")

    user = st.text_input("Usuario", key="login_user")

    if st.button("Entrar", key="login_btn"):

        if user.strip() == "":
            st.warning("Escribe un usuario")
        else:
            st.session_state.user = user.strip()
            st.rerun()

# =========================
# APP PRINCIPAL
# =========================
else:

    st.title(f"📚 Bienvenido {st.session_state.user}")

    # =========================
    # CREAR TAREA
    # =========================
    st.sidebar.header("Nueva tarea")

    actividad = st.sidebar.text_input("Actividad", key="actividad_input")

    materia = st.sidebar.selectbox(
        "Materia",
        ["Programación", "Matemáticas", "Marketing", "Diseño", "Otro"],
        key="materia_select"
    )

    prioridad = st.sidebar.selectbox(
        "Prioridad",
        ["🟥 Alta", "🟡 Media", "🟢 Baja"],
        key="prioridad_select"
    )

    fecha = st.sidebar.date_input("Fecha límite", date.today(), key="fecha_input")

    if st.sidebar.button("Guardar tarea", key="guardar_btn"):

        if actividad.strip() == "":
            st.warning("Escribe una actividad")
        else:
            guardar_tarea(
                st.session_state.user,
                actividad,
                materia,
                prioridad,
                fecha
            )
            st.success("Tarea guardada")
            st.rerun()

    # =========================
    # MOSTRAR TAREAS
    # =========================
    st.subheader("📋 Tus tareas")

    tareas = cargar_tareas(st.session_state.user)

    if not tareas:
        st.info("No tienes tareas aún")

    else:
        for t in tareas:

            st.write(f"""
            **📝 {t[1]}**
            - Materia: {t[2]}
            - Prioridad: {t[3]}
            - Fecha: {t[4]}
            """)

            if st.button("🗑️ Eliminar", key=f"del_{t[0]}"):
                eliminar_tarea(t[0])
                st.rerun()

    # =========================
    # 📊 GRÁFICO POR MATERIA
    # =========================
    st.subheader("📊 Progreso por materia")

    if tareas:

        conteo_materia = {}

        for t in tareas:
            materia_t = t[2]
            conteo_materia[materia_t] = conteo_materia.get(materia_t, 0) + 1

        st.bar_chart(conteo_materia)

    # =========================
    # 📊 GRÁFICO POR PRIORIDAD
    # =========================
    st.subheader("📊 Distribución por prioridad")

    if tareas:

        prioridad_count = {
            "🟥 Alta": 0,
            "🟡 Media": 0,
            "🟢 Baja": 0
        }

        for t in tareas:
            prioridad_t = t[3]
            if prioridad_t in prioridad_count:
                prioridad_count[prioridad_t] += 1

        st.bar_chart(prioridad_count)

    # =========================
    # LOGOUT
    # =========================
    if st.button("Cerrar sesión", key="logout_btn"):
        st.session_state.user = None
        st.rerun()
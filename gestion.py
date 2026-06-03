import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor de Tiempo Estudiantil", layout="wide")

st.title("🚀 Planificador y Seguimiento de Actividades")
st.markdown("Optimiza tu ritmo de estudio y organiza tus entregas.")
if 'tareas' not in st.session_state:
    st.session_state.tareas = pd.DataFrame(columns=["Actividad", "Materia", "Fecha Límite", "Estado"])

st.sidebar.header("Nueva Actividad")
with st.sidebar.form("formulario_tareas"):
    nombre = st.text_input("Nombre de la tarea:")
    materia = st.selectbox("Materia:", ["Programación", "Marketing", "Diseño", "Matemáticas", "Otro"])
    fecha = st.date_input("Fecha de entrega:", datetime.now())
    boton_agregar = st.form_submit_button("Añadir Tarea")

    if boton_agregar and nombre:
        nueva_fila = pd.DataFrame({"Actividad": [nombre], "Materia": [materia], 
                                    "Fecha Límite": [fecha], "Estado": ["Pendiente"]})
        st.session_state.tareas = pd.concat([st.session_state.tareas, nueva_fila], ignore_index=True)
        st.success("Tarea guardada.")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Lista de Pendientes")
    if not st.session_state.tareas.empty:

        st.dataframe(st.session_state.tareas, use_container_width=True)
        
        if st.button("Marcar última como 'Completada'"):
            st.session_state.tareas.iloc[-1, 3] = "✅ Completado"
            st.rerun()
    else:
        st.info("No hay actividades registradas aún.")

with col2:
    st.subheader("💡 Tips de Productividad")
    with st.expander("Técnica Pomodoro"):
        st.write("Estudia 25 minutos sin distracciones y descansa 5 minutos.")
    with st.expander("Matriz de Eisenhower"):
        st.write("Prioriza lo importante y urgente sobre lo que puede esperar.")

st.divider()
st.subheader("📊 Progreso de Estudios")
if not st.session_state.tareas.empty:
    conteo_materias = st.session_state.tareas['Materia'].value_counts()
    st.bar_chart(conteo_materias)
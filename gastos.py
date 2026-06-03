import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Control de Gastos Personal", layout="wide")

st.title("💸 Gestor de Gastos Inteligente")
st.markdown("Registra tus movimientos y visualiza en qué se va tu dinero.")

# Inicializar el estado de la sesión para guardar datos si no existen
if 'gastos_df' not in st.session_state:
    st.session_state.gastos_df = pd.DataFrame(columns=["Fecha", "Categoría", "Descripción", "Monto"])

# --- SECCIÓN DE ENTRADA ---
with st.sidebar:
    st.header("Añadir Nuevo Gasto")
    with st.form("formulario_gastos", clear_on_submit=True):
        fecha = st.date_input("Fecha", datetime.now())
        categoria = st.selectbox("Categoría", ["Alimentación", "Transporte", "Vivienda", "Ocio", "Salud", "Otros"])
        descripcion = st.text_input("Descripción")
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.01)
        
        submit = st.form_submit_button("Registrar Gasto")

    if submit and monto > 0:
        nuevo_gasto = pd.DataFrame([[fecha, categoria, descripcion, monto]], 
                                    columns=["Fecha", "Categoría", "Descripción", "Monto"])
        st.session_state.gastos_df = pd.concat([st.session_state.gastos_df, nuevo_gasto], ignore_index=True)
        st.success("¡Gasto registrado!")

# --- VISUALIZACIÓN Y ANÁLISIS ---
df = st.session_state.gastos_df

if not df.empty:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Historial de Movimientos")
        st.dataframe(df.sort_values(by="Fecha", ascending=False), use_container_width=True)
        
        total = df["Monto"].sum()
        st.metric("Gasto Total", f"${total:,.2f}")

    with col2:
        st.subheader("Distribución por Categoría")
        fig = px.pie(df, values='Monto', names='Categoría', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico de barras por tiempo
    st.subheader("Tendencia de Gastos")
    df_fecha = df.groupby("Fecha")["Monto"].sum().reset_index()
    fig_linea = px.bar(df_fecha, x="Fecha", y="Monto", color_discrete_sequence=["#00CC96"])
    st.plotly_chart(fig_linea, use_container_width=True)

else:
    st.info("Aún no hay gastos registrados. Usa el panel de la izquierda para comenzar.")

# Opción para descargar los datos
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar Reporte CSV", data=csv, file_name="mis_gastos.csv", mime="text/csv")
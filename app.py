import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Configuración de la página web
st.set_page_config(
    page_title="Caracterización Socioeconómica - Mujeres Emprendedoras Zarzal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado básico
st.markdown("""
    <style>
    .main-header {
        font-size:2.2rem;
        color:#2D5016;
        font-weight:700;
        margin-bottom:0px;
    }
    .sub-header {
        font-size:1.1rem;
        color:#555;
        margin-bottom:20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cargar datos
@st.cache_data
def cargar_datos():
    ruta = os.path.join("data", "processed", "caracterizacion_limpia.csv")
    if not os.path.exists(ruta):
        st.error(f"⚠️ No se encontró el archivo '{ruta}'. Por favor, ejecuta primero 'python clean_data.py'.")
        return pd.DataFrame()
    return pd.read_csv(ruta)

df = cargar_datos()

if not df.empty:

    # ---------------------------------------------------------
    # ENCABEZADO PRINCIPAL
    # ---------------------------------------------------------
    st.markdown('<p class="main-header">📊 Diagnóstico y Caracterización Socioeconómica</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Asociación de Mujeres Afrocolombianas Emprendedoras de Zarzal (Afroenzar)</p>', unsafe_allow_html=True)
    st.divider()

    # ---------------------------------------------------------
    # FILTROS LATERALES (SIDEBAR)
    # ---------------------------------------------------------
    st.sidebar.header("🔍 Filtros de Caracterización")
    
    # Filtro por Rango de Edad
    rangos_edad = ["Todos"] + sorted(list(df["rango_edad"].dropna().unique()))
    filtro_edad = st.sidebar.selectbox("Rango de Edad:", rangos_edad)
    
    # Filtro por Nivel Educativo
    niveles_edu = ["Todos"] + sorted(list(df["nivel_educativo"].dropna().unique()))
    filtro_edu = st.sidebar.selectbox("Nivel Educativo:", niveles_edu)
    
    # Filtro por Situación Laboral
    sit_laboral = ["Todos"] + sorted(list(df["situacion_laboral"].dropna().unique()))
    filtro_laboral = st.sidebar.selectbox("Situación Laboral:", sit_laboral)

    # Aplicar Filtros
    df_filtrado = df.copy()
    if filtro_edad != "Todos":
        df_filtrado = df_filtrado[df_filtrado["rango_edad"] == filtro_edad]
    if filtro_edu != "Todos":
        df_filtrado = df_filtrado[df_filtrado["nivel_educativo"] == filtro_edu]
    if filtro_laboral != "Todos":
        df_filtrado = df_filtrado[df_filtrado["situacion_laboral"] == filtro_laboral]

    # ---------------------------------------------------------
    # MÉTRICAS CLAVE (KPIs)
    # ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    
    total_personas = len(df_filtrado)
    col1.metric("Total Integrantes Caracterizadas", f"{total_personas}")

    # % Ingresos insuficientes
    if "suficiencia_ingresos" in df_filtrado.columns:
        insuficiente = df_filtrado["suficiencia_ingresos"].str.contains("No", na=False).sum()
        pct_insuficiente = (insuficiente / total_personas * 100) if total_personas > 0 else 0
        col2.metric("% Ingresos Insuficientes", f"{pct_insuficiente:.1f}%")

    # % Con internet
    if "servicios_publicos" in df_filtrado.columns:
        con_internet = df_filtrado["servicios_publicos"].str.contains("Internet", na=False).sum()
        pct_internet = (con_internet / total_personas * 100) if total_personas > 0 else 0
        col3.metric("% Con Acceso a Internet", f"{pct_internet:.1f}%")

    # Nivel digital dominante
    if "nivel_digital" in df_filtrado.columns and total_personas > 0:
        modo_digital = df_filtrado["nivel_digital"].mode()[0] if not df_filtrado["nivel_digital"].empty else "N/A"
        col4.metric("Nivel Digital Predominante", f"{modo_digital}")

    st.divider()

    # ---------------------------------------------------------
    # PESTAÑAS TEMÁTICAS
    # ---------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Demografía y Vivienda", 
        "💼 Empleo e Ingresos", 
        "💻 Inclusión Digital", 
        "🌱 Salud y Cuidado",
        "📋 Explorador de Datos"
    ])

    # --- TAB 1: DEMOGRAFÍA Y VIVIENDA ---
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Distribución por Rango de Edad")
            fig_edad = px.pie(
                df_filtrado, 
                names="rango_edad", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_edad, use_container_width=True)

        with c2:
            st.subheader("Nivel Educativo Alcanzado")
            fig_edu = px.bar(
                df_filtrado["nivel_educativo"].value_counts().reset_index(),
                x="count", y="nivel_educativo",
                orientation="h",
                labels={"count": "Cantidad", "nivel_educativo": "Nivel Educativo"},
                color_discrete_sequence=["#2D5016"]
            )
            st.plotly_chart(fig_edu, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Tenencia de la Vivienda")
            fig_viv = px.pie(df_filtrado, names="tenencia_vivienda", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_viv, use_container_width=True)

        with c4:
            st.subheader("Estrato Socioeconómico")
            fig_estrato = px.bar(
                df_filtrado["estrato"].value_counts().reset_index(),
                x="estrato", y="count",
                labels={"count": "Hogares", "estrato": "Estrato"},
                color_discrete_sequence=["#F4A500"]
            )
            st.plotly_chart(fig_estrato, use_container_width=True)

    # --- TAB 2: EMPLEO E INGRESOS ---
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Situación Laboral Actual")
            fig_lab = px.bar(
                df_filtrado["situacion_laboral"].value_counts().reset_index(),
                x="situacion_laboral", y="count",
                labels={"situacion_laboral": "Estado", "count": "Personas"},
                color_discrete_sequence=["#1B4B6B"]
            )
            st.plotly_chart(fig_lab, use_container_width=True)

        with c2:
            st.subheader("Carga de Trabajo Doméstico y Cuidado")
            fig_dom = px.pie(df_filtrado, names="horas_trabajo_domestico", color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_dom, use_container_width=True)

    # --- TAB 3: INCLUSIÓN DIGITAL ---
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Nivel de Familiaridad Digital")
            fig_dig = px.bar(
                df_filtrado["nivel_digital"].value_counts().reset_index(),
                x="nivel_digital", y="count",
                labels={"nivel_digital": "Nivel", "count": "Personas"},
                color_discrete_sequence=["#6B2C91"]
            )
            st.plotly_chart(fig_dig, use_container_width=True)

        with c2:
            st.subheader("Dispositivos Tecnológicos Disponibles")
            fig_disp = px.bar(
                df_filtrado["dispositivos_disponibles"].value_counts().reset_index(),
                x="count", y="dispositivos_disponibles",
                orientation="h",
                labels={"count": "Frecuencia", "dispositivos_disponibles": "Dispositivo"},
                color_discrete_sequence=["#E86F25"]
            )
            st.plotly_chart(fig_disp, use_container_width=True)

    # --- TAB 4: SALUD Y BIENESTAR ---
    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Percepción de Apoyo Emocional")
            fig_emo = px.pie(df_filtrado, names="apoyo_emocional", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_emo, use_container_width=True)

        with c2:
            st.subheader("Percepción de Seguridad en el Barrio")
            fig_seg = px.bar(
                df_filtrado["percepcion_seguridad"].value_counts().reset_index(),
                x="percepcion_seguridad", y="count",
                labels={"percepcion_seguridad": "Sensación", "count": "Personas"},
                color_discrete_sequence=["#C1440E"]
            )
            st.plotly_chart(fig_seg, use_container_width=True)

    # --- TAB 5: EXPLORADOR DE DATOS ---
    with tab5:
        st.subheader("Vista Detallada de Registros")
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Botón para descargar los datos filtrados en CSV
        csv_data = df_filtrado.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv_data,
            file_name="caracterizacion_afroenzar_filtrada.csv",
            mime="text/csv"
        )
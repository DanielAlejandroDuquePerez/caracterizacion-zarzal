import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Configuración de página
st.set_page_config(
    page_title="Caracterización Socioeconómica - Afroenzar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Paleta Oficial Afroenzar
PALETA_AFROENZAR = [
    "#2D5016",  # Verde Selva
    "#F4A500",  # Amarillo Dorado
    "#C1440E",  # Terracota
    "#1B4B6B",  # Azul Río
    "#6B2C91",  # Morado Ancestral
    "#E86F25",  # Naranja Vivo
]

# 3. CSS Personalizado (Tarjetas de Métricas y Encabezados)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F4A500;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #EAD7C3;
        margin-bottom: 25px;
    }
    
    /* Tarjetas de Métricas (KPI Cards) */
    .kpi-card {
        background-color: #1A2417;
        border-left: 5px solid #F4A500;
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #A0A0A0;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Carga de datos
@st.cache_data
def cargar_datos():
    ruta = os.path.join("data", "processed", "caracterizacion_limpia.csv")
    if not os.path.exists(ruta):
        st.error(f"⚠️ No se encontró el archivo '{ruta}'. Ejecuta primero 'python clean_data.py'.")
        return pd.DataFrame()
    return pd.read_csv(ruta)

df = cargar_datos()

if not df.empty:

    # Encabezado
    st.markdown('<div class="main-title">📊 Caracterización Socioeconómica</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Asociación de Mujeres Afrocolombianas Emprendedoras de Zarzal (Afroenzar)</div>', unsafe_allow_html=True)

    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros de Diagnóstico")
    
    rangos_edad = ["Todos"] + sorted(list(df["rango_edad"].dropna().unique()))
    filtro_edad = st.sidebar.selectbox("Rango de Edad:", rangos_edad)
    
    niveles_edu = ["Todos"] + sorted(list(df["nivel_educativo"].dropna().unique()))
    filtro_edu = st.sidebar.selectbox("Nivel Educativo:", niveles_edu)

    sit_laboral = ["Todos"] + sorted(list(df["situacion_laboral"].dropna().unique()))
    filtro_laboral = st.sidebar.selectbox("Situación Laboral:", sit_laboral)

    # Filtrar DataFrame
    df_filtrado = df.copy()
    if filtro_edad != "Todos":
        df_filtrado = df_filtrado[df_filtrado["rango_edad"] == filtro_edad]
    if filtro_edu != "Todos":
        df_filtrado = df_filtrado[df_filtrado["nivel_educativo"] == filtro_edu]
    if filtro_laboral != "Todos":
        df_filtrado = df_filtrado[df_filtrado["situacion_laboral"] == filtro_laboral]

    total_personas = len(df_filtrado)

    # Métricas KPIs con HTML/CSS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Muestra Analizada</div>
                <div class="kpi-value">{total_personas} Integrantes</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        insuficiente = df_filtrado["suficiencia_ingresos"].str.contains("No", na=False).sum() if "suficiencia_ingresos" in df_filtrado.columns else 0
        pct_insuficiente = (insuficiente / total_personas * 100) if total_personas > 0 else 0
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #C1440E;">
                <div class="kpi-title">Ingresos Insuficientes</div>
                <div class="kpi-value">{pct_insuficiente:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        con_internet = df_filtrado["servicios_publicos"].str.contains("Internet", na=False).sum() if "servicios_publicos" in df_filtrado.columns else 0
        pct_internet = (con_internet / total_personas * 100) if total_personas > 0 else 0
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #1B4B6B;">
                <div class="kpi-title">Acceso a Internet</div>
                <div class="kpi-value">{pct_internet:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        modo_digital = df_filtrado["nivel_digital"].mode()[0] if "nivel_digital" in df_filtrado.columns and not df_filtrado["nivel_digital"].empty else "N/A"
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #6B2C91;">
                <div class="kpi-title">Familiaridad Digital</div>
                <div class="kpi-value">{modo_digital}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Pestañas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Demografía y Vivienda", 
        "💼 Empleo e Ingresos", 
        "💻 Inclusión Digital", 
        "🌱 Salud y Bienestar",
        "📋 Explorador de Datos"
    ])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Distribución por Rango de Edad")
            fig_edad = px.pie(
                df_filtrado, names="rango_edad", hole=0.45,
                color_discrete_sequence=PALETA_AFROENZAR
            )
            fig_edad.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_edad, use_container_width=True)

        with c2:
            st.markdown("##### Nivel Educativo Alcanzado")
            fig_edu = px.bar(
                df_filtrado["nivel_educativo"].value_counts().reset_index(),
                x="count", y="nivel_educativo", orientation="h",
                labels={"count": "Cantidad", "nivel_educativo": ""},
                color_discrete_sequence=["#F4A500"]
            )
            fig_edu.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_edu, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Situación Laboral Actual")
            fig_lab = px.bar(
                df_filtrado["situacion_laboral"].value_counts().reset_index(),
                x="situacion_laboral", y="count",
                labels={"situacion_laboral": "Estado", "count": "Personas"},
                color_discrete_sequence=["#1B4B6B"]
            )
            fig_lab.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_lab, use_container_width=True)

        with c2:
            st.markdown("##### Horas Diarias Dedicadas al Cuidado y Trabajo Doméstico")
            fig_dom = px.pie(
                df_filtrado, names="horas_trabajo_domestico",
                color_discrete_sequence=PALETA_AFROENZAR
            )
            fig_dom.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_dom, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Nivel de Familiaridad Digital")
            fig_dig = px.bar(
                df_filtrado["nivel_digital"].value_counts().reset_index(),
                x="nivel_digital", y="count",
                labels={"nivel_digital": "Nivel", "count": "Personas"},
                color_discrete_sequence=["#6B2C91"]
            )
            fig_dig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_dig, use_container_width=True)

        with c2:
            st.markdown("##### Dispositivos Tecnológicos Disponibles")
            fig_disp = px.bar(
                df_filtrado["dispositivos_disponibles"].value_counts().reset_index(),
                x="count", y="dispositivos_disponibles", orientation="h",
                labels={"count": "Frecuencia", "dispositivos_disponibles": ""},
                color_discrete_sequence=["#E86F25"]
            )
            fig_disp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_disp, use_container_width=True)

    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Percepción de Apoyo Emocional o Psicológico")
            fig_emo = px.pie(
                df_filtrado, names="apoyo_emocional",
                color_discrete_sequence=["#2D5016", "#C1440E", "#F4A500"]
            )
            fig_emo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_emo, use_container_width=True)

        with c2:
            st.markdown("##### Percepción de Seguridad en el Barrio")
            fig_seg = px.bar(
                df_filtrado["percepcion_seguridad"].value_counts().reset_index(),
                x="percepcion_seguridad", y="count",
                labels={"percepcion_seguridad": "Percepción", "count": "Personas"},
                color_discrete_sequence=["#C1440E"]
            )
            fig_seg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_seg, use_container_width=True)

    with tab5:
        st.subheader("Matriz de Datos")
        st.dataframe(df_filtrado, use_container_width=True)
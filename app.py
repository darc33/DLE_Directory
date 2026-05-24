import streamlit as st
import plotly.express as px

from utils.data_loader import (
    cargar_datos,
    obtener_resumen_anual,
    obtener_conteos
)

from utils.styles import cargar_estilos

st.set_page_config(
    page_title="DLE Antonio Nariño",
    page_icon="🏫",
    layout="wide"
)

cargar_estilos()

# CARGA DE DATOS
(
    instituciones,
    resoluciones,
    _,
    _,
    _,
    _,
    _,
    cerrados,
    _,
    update_date
) = cargar_datos()

# HEADER
top_left, top_right = st.columns([5, 1])

with top_left:

    st.title("DIRECCIÓN LOCAL DE EDUCACIÓN ANTONIO NARIÑO")

    st.caption("Sistema de Consulta Institucional")

with top_right:

    st.markdown(
        f"""
        <div style="
            text-align: right;
            font-size: 0.85rem;
            margin-top: 35px;
            line-height: 1.6;
        ">
            <b>Versión:</b> v1.1.0<br>
            <b>Actualizado:</b> {update_date.strftime('%d/%m/%Y %H:%M')}
        </div>
        """,
        unsafe_allow_html=True
    )

# BOTÓN CONSULTA
if st.button(
    "🔍 CONSULTAR INSTITUCIONES",
    width="stretch"
):
    st.switch_page("pages/Instituciones.py")

st.divider()

# KPIs
conteos = obtener_conteos(instituciones)

conteos["CERRADOS"] = len(cerrados)

# RESUMEN ANUAL
resumen = obtener_resumen_anual(resoluciones)

# LAYOUT
left, right = st.columns([1, 5])

# TARJETAS KPI
with left:

    for categoria, valor in conteos.items():

        if st.button(
            f"{valor}\n\n{categoria}",
            width="stretch"
        ):

            st.session_state["categoria"] = categoria

            st.switch_page("pages/Categorias.py")

# TABLA + GRÁFICO
with right:

    st.subheader("RESOLUCIONES POR AÑO")

    st.dataframe(
        resumen,
        width="stretch",
        hide_index=True
    )

    fig = px.bar(
        resumen,
        x="Año",
        y="Resoluciones",
        title="Resoluciones por Año"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

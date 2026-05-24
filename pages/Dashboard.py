import streamlit as st
import plotly.express as px

from utils.data_loader import (
    cargar_datos,
    obtener_resumen_anual,
    obtener_conteos
)

from utils.styles import cargar_estilos

cargar_estilos()

st.title("DASHBOARD")

(
    instituciones,
    resoluciones,
    _,
    _,
    _,
    _,
    _,
    cerrados,
    _
) = cargar_datos()

conteos = obtener_conteos(instituciones)
conteos["CERRADOS"] = len(cerrados)

resumen = obtener_resumen_anual(resoluciones)

left, right = st.columns([1, 5])

with left:

    for categoria, valor in conteos.items():

        if st.button(
            f"{valor}\n\n{categoria}",
            width='stretch', #use_container_width=True
        ):

            st.session_state["categoria"] = categoria
            st.switch_page("pages/Categorias.py")

with right:

    st.dataframe(
        resumen,
        width='stretch', #use_container_width=True,
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
        width='stretch', #use_container_width=True
    )

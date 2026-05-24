import streamlit as st
import pandas as pd

from utils.data_loader import cargar_archivo
from utils.styles import cargar_estilos

cargar_estilos()

st.title("ARCHIVO FÍSICO")

# BOTÓN VOLVER
if st.button(
    "⬅️ Volver al Dashboard",
    width="stretch"
):
    st.switch_page("app.py")

archivo, total_cajas, total_carpetas = cargar_archivo()

# Quitar horas en fechas
for col in archivo.columns:

    if "fecha" in str(col).lower():

        archivo[col] = pd.to_datetime(
            archivo[col],
            errors="coerce"
        ).dt.date

# KPIs
col1, col2 = st.columns(2)

with col1:

    st.metric(
        "TOTAL CAJAS",
        total_cajas
    )

with col2:

    st.metric(
        "TOTAL CARPETAS",
        total_carpetas
    )

st.divider()

# Buscador
busqueda = st.text_input(
    "Buscar"
)

if busqueda:

    archivo = archivo[
        archivo.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                busqueda,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]

st.dataframe(
    archivo,
    width="stretch",
    hide_index=True
)
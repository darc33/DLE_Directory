import streamlit as st
import pandas as pd

from utils.data_loader import cargar_bienes
from utils.styles import cargar_estilos

cargar_estilos()

st.title("BIENES")

# VOLVER
if st.button(
    "⬅️ Volver al Dashboard",
    width="stretch"
):
    st.switch_page("app.py")

bienes = cargar_bienes()

# FORMATEAR FECHAS
for col in bienes.columns:

    if "fecha" in str(col).lower():

        bienes[col] = pd.to_datetime(
            bienes[col],
            errors="coerce"
        ).dt.date

# BUSCADOR
busqueda = st.text_input(
    "Buscar bienes"
)

if busqueda:

    bienes = bienes[
        bienes.astype(str)
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

# KPIs
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "TOTAL BIENES",
        len(bienes)
    )

with col2:

    st.metric(
        "RESPONSABLES",
        bienes["RESPONSABLE"].nunique()
    )

with col3:

    st.metric(
        "UBICACIONES",
        bienes["UBICACIÓN"].nunique()
    )

st.divider()

# TABLA
st.dataframe(
    bienes,
    width="stretch",
    hide_index=True
)
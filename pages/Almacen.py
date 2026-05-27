import streamlit as st

from utils.data_loader import cargar_almacen
from utils.styles import cargar_estilos

cargar_estilos()

st.title("ALMACÉN")

almacen = cargar_almacen()

# VOLVER
if st.button(
    "⬅️ Volver al Dashboard",
    width="stretch"
):
    st.switch_page("app.py")

# BUSCADOR
busqueda = st.text_input(
    "Buscar productos"
)

if busqueda:

    almacen = almacen[
        almacen.astype(str)
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
        "PRODUCTOS",
        len(almacen)
    )

with col2:

    st.metric(
        "CATEGORÍAS",
        almacen["CATEGORIA"].nunique()
    )

with col3:

    st.metric(
        "UNIDADES",
        almacen["CANTIDAD"].sum()
    )

st.divider()

# TABLA
st.dataframe(
    almacen,
    width="stretch",
    hide_index=True
)
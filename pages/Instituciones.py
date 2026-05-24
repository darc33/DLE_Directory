import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
from utils.styles import cargar_estilos

cargar_estilos()

(
    instituciones,
    resoluciones,
    _,
    _,
    _,
    _,
    _,
    _,
    _
) = cargar_datos()

st.title("CONSULTA DE INSTITUCIONES")

institucion_nombre = st.selectbox(
    "Buscar institución",
    instituciones["Nombre Institución"].sort_values().unique()
)

institucion = instituciones[
    instituciones["Nombre Institución"] == institucion_nombre
].iloc[0]

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    ### Información General

    **Código DANE:** {institucion['CODIGO DANE']}

    **Institución:** {institucion['Nombre Institución']}

    **Estado:** {institucion['STATUS']}

    **Tipo:** {institucion['TIPO']}
    """)

with col2:
    st.markdown(f"""
    ### Información de Contacto
    """)

    '''st.markdown(f"""
    ### Información de Contacto

    **Dirección:** {institucion['direccion']}

    **Teléfono:** {institucion['telefono']}

    **Email:** {institucion['email']}

    **Contacto:** {institucion['contacto']}
    """)'''

st.divider()

st.subheader("RESOLUCIONES")

res_inst = resoluciones[
    resoluciones["Nombre Institución"] == institucion["Nombre Institución"]
].copy()

# Convertir fechas
columnas_fecha = [
    "Fecha de Resolución",
    "Fecha de Notificación",
    "Fecha de Ejecutoria",
    "Fecha entrega archivo"
]

for col in columnas_fecha:

    res_inst[col] = pd.to_datetime(
        res_inst[col],
        errors="coerce"
    ).dt.date

# Ordenar por fecha de resolución descendente
res_inst = res_inst.sort_values(
    by="Fecha de Resolución",
    ascending=False
)

# Seleccionar columnas a mostrar
res_inst = res_inst[
    [
        "# RESOLUCIÓN",
        "Fecha de Resolución",
        "Fecha de Notificación",
        "Fecha de Ejecutoria",
        "Descripcion",
        "SIET",
        "DUEB",
        "Fecha entrega archivo",
        "OBSERVACIONES"
    ]
]

st.dataframe(
    res_inst,
    width='stretch',
    hide_index=True
)
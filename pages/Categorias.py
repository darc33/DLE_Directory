import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
from utils.styles import cargar_estilos

cargar_estilos()

(
    instituciones,
    _,
    oficiales,
    privados,
    adultos,
    etdh,
    cea,
    cerrados,
    ilegales
) = cargar_datos()

categoria = st.session_state.get("categoria", None)

st.title(f"CATEGORÍA: {categoria}")

if categoria == "OFICIALES":
    df = oficiales

elif categoria == "PRIVADOS":
    df = privados

elif categoria == "ADULTOS":
    df = adultos

elif categoria == "ETDH":
    df = etdh

elif categoria == "CEAs":
    df = cea

elif categoria == "ILEGALES":
    df = ilegales

elif categoria == "CERRADOS":
    df = cerrados

else:

    df = instituciones

# Detectar y formatear columnas fecha
for col in df.columns:

    if "fecha" in str(col).lower():

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        ).dt.date

st.dataframe(
    df,
    width='stretch',
    hide_index=True
)
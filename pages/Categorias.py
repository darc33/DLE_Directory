import streamlit as st

from utils.data_loader import cargar_datos
from utils.styles import cargar_estilos

cargar_estilos()

instituciones, _ = cargar_datos()

categoria = st.session_state.get("categoria", None)

st.title(f"CATEGORÍA: {categoria}")

if categoria == "OFICIALES":
    df = instituciones[(instituciones["TIPO"] == "OFICIAL") & (instituciones["STATUS"] == "ABIERTO")]

elif categoria == "PRIVADOS":
    df = instituciones[(instituciones["TIPO"] == "PRIVADO") & (instituciones["STATUS"] == "ABIERTO")]

elif categoria == "ADULTOS":
    df = instituciones[(instituciones["TIPO"] == "ADULTOS") & (instituciones["STATUS"] == "ABIERTO")]

elif categoria == "ETDH":
    df = instituciones[(instituciones["TIPO"] == "ETDH") & (instituciones["STATUS"] == "ABIERTO")] 

elif categoria == "CEAs":
    df = instituciones[(instituciones["TIPO"] == "CEA") & (instituciones["STATUS"] == "ABIERTO")]

elif categoria == "ILEGALES":
    df = instituciones[instituciones["STATUS"] == "ILEGAL"]

elif categoria == "CERRADOS":
    df = instituciones[instituciones["STATUS"] == "CERRADO"]

else:
    df = instituciones

st.dataframe(
    df,
    width='stretch',
    hide_index=True
)
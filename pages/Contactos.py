import streamlit as st

from utils.data_loader import cargar_contactos
from utils.styles import cargar_estilos

cargar_estilos()

st.title("DIRECTORIO DE CONTACTOS")

contactos = cargar_contactos()

# VOLVER
if st.button(
    "⬅️ Volver al Dashboard",
    width="stretch"
):
    st.switch_page("app.py")

# BUSCADOR
busqueda = st.text_input(
    "Buscar contactos"
)

if busqueda:

    contactos = contactos[
        contactos.astype(str)
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

st.divider()

# TABLA
st.dataframe(
    contactos,
    width="stretch",
    hide_index=True
)

# ÁREAS
areas = contactos["AREA"].dropna().unique()

for area in areas:

    with st.expander(
        area,
        expanded=False
    ):

        df_area = contactos[
            contactos["AREA"] == area
        ]

        for _, contacto in df_area.iterrows():

            st.markdown(
                f"""
                ### {contacto['NOMBRE']}

                🏢 {contacto['DEPENDENCIA']}

                📱 {contacto['CELULAR']}

                ☎️ {contacto['TELEFONO']}

                ✉️ {contacto['EMAIL']}

                📝 {contacto['OBSERVACIONES']}
                """
            )

            st.divider()
import pandas as pd
import streamlit as st

# LINK DIRECTO DE ONEDRIVE
EXCEL_URL = "https://internoredpedu-my.sharepoint.com/:x:/g/personal/cadel15_educacionbogota_edu_co/IQAJTK1Jq-gESaNLyJy_1tzrARu5pMHuf6K64Ircj1nWeP4?e=Zkx9sx&download=1"

@st.cache_data(ttl=300)
def cargar_datos():

    instituciones = pd.read_excel(
        EXCEL_URL,
        sheet_name="LISTAS"
    )

    resoluciones = pd.read_excel(
        EXCEL_URL,
        sheet_name="CONSOLIDADO RESOLUCIONES"
    )

    return instituciones, resoluciones


def obtener_resumen_anual(resoluciones):

    resoluciones["año"] = pd.to_datetime(
        resoluciones["Fecha de Resolución"]
        #errors = "coerce"
    ).dt.year

    resumen = (
        resoluciones
        .groupby("año")
        .agg(
            resoluciones=("# RESOLUCIÓN", "count"),
            notificadas=("Fecha de Notificación", lambda x: x.notna().sum()),
            ejecutoriadas=("Fecha de Ejecutoria", lambda x: x.notna().sum()),
            archivadas=("Fecha entrega archivo", lambda x: x.notna().sum())
        )
        .reset_index()
        .sort_values("año", ascending=False)
    )

    return resumen


def obtener_conteos(instituciones):

    return {
        "OFICIALES": len(instituciones[(instituciones["TIPO"] == "OFICIAL") & (instituciones["STATUS"] == "ABIERTO")]),
        "PRIVADOS": len(instituciones[(instituciones["TIPO"] == "PRIVADO") & (instituciones["STATUS"] == "ABIERTO")]),
        "ADULTOS": len(instituciones[(instituciones["TIPO"] == "ADULTOS") & (instituciones["STATUS"] == "ABIERTO")]),
        "ETDH": len(instituciones[(instituciones["TIPO"] == "ETDH") & (instituciones["STATUS"] == "ABIERTO")]),
        "CEAs": len(instituciones[(instituciones["TIPO"] == "CEA") & (instituciones["STATUS"] == "ABIERTO")]),
        "ILEGALES": len(instituciones[instituciones["STATUS"] == "ILEGAL"]),
        "CERRADOS": len(instituciones[instituciones["STATUS"] == "CERRADO"]),
    }

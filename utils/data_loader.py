import pandas as pd
import streamlit as st
import requests
from io import BytesIO
from datetime import datetime
from config import TTL

CACHE_TTL = TTL

# LINK DIRECTO DE ONEDRIVE
EXCEL_URL = "https://internoredpedu-my.sharepoint.com/:x:/g/personal/cadel15_educacionbogota_edu_co/IQAJTK1Jq-gESaNLyJy_1tzrARu5pMHuf6K64Ircj1nWeP4?e=Zkx9sx&download=1"
ARCHIVO_URL = "https://internoredpedu-my.sharepoint.com/:x:/g/personal/diego_ramirez441_educacionbogota_edu_co/IQBZ7hqV5TzEQKzNJr_5I-YcAYATXoegNCttZu35YqJy13Q?e=5yUApD&download=1"


def limpiar_dataframe(df):

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return df

@st.cache_data(ttl=300)
def cargar_datos():
    update_date = datetime.now()
    response = requests.get(EXCEL_URL)

    if response.status_code != 200:
        raise Exception(f"Error descargando archivo: {response.status_code}")

    excel_file = BytesIO(response.content)

    instituciones = pd.read_excel(
        excel_file,
        sheet_name="LISTAS"
    )
    excel_file.seek(0)
    
    resoluciones = pd.read_excel(
        excel_file,
        sheet_name="CONSOLIDADO RESOLUCIONES"
    )

    # CATEGORÍAS
    hojas = [
        "OFICIALES",
        "PRIVADOS",
        "Adultos",
        "ETDH",
        "CEAs",
        "CERRADOS",
        "ILEGALES"
    ]
    dataframes = {}

    for hoja in hojas:
        excel_file.seek(0)

        df = pd.read_excel(
            excel_file,
            sheet_name=hoja,
            header=1
        )

        dataframes[hoja] = limpiar_dataframe(df)
    
    oficiales = dataframes["OFICIALES"]
    privados = dataframes["PRIVADOS"]
    adultos = dataframes["Adultos"]
    etdh = dataframes["ETDH"]
    cea = dataframes["CEAs"]
    cerrados = dataframes["CERRADOS"]
    ilegales = dataframes["ILEGALES"]
    
    return (
        instituciones,
        resoluciones,
        oficiales,
        privados,
        adultos,
        etdh,
        cea,
        cerrados,
        ilegales,
        update_date
    )


def obtener_resumen_anual(resoluciones):

    resoluciones["Año"] = pd.to_datetime(
        resoluciones["Fecha de Resolución"]
        #errors = "coerce"
    ).dt.year

    

    resumen = (
        resoluciones
        .groupby("Año")
        .agg(
            Resoluciones=("# RESOLUCIÓN", "count"),
            Notificadas=("Fecha de Notificación", lambda x: x.notna().sum()),
            Ejecutoriadas=("Fecha de Ejecutoria", lambda x: x.notna().sum()),
            Archivadas=("Fecha entrega archivo", lambda x: x.notna().sum())
        )
        .reset_index()
        .sort_values("Año", ascending=False)
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

@st.cache_data(ttl=300)
def cargar_archivo():

    response = requests.get(ARCHIVO_URL)

    if response.status_code != 200:
        raise Exception(
            f"Error descargando archivo: {response.status_code}"
        )

    excel_file = BytesIO(response.content)

    # LEER TABLA
    archivo = pd.read_excel(
        excel_file,
        sheet_name="FUID EDITABLE",
        header=8
    )

    archivo = limpiar_dataframe(archivo)

    # ELIMINAR COLUMNA AÑO
    if "AÑO" in archivo.columns:

        archivo = archivo.drop(columns=["AÑO"])

    # LEER MÉTRICAS
    excel_file.seek(0)

    resumen = pd.read_excel(
        excel_file,
        sheet_name="FUID EDITABLE",
        header=None
    )

    total_cajas = resumen.iloc[6, 15]      # P7
    total_carpetas = resumen.iloc[6, 17]   # R7

    return archivo, total_cajas, total_carpetas

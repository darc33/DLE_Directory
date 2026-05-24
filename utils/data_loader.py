import pandas as pd
import streamlit as st
import requests
from io import BytesIO

# LINK DIRECTO DE ONEDRIVE
EXCEL_URL = "https://internoredpedu-my.sharepoint.com/:x:/g/personal/cadel15_educacionbogota_edu_co/IQAJTK1Jq-gESaNLyJy_1tzrARu5pMHuf6K64Ircj1nWeP4?e=Zkx9sx&download=1"

@st.cache_data(ttl=300)
def limpiar_dataframe(df):

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return df

def cargar_datos():

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
    '''
    oficiales = pd.read_excel(
        excel_file,
        sheet_name="OFICIALES",
        header=1
    )

    excel_file.seek(0)

    privados = pd.read_excel(
        excel_file,
        sheet_name="PRIVADOS",
        header=1
    )

    excel_file.seek(0)

    adultos = pd.read_excel(
        excel_file,
        sheet_name="Adultos",
        header=1
    )

    excel_file.seek(0)

    etdh = pd.read_excel(
        excel_file,
        sheet_name="ETDH",
        header=1
    )

    excel_file.seek(0)

    cea = pd.read_excel(
        excel_file,
        sheet_name="CEAs",
        header=1
    )

    excel_file.seek(0)

    cerrados = pd.read_excel(
        excel_file,
        sheet_name="CERRADOS",
        header=1
    )

    excel_file.seek(0)

    ilegales = pd.read_excel(
        excel_file,
        sheet_name="ILEGALES",
        header=1
    )'''

    return (
        instituciones,
        resoluciones,
        oficiales,
        privados,
        adultos,
        etdh,
        cea,
        cerrados,
        ilegales
    )


def obtener_resumen_anual(resoluciones):

    resoluciones["Año"] = pd.to_datetime(
        resoluciones["Fecha de Resolución"]
        #errors = "coerce"
    ).dt.year

    """# DEBUG
    debug_2026 = resoluciones[
        (resoluciones["Año"] == 2019)
    ]

    print("\n===== NOTIFICADAS 2024 =====")
    print(debug_2026[[
        "# RESOLUCIÓN",
        "Fecha de Resolución",
        "Fecha de Notificación"
    ]].to_string())"""

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

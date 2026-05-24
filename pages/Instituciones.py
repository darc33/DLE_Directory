import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
from utils.styles import cargar_estilos

cargar_estilos()

(
    instituciones,
    resoluciones,
    oficiales,
    privados,
    adultos,
    etdh,
    cea,
    cerrados,
    ilegales
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

    st.markdown("### Información Detallada")

    tipo = str(institucion["TIPO"]).strip().upper()
    status = str(institucion["STATUS"]).strip().upper()

    # Prioridad a status
    if status == "ILEGAL":
        hoja_detalle = ilegales

    elif status == "CERRADO":
        hoja_detalle = cerrados

    # Seleccionar hoja según tipo
    elif tipo == "OFICIAL":
        hoja_detalle = oficiales

    elif tipo == "PRIVADO":
        hoja_detalle = privados

    elif tipo == "ADULTOS":
        hoja_detalle = adultos

    elif tipo == "ETDH":
        hoja_detalle = etdh

    elif tipo == "CEA":
        hoja_detalle = cea

    else:
        hoja_detalle = instituciones

    '''print("\n===== DEBUG BUSQUEDA =====")
    print("INSTITUCION BASE:")
    print(repr(institucion["Nombre Institución"]))
    print("\nINSTITUCIONES EN HOJA:")
    print(
        hoja_detalle["INSTITUCIÓN"]
        .astype(str)
        .head(20)
        .tolist()
    )'''
    # Buscar institución en hoja correspondiente
    detalle = hoja_detalle[
        hoja_detalle["INSTITUCIÓN"] == institucion["Nombre Institución"]
    ]

    if not detalle.empty:

        detalle = detalle.iloc[0]

        columnas_excluir = [
            "Nº",
            "CLASE",
            "CODIGO DANE",
            "Nombre Institución",
            "INSTITUCIÓN",
            "TIPO"
        ]

        for columna in detalle.index:

            if columna not in columnas_excluir:

                valor = detalle[columna]

                # Quitar hora si es fecha
                if isinstance(valor, pd.Timestamp):
                    valor = valor.date()

                st.markdown(f"""
                **{columna}:** {valor}
                """)

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
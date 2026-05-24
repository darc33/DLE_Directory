import streamlit as st

def cargar_estilos():

    st.markdown("""
    <style>

    .main {
        background-color: #1E1E1E;
    }

    .block-container {
        padding-top: 1rem;
    }

    .card {
        background-color: #2A2A2A;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
        text-align: center;
        margin-bottom: 10px;
    }

    .card-number {
        font-size: 32px;
        font-weight: bold;
        color: white;
    }

    .card-label {
        font-size: 18px;
        color: #CCCCCC;
    }

    .titulo {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .stDataFrame {
        border: 1px solid #444;
    }

    .stDataFrame td {
        text-align: center !important;
    }

    .stDataFrame th {
        text-align: center !important;
    }

    </style>
    """, unsafe_allow_html=True)

import streamlit as st

ACTIVE_ENV = st.secrets["ENV"]

CONFIG = st.secrets[ACTIVE_ENV]

TTL = CONFIG["TTL"]
VERSION = CONFIG["VERSION"]
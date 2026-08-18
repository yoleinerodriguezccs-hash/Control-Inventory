import streamlit as st
import pandas as pd

st.title("📦 Control de Inventario")

st.write("Sube un archivo Excel para analizar tu inventario.")

archivo = st.file_uploader(
    "Selecciona tu archivo Excel",
    type=["xlsx"]
)

if archivo is not None:

    datos = pd.read_excel(archivo)

    st.subheader("📋 Inventario")

    st.dataframe(datos)

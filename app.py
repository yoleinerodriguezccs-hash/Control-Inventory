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

    # Crear estado del producto
    datos["Estado"] = datos["Cantidad"].apply(
        lambda cantidad: "❌ Agotado" if cantidad == 0 else "✅ Disponible"
    )

    st.subheader("📋 Inventario")

    st.dataframe(datos)

    # Estadísticas
    total_productos = len(datos)
    disponibles = (datos["Cantidad"] > 0).sum()
    agotados = (datos["Cantidad"] == 0).sum()

    st.subheader("📊 Estadísticas")

    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Productos", total_productos)
    col2.metric("✅ Disponibles", disponibles)
    col3.metric("❌ Agotados", agotados)

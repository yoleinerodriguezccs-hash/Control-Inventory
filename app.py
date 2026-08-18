import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Control de Inventario")

st.write("Sube un archivo Excel para analizar tu inventario.")

archivo = st.file_uploader(
    "Selecciona tu archivo Excel",
    type=["xlsx"]
)

if archivo is not None:

    datos = pd.read_excel(archivo)

    # Convertir la fecha de vencimiento
    datos["Fecha vencimiento"] = pd.to_datetime(
        datos["Fecha vencimiento"],
        errors="coerce"
    )

    # Estado del producto
    datos["Estado"] = datos["Cantidad"].apply(
        lambda cantidad: "❌ Agotado" if cantidad == 0 else "✅ Disponible"
    )

    # Fecha actual
    hoy = pd.Timestamp.today().normalize()

    # Calcular días que faltan para vencer
    datos["Días para vencer"] = (
        datos["Fecha vencimiento"] - hoy
    ).dt.days

    # Estado de vencimiento
    def revisar_vencimiento(dias):
        if pd.isna(dias):
            return "⚪ Sin fecha"
        elif dias < 0:
            return "🔴 Vencido"
        elif dias <= 30:
            return "🟡 Próximo a vencer"
        else:
            return "🟢 Vigente"

    datos["Vencimiento"] = datos["Días para vencer"].apply(
        revisar_vencimiento
    )

    # Mostrar inventario
    st.subheader("📋 Inventario")

    st.dataframe(datos)

    # Estadísticas
    total_productos = len(datos)
    disponibles = (datos["Cantidad"] > 0).sum()
    agotados = (datos["Cantidad"] == 0).sum()
    proximos = (datos["Vencimiento"] == "🟡 Próximo a vencer").sum()
    vencidos = (datos["Vencimiento"] == "🔴 Vencido").sum()

    st.subheader("📊 Estadísticas")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📦 Productos", total_productos)
    col2.metric("✅ Disponibles", disponibles)
    col3.metric("❌ Agotados", agotados)
    col4.metric("🟡 Próximos", proximos)
    col5.metric("🔴 Vencidos", vencidos)

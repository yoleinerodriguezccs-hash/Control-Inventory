# -------------------------
# GRÁFICOS
# -------------------------

st.subheader("📊 Gráficos del inventario")

# Gráfico de productos por categoría
st.write("### 📁 Productos por categoría")

productos_categoria = (
    filtrados.groupby("Categoría")["Cantidad"]
    .sum()
)

st.bar_chart(productos_categoria)


# Gráfico de disponibles y agotados
st.write("### 📦 Disponibles vs. agotados")

disponibilidad = pd.DataFrame({
    "Cantidad": [
        disponibles,
        agotados
    ]
}, index=[
    "✅ Disponibles",
    "❌ Agotados"
])

st.bar_chart(disponibilidad)


# Gráfico de vencimientos
st.write("### ⚠️ Estado de vencimiento")

vencimiento_grafico = pd.DataFrame({
    "Cantidad": [
        (filtrados["Vencimiento"] == "🟢 Vigente").sum(),
        (filtrados["Vencimiento"] == "🟡 Próximo a vencer").sum(),
        (filtrados["Vencimiento"] == "🔴 Vencido").sum()
    ]
}, index=[
    "🟢 Vigente",
    "🟡 Próximo a vencer",
    "🔴 Vencido"
])

st.bar_chart(vencimiento_grafico)

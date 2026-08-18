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

    # Convertir fechas
    datos["Fecha vencimiento"] = pd.to_datetime(
        datos["Fecha vencimiento"],
        errors="coerce"
    )

    # Estado del inventario
    datos["Estado"] = datos["Cantidad"].apply(
        lambda cantidad: "❌ Agotado"
        if cantidad == 0
        else "✅ Disponible"
    )

    # Fecha actual
    hoy = pd.Timestamp.today().normalize()

    # Días para vencer
    datos["Días para vencer"] = (
        datos["Fecha vencimiento"] - hoy
    ).dt.days

    # Revisar vencimiento
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

    # -------------------------
    # FILTROS
    # -------------------------

    st.sidebar.header("⚙️ Filtros")

    categorias = ["Todas"] + sorted(
        datos["Categoría"].dropna().unique().tolist()
    )

    categoria_seleccionada = st.sidebar.selectbox(
        "Categoría",
        categorias
    )

    estados = ["Todos", "✅ Disponible", "❌ Agotado"]

    estado_seleccionado = st.sidebar.selectbox(
        "Estado",
        estados
    )

    vencimientos = [
        "Todos",
        "🟢 Vigente",
        "🟡 Próximo a vencer",
        "🔴 Vencido"
    ]

    vencimiento_seleccionado = st.sidebar.selectbox(
        "Vencimiento",
        vencimientos
    )

    # Aplicar filtros
    filtrados = datos.copy()

    if categoria_seleccionada != "Todas":
        filtrados = filtrados[
            filtrados["Categoría"] == categoria_seleccionada
        ]

    if estado_seleccionado != "Todos":
        filtrados = filtrados[
            filtrados["Estado"] == estado_seleccionado
        ]

    if vencimiento_seleccionado != "Todos":
        filtrados = filtrados[
            filtrados["Vencimiento"] == vencimiento_seleccionado
        ]

    # -------------------------
    # ESTADÍSTICAS
    # -------------------------

    st.subheader("📊 Estadísticas")

    total_productos = len(filtrados)

    disponibles = (
        filtrados["Cantidad"] > 0
    ).sum()

    agotados = (
        filtrados["Cantidad"] == 0
    ).sum()

    proximos = (
        filtrados["Vencimiento"] ==
        "🟡 Próximo a vencer"
    ).sum()

    vencidos = (
        filtrados["Vencimiento"] ==
        "🔴 Vencido"
    ).sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "📦 Productos",
        total_productos
    )

    col2.metric(
        "✅ Disponibles",
        disponibles
    )

    col3.metric(
        "❌ Agotados",
        agotados
    )

    col4.metric(
        "🟡 Próximos a vencer",
        proximos
    )

    col5.metric(
        "🔴 Vencidos",
        vencidos
    )

    # -------------------------
    # TABLA
    # -------------------------

    st.subheader("📋 Inventario")

    st.dataframe(
        filtrados,
        use_container_width=True
    )

import streamlit as st
from conversor_bce import descargar_xml, parsear_xml, convertir_divisa

st.set_page_config(
    page_title="Conversor de Divisas (BCE)",
    page_icon="💶",
    layout="centered"
)


@st.cache_data(ttl=3600)
def cargar_datos_bce():
    contenido_xml = descargar_xml()
    fecha_oficial, dict_tasas = parsear_xml(contenido_xml)
    return contenido_xml, fecha_oficial, dict_tasas


st.title("💶 Conversor de Divisas (BCE)")
st.write("Esta aplicación consume **XML en tiempo real** del Banco Central Europeo.")

try:
    xml_bytes, fecha, tasas = cargar_datos_bce()
except Exception as error:
    st.error(f"❌ Error al obtener los tipos de cambio del BCE: {error}")
    st.stop()

with st.expander("🔍 Ver Estructura XML recibida (Raw Data)"):
    st.code(xml_bytes.decode("utf-8", errors="replace"), language="xml")

st.success(f"✅ Datos cargados. Fecha oficial: **{fecha}**")

col1, col2, col3 = st.columns([1.5, 1, 1])

lista_monedas = sorted(tasas.keys())
idx_eur = lista_monedas.index("EUR") if "EUR" in lista_monedas else 0
idx_usd = lista_monedas.index("USD") if "USD" in lista_monedas else 0

with col1:
    importe_input = st.text_input("Cantidad", value="100.00")

with col2:
    moneda_origen = st.selectbox("De:", options=lista_monedas, index=idx_eur)

with col3:
    moneda_destino = st.selectbox("A:", options=lista_monedas, index=idx_usd)

boton_calcular = st.button("Calcular Conversión", type="primary")

if boton_calcular:
    try:
        resultado = convertir_divisa(importe_input, moneda_origen, moneda_destino, tasas)
        tasa_unitaria = convertir_divisa("1.0", moneda_origen, moneda_destino, tasas)

        st.markdown(f"**Valor en {moneda_destino}**")
        st.markdown(f"## {resultado:,.2f} {moneda_destino}")
        st.markdown(f":green[↑ Tipo de cambio: 1 {moneda_origen} = {tasa_unitaria:.4f} {moneda_destino}]")

    except ValueError as err_val:
        st.error(f"⚠️ {err_val}")

st.divider()

st.subheader("📊 Tabla de Tipos de Cambio (Base EUR)")

datos_tabla = [{"Moneda": m, "Tasa": t} for m, t in tasas.items()]
st.dataframe(datos_tabla, use_container_width=True, hide_index=True)

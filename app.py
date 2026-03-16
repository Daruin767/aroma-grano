import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="BizIntelligence Aroma & Grano", layout="wide")
st.title("📊 BI Dashboard: Aroma & Grano")

# --- CARGA PROFESIONAL ---
@st.cache_data
def cargar_inventario():
    # Usamos low_memory=False para archivos grandes (en este caso es pequeño pero es buena práctica)
    return pd.read_csv("ventas_pro.csv")

df = cargar_inventario()

# --- SONDEO INICIAL (Teoría en acción) ---
st.header("🔍 1. Sondeo de Categorías")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Productos Únicos", df['producto'].nunique())
    
with col2:
    st.write("Tipos de productos encontrados:")
    st.write(df['tipo'].unique())

with col3:
    st.write("Frecuencia de ventas por producto:")
    st.write(df['producto'].value_counts())

resultado = st.text_area(
"El motor de carga y sondeo, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se esta cargando la información de archivo CSV, despues de que se cargan los datos, se hace un sondeo inicial para conocer el numero de productos únicos, los tipos de productos y la frecuencia de ventas por producto.
""",
)


st.divider()
st.header("🛠️ 2. Motor de Limpieza")

# PASO A: Eliminar Duplicados (Vimos el ID 2 y 10 repetidos en el CSV)
df = df.drop_duplicates(subset=['id'])

# PASO B: Corregir Tipos de Datos
# El CSV tiene el ID 12 con cantidad "1" entre comillas (texto). Lo forzamos a número.
df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')

# PASO C: Rellenar Nulos (NaN)
# Si no sabemos la cantidad, asumiremos que se vendió 1 unidad.
df['cantidad'] = df['cantidad'].fillna(1)

st.success("✅ Limpieza automátizada: Duplicados removidos, números corregidos y nulos rellenados.")
st.dataframe(df)


resultado = st.text_area(
"Limpieza profunda paso a paso, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se eliminan los elementos duplicados en el archivo CSV, se corrigen los números que están entre comillas y se fuerzan a que sean números y se rellenas los datos nulos, como no se sabe la cantidad se asume que se vendió 1 unidad.
""",
)



st.divider()
st.header("✨ 3. Transformación de Reporte")

# Calculamos el subtotal primero
df['Ingreso_Bruto'] = df['precio'] * df['cantidad']

# CREAMOS UNA VISTA LIMPIA PARA EL REPORTE
# Renombramos y ordenamos de mayor ingreso a menor
reporte_ejecutivo = df.rename(columns={
    'id': 'ID Pedido',
    'producto': 'Producto',
    'Ingreso_Bruto': 'Venta Total ($)'
}).sort_values(by='Venta Total ($)', ascending=False)

st.write("Top de ventas del mes (Ordenado):")
st.dataframe(reporte_ejecutivo[['ID Pedido', 'Producto', 'Venta Total ($)']].head(10))

resultado = st.text_area(
"Transformacion y orden, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se calcula el ingreso bruto multiplicando el precio por la cantidad, luego se crea una vista limpia para el reporte, se renombran las columnas y se ordena de mayor a menor ingreso.
""",
)


st.sidebar.header("⚙️ Panel de Auditoría")

# Filtro multi-selección
ciudades_filtro = st.sidebar.multiselect(
    "Filtrar por Tipo:",
    options=df['tipo'].unique(),
    default=df['tipo'].unique()
)

# Filtro Slider
monto_min = st.sidebar.slider("Ver ventas superiores a ($):", 0, 100, 0)

# APLICACIÓN DE LÓGICA FILTRADO (AND)
# Que pertenezca al tipo seleccionado Y supere el monto mínimo
df_final = df[(df['tipo'].isin(ciudades_filtro)) & (df['Ingreso_Bruto'] >= monto_min)]

st.subheader("📋 Pedidos Filtrados")
st.table(df_final)

resultado = st.text_area(
"Dashboard interactivo, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se pueden seleccionar los tipos de productos que se quieren ver y también se puede filtrar por monto mínimo de venta. El resultado es una tabla que muestra solo los pedidos que cumplen con ambos criterios.
""",
)



st.divider()
st.header("📈 4. Análisis Agregado")

# Agrupamos por tipo y sumamos ingresos
resumen = df.groupby('tipo')['Ingreso_Bruto'].agg(['sum', 'count', 'mean']).round(2)
st.write(resumen)

st.bar_chart(resumen['sum'])

resultado = st.text_area(
"Resumen por categoria, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se agrupa por tipo de producto y se suman los ingresos brutos, también se cuenta el número de pedidos y se calcula el ingreso promedio por tipo. Luego se muestra un gráfico de barras con la suma de ingresos por tipo.
""",
)



# Tabla de ejemplo de proveedores
proveedores = pd.DataFrame({
    'producto': ['Espresso', 'Latte', 'Capuccino', 'Muffin', 'Cold Brew', 'Pastel de Chocolate'],
    'Proveedor': ['Granos del Cauca', 'Lácteos Central', 'Lácteos Central', 'Trigo & Sal', 'Refrescantes S.A.', 'Delicias Doña Ana']
})

# Fusión (Merge)
df_maestro = pd.merge(df, proveedores, on='producto', how='left')

st.header("🏢 Contacto de Proveedores por Pedido")

st.dataframe(df_maestro[['id', 'producto', 'Proveedor']])

resultado = st.text_area(
"Union con proveedores, ✍️ Tu explicación (Propias palabras, sin IA)",
value="""Primero se crea una tabla de proveedores donde cada producto está asociado con su proveedor correspondiente. 
Luego se realiza una fusión entre el DataFrame original de pedidos y la tabla de proveedores usando la columna "producto" como clave. 
Se utiliza un tipo de unión para mantener todos los registros del DataFrame original y agregar la información del proveedor cuando exista coincidencia. 
El resultado es un DataFrame maestro que muestra cada pedido junto con el proveedor del producto.
""",
)   
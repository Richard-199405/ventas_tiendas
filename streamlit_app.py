import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título de la aplicación
st.title("Análisis Exploratorio de Datos (EDA)")

# Cargar los datos desde un archivo CSV
@st.cache_data  # Decorador para cachear los datos y evitar recargas constantes
def cargar_datos():
    try:
        data = pd.read_csv('ventas_tienda.csv')  # Reemplaza con la ruta de tu archivo CSV
        # Validar que las columnas necesarias existan
        columnas_necesarias = ['cantidad', 'precio_unitario', 'mes', 'año', 'Producto', 'Categoria']
        for columna in columnas_necesarias:
            if columna not in data.columns:
                raise ValueError(f"Falta la columna requerida: {columna}")
        return data
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

data = cargar_datos()

# Verificar si los datos se cargaron correctamente
if data.empty:
    st.stop()  # Detener la ejecución si no hay datos

# Calcular el total de venta por producto
data['Total_Venta'] = data['cantidad'] * data['precio_unitario']  # Multiplica cantidad por precio

# Mostrar los datos crudos con una opción para expandir/contraer
with st.expander('Ver datos crudos'):
    st.dataframe(data)

# Gráfico de barras: Total de ventas por mes
st.subheader('Total de ventas por mes')
ventas_por_mes = data.groupby('mes')['Total_Venta'].sum()
st.bar_chart(ventas_por_mes)

# Gráfico de líneas: Total de ventas por año
st.subheader('Total de ventas por año')
ventas_por_año = data.groupby('año')['Total_Venta'].sum()
st.line_chart(ventas_por_año)

# a. Cantidad de productos vendidos (Top 10)
st.subheader("Top 10 Productos Más Vendidos")
cantidad_productos = data.groupby('Producto').size().sort_values(ascending=False).head(10)
st.bar_chart(cantidad_productos)

# b. Ventas por Categoría
st.subheader("Ventas Totales por Categoría")
ventas_por_categoria = data.groupby('Categoria')['Total_Venta'].sum().sort_values(ascending=False)
st.bar_chart(ventas_por_categoria)

# c. Factura total
factura_total = data['Total_Venta'].sum()
st.metric(label="Factura Total", value=f"${factura_total:,.2f}")

# d. Visualizaciones adicionales
st.subheader("Distribución de Ventas")
fig_dist_ventas, ax_dist_ventas = plt.subplots()
sns.histplot(data['Total_Venta'], kde=True, ax=ax_dist_ventas)
ax_dist_ventas.set_title("Distribución de Ventas")
ax_dist_ventas.set_xlabel("Total Venta")
ax_dist_ventas.set_ylabel("Frecuencia")
st.pyplot(fig_dist_ventas)

st.subheader("Ventas por Categoría (Boxplot)")
fig_boxplot_ventas_cat, ax_boxplot_ventas_cat = plt.subplots()
sns.boxplot(x='Categoria', y='Total_Venta', data=data, ax=ax_boxplot_ventas_cat)
ax_boxplot_ventas_cat.set_title("Ventas por Categoría (Boxplot)")
ax_boxplot_ventas_cat.set_xlabel("Categoría")
ax_boxplot_ventas_cat.set_ylabel("Total Venta")
plt.xticks(rotation=45, ha='right')  # Rotación de etiquetas para legibilidad
st.pyplot(fig_boxplot_ventas_cat)
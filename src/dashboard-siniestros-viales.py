import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import os

# Cargar datos
fields = ['n_victimas', 'fecha', 'lugar_del_hecho', 'participantes', 'acusado', 'victima']
df = pd.read_csv('homicidios_etl.csv', usecols=fields)
df.dropna(inplace=True)
df['fecha'] = pd.to_datetime(df['fecha'])

# Función para mostrar el contenido del archivo README.md
def mostrar_readme():
    st.title("README")
    # Construir la ruta completa al archivo README.md
    with open("C:/Users/javie/Downloads/Proyecto-II-Henry/README.md", "r", encoding="utf-8") as readme_file:        
        readme_content = readme_file.read()
    st.markdown(readme_content)
# Función para mostrar la página de Estadísticas Básicas
def mostrar_estadisticas_basicas():
    st.write("Estadísticas Básicas:")
    st.write(df.describe())

# Función para mostrar la página de Distribución por Fecha
def mostrar_distribucion_fecha():
    st.write("Distribución de Incidentes por Fecha:")
    fig_fecha = px.histogram(df, x='fecha', title='Distribución de Incidentes por Fecha')
    fig_fecha.update_layout(bargap=0.2)
    st.plotly_chart(fig_fecha)

# Función para mostrar la página de Distribución por Ubicación
def mostrar_distribucion_ubicacion():
    st.write("Distribución de Incidentes por Ubicación:")
    fig_ubicacion = px.bar(df['lugar_del_hecho'].value_counts().head(10), x=df['lugar_del_hecho'].value_counts().head(10).index, y=df['lugar_del_hecho'].value_counts().head(10).values, title='Top 10 de Ubicaciones con Mayor Cantidad de Incidentes')
    st.plotly_chart(fig_ubicacion)

# Función para mostrar la página de KPIs
def mostrar_kpis():
    st.title('KPIs: Análisis de Seguridad Vial en CABA')

    # Calcular la tasa de homicidios en siniestros viales
    def calcular_tasa_homicidios():
        total_homicidios = df['n_victimas'].sum()
        poblacion_caba = 3000000  # Suponiendo una población de 3,000,000 en CABA (solo como ejemplo)
        tasa_homicidios = (total_homicidios / poblacion_caba) * 100000
        return tasa_homicidios

    tasa_homicidios = calcular_tasa_homicidios()

    # Visualizar el KPI
    st.title('KPI: Tasa de Homicidios en Siniestros Viales')
    fig_indicador = go.Figure(go.Indicator(
        mode="number",
        value=tasa_homicidios,
        title="Tasa de Homicidios por 100,000 Habitantes",
    ))
    st.plotly_chart(fig_indicador)

    # Descripción
    st.write("""
    La tasa de homicidios en siniestros viales representa el número de víctimas fatales en accidentes de tráfico por cada 100,000 habitantes en CABA.
    """)

# Función para mostrar la página de Reducción de Accidentes de Motociclistas
def mostrar_reduccion_accidentes_motociclistas():
    st.title('KPI 2: Reducción de Accidentes Mortales de Motociclistas')
    # Calcular la reducción de accidentes de motociclistas
    accidentes_motociclistas_anterior = ((df['victima'] == 'MOTO') & (df['fecha'].dt.year == 2019)).sum()
    accidentes_motociclistas_actual = ((df['victima'] == 'MOTO') & (df['fecha'].dt.year == 2020)).sum()

    if accidentes_motociclistas_anterior != 0:
        porcentaje_reduccion = ((accidentes_motociclistas_anterior - accidentes_motociclistas_actual) / accidentes_motociclistas_anterior) * 100
    else:
        porcentaje_reduccion = float('nan')  # Otra opción sería asignar None o algún otro valor representativo

    # Visualizar el KPI de cantidad de accidentes mortales de motociclistas
    fig_accidentes_motociclistas = go.Figure(go.Indicator(
        mode="number",
        value=accidentes_motociclistas_actual,
        delta={'reference': accidentes_motociclistas_anterior, 'relative': True},
        title="Accidentes Mortales de Motociclistas",
        domain={'row': 1, 'column': 0}
    ))
    st.plotly_chart(fig_accidentes_motociclistas)

    # Mostrar porcentaje de reducción
    st.write(f"Porcentaje de reducción de accidentes mortales de motociclistas: {porcentaje_reduccion:.2f}%")

# Función para mostrar la página de Ayuda
def mostrar_ayuda():
    st.write("¡Bienvenido a la página de Ayuda!")
    st.write("Esta página proporciona información sobre cómo utilizar la aplicación.")

# Función para mostrar todas las páginas en una sola
def mostrar_todas_las_paginas():
    st.title("Dashboard")
    st.write("Aquí puedes ver todas las páginas en una sola.")
    st.write("---")
    # Visualizaciones interactivas
    st.header('Visualizaciones Interactivas')
    if st.checkbox('Mostrar DataFrame'):
        st.dataframe(df)
    
    if st.checkbox('Vista de datos Head o Tail'):
        if st.button('Mostrar Head'):
            st.write(df.head())
        if st.button('Mostrar Tail'):
            st.write(df.tail())
    dim = st.radio('Dimension a Mostrar',('Filas','Columnas'), horizontal = True)

    if dim == 'Filas':
        st.write('Cantidad de Filas: ', df.shape[0])
    if dim == 'Columnas':
        st.write('Cantidad de Columnas', df.shape[1])
    mostrar_estadisticas_basicas()
    mostrar_distribucion_fecha()
    mostrar_distribucion_ubicacion()
    mostrar_kpis()
    mostrar_reduccion_accidentes_motociclistas()

# Sidebar
st.sidebar.title("Navegación")
pages = ["README","Todas las Páginas", "Estadísticas Básicas", "Distribución por Fecha", "Distribución por Ubicación", "KPI:Tasa de Homicidios en Siniestros Viales", "KPI2:Reducción de Accidentes de Motociclistas", "Ayuda"]
selected_page = st.sidebar.selectbox("Seleccionar Página", pages)

# Mostrar página seleccionada
if selected_page == "README":
    mostrar_readme()
elif selected_page == "Todas las Páginas":
    mostrar_todas_las_paginas()
elif selected_page == "Estadísticas Básicas":
    mostrar_estadisticas_basicas()
elif selected_page == "Distribución por Fecha":
    mostrar_distribucion_fecha()
elif selected_page == "Distribución por Ubicación":
    mostrar_distribucion_ubicacion()
elif selected_page == "KPIs":
    mostrar_kpis()
elif selected_page == "Reducción de Accidentes de Motociclistas":
    mostrar_reduccion_accidentes_motociclistas()
elif selected_page == "Ayuda":
    mostrar_ayuda()

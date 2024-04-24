import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

# Cargar datos
fields = ['n_victimas', 'fecha', 'lugar_del_hecho', 'participantes', 'acusado', 'victima']
df = pd.read_csv('homicidios_etl.csv', usecols=fields)
df.dropna(inplace=True)
df['fecha'] = pd.to_datetime(df['fecha'])

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

# Función para mostrar la página de KPI: Tasa de Homicidios en Siniestros Viales
def mostrar_tasa_homicidios():
    st.title('KPI: Tasa de Homicidios en Siniestros Viales')
    # Calcular la tasa de homicidios en siniestros viales
    total_homicidios = df['n_victimas'].sum()
    poblacion_caba = 3000000  # Suponiendo una población de 3,000,000 en CABA (solo como ejemplo)
    tasa_homicidios = (total_homicidios / poblacion_caba) * 100000

    # Visualizar el KPI
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

# Función para mostrar la página de KPI 2: Reducción de Accidentes Mortales de Motociclistas
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

# Define la función para mostrar la reducción del 10% en la tasa de homicidios en siniestros viales de los últimos seis meses
def mostrar_reduccion_tasa_homicidios():
    st.title('KPI: Reducción del 10% en la Tasa de Homicidios en Siniestros Viales')
    
    # Función para calcular la tasa de homicidios en siniestros viales del semestre anterior
    def calcular_tasa_homicidios_semestre_anterior():
        # Obtener la fecha actual
        fecha_actual = pd.Timestamp.today()
        
        # Calcular la fecha seis meses atrás
        fecha_semestre_anterior = fecha_actual - pd.DateOffset(months=6)
        
        # Filtrar el DataFrame para obtener solo los datos del semestre anterior
        df_semestre_anterior = df[(df['fecha'] >= fecha_semestre_anterior) & (df['fecha'] < fecha_actual)]

        # Calcular la tasa de homicidios en siniestros viales del semestre anterior
        total_victimas_semestre_anterior = df_semestre_anterior['n_victimas'].sum()
        poblacion_caba = 3000000  # Suponiendo una población de 3,000,000 en CABA (solo como ejemplo)
        tasa_homicidios_semestre_anterior = (total_victimas_semestre_anterior / poblacion_caba) * 100000

        return tasa_homicidios_semestre_anterior

    # Función para calcular la tasa de homicidios en siniestros viales de los últimos seis meses
    def calcular_tasa_homicidios_ultimos_seis_meses():
        # Obtener la fecha actual
        fecha_actual = pd.Timestamp.today()
        
        # Calcular la fecha seis meses atrás
        fecha_seis_meses_atras = fecha_actual - pd.DateOffset(months=6)
        
        # Filtrar el DataFrame para obtener solo los datos de los últimos seis meses
        df_ultimos_seis_meses = df[df['fecha'] >= fecha_seis_meses_atras]

        # Calcular la tasa de homicidios en siniestros viales de los últimos seis meses
        total_victimas_ultimos_seis_meses = df_ultimos_seis_meses['n_victimas'].sum()
        poblacion_caba = 3000000  # Suponiendo una población de 3,000,000 en CABA (solo como ejemplo)
        tasa_homicidios_ultimos_seis_meses = (total_victimas_ultimos_seis_meses / poblacion_caba) * 100000

        return tasa_homicidios_ultimos_seis_meses

    # Calcular la tasa de homicidios en siniestros viales del semestre anterior
    tasa_homicidios_semestre_anterior = calcular_tasa_homicidios_semestre_anterior()
    
    # Calcular la tasa de homicidios en siniestros viales de los últimos seis meses
    tasa_homicidios_ultimos_seis_meses = calcular_tasa_homicidios_ultimos_seis_meses()

    # Verificar si las tasas son válidas y diferentes
    if tasa_homicidios_semestre_anterior is not None and tasa_homicidios_ultimos_seis_meses is not None:
        if tasa_homicidios_semestre_anterior * 0.9 > tasa_homicidios_ultimos_seis_meses:
            # Calcular la reducción porcentual
            porcentaje_reduccion = ((tasa_homicidios_semestre_anterior - tasa_homicidios_ultimos_seis_meses) / tasa_homicidios_semestre_anterior) * 100

            # Visualizar el KPI de reducción
            fig_kpi_reduccion = go.Figure(go.Indicator(
                mode="number",
                value=porcentaje_reduccion,
                title="Porcentaje de Reducción",
                number={"suffix": "%"},
                domain={'row': 1, 'column': 0}
            ))
            st.plotly_chart(fig_kpi_reduccion)
        else:
            st.write("La tasa de homicidios del semestre anterior no ha reducido en un 10% con respecto a la tasa de homicidios de los últimos seis meses.")
    else:
        st.write("No hay datos disponibles para calcular la reducción de la tasa de homicidios.")

# Define la función para calcular la tasa de homicidios de los últimos 6 meses
def calcular_tasa_homicidios_ultimos_seis_meses():
    # Obtener la fecha actual
    fecha_actual = pd.Timestamp.today()
    
    # Calcular la fecha seis meses atrás
    fecha_seis_meses_atras = fecha_actual - pd.DateOffset(months=6)
    
    # Filtrar el DataFrame para obtener solo los datos de los últimos seis meses
    df_ultimos_seis_meses = df[df['fecha'] >= fecha_seis_meses_atras]

    # Calcular la tasa de homicidios en siniestros viales de los últimos seis meses
    total_victimas_ultimos_seis_meses = len(df_ultimos_seis_meses)
    print(total_victimas_ultimos_seis_meses)
    poblacion_caba = 3000000  # Suponiendo una población de 3,000,000 en CABA (solo como ejemplo)
    tasa_homicidios_ultimos_seis_meses = (total_victimas_ultimos_seis_meses / poblacion_caba) * 100000

    return tasa_homicidios_ultimos_seis_meses

# Define la función para mostrar todas las páginas en una sola
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
    mostrar_tasa_homicidios()
    mostrar_reduccion_accidentes_motociclistas()
    mostrar_reduccion_tasa_homicidios()  # Aquí llamamos la función para mostrar la reducción de la tasa de homicidios
    st.title('Tasa de Homicidios Últimos 6 Meses')
    st.write(calcular_tasa_homicidios_ultimos_seis_meses())  # Aquí llamamos la función para calcular la tasa de homicidios de los últimos 6 meses

# Sidebar
st.sidebar.title("Navegación")
pages = ["Todas las Páginas", "Estadísticas Básicas", "Distribución por Fecha", "Distribución por Ubicación", "KPI: Tasa de Homicidios en Siniestros Viales", "KPI 2: Reducción de Accidentes Mortales de Motociclistas", "Reducción de la Tasa de Homicidios", "Tasa de Homicidios Últimos 6 Meses"]
selected_page = st.sidebar.selectbox("Seleccionar Página", pages)

# Mostrar página seleccionada
if selected_page == "Todas las Páginas":
    mostrar_todas_las_paginas()
elif selected_page == "Estadísticas Básicas":
    mostrar_estadisticas_basicas()
elif selected_page == "Distribución por Fecha":
    mostrar_distribucion_fecha()
elif selected_page == "Distribución por Ubicación":
    mostrar_distribucion_ubicacion()
elif selected_page == "KPI: Tasa de Homicidios en Siniestros Viales":
    mostrar_tasa_homicidios()
elif selected_page == "KPI 2: Reducción de Accidentes Mortales de Motociclistas":
    mostrar_reduccion_accidentes_motociclistas()
elif selected_page == "Reducción de la Tasa de Homicidios":
    mostrar_reduccion_tasa_homicidios()
elif selected_page == "Tasa de Homicidios Últimos 6 Meses":
    st.title('Tasa de Homicidios Últimos 6 Meses')
    st.write(calcular_tasa_homicidios_ultimos_seis_meses())

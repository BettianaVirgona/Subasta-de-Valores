import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Dinámica de Valores", page_icon="🌟", layout="centered")

st.title("🌟 Dinámica de Valores")
st.write("Puntúa del 0 al 100 qué tan importante es cada uno de estos principios para ti.")

# Lista de 18 valores (puedes editar, quitar o agregar los que quieras)
valores = [
    "Amistad", "Esperanza", "Honestidad", "Respeto", "Responsabilidad",
    "Empatía", "Justicia", "Solidaridad", "Tolerancia", "Libertad",
    "Paz", "Lealtad", "Compasión", "Humildad", "Perseverancia",
    "Equidad", "Valentía", "Integridad"
]

resultados = {}

# Dividimos en dos columnas para que la interfaz sea más amigable
col1, col2 = st.columns(2)

with col1:
    for valor in valores[:9]:
        # El valor por defecto al abrir la app será 50
        resultados[valor] = st.slider(valor, 0, 100, 50)

with col2:
    for valor in valores[9:]:
        resultados[valor] = st.slider(valor, 0, 100, 50)

st.write("---")

# Botón para generar el gráfico
if st.button("📊 Ver mi gráfico de valores", use_container_width=True):
    # Convertimos los resultados a un DataFrame de Pandas
    df = pd.DataFrame(list(resultados.items()), columns=["Valor", "Puntaje"])
    
    # Filtramos los valores que quedaron en 0 para no saturar la torta
    df = df[df["Puntaje"] > 0]
    
    if not df.empty:
        st.subheader("Distribución de tus principios")
        
        # Creamos el gráfico de torta con Plotly
        fig = px.pie(df, values='Puntaje', names='Valor', 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        
        # Configuramos para que se vea el nombre y el porcentaje en las porciones
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        # Mostramos el gráfico
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Debes darle al menos 1 punto a algún valor para poder generar el gráfico.")

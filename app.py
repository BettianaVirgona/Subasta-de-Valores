import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="Dinámica de Valores", page_icon="🌟", layout="centered")

# --- MEMORIA DE LA APP (Session State) ---
# Esto permite que la app recuerde los valores cargados paso a paso
if 'valores_cargados' not in st.session_state:
    st.session_state.valores_cargados = {}
if 'puntos_restantes' not in st.session_state:
    st.session_state.puntos_restantes = 100

st.title("🌟 Dinámica: Mapa de Valores")
st.write("Agrega los principios que guían tu forma de actuar. ¡Tienes **100 puntos** en total para repartir entre todos ellos!")

# 1. Mostrar cuántos puntos le quedan (100 - X)
st.metric(label="Puntos disponibles para asignar", value=st.session_state.puntos_restantes)

# 2. Sección para cargar un valor paso a paso
st.write("### Agregar un nuevo valor")

# Si ya no le quedan puntos, deshabilitamos las entradas para que no pueda pasarse de 100
sin_puntos = st.session_state.puntos_restantes <= 0

col1, col2 = st.columns([2, 1])
with col1:
    nuevo_valor = st.text_input("Nombre del valor (ej. Esperanza):", disabled=sin_puntos)
with col2:
    # El puntaje máximo que puede elegir es igual a los puntos que le sobran
    max_permitido = max(1, st.session_state.puntos_restantes)
    puntaje = st.number_input("Puntaje:", min_value=1, max_value=max_permitido, disabled=sin_puntos)

# Botón para guardar el valor
if st.button("➕ Agregar valor", disabled=sin_puntos):
    if nuevo_valor.strip() == "":
        st.warning("Por favor, escribe el nombre del valor.")
    elif nuevo_valor.strip() in st.session_state.valores_cargados:
        st.warning("¡Ya agregaste ese valor! Intenta con otro nombre.")
    else:
        # Guardamos el valor y restamos los puntos
        st.session_state.valores_cargados[nuevo_valor.strip()] = puntaje
        st.session_state.puntos_restantes -= puntaje
        st.rerun() # Recarga la página para actualizar los números

# 3. Mostrar lo que ya cargó
if st.session_state.valores_cargados:
    st.write("---")
    st.write("**Valores cargados hasta ahora:**")
    # Mostramos los datos en una tabla limpia
    df_actual = pd.DataFrame(list(st.session_state.valores_cargados.items()), columns=["Valor", "Puntaje"])
    st.dataframe(df_actual, use_container_width=True, hide_index=True)
    
    # Botón por si quieren empezar de cero
    if st.button("🔄 Reiniciar dinámica"):
        st.session_state.valores_cargados = {}
        st.session_state.puntos_restantes = 100
        st.rerun()

st.write("---")

# 4. El botón para ver el gráfico (siempre disponible)
if st.button("📊 Ver mi gráfico de valores", type="primary", use_container_width=True):
    if len(st.session_state.valores_cargados) == 0:
        st.info("Primero debes agregar al menos un valor para generar el gráfico.")
    else:
        df_final = pd.DataFrame(list(st.session_state.valores_cargados.items()), columns=["Valor", "Puntaje"])
        
        st.subheader("Tu distribución de principios")
        
        # Gráfico de torta interactivo
        fig = px.pie(df_final, values='Puntaje', names='Valor', 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Pequeña nota si decide ver el gráfico antes de gastar los 100 puntos
        if st.session_state.puntos_restantes > 0:
            st.caption(f"*Nota: Aún te sobran {st.session_state.puntos_restantes} puntos. Este gráfico representa el porcentaje sobre los puntos que ya asignaste.*")

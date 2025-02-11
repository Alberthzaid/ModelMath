import streamlit as st
import time
import numpy as np
import pandas as pd
import joblib


st.set_page_config(page_title="Predicción FIFA", page_icon="⚽")

st.markdown("# Predicción de Resultados FIFA")
st.sidebar.header("Comparación de Equipos")
st.write(
    """Esta visualización muestra la evolución de los puntajes FIFA de varios equipos 
    en una animación progresiva."""
)


model = joblib.load("Helpers/fifa_winner_model.pkl")

teams_data = pd.DataFrame({
    "Equipo": ["Brazil", "Belgium", "France", "Argentina", "England", 
               "Italy", "Spain", "Portugal", "Mexico", "Netherlands"],
    "Ranking": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Puntos FIFA": [1832, 1827, 1789, 1765, 1761, 1723, 1709, 1674, 1658, 1658]
})


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
chart_data = pd.DataFrame({"Equipo": [], "Puntos FIFA": []})
chart = st.line_chart(chart_data)


for i in range(1, 101):
    noise = np.random.randint(-5, 5, size=len(teams_data)) 
    teams_data["Puntos FIFA"] = teams_data["Puntos FIFA"] + noise 
    

    new_chart_data = teams_data.set_index("Equipo")["Puntos FIFA"]
    chart.line_chart(new_chart_data) 
    
    status_text.text(f"{i}% Completado")
    progress_bar.progress(i)
    time.sleep(0.05)

progress_bar.empty()


if st.button("Mostrar equipo con más puntos"):
    best_team = teams_data.loc[teams_data["Puntos FIFA"].idxmax()]
    st.success(f"🏆 El equipo con más puntos es {best_team['Equipo']} con {best_team['Puntos FIFA']} puntos.")

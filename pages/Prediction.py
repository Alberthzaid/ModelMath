import streamlit as st
import time
import numpy as np
import pandas as pd
import joblib


st.set_page_config(page_title="Predicción FIFA", page_icon="⚽")

st.markdown("# 🏆 Predicción del Campeón del Mundial")
st.sidebar.header("Comparación de Equipos")
st.write("Esta visualización muestra la evolución de los puntajes FIFA de varios equipos y predice al campeón.")


model = joblib.load("fifa_winner_model.pkl")


teams_data = pd.DataFrame({
    "Equipo": ["Brazil", "Belgium", "France", "Argentina", "England", 
               "Italy", "Spain", "Portugal", "Mexico", "Netherlands"],
    "Ranking": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Puntos FIFA": [1832, 1827, 1789, 1765, 1761, 1723, 1709, 1674, 1658, 1658]
})


teams_data = teams_data.rename(columns={"Ranking": "rank", "Puntos FIFA": "rank_points"})


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
chart_data = pd.DataFrame({"Equipo": [], "rank_points": []})
chart = st.line_chart(chart_data)

for i in range(1, 101):
    noise = np.random.randint(-5, 5, size=len(teams_data))  
    teams_data["rank_points"] = teams_data["rank_points"] + noise  

    new_chart_data = teams_data.set_index("Equipo")["rank_points"]
    chart.line_chart(new_chart_data)  

    status_text.text(f"{i}% Completado")
    progress_bar.progress(i)
    time.sleep(0.05)

progress_bar.empty()

st.subheader("🏆 Predecir el Campeón del Mundial")

if st.button("Predecir Campeón"):

    X = teams_data[['rank', 'rank_points']]


    predictions = model.predict_proba(X)[:, 1]  

    teams_data["Probabilidad de Victoria"] = predictions


    champion_index = predictions.argmax()
    champion_team = teams_data.iloc[champion_index]["Equipo"]


    st.success(f"🎉 ¡El modelo predice que el campeón del Mundial será **{champion_team}**! 🏆")


    st.subheader("📊 Probabilidades de Victoria de Cada Equipo")
    st.bar_chart(teams_data.set_index("Equipo")["Probabilidad de Victoria"])

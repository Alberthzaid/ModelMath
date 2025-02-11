from urllib.error import URLError

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Charts Mundial 2026", page_icon="assets/LogoWithoutBg.png")

st.title("📊 Charts de estatisticas anteriores al Mundial 2026")
st.sidebar.header("Opciones de visualización")


seccion = st.sidebar.selectbox("Selecciona una sección:", ["Grupos", "Equipos por Grupo", "Historial de Partidos"])

grupo_df = pd.read_csv("datasets/Groupes.csv")
partidos_df = pd.read_csv("datasets/international_matches.csv")

if seccion == "Grupos":
    st.subheader("🏆 Grupos y Partidos")
    st.dataframe(grupo_df)

    group_chart = alt.Chart(grupo_df).mark_bar().encode(
        x='groups:N',
        y='team:N',
        color='groups:N'
    ).properties(title="Equipos por Grupo")
    st.altair_chart(group_chart, use_container_width=True)

elif seccion == "Equipos por Grupo":
    st.subheader("📌 Equipos por Grupo")
    grupo_seleccionado = st.selectbox("Selecciona un grupo:", grupo_df["groups"].unique())
    equipos_filtrados = grupo_df[grupo_df["groups"] == grupo_seleccionado]
    st.dataframe(equipos_filtrados)

elif seccion == "Historial de Partidos":
    st.subheader("⚔️ Historial de Partidos Internacionales")

    torneo_seleccionado = st.selectbox("Selecciona un torneo:", partidos_df["tournament"].unique())
    partidos_filtrados = partidos_df[partidos_df["tournament"] == torneo_seleccionado]
    st.dataframe(partidos_filtrados)

    ranking_chart = alt.Chart(partidos_filtrados).mark_circle(size=100).encode(
        x='home_team_fifa_rank:Q',
        y='away_team_fifa_rank:Q',
        color='home_team:N',
        tooltip=['home_team', 'away_team', 'home_team_score', 'away_team_score']
    ).properties(title="Comparación de Rankings FIFA en Partidos")
    st.altair_chart(ranking_chart, use_container_width=True)

st.write("Este análisis ayuda a visualizar los equipos y su hipotetico rendimiento que podrian presentar en el Mundial 2026 basado en datos históricos y rankings FIFA.")

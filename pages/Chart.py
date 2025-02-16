from urllib.error import URLError

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Charts Mundial 2026", page_icon="assets/LogoWithoutBg.png")

st.title("📊 Charts de estatisticas anteriores al Mundial 2026")
st.sidebar.header("Opciones de visualización")


seccion = st.sidebar.selectbox("Selecciona una sección:", ["Grupos", "Equipos por Grupo", "Historial de Partidos"])

grupo_df = pd.read_csv("datasets/groups.csv")
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

    ranking_avg_df = (
        partidos_filtrados.groupby("home_team")["home_team_fifa_rank"]
        .mean()
        .reset_index()
        .rename(columns={"home_team_fifa_rank": "ranking_promedio"})
    )

    ranking_chart = alt.Chart(ranking_avg_df).mark_bar().encode(
        x=alt.X("ranking_promedio:Q", title="Ranking FIFA Promedio"),
        y=alt.Y("home_team:N", title="Equipo", sort="-x"),
        color=alt.Color("home_team:N", legend=None)
    ).properties(title=f"Ranking Promedio de Equipos en {torneo_seleccionado}")

    st.altair_chart(ranking_chart, use_container_width=True)

st.write("Este análisis ayuda a visualizar los equipos y su hipotetico rendimiento que podrian presentar en el Mundial 2026 basado en datos históricos y rankings FIFA.")

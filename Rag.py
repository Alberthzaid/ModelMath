import streamlit as st
from models_clients.deepseek import DeepseekClient
from rag_clients.world_cup_rag import WorldCupRAG


st.set_page_config(page_title="RAG Mundial", page_icon="⚽")
st.sidebar.success("Selecciona una opción")

st.markdown("# Predicción de Partidos del Mundial 2026")
st.sidebar.header("RAG Mundial")

model_client = DeepseekClient(version="1.5b")
rag = WorldCupRAG(model_client)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


team1 = st.text_input("Ingrese el primer equipo:", key="team1")
team2 = st.text_input("Ingrese el segundo equipo:", key="team2")


if st.button("Predecir Resultado"):

    if team1 and team2:

        response = rag.predict_match(team1, team2)


        st.session_state.messages.append({"role": "user", "content": f"¿Quién ganará entre {team1} y {team2}?"})
        with st.chat_message("user"):
            st.markdown(f"¿Quién ganará entre {team1} y {team2}?")


        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        st.warning("Por favor, ingrese ambos equipos.")


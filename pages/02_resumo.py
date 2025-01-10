import streamlit as st

st.header("Resumo dos Dados")

if "dados" not in st.session_state:

    st.error("Os dados não foram carregados")

else:

    top_n = st.session_state.get("top_n",10)

    dados = st.session_state["dados"].describe().reset_index()

    st.write(dados)

    
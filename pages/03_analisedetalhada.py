import streamlit as st
import plotly.express as px

st.header("Distribuição de Dados")

if "dados" not in st.session_state:

    st.error("Os dados não foram carregados")

else:

    top_n = st.session_state.get("top_n",10)

    dados = st.session_state["dados"]

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.histogram(dados,x="VALOREMPENHO", title="Histograma do Valor de Empenho")

        st.plotly_chart(fig1,use_container_width=True)

        fig2 = px.box(dados,x="VALOREMPENHO", title="Boxplot do Valor de Empenho")

        st.plotly_chart(fig2,use_container_width=True)
    
    with col2:

        fig3 = px.histogram(dados,x="PIB", title="Histograma do PIB")

        st.plotly_chart(fig3,use_container_width=True)

        fig4 = px.box(dados,x="PIB", title="Boxplot do PIB")

        st.plotly_chart(fig4,use_container_width=True)
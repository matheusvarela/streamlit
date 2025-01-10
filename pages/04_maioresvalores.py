import streamlit as st
import plotly.express as px

st.header("Distribuição de Dados")

if "dados" not in st.session_state:

    st.error("Os dados não foram carregados")

else:

    top_n = st.session_state.get("top_n",10)

    dados = st.session_state["dados"]

    col1, col2, col3 = st.columns(3)

    with col1:

        Mempenho = dados.nlargest(top_n, 'VALOREMPENHO')

        fig = px.bar(Mempenho, x="MUNICIPIO",y="VALOREMPENHO", title="Maiores Empenhos")

        st.plotly_chart(fig,use_container_width=True)
    
    with col2:

        Mpibs = dados.nlargest(top_n, 'PIB')

        fig = px.pie(Mpibs, names="MUNICIPIO",values="PIB", title="Maiores PIBs")

        st.plotly_chart(fig,use_container_width=True)
    
    with col3:

        Mproporcao = dados.nlargest(top_n, 'PROPORCAO')

        fig = px.bar(Mproporcao, x="MUNICIPIO",y="PROPORCAO", title="Maiores Proporções")

        st.plotly_chart(fig,use_container_width=True)




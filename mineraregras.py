import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

st.set_page_config(page_title="Geração de Regras de Recomendação",layout="wide")

st.title("Geração de Regas de Recomendação")

with st.sidebar:

    uploaded_file = st.file_uploader("Escolha o arquivo", type=["csv"])

    suporte_minimo = st.number_input("Suporte Mínimo ",min_value=0.001, max_value=1.0,value=0.01,step=0.01)
    
    confianca_minima = st.number_input("Confiança mínima ",min_value=0.001, max_value=1.0,value=0.2,step=0.01)

    lift_minimo = st.number_input("Lift Mínimo ",min_value=0.001, max_value=10.0,value=1.0,step=0.1)

    tamanho_minimo = st.number_input("Tamanho Mínimo ",min_value=1, max_value=10,value=2,step=1)

    processar = st.button("Processar")

if processar and uploaded_file is not None:

    try:
        transactions = []

        for line in uploaded_file:

            transaction = line.decode("utf-8").strip().split(",")

            transactions.append(transaction)

        print(transactions)
        
        te = TransactionEncoder()

        te_ary = te.fit(transactions).transform(transactions)

        df = pd.DataFrame(te_ary, columns=te.columns_)

        print("AAAAAAAAAAAAA")

        frequent_itemsets = apriori(df, min_support = suporte_minimo, use_colnames=True)

        regras = association_rules(frequent_itemsets,metric="confidence", min_threshold=confianca_minima)

        print("BBBBBBBBBBB")

        regras_filtradas = regras[(regras['lift'] >= lift_minimo) & (regras['antecedents'].apply(lambda x: len(x) >= tamanho_minimo))]

        print("CCCCCCCCCC")

        if not regras_filtradas.empty:

            col1, col2, col3 = st.columns(3)

            print("DDDDDDDDDDDD")

            with col1:

                st.header("Transações")

                print("EEEEEEEEEEEEEEEE")

                st.dataframe(df)

                print("FFFFFFFFFFFFF")

            with col2:

                st.header("Regras encontradas")

                #st.dataframe(regras_filtradas)

            with col3:

                st.header("Visualização")

                fig, ax = plt.subplots()

                scatter = ax.scatter(
                    regras_filtradas["support"], 
                    regras_filtradas["confidence"], 
                    alpha = 0.5, 
                    c = regras_filtradas['lift'], 
                    cmap = "viridis")

                plt.colorbar(scatter, label="lift")

                ax.set_title("Regras de Associação")

                ax.set_xlabel("Suporte")

                ax.set_ylabel("Confiança")

                st.pyplot(fig)

            st.header("Resumo das regras")

            st.write(f"Total de regras geradas: {len(regras_filtradas)}")

            st.write(f"Suporte médio: {regras_filtradas['support'].mean():.4f}")
            
            st.write(f"Confiança média: {regras_filtradas['confidence'].mean():.4f}")
            
            st.write(f"Lift médio: {regras_filtradas['lift'].mean():.4f}")

            st.download_button(
                label="Exportar Regras como csv", 
                data = regras_filtradas.to_csv(index=False),
                file_name="regras_associacao.csv",
                mime="text/csv")

        else: 

            st.write("Nenhuma regra foi encontrada com os parâmetros definidos")
            

    except Exception as e:
        
        st.error(f"Erro ao processar o arquivo: {e}")
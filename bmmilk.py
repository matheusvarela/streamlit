import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.api import Holt, ExponentialSmoothing 
from pmdarima import auto_arima
from matplotlib import pyplot as plt

st.set_page_config(page_title="Benchmark series temporais",layout="wide")

st.title("Benchmark series temporais")

def load_data(uploaded_file):

    data = pd.read_csv(uploaded_file,header=None)

    return data

def plot_forecasts(actual, forecasts,titles):

    plt.figure(figsize=(10,6))

    plt.plot(actual, label="Dados Atuais")

    for forecast, title in zip(forecasts,titles): 
         
        plt.plot(np.arange(len(actual), len(actual) + len(forecast)), data= forecast, label=title)

        plt.title("Benchmark de Series Temporais")

        plt.grid(True)

        return plt

def forecast_methods(train, h, methods):

    forecast = []

    titles = []

    if methods['naive']: 

        naive_forecast = np.tile(train.iloc[-1],h)

        forecast.append(naive_forecast)
    
        titles.append("Naive")

    if methods['mean']:

        mean_forecast = np.tile(train.mean(), h)

        forecast.append(mean_forecast)
    
        titles.append("Mean")

    if methods["drift"]:

        drift_forecast = train.iloc[-1] + (np.arange(1, h +1) * ((train.iloc[-1] - train.iloc[0]) / (len(train)-1)))

        forecast.append(drift_forecast)
    
        titles.append("Drift")

    if methods["holt"]:

        holt_forecast = Holt(train).fit().forecast(h)

        forecast.append(holt_forecast)
    
        titles.append("Holt")
    
    if methods["hw"]:

        hw_forecast = ExponentialSmoothing(train, 
        
        seasonal = "additive", 
        
        seasonal_periods = 12).fit().forecast(h)
        
        forecast.append(hw_forecast)
        
        titles.append("HW Additive")
    
    if methods["arima"]:

        arima_model = auto_arima(train,seasonal='additive',m=12,suppress_warnings=True)

        arima_forecast = arima_model.predict(n_periods=h)

        forecast.append(arima_forecast)

        titles.append("Arima")
    
    return forecast, titles

with st.sidebar:

    uploade_file = st.file_uploader("Selecione o CSV", type="csv")

    if uploade_file is not None:

        date_range = st.date_input("Informe período",value=[])

        forecast_horizon = st.number_input("Informe período de previsão", min_value=1, value=24,step=1)

        st.write("Escolha os métodos de previsão")

        methods = {
            "naive" : st.checkbox(label="Naive",value=True),
            "mean" : st.checkbox(label="Mean",value=True),
            "drift" : st.checkbox(label="Drift",value=True),
            "holt" : st.checkbox(label="Holt",value=True),
            "hw" : st.checkbox(label="Holt-Winters",value=True),
            "arima" : st.checkbox(label="Arima",value=True)
        }

        process_button = st.button("Processa")

if uploade_file is not None:

    data = load_data(uploade_file)

    if process_button and len(date_range) == 2:

        col1, col2 = st.columns([1,4])

        with col1:

            st.write("")
            #st.dataframe(data)

        with col2:

            with st.spinner("Processando... Por favor aguarde"):

                start_date, end_date = date_range

                train = data.iloc[:,0]

                forecast, titles = forecast_methods(train, forecast_horizon, methods)

                plt = plot_forecasts(train, forecast, titles)

                st.pyplot(plt)

    elif process_button:

        st.warning("Por favor selecione um período de datas válidos")  

else:

    st.warning("Faça upload do arquivo csv")


        


        
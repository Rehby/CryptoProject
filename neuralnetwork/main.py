import torch
import numpy as np
import streamlit as st
import pandas as pd
from neuralnetwork.dataBase import add_predict,check_actual
from neuralnetwork.Predictor import CryptoPredictor
from neuralnetwork.Train import train_model
from neuralnetwork.DataProcessing import normalize_data

import plotly.graph_objects as go
import plotly.express as px

def charts(ticker,total_price, daily_price,predicted_cases,train,num_epochs):


    fig1 = px.bar(title=f"Стоимость {ticker}")
    fig1.update_layout(xaxis_title="Дата", yaxis_title="Стоимсоть Usd")
    fig1.add_trace(go.Scatter(x=total_price.index, y=total_price))
    st.plotly_chart(fig1, use_container_width=True)

    fig = px.bar(title=f"Стоимость {ticker}")
    fig.add_trace(go.Scatter(x=daily_price.index, y=daily_price,
                             name="Данные о стоимости"))
    fig.add_trace(go.Scatter(x=predicted_cases.index, y=predicted_cases,
                             name="Прогнозируемая стоимость", mode='lines'))
    fig.update_layout(xaxis_title="Дата", yaxis_title="Стоимсоть Usd")
    st.plotly_chart(fig, use_container_width=True)


    df = pd.Series(train.tolist())
    ind= range(1,num_epochs+1)
    df.index=ind
    fig = px.bar(title=f"Обучение нейронной сети")
    fig.add_trace(go.Scatter(x=df.index, y=df))

    fig.update_layout(xaxis_title="Эпоха", yaxis_title="Ошибка")
    st.plotly_chart(fig, use_container_width=True)


def init(num_epochs = 200,seq_length = 6):
     RANDOM_SEED = 12
     np.random.seed(RANDOM_SEED)
     torch.manual_seed(RANDOM_SEED)
     return seq_length, num_epochs



def predict(ticker,DAYS_TO_PREDICT,seq_length, num_epochs):
    model = CryptoPredictor(
        n_features=1,
        n_hidden=10,
        seq_len=seq_length,
        n_layers=2)

    model, train, test, preds, total_price, daily_price, scaler = train_model(
        model,
        num_epochs,
        seq_length,
        ticker,
        DAYS_TO_PREDICT)




    predicted_cases = normalize_data(scaler, preds, total_price, DAYS_TO_PREDICT)
    add_predict(predicted_cases, 1)

    return total_price, daily_price, predicted_cases,train


if __name__=="__main__":
    # init()
    # predict("BTC-USD",15,4,2)
    print(check_actual("BTC-USD",12))
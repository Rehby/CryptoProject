import torch
import numpy as np
import streamlit as st
import pandas as pd

from neuralnetwork.dataBase import add_predict, check_actual, get_nn_param
from neuralnetwork.Predictor import CryptoPredictor
from neuralnetwork.Train import train_model
from neuralnetwork.DataProcessing import normalize_data, get_data, normalize_db_data

import plotly.graph_objects as go
import plotly.express as px


def charts(ticker, total_price, daily_price, predicted_cases, train, num_epochs):
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

    if train!=[]:
        df = pd.Series(train.tolist())
        ind = range(1, num_epochs + 1)
        df.index = ind
        fig = px.bar(title=f"Обучение нейронной сети")
        fig.add_trace(go.Scatter(x=df.index, y=df))

        fig.update_layout(xaxis_title="Эпоха", yaxis_title="Ошибка")
        st.plotly_chart(fig, use_container_width=True)


def init():
    RANDOM_SEED = 12
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)


def predict(ticker, DAYS_TO_PREDICT):
    params = get_nn_param(ticker)
    seq = params[0]
    epoch = params[1]
    hidden = params[2]
    layers = params[3]

    model = CryptoPredictor(
        n_features=1,
        n_hidden=hidden,
        seq_len=seq,
        n_layers=layers)
    total_price, daily_price = get_data(ticker)

    data = check_actual(ticker, DAYS_TO_PREDICT)

    if (data):
        predicted_cases = normalize_db_data(data, total_price, DAYS_TO_PREDICT)
        train = []


    else:
        model, train, _, preds, _, _, scaler = train_model(
            model,
            epoch,
            seq,
            ticker,
            DAYS_TO_PREDICT)

        predicted_cases = normalize_data(scaler, preds, total_price, DAYS_TO_PREDICT)
        add_predict(predicted_cases, 1)

    return total_price, daily_price, predicted_cases, train, epoch


if __name__ == "__main__":
    # init()
    print(predict("BTC-USD", 4))
    # print(check_actual("BTC-USD",12))

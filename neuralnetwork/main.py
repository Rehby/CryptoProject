from datetime import date
import torch
import numpy as np
import streamlit as st

from neuralnetwork import dataBase
from neuralnetwork.Predictor import CryptoPredictor
from neuralnetwork.Train import train_model
from neuralnetwork.DataProcessing import normalize_data

def Charts(ticker,total_price, daily_price,predicted_cases):
    import plotly.graph_objects as go
    import plotly.express as px

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

def init(num_epochs = 20,seq_length = 64):
     RANDOM_SEED = 12
     np.random.seed(RANDOM_SEED)
     torch.manual_seed(RANDOM_SEED)
     TODAY = date.today().strftime("%Y-%m-%d")
     return seq_length, num_epochs

def predict(ticker,DAYS_TO_PREDICT,seq_length, num_epochs):
    model = CryptoPredictor(
        n_features=1,
        n_hidden=80,
        seq_len=seq_length,
        n_layers=2)

    _, _, _, preds, total_price, daily_price, scaler = train_model(
        model,
        num_epochs,
        seq_length,
        ticker,
        DAYS_TO_PREDICT)

    predicted_cases = normalize_data(scaler, preds, total_price, DAYS_TO_PREDICT)

    print(predicted_cases)
    return total_price, daily_price,predicted_cases 


# def userInterface():
#     stocks = [row[0] for row in dataBase.get_Currency()]
#
#     # st.set_page_config(layout="wide")
#     # st.sidebar.title('Предсказание цены акций')
#
#     # form = st.sidebar.form(key='crypto_select')
#
#     buff, col, buff2 = st.columns([1, 2, 1])
#
#
#     form = col.form(key='crypto_select')
#     ticker = form.selectbox('Выберите пару криптовалюты для предсказания', stocks)
#     DAYS_TO_PREDICT=form.slider('Период предсказания: ', 15, 30)
#     submit_button = form.form_submit_button(label='Рассчитать')
#
#     if submit_button:
#         seq_length, num_epochs=init()
#         total_price, daily_price,predicted_cases=predict(ticker, DAYS_TO_PREDICT, seq_length, num_epochs)
#         Charts(ticker,total_price, daily_price,predicted_cases)
#         col.write(predicted_cases)

# if __name__ == "__main__":
#     userInterface()
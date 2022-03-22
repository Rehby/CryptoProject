from neuralnetwork import dataBase
import streamlit as st
from neuralnetwork.main import predict, init, charts

def load_view():
    stocks = [row[0] for row in dataBase.get_Currency()]

    buff, col, buff2 = st.columns([1, 2, 1])

    form = col.form(key='crypto_select')
    ticker = form.selectbox('Выберите пару криптовалюты для предсказания', stocks)
    DAYS_TO_PREDICT = form.slider('Период предсказания: ', 15, 30)
    submit_button = form.form_submit_button(label='Рассчитать')

    if submit_button:
        seq_length, num_epochs = init()
        total_price, daily_price, predicted_cases = predict(ticker, DAYS_TO_PREDICT, seq_length, num_epochs)
        charts(ticker, total_price, daily_price, predicted_cases)
        buff, col, buff2 = st.columns([1, 2, 1])
        col.write(predicted_cases)

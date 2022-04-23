from neuralnetwork import dataBase
import streamlit as st
import re


def name_ok(text):
    match = re.match("^[a-zA-Z0-9]+$", text)
    return bool(match)
def short_name_ok(text):
    match = re.match("^[a-zA-Z0-9]+[-]+[a-zA-Z]+$", text)
    return bool(match)

def load_view():
    stocks = [row[0] for row in dataBase.get_Currency()]

    buff, col, buff2 = st.columns([1, 2, 1])

    with col.form("crypto_add"):
        stock=["Yfinance"]
        name=st.text_input("Введите название валюты")
        short_name = st.text_input("Введите короткое название валюты")
        ticker = st.selectbox('Выберите сайт с данными', stock)
        submit_button = st.form_submit_button(label='Добавить')
        try:

            if submit_button and name_ok(name) and short_name_ok(short_name):
                st.warning("Данные добавлены")
            elif submit_button:
                st.warning("Введены некорректные данные")
        except:
            st.warning("Введены некорректные данные")


    with col.form("my_form"):
        cc_name = st.selectbox("Криптовалюта для редактирования", stocks)
        neurons = st.text_input("Введите число нейронов в слое(10-100)")
        layer_count = st.text_input("Введите число слоев(1-5)")
        submitted = st.form_submit_button("Изменить")
        try:
            if submitted and float(neurons)>=100 and float(neurons)<=10 and float(layer_count)<=1 and float(layer_count)>=5:
                st.warning("Введены некорректные данные")
            elif submitted:
                st.warning("Данные изменены")
        except:
            st.warning("Введены некорректные данные")




import datetime
from datetime import date
import torch
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from Predictor import CryptoPredictor
from Train import train_model


from plotly import graph_objs as go
import plotly

import plotly.tools as tls
import streamlit as st


sns.set(style='whitegrid', palette='muted', font_scale=1.2)

HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#93D30C", "#8F00FF"]

sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))

rcParams['figure.figsize'] = 14, 10
register_matplotlib_converters()

RANDOM_SEED = 12
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

num_epochs = 21
seq_length = 64


ticker="BTC-USD"

stocks = ('BTC-USD', 'LTC-USD', 'BNB-USD', 'DOGE-USD', 'XRP-USD',  'ETH-USD', "AAPL")
TODAY = date.today().strftime("%Y-%m-%d")

st.sidebar.title('Предсказание цены акций')

form = st.sidebar.form(key='my_form')
ticker = form.selectbox('Выберите пару криптовалюты для предсказания', stocks)
DAYS_TO_PREDICT=form.slider('Период предсказания: ', 15, 30)
submit_button = form.form_submit_button(label='Рассчитать')
if submit_button:

    model = CryptoPredictor(
      n_features=1,
      n_hidden=80,
      seq_len=seq_length,
      n_layers=2
    )
    _, _, _, preds, total_price,daily_price,scaler = train_model(
      model,
      num_epochs,
      seq_length,
      ticker,
      DAYS_TO_PREDICT
    )

    predicted_cases = scaler.inverse_transform(
      np.expand_dims(preds, axis=0)
    ).flatten()
    predicted_index = pd.date_range(
      start=total_price.index[-1],
      periods=DAYS_TO_PREDICT + 1,
      closed='right'
    )

    predicted_cases = pd.Series(
      data=predicted_cases,
      index=predicted_index
    )

    print( predicted_cases)
    plt.plot(total_price, label='Historical Daily Cases')


    import plotly.graph_objects as go
    import plotly.express as px

    # plt.figlegend()
    # st.pyplot(plt)
    # plt.show()
    # plt.close()
    # plt.plot(daily_price, label='Historical Daily Cases')
    # fig = go.Figure([go.Scatter(x=daily_price.index, y=daily_price)])
    # fig.show()
    fig1 = px.bar(
        title=f"Стоимость {ticker}")

    fig1.update_layout(xaxis_title="Дата",
        yaxis_title="Стоимсоть Usd")
    fig1.add_trace(go.Scatter(x=total_price.index, y=total_price))
    st.plotly_chart(fig1)

    fig = px.bar(
          title=f"Стоимость {ticker}")
    fig.add_trace(go.Scatter(x=daily_price.index, y=daily_price, name="Данные о стоимости"))
    fig.add_trace(go.Scatter(x=predicted_cases.index, y=predicted_cases, name="Прогнозируемая стоимость",mode='lines'))
    # fig.show()
    fig.update_layout(xaxis_title="Дата",
        yaxis_title="Стоимсоть Usd",
      )

    # plt.figlegend()

    st.plotly_chart(fig)
    # st.write(predicted_cases)
    # plt.show()


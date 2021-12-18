import datetime
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

import pandas_datareader.data as pdr
import time

import torch
import yfinance as fix
fix.pdr_override()

def get_stock_data(ticker) :
    """
    Gets historical stock data of given tickers between dates
    :param ticker: company, or companies whose data is to fetched
    :type ticker: string or list of strings
    :param start_date: starting date for stock prices
    :type start_date: string of date "YYYY-mm-dd"
    :param end_date: end date for stock prices
    :type end_date: string of date "YYYY-mm-dd"
    :return: stock_data.csv
    """
    start_date = datetime.date(2000,1,1)
    end_date = datetime.datetime.now()
    i = 1
    try:
        all_data = pdr.get_data_yahoo(ticker, start_date, end_date)
    except ValueError:
        print("ValueError, trying again")
        i += 1
        if i < 5:
            time.sleep(10)
            get_stock_data(ticker, start_date, end_date)
        else:
            print("Tried 5 times, Yahoo error. Trying after 2 minutes")
            time.sleep(120)
            get_stock_data(ticker, start_date, end_date)
    stock_data = all_data["Close"]
    stock_data.to_csv(f"data/{ticker}.csv")



def get_data(ticker):
    df = pd.read_csv(f"data/{ticker}.csv")
    total_price = df["Close"]
    total_price.index = pd.to_datetime(df["Date"])
    dt=datetime.datetime.now()
    dt = dt.replace(year=dt.year - 1)
    df= df[(pd.to_datetime(df["Date"]) > dt.strftime("%m-%d-%Y"))]
    daily_price = df["Close"]
    daily_price.index = pd.to_datetime(df["Date"])

    return  daily_price, total_price


def create_sequences(data, seq_length):
    xs = []
    ys = []

    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)

def secData(daily_price,seq_length):
   scaler = MinMaxScaler()
   scaler = scaler.fit(np.expand_dims(daily_price, axis=1))
   all_data = scaler.transform(np.expand_dims(daily_price, axis=1))
   X_all, y_all = create_sequences(all_data, seq_length)

   X_all = torch.from_numpy(X_all).float()
   y_all = torch.from_numpy(y_all).float()
   return  X_all,y_all,scaler
import datetime
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import time
import torch
import yfinance as fix

fix.pdr_override()

def get_stock_data(ticker,site="yfinance") :

    start_date = datetime.date(2010,1,1)
    end_date = datetime.datetime.now()


    if site=="yfinance":
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
    elif site =="alphavantage":
        pass


def get_data(ticker):

    try:
        df = pd.read_csv(f"data/{ticker}.csv")
    except:
        df = pd.read_csv(f"../data/{ticker}.csv")
    data = pd.to_datetime(df["Date"])
    print(data[-1:])
    if data[data.count()-1] < datetime.date.today():
        print("Получаю данные")
        get_stock_data(ticker)

        try:
            df = pd.read_csv(f"data/{ticker}.csv")
        except:
            df = pd.read_csv(f"../data/{ticker}.csv")
        total_price = df["Close"]
        total_price.index = pd.to_datetime(df["Date"])

    total_price = df["Close"]
    total_price.index = pd.to_datetime(df["Date"])
    dt=datetime.datetime.now()
    dt = dt.replace(year=dt.year - 2)
    df= df[(pd.to_datetime(df["Date"]) > dt.strftime("%m-%d-%Y"))]

    daily_price = df["Close"]
    daily_price.index = pd.to_datetime(df["Date"])

    return  total_price, daily_price


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
   return  X_all, y_all, scaler


def normalize_data(scaler,
                   preds ,
                   total_price,
                   DAYS_TO_PREDICT):
    predicted_cases = scaler.inverse_transform(
        np.expand_dims(
                    preds,
                    axis=0)
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

    return predicted_cases

def normalize_db_data(data,total_price,DAYS_TO_PREDICT):
    preds = pd.DataFrame(data)
    predicted_cases = np.asarray(preds[4])

    predicted_index = pd.date_range(
        start=total_price.index[-1],
        periods=DAYS_TO_PREDICT + 1,
        closed='right'
    )

    predicted_cases = pd.Series(
        data=predicted_cases,
        index=predicted_index

    )
    return predicted_cases









if __name__ =="__main__":
    get_stock_data("BTC-USD")
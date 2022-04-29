import psycopg2
import datetime
import pandas as pd


def con():
    conn = psycopg2.connect(dbname='CryptoPredict', user='postgres',
                            password='root', host='localhost')
    c = conn.cursor()
    return conn, c


def get_Currency():
    conn, c = con()
    c.execute(f"SELECT c_short_name FROM currency")
    data = c.fetchall()
    conn.close()
    return data


def add_Currency(name, short_name):
    conn, c = con()
    c.execute(f'INSERT INTO currency(cName,c_short_name) VALUES ({name},{short_name})')
    c.commit()
    conn.close()
    conn.close()


def login_user(username, password):
    conn, c = con()
    c.execute(f"SELECT * FROM users WHERE login ='{username}' AND pass = '{password}'")
    data = c.fetchone()
    conn.close()
    return data


def add_userdata(username, password, email):
    conn, c = con()
    c.execute(f'INSERT INTO users(login,pass,email) VALUES ({username},{password},{email})')
    conn.commit()
    conn.close()


def add_crypto_currency(site, values, currency):
    conn, c = con()
    for index in values.index:
        c.execute(f'INSERT INTO Crypto_currency(site_id,upd_date,value,date,currency_id) VALUES ( %s,%s,%s,%s,%s )', (
        site, str(datetime.date.today().strftime("%d-%m-%Y")), float(values[index]), str(index.strftime("%d-%m-%Y")),
        currency))
    conn.commit()
    conn.close()


def add_predict(values, currency):
    conn, c = con()
    for index in values.index:
        c.execute(f'INSERT INTO Predict(cc_id,predict_date,date,value) VALUES ( %s,%s,%s,%s )', (
        currency, str(index.strftime("%d-%m-%Y")), str(datetime.date.today().strftime("%d-%m-%Y")),
        float(values[index])))
    conn.commit()
    conn.close()


def check_actual(ticker, days):
    """

    :param ticker:
    :param days:
    :return: ndaray with price  data
                or False if 1 or more days not exist in db
    """
    conn, c = con()
    day = datetime.date.today()
    id=get_cc_id(ticker)
    data=[]
    prevdate=datetime.date.today()-datetime.timedelta(days=1)
    for i in range(days):
        day += datetime.timedelta(days=1)
        c.execute(f'SELECT * FROM Predict WHERE  cc_id=%s AND predict_date=%s AND date>=%s', [id, str(day.strftime("%d-%m-%Y")), str(prevdate.strftime("%d-%m-%Y"))])
        abs = c.fetchall()


        if abs==[]:
            print("Прогноз отсутствует")
            return False

        data.append(abs[len(abs)-1])

    conn.commit()
    conn.close()

    return data

def get_nn_param(ticker):
    id=get_cc_id(ticker)
    id=3
    conn, c = con()
    c.execute(f'SELECT sequence,epoch,hidden,layers FROM nn WHERE  currency_id=%s',
              [id])
    params = c.fetchone()
    conn.commit()
    conn.close()
    if params==None:
        # Если отсутствуют параметры для криптовалюты
        params=[]
        params.append(8)
        params.append(80)
        params.append(20)
        params.append(2)

    return params


def get_cc_id(ticker):
    conn, c = con()
    c.execute(f"SELECT id FROM currency WHERE  c_short_name=%s",[ticker,])
    ticker_id=c.fetchone()
    conn.commit()
    conn.close()

    return ticker_id[0]


def add_new_currency(name,short_name):
    conn, c = con()
    c.execute(f'INSERT INTO Currency(cName,c_short_name) VALUES ( %s,%s )', [name,short_name,])
    conn.commit()
    conn.close()

def edit_nn_params(sequence,epoch,hidden,layers,ticker):
    id=get_cc_id(ticker)
    conn, c = con()
    c.execute(f'SELECT sequence,epoch,hidden,layers FROM nn WHERE  currency_id=%s',
              [id])
    params = c.fetchone()
    if params==None:
        c.execute(f'INSERT INTO nn(sequence,epoch,hidden,layers,currency_id) VALUES (%s,%s,%s,%s,%s)',
              [sequence,epoch,hidden,layers,id])
    else:
        c.execute(f'UPDATE nn SET sequence=%s,epoch=%s,hidden=%s,layers=%s WHERE currency_id=%s',
                 [sequence, epoch, hidden, layers, id])

    conn.commit()
    conn.close()





if __name__ == "__main__":
    edit_nn_params(8,20,40,2,"XRP-USD")
    # get_nn_param("LTC-USD")
    # add_new_currency("Litecion","LTC-USD")
    # df = pd.read_csv(f"../data/{'BTC-USD'}.csv")
    # total_price = df["Close"]
    # total_price.index = pd.to_datetime(df["Date"]).dt.date
    # add_crypto_currency(1, total_price, 1)

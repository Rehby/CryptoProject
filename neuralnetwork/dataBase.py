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
    conn, c = con()
    day = datetime.date.today()
    id=1
    data=[]
    prevdate=datetime.date.today()-datetime.timedelta(days=1)
    for i in range(days):
        day += datetime.timedelta(days=1)
        c.execute(f'SELECT * FROM Predict WHERE  cc_id=%s AND predict_date=%s AND date>=%s', [id, str(day.strftime("%d-%m-%Y")), str(prevdate.strftime("%d-%m-%Y"))])
        abs = c.fetchall()


        if abs==[]:
            print("Отсутствует")
            return 0

        data.append(abs[len(abs)-1])

    conn.commit()
    conn.close()

    return data




if __name__ == "__main__":
    df = pd.read_csv(f"../data/{'BTC-USD'}.csv")
    total_price = df["Close"]
    total_price.index = pd.to_datetime(df["Date"]).dt.date
    add_crypto_currency(1, total_price, 1)

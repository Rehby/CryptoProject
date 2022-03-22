import psycopg2
import datetime
import pandas as pd

def con():
	conn = psycopg2.connect(dbname='CryptoPredict', user='postgres',
							password='root', host='localhost')
	c = conn.cursor()
	return conn,c

def get_Currency():
	conn,c=con()
	c.execute(f"SELECT c_short_name FROM currency")
	data = c.fetchall()
	conn.close()
	return data

def add_Currency(name,short_name):
	conn, c = con()
	c.execute(f'INSERT INTO currency(cName,c_short_name) VALUES ({name},{short_name})')
	c.commit()
	conn.close()
	conn.close()


def login_user(username,password):
	conn, c = con()
	c.execute(f"SELECT * FROM users WHERE login ='{username}' AND pass = '{password}'")
	data = c.fetchone()
	conn.close()
	return data

def add_userdata(username,password,email):
	conn, c = con()
	c.execute(f'INSERT INTO users(login,pass,email) VALUES ({username},{password},{email})')
	conn.commit()
	conn.close()

def add_crypto_currency(site,values,currency):
	conn, c = con()
	for index in values.index:
		print(index.strftime("%d-%m-%Y"))
		c.execute(f'INSERT INTO Crypto_currency(site_id,upd_date,value,date,currency_id) VALUES ({1},{ datetime.date.today().strftime("%d-%m-%Y")},{float( values[index])},CAST({index.strftime("%d-%b-%Y")}),{1})')
	conn.commit()
	conn.close()

if __name__=="__main__":
	df = pd.read_csv(f"data/{'BTC-USD'}.csv")
	total_price = df["Close"]
	total_price.index = pd.to_datetime(df["Date"]).dt.date
	add_crypto_currency(1,total_price,1)

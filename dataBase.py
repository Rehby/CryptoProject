import psycopg2

conn = psycopg2.connect(dbname='CryptoPredict', user='postgres',
                        password='root', host='localhost')
def get_Currency():
	c = conn.cursor()
	c.execute(f"SELECT c_short_name FROM currency")
	data = c.fetchall()
	return data

def add_Currency(name,short_name):
	c = conn.cursor()
	c.execute(f'INSERT INTO currency(cName,c_short_name) VALUES ({name},{short_name})')
	c.commit()
	conn.close()

def add_userdata(username,password,email):
	c = conn.cursor()
	c.execute(f'INSERT INTO users(login,pass,email) VALUES ({username},{password},{email})')
	conn.commit()

def login_user(username,password):
	c = conn.cursor()
	c.execute(f"SELECT * FROM users WHERE login ='{username}' AND pass = '{password}'")
	data = c.fetchone()
	return data


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


import psycopg2
import  streamlit as st

def add_userdata(username,password,email):

	c.execute(f'INSERT INTO users(login,pass,email) VALUES ({username},{password},{email})')
	conn.commit()

def login_user(username,password):
	c.execute(f"SELECT * FROM users WHERE login ='{username}' AND pass = '{password}'")
	data = c.fetchone()
	return data


if (__name__ =="__main__"):
	conn = psycopg2.connect(dbname='CryptoPredict', user='postgres',
							 password='root', host='localhost')
	c = conn.cursor()

	st.title("Test application form")
	menu = ["Home","Login"]
	choice = st.sidebar.selectbox("Menu", menu)
	if choice == "Home":
		st.subheader("Home")
	elif choice == "Login":

		username = str(st.sidebar.text_input("User Name"))
		password = str(st.sidebar.text_input("Password", type='password'))

		if st.sidebar.button("Login"):
			try:
				if(login_user(username, password)!=None):
					st.write(login_user(username, password))
				else:
					st.write("Неправильный логин или пароль")
			except:
				pass

	add_userdata("123","123","1234")

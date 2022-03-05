from dataBase import  login_user,add_userdata
import  streamlit as st

if (__name__ =="__main__"):
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
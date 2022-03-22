import  streamlit as st
import utils as utl
from pages import home, help,about



st.set_page_config(layout="wide", page_title='Прогнозирование рынка криптовалют')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()
def navigation():
	route = utl.get_current_route()
	if route == "home":
		home.load_view()
	elif route == "help":
		help.load_view()

	elif route == "about":
		about.load_view()
	elif route == "admin":
		pass


if (__name__ =="__main__"):
	navigation()
	# st.title("")
	# menu = ["Главное меню","Логин","Составить прогноз"]
	# choice = st.sidebar.selectbox("Menu", menu)
	#
	# if choice == "Главное меню":
	# 	st.subheader("Главное меню")
	# 	# st.write("Раздел 'Главное меню' содержит основную информацию")
	# 	# st.write("Раздел 'Составить прогноз' предоставляет функционал прогнозирования стоимости криптовалюты")
	# 	# st.write("Криптовалю́та — разновидность цифровой валюты, учёт внутренних расчётных единиц которой обеспечивает децентрализованная платёжная система (нет внутреннего или внешнего администратора или какого-либо его аналога)[1][2], работающая в полностью автоматическом режиме. Сама по себе криптовалюта не имеет какой-либо особой материальной или электронной формы — это просто число, обозначающее количество данных расчётных единиц, которое записывается в соответствующей позиции информационного пакета протокола передачи данных и зачастую даже не подвергается шифрованию, как и вся иная информация о транзакциях между адресами системы.")
	# 	# st.write("Основной задачей автоматизированной информационной системы является определение стоимость криптовалюты на определенный, выбранный пользователем, период.")
	#
	# 	st.image("https://www.ixbt.com/img/n1/news/2021/10/3/iStock-1034363382-1-1_large_large_large.jpg",caption=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
	# elif choice == "Логин":
	# 	st.image("https://www.ixbt.com/img/n1/news/2021/10/3/iStock-1034363382-1-1_large_large_large.jpg", caption=None,
	# 			 use_column_width=None, clamp=False, channels="RGB", output_format="auto")
	# 	username = str(st.sidebar.text_input("User Name"))
	# 	password = str(st.sidebar.text_input("Password", type='password'))
	#
	# 	if st.sidebar.button("Вход"):
	# 		try:
	# 			if(login_user(username, password)!=None):
	# 				st.write(login_user(username, password))
	# 			else:
	# 				st.sidebar.write("Неправильный логин или пароль")
	# 		except:
	# 			pass
	#
	# 	st.sidebar.button("Регистрация")
	# elif choice == "Составить прогноз":
	# 	userInterface()
	#
	# # st.button("📆", on_click=style_button_row, kwargs={
	# # 	'clicked_button_ix': 1, 'n_buttons': 4
	# # })
	# st.sidebar.text("Помощь")
	# st.sidebar.text("Инфо",)

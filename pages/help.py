import streamlit as st


def load_view():
    buff, col, buff2 = st.columns([1, 4, 1])

    col.write("Раздел '📈 Прогнозирование' предоставляет функционал прогнозирования стоимости криптовалюты")
    col.write("Раздел 'ℹ️ О программе' содержит справочную информацию")
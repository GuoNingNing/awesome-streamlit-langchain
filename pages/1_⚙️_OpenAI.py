import streamlit as st

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""

st.set_page_config(page_title="OpenAI Settings", layout="wide")

st.title("OpenAI Settings")


openai_api_key = st.text_input("API Key", value=st.session_state["OPENAI_API_KEY"], max_chars=None, key=None, type='password')

saved = st.button("Save")

if saved:
    st.session_state["OPENAI_API_KEY"] = openai_api_key
    # 当用户点击按钮时，将数据保存到LocalStorage中
    st.write('数据已保存到LocalStorage')
    st.write(f'用户输入的数据为: {openai_api_key}')

    # 执行JavaScript代码将数据保存到LocalStorage
    st.markdown(f'<script>localStorage.setItem("OPENAI_API_KEY", "{openai_api_key}")</script>', unsafe_allow_html=True)

    # 在页面上显示从LocalStorage中读取的数据
    stored_data = st.markdown('<script>localStorage.getItem("OPENAI_API_KEY")</script>', unsafe_allow_html=True)
    st.write(stored_data)

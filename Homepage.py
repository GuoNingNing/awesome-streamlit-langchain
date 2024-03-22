import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage
)

# Initialize the ChatOpenAI object
chat = None

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
elif st.session_state["OPENAI_API_KEY"] != "":
    chat = ChatOpenAI(openai_api_key=st.session_state["OPENAI_API_KEY"])

st.set_page_config(page_title="Welcome to ASL", layout="wide")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if chat:
    with st.container():
        # 创建一个空元素用于流式呈现AI输出内容
        ai_output = st.empty()

        for message in st.session_state["messages"]:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

        prompt = st.chat_input("Type something...")
        if prompt:
            st.session_state["messages"].append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)

            ai_message = AIMessage(content="")
            # 更新空元素中的内容，实现流式呈现
            with st.chat_message("assistant"):
                for chunk in chat.stream(st.session_state["messages"]):
                    ai_message = ai_message + chunk
                    ai_output.markdown(chunk.content)

            st.session_state["messages"].append(ai_message)

else:
    with st.container():
        st.warning("Please set your OpenAI API key in the settings page.")

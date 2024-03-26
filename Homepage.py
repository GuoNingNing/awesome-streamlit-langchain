import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
st.set_page_config(page_title="哇卡玛咖", layout="wide")
chat = None
# Initialize the ChatOpenAI object
if "key" not in st.query_params:
    st.error("请输入openai_api_key")

else:
    if chat is None:
        print("初始化OpenAi")
        chat = ChatOpenAI(openai_api_key=st.query_params["key"],
                          model_name="gpt-3.5-turbo-instruct-0914"
                          )


def init():

    st.session_state["messages"] = []


if "messages" not in st.session_state:
    init()


def show_messages():
    for message in st.session_state["messages"]:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, SystemMessage):
            with st.chat_message("system"):
                st.markdown(message.content)


def ask(prompt):
    st.session_state["messages"].append(HumanMessage(content=prompt))
    ai_messages = ""
    for chunk in chat.stream(st.session_state["messages"]):
        ai_messages += chunk.content
        yield chunk.content
    st.session_state["messages"].append(AIMessage(content=ai_messages))


def main():
    with st.container(height=680, border=False):
        show_messages()
        user = st.empty()
        ai = st.empty()

    with st.container(height=80, border=False):
        prompt = st.chat_input("键入内容...")
        if prompt:

            if prompt == '#清除':
                init()
            else:
                # 更新空元素中的内容，实现流式呈现
                user.chat_message('user').write(prompt)
                ai.chat_message('assistant').write("思考中....")
                ai.chat_message('assistant').write_stream(ask(prompt))


if __name__ == '__main__':
    main()

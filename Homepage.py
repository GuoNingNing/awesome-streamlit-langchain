import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Initialize the ChatOpenAI object
chat = None

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
elif st.session_state["OPENAI_API_KEY"] != "":
    chat = ChatOpenAI(openai_api_key=st.session_state["OPENAI_API_KEY"])

st.set_page_config(page_title="Welcome to ASL", layout="wide")

if "messages" not in st.session_state:
    st.session_state["messages"] = [SystemMessage(content="你是无所不能的罗伯特，请问我任何你想提问的问题")]


def show_messages():
    print("show_messages")
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
    with st.container(height=600):
        show_messages()
        assistant = st.empty()
        ai = st.empty()

    with st.container(height=80):
        prompt = st.chat_input("Type something...")
        if prompt:
            # 更新空元素中的内容，实现流式呈现
            assistant.chat_message('user').write(prompt)
            ai.chat_message('assistant').write("思考中....")
            ai.chat_message('assistant').write_stream(ask(prompt))


if __name__ == '__main__':
    main()

import streamlit as st
from utils import qa_agent
from langchain.memory import  ConversationBufferMemory

st.title("PDF Chatbot：智能问答助手")

with st.sidebar:
    api_key = st.text_input("请输入OpenAI API密钥", type="password")
    api_base = st.text_input("请输入OpenAI API地址")
    st.markdown = ("[获取Open AI key](https://platform.openai.com/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
uploaded_file = st.file_uploader("上传你的PDF文件：",type="pdf")
question = st.text_input("请输入你的问题：",disabled=not uploaded_file)

if uploaded_file and question and not (api_key or api_base):
    st.info("请在侧边栏中输入OpenAI API密钥和地址")

if uploaded_file and question and api_key and api_base:
    with st.spinner("AI正在思考中……"):
        response = qa_agent(api_key, api_base, st.session_state["memory"], uploaded_file, question)

    st.write("### 回答")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0,len(st.session_state["chat_history"]),2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i<len(st.session_state["chat_history"])-2 :
                st.divider()

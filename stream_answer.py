from api import chat
from openai import RateLimitError
import streamlit as st
import json
import time

sys_messages = [
        {
            "role": "system",
            "content": "1.你是资深数学高中教师，你擅长求解数学题目。2.我给你提供了高中数学教材和课标，你的回答要指出课本的知识点在那哪一章节。3.你的解答如果有数学公式请使用$$包裹，如$x_1^2+x_2^2=1$"
            # "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为markdown形式，但是请直接文本输出latex公式。3.如果识别的某个数学公式长度超过10个字母，你会自动添加换行符。"
        },
         {
            "role": "system",
            "content": "1.你解答题目时先说一下知识点20字左右，然后给出分布解答，最后给出教师需要重点讲解的部分30字左右$"
            # "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为markdown形式，但是请直接文本输出latex公式。3.如果识别的某个数学公式长度超过10个字母，你会自动添加换行符。"
        }
    ]

#
#st.session_state可以定义不被重置的量
def clear_chat_history():
    del st.session_state.messages2
    del st.session_state.number2

def init_chat_history():
    # st.write(st.session_state.messages)
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是IM Teacher，很高兴为您服务")
    if "number2" not in st.session_state:
         st.session_state.number2=0
    if "messages2" in st.session_state:
         for message in st.session_state.messages2:
            if message["role"] == "user":
                with st.chat_message(message["role"], avatar = '🧑'):
                    st.markdown(message["content"])
            if message["role"] == "assistant":
                with st.chat_message(message["role"],avatar = '🤖'):
                    st.markdown(message["content"])
        
    else:
        st.session_state.messages2 = []
    return st.session_state.messages2

def stream_ans():
    collected_messages = ""
    with st.chat_message("assistant", avatar='🤖'):
        placeholder = st.empty()
        try:
            response = chat(history=st.session_state.messages2)
        except RateLimitError as e:
            st.markdown(e)
            st.session_state.messages2.append({"role": "assistant", "content": "error"+e})
        for chunk in response:
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            chunk_message = chunk_message.content
            # print(chunk_message)
            collected_messages = collected_messages + chunk_message
            placeholder.markdown(collected_messages)
        st.session_state.messages2.append({"role": "assistant", "content": collected_messages})

def q_a():
        if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
            st.session_state.number2+=1
            if st.session_state.number2%5==0:
                for i in sys_messages:st.session_state.messages2.append(i)
            with st.chat_message("user", avatar='🧑'):
                st.markdown(prompt)
                st.session_state.messages2.append({"role": "user", "content": prompt})
            stream_ans()
            st.button("清空对话", on_click=clear_chat_history)


init_chat_history()
q_a()
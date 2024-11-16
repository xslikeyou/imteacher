from api import chat,set_client
from openai import RateLimitError
from pathlib import Path
import streamlit as st
import json
sys_messages = [
     {
         "role": "system",
         "content": "1.你是一位高中数学老师，你擅长解题。2.你可以找出问题中的关键知识点，然后后针对关键知识点生成类似的题目。"
     },
     {"role": "system", 
      "content": "请根据下面的题目，生成类似的题目,把数学公式输出为latex形式，公式($$)包裹,例如$x_1^2+x_2^2=1$"
      },
 ]

def clear_chat_history():
    del st.session_state.messages

def init_chat_history():
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是IM Teacher，很高兴为您服务")
    if "messages" in st.session_state:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message(message["role"], avatar = '🧑'):
                    st.markdown(message["content"])
            if message["role"] == "assistant":
                with st.chat_message(message["role"],avatar = '🤖'):
                    st.markdown(message["content"])
    else:
        st.session_state.messages = []
    return st.session_state.messages


def generate_question(history):
    for i in sys_messages:
        history.append(i)
    collected_messages = ""
    # print(f"[user] {prompt}", flush=True)
    with st.chat_message("assistant", avatar='🤖'):
        placeholder = st.empty()
        try:
            response = chat(history)
        except RateLimitError as e:
            st.markdown(e)
            st.session_state.messages.append({"role": "assistant", "content": "error"+e})
        for chunk in response:
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            chunk_message = chunk_message.content
            # print(chunk_message)
            collected_messages = collected_messages + chunk_message
            placeholder.markdown(collected_messages)
        st.session_state.messages.append({"role": "assistant", "content": collected_messages})
        # st.write(st.session_state.messages)


def main():
    uploaded_file = st.file_uploader("请上传文件", type=["pdf", "doc", "png", "jpg", "jpeg", "bmp", "gif"])
    st.write(uploaded_file)
    init_chat_history()
    # 检查是否有文件被上传
    if uploaded_file is not None:
        st.write("文件上传中...")
        # 获取文件路径
        file_path = Path(uploaded_file.name)
        # # 保存文件到本地
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            # 图片文件
            try:
                print("获取图片")
                file_object = set_client.files.create(file=file_path, purpose="file-extract")
                print("识别图片")
                file_content = set_client.files.content(file_id=file_object.id).text
            except RateLimitError as e:
                    st.markdown(e)
                    st.session_state.messages.append({"role": "assistant", "content": "error"+e})

            with st.chat_message("user", avatar='🧑'):
                st.markdown(file_content)
            st.session_state.messages.append({"role": "system","content": file_content,})
            generate_question(st.session_state.messages)
        else:st.write("文件类型错误")  
    st.button("清空对话", on_click=clear_chat_history,key="clear")
    # st.button("再来一题", on_click=generate_question(st.session_state.messages),key="create_q")



main()



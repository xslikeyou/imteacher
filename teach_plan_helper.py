from api import chat
from openai import RateLimitError
import streamlit as st
#stream_ans里面调用chat接口
sys_messages = [
        {
            "role": "system",
            "content": "1.你是资深数学高中教师，你擅长教案编写。2.我会提供给你需要教学的知识，教材版本，教学方法。3.你需要按照教材分析、学情分析、教学重点、教学过程、教学反思角度设计教案。4.尤其教学过程，你需要按照我写的教学方法编写，你可以自行查找优秀的教学过程进行参考"
            # "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为markdown形式，但是请直接文本输出latex公式。3.如果识别的某个数学公式长度超过10个字母，你会自动添加换行符。"
        },
    ]

def clear_chat_history():
    del st.session_state.messages1
    del st.session_state.number1

def init_chat_history():
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是IM Teacher，很高兴为您服务")
    if "choice" not in st.session_state:
         st.session_state.choice={}
    if "number1" not in st.session_state:
         st.session_state.number1=0 
    if "messages1" in st.session_state:
        for message in st.session_state.messages1:
            if message["role"] == "user":
                with st.chat_message(message["role"], avatar='🧑'):
                    st.markdown(message["content"])
            if message["role"] == "assistant":
                with st.chat_message(message["role"], avatar='🤖'):
                    st.markdown(message["content"])
    else:
        st.session_state.messages1 = []
    return st.session_state.messages1

def prompt_chose():
    with st.form('prompt_choice'):
        # 添加教材版本选择框
        st.session_state.choice["教材"]= st.selectbox("请选择教材版本", ["沪教版", "人教版", "鲁教版", "其他"])
        st.session_state.choice["其他教材"]=st.text_input("选择其他教材版本请输入", key="textbook_others")
        st.session_state.choice["教法"] = st.selectbox("请选择教法", ["凯洛夫教学法", "布鲁姆教学法", "加涅教学法","基于建构主义的教学法", "其他"])
        st.session_state.choice["其他教法"]= st.text_input("选择其他教法请输入", key="teach_others")
        st.form_submit_button('开始生成')

def stream_ans():
    collected_messages = ""
    with st.chat_message("assistant", avatar='🤖'):
        placeholder = st.empty()
        try:
            response = chat(history=st.session_state.messages1)
        except RateLimitError as e:
            st.markdown("Ratelimit error")
            st.session_state.messages1.append({"role": "assistant", "content": "Ratelimit error"})
        for chunk in response:
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            chunk_message = chunk_message.content
            # print(chunk_message)
            collected_messages = collected_messages + chunk_message
            placeholder.markdown(collected_messages)
        st.session_state.messages1.append({"role": "assistant", "content": collected_messages})

def main():
        init_chat_history()
        prompt_chose()

        if prompt := st.chat_input("请描述你要教授的知识"):
            st.session_state.number1+=1
            if st.session_state.number1%5==0:
              for i in sys_messages:st.session_state.messages1.append(i)
            with st.chat_message("user", avatar='🧑'):
                st.markdown(prompt)
                st.session_state.messages1.append({"role": "user", "content": prompt+"请开始工作，帮我生成教案"})
            stream_ans()
            # st.write(st.session_state.messages)#
            st.button("清空对话", on_click=clear_chat_history)

main()

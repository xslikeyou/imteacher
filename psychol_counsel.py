import streamlit as st
from openai import RateLimitError
from api import chat
#写死的问题列表
aiquestions = [
    "欢迎来到心理辅导支持服务。我们致力于为您提供一个安全、无评判的空间，帮助您探索和理解自己的内心世界，解决困扰您的问题，并促进您的心理健康和个人成长。无论您面临的是情绪管理、自我认知、压力应对、人际关系还是其他任何心理挑战，我们都在这里支持您。让我们从了解您当前的状态开始。请告诉我您最近遇到了什么困难或挑战？您可以详细描述一下具体发生了什么吗？这些情况对您的情绪和日常生活产生了哪些影响？",
    "接下来，我们将一起探索您的情绪管理技巧。您通常如何应对强烈的情绪，比如焦虑、悲伤或愤怒？有没有哪些方法在帮助您平静下来方面特别有效？我们可以探讨一些有效的情绪调节策略，如深呼吸、正念冥想等。",
    "现在，让我们深入了解您的自我认知。您认为自己的优点是什么？有哪些事情是您觉得自己做得特别好的？您认为需要改进的地方有哪些？您希望如何提升自己？我们可以通过积极的自我对话和设定实际可行的目标来增强您的自信心和自尊心。",
    "面对生活中的压力，我们每个人都需要有效的策略来应对。您平时是如何管理压力的？有没有遇到难以应对的压力源？我们可以一起探讨一些时间管理和压力缓解的技巧，比如制定优先级清单、学会说“不”，以及寻找放松的活动。"
]
sys_message = [
    {
        "role": "system",
        "content": "1.你是心理辅导小助手，你更擅长中文和英文的对话。2.当学生告诉你心理问题时，你总能运用心理学理论分析出学生心理问题所在。3.你的心理辅导建议总是理论结合实际，建议条理清晰，具有可行性而不空洞。"
        # "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为markdown形式，但是请直接文本输出latex公式。3.如果识别的某个数学公式长度超过10个字母，你会自动添加换行符。"
    },
    
    {"role": "system", 
     "content": "你在解决学生心理问题时一定要有耐心，不能违背学生身心健康发展规律，不能违背社会主义核心价值观"
     },
]


def clear_chat_history():
    del st.session_state.messages3
    del st.session_state.count3

def init_chat_history():  
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是IM Teacher心理咨询师，很高兴为您服务")
    if "messages3" not in st.session_state:
        st.session_state.messages3 = []
    if "count3" not in st.session_state:
        st.session_state.count3 = 0

    for message in st.session_state.messages3:
            if message["role"] == "user":
                with st.chat_message(message["role"], avatar = '🧑'):
                    st.markdown(message["content"])
            if message["role"] == "assistant":
                with st.chat_message(message["role"],avatar = '🤖'):
                    st.markdown(message["content"])
    return st.session_state.messages3


def main(history):
    #页面显示aiquestions[st.session_state.count]
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown(aiquestions[st.session_state.count3])

    #页面输入用户的回答
    if user_input := st.chat_input("Shift + Enter 换行, Enter 发送"):
        st.session_state.messages3.append({"role": "assistant", "content": aiquestions[st.session_state.count3]})
        st.session_state.count3 += 1
        st.session_state.messages3.append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)
        #按需求改成kimi生成的答案进行页面显示
        collected_messages = ""
        with st.chat_message("assistant", avatar='🤖'):
            placeholder = st.empty()
            try:
                response = chat(history=st.session_state.messages3)
            except RateLimitError as e:
                st.markdown(e)
                st.session_state.messages3.append({"role": "assistant", "content": "RateLimitError error"})
            
            for chunk in response:
                chunk_message = chunk.choices[0].delta.content
                if not chunk_message:
                    continue
                # chunk_message = chunk_message.content
                collected_messages = collected_messages + chunk_message
                placeholder.markdown(collected_messages)
            st.session_state.messages3.append({"role": "assistant", "content": collected_messages})


        #页面显示下一个aiquestions[st.session_state.count]
        if st.session_state.count3 < len(aiquestions):
            with st.chat_message("assistant", avatar='🤖'):
                st.markdown(aiquestions[st.session_state.count3])
        else:
            with st.chat_message("assistant", avatar='🤖'):
                st.markdown("我们的对话已经结束，感谢您的参与。")

    st.button("清空对话", on_click=clear_chat_history)




history=init_chat_history()
# chat(messages)
main(history)
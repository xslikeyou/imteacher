from pathlib import Path
from api import chat,set_client
from openai import RateLimitError
import streamlit as st
import os#上传文件后需要缓存


# 创建一个文件上传器，允许用户上传文件
uploaded_file = st.file_uploader("请上传文件", type=["pdf", "doc", "png", "jpg", "jpeg", "bmp", "gif"])

# 检查是否有文件被上传
if uploaded_file is not None:
    st.write("文件上传中...")
    # 构造完整的保存路径,
    save_directory='upload_file'
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory,uploaded_file.name)
    # 保存文件到指定位置
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 根据文件类型调用不同的API***********************************************************************
    if Path(uploaded_file.name).suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif','.pdf', '.doc']:
        try:
                print("获取图片")
                file_object = set_client.files.create(file=uploaded_file, purpose="file-extract")
                print("识别图片")
                file_content = set_client.files.content(file_id=file_object.id).text
        except RateLimitError as e:
                st.markdown(e)
                st.session_state.messages.append({"role": "assistant", "content": "error"+e})

    else:
        st.error("不支持的文件格式")
        file_content = ""

    # 将文件内容放入消息中
    messages = [
        {
            "role": "system",
            "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为latex形式，但是请直接文本输出latex公式，不要添加```latex。3.数学公式单独成行，你会自动为latex代码添加换行符'\\'。"
            # "content": "1.你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。2.你擅长提取图片中的内容,把文字输出为文本；把数学公式输出为markdown形式，但是请直接文本输出latex公式。3.如果识别的某个数学公式长度超过10个字母，你会自动添加换行符。"
        },
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "system", 
         "content": "1.请输出上面文件里的内容，一定不要输出其他提示语2.确保文本中的latex代码无语法错误"
         },
    ]

    # 然后调用 chat-completion, 获取 Kimi 的回答
    st.write("上传成功，题目识别...")
    completion = chat(history=messages)

    # 输出结果
    with st.chat_message("assistant", avatar='🤖'):
                st.write("识别结果")
                placeholder = st.empty()
                collected_messages=""
                for chunk in completion:
                    temp_messages=chunk.choices[0].delta.content
                    print(temp_messages,end="")
                    if not temp_messages:
                            continue
                    collected_messages = collected_messages + temp_messages
                    placeholder.code(collected_messages, language="latex")
                # st.write("普通文本")
                # st.text_area(collected_messages)

                st.write("latex渲染结果")
                # collected_messages = collected_messages.replace("$", "")
                print("*"*30)
                print(collected_messages)
                # st.markdown(collected_messages)
                # 将字符串转换为Markdown格式，并设置背景颜色
                collected_messages='\n'+collected_messages
                md_with_background = f"""
                <div style="background-color: lightblue; padding: 10px; border-radius: 5px;">
                    {collected_messages}
                </div>
                """

                # 使用st.markdown渲染带有背景颜色的Markdown内容
                st.markdown(md_with_background, unsafe_allow_html=True)

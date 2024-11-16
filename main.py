import streamlit as st

st.set_page_config(page_title="IM Teacher", page_icon="images/logo.png")
st.title("IM Teacher")
st.logo("images/logo.png")


def main():
    #st.Page创建页面
    qa_page = st.Page("stream_answer.py", title="问答",icon="💡")
    ocr_page = st.Page("ques_ocr.py", title="题目识别")
    mind_page=st.Page("psychol_counsel.py",title="心理咨询")
    similarq_page=st.Page("similar_question.py",title="相似题目生成")
    # tplan_page=st.Page("teach_plan_helper.py",title="教案助手")
    ziliao_page=st.Page("ziliao.py",title="资源库")
    caozuo_page=st.Page("caozuo.py",title="操作手册")
    
    pg = st.navigation([qa_page,ocr_page, mind_page,similarq_page,ziliao_page,caozuo_page])   
    pg.run()
        


if __name__ == "__main__":
    main()

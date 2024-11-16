import streamlit as st

# 创建一个包含说明和超链接的数据
data = [
    ("各学科教材大全", "https://basic.smartedu.cn/tchMaterial"),
    ("Latex公式编辑器", "https://www.latexlive.com/"),
    ("PPT模板", "https://www.1ppt.com/")
]

# 显示表格
st.write("### 声明：本页面为资料分享，本网站未获取任何广告费")

# 使用 markdown 来手动构建一个表格，第二列为超链接
table = "| 链接说明  | 链接  |\n"
table += "|-----------|-------|\n"
for description, url in data:
    table += f"| {description} | {url} |\n"#[{description}]({url})

# 使用 st.markdown 渲染这个表格
st.markdown(table)

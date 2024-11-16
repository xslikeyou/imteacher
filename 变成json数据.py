import json
from api import chat,set_client
from pathlib import Path
from openai import OpenAI
# 假设你有一个Python字典
print("读取文件")
file_object = set_client.files.create(file=Path("必修一.pdf"), purpose="file-extract")
print("分析文件")
data = set_client.files.content(file_id=file_object.id).text

# 将字典保存到JSON文件
# print("写入文件",type(data))
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4)

# print("输出文件")
# # 从JSON文件中读取数据
# with open('data.json', 'r') as f:
#     data = json.load(f)
#     # 打印读取的数据
# with open('example.txt', 'w', encoding='utf-8') as file:
#     file.write(data)
print(data)
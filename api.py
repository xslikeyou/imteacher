from openai import OpenAI, RateLimitError
set_client=OpenAI(
        api_key="替换成月之暗面的api",
        base_url="https://api.moonshot.cn/v1",
    )
# def system_chat(query, history):
#     history.append({
#         "role": "system",
#         "content": query
#     })
#     client = set_client
#     response = client.chat.completions.create(
#         model="moonshot-v1-8k",
#         messages=history,
#         temperature=0.3,
#         stream=True,
#     )
#     return response
def chat(history):
    client = set_client
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
        stream=True,
    )
    return response
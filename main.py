import requests

url = "http://www.pushplus.plus/send"
data = {
    "token": "你的Token",
    "title": "手机测试",
    "content": "这是一条手机网页端测试消息",
}
res = requests.post(url, json=data)
print(res.text)

import requests

token = "5758507929d44bf8b067c06781bcbe84"
url = "https://www.pushplus.plus/send"

payload = {
    "token": token,
    "title": "量化脚本连通性测试",
    "content": "如果你看到这条消息，说明你的 PushPlus Token 配置完全正确！",
    "template": "html"
}

headers = {
    "Content-Type": "application/json"
}

try:
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"状态码: {res.status_code}")
    print(f"返回内容: {res.text}")
except Exception as e:
    print(f"请求异常: {e}")

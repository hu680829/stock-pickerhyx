import requests

# 你的专属 SendKey 已经自动填入
send_key = "SCT400318Tb9hYe4hHbchclEqyRTV3o2wZ"
url = f"https://sctapi.ftqq.com/{send_key}.send"

# 消息的标题和内容
data = {
    "title": "股票选股通知",
    "desp": "选股脚本测试成功！微信通道已经打通。",
}

response = requests.post(url, data=data)
print("推送结果：", response.text)

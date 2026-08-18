import requests

# 将下面这行里的 URL 换成你的 Bark 链接
bark_url = (
    "https://api.day.app/eYYVUfX3NKDcU9j6FGPMon/股票选股通知/选股脚本运行成功！"
)

response = requests.get(bark_url)
print(response.text)

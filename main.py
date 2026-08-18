import requests

# 你的 Bark 专属链接
url = "https://api.day.app/eYYVUfX3NKDcU9j6FGPMon/股票通知测试/脚本正在运行中"

print("开始发送 Bark 通知...")

try:
  # 设置一个超时时间，防止请求卡死
  response = requests.get(url, timeout=10)
  print("请求状态码:", response.status_code)
  print("服务器返回内容:", response.text)
except Exception as e:
  print("发送请求时发生错误:", str(e))

import os
import time
import random
import datetime
import pytz
import yfinance as yf
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_warm_greeting():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now_hour = datetime.datetime.now(beijing_tz).hour
    if 5 <= now_hour < 12:
        return "☀️ 主人，早安！新的一天充满无限希望。", "🌸 祝您吉星高照，所念皆所愿！"
    elif 12 <= now_hour < 18:
        return "☕ 主人，下午好！忙碌了半天辛苦啦。", "💰 祝您财源滚滚，投资长虹！"
    elif 18 <= now_hour < 22:
        return "🌙 主人，晚上好！卸下一身疲惫，安享惬意时光。", "🍃 祝您平安喜乐，诸事顺遂！"
    else:
        return "✨ 主人，夜深了呢，晚安哦。", "🌟 祝您好梦连连！"

def run_stock_picker():
    # 你的专属 PushPlus Token
    PUSHPLUS_TOKEN = "5758507929d44bf8b067c06781bcbe84"
    
    time_greeting, chosen_blessing = generate_warm_greeting()
    
    # 简单生成一个测试报告内容
    content = f"""
    <div style="font-family: Arial, sans-serif; color: #2c3e50;">
        <div style="background: #fff5f5; border: 1px solid #ffe3e3; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
            <p style="font-size: 14px; color: #d9534f; font-weight: bold; margin: 0 0 4px 0;">{time_greeting}</p>
            <p style="font-size: 13px; color: #555; margin: 0;">{chosen_blessing}</p>
        </div>
        <h4 style="color:#5cb85c; margin-bottom:5px;">🟢 【测试推送成功】</h4>
        <p style="font-size: 13px;">如果你看到这条消息，说明你的 PushPlus 微信推送已经完全配置成功，成功摆脱了 Bark！</p>
        <div style="text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 15px;">✨ 祝您交易顺利，收益长虹！</div>
    </div>
    """
    
    print("正在通过 PushPlus 向微信发送测试报告...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": "🚀 量化报告通道测试",
        "content": content,
        "template": "html"
    }
    
    try:
        res = requests.post("https://www.pushplus.plus/send", json=payload, headers=headers, timeout=15)
        print(f"推送接口返回状态码: {res.status_code}")
        print(f"推送接口返回内容: {res.text}")
    except Exception as err:
        print(f"推送异常: {err}")

if __name__ == "__main__":
    run_stock_picker()

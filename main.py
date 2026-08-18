import yfinance as yf
import pandas as pd
import requests

def run_stock_picker():
    # 替换为你自己的 PushPlus Token
    PUSHPLUS_TOKEN = "5758507929d44bf8b067c06781bcbe84"
    
    # 选取部分热门/核心 A 股标的测试（美股/港股/A股均支持）
    # A股沪市加 .SS，深市加 .SZ，例如 600519.SS (贵州茅台)
    symbols = [
        "600519.SS", "000858.SZ", "601318.SS", "002594.SZ", 
        "300750.SZ", "600036.SS", "000001.SZ", "601899.SS"
    ]
    
    picked_list = []
    print("正在拉取行情...")
    
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            info = ticker.fast_info
            price = info.last_price
            prev_close = info.previous_close
            change_pct = ((price - prev_close) / prev_close) * 100
            
            # 选股策略示例：涨幅 > 1%
            if change_pct > 1.0:
                picked_list.append({
                    "代码": sym,
                    "最新价": round(price, 2),
                    "涨跌幅(%)": round(change_pct, 2)
                })
        except Exception as e:
            continue

    df_res = pd.DataFrame(picked_list)
    count = len(df_res)
    
    # 微信推送
    if PUSHPLUS_TOKEN and PUSHPLUS_TOKEN != "YOUR_PUSHPLUS_TOKEN":
        url = "http://www.pushplus.plus/send"
        title = f"📈 今日选股结果（共{count}只）"
        content = f"<h3>筛选结果：</h3>{df_res.to_html(index=False) if count > 0 else '<p>今日无符合条件股票</p>'}"
        
        payload = {
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content,
            "template": "html"
        }
        requests.post(url, json=payload)
        print("推送成功！")

if __name__ == "__main__":
    run_stock_picker()

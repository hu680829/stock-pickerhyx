import akshare as ak
import requests

def run_stock_picker():
    # 粘贴你的 PushPlus Token
    PUSHPLUS_TOKEN = "5758507929d44bf8b067c06781bcbe84"
    
    print("正在获取股票数据...")
    df = ak.stock_zh_a_spot_em()

    # 选股条件：涨幅 > 3% 且 动态市盈率在 0~30 之间 且 市净率 < 3
    picked = df[
        (df['涨跌幅'] > 3) & 
        (df['市盈率-动态'] > 0) & 
        (df['市盈率-动态'] < 30) &
        (df['市净率'] < 3)
    ]

    result = picked[['代码', '名称', '最新价', '涨跌幅', '市盈率-动态', '市净率']]
    count = len(result)

    # 微信推送
    if PUSHPLUS_TOKEN and PUSHPLUS_TOKEN != "你的Token":
        url = "http://www.pushplus.plus/send"
        title = f"📈 今日选股结果（共{count}只）"
        msg_table = result.head(15).to_html(index=False)
        content = f"<h3>筛选出以下股票：</h3>{msg_table}"

        payload = {
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content,
            "template": "html"
        }
        requests.post(url, json=payload)
        print("已发送至微信")

if __name__ == "__main__":
    run_stock_picker()

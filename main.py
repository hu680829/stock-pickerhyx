import os
import time
import random
import datetime
import pytz
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------------------------------------------------
# 🌟 0. 管家问候与精准北京时间
# ----------------------------------------------------------------------
def generate_warm_greeting():
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now_hour = datetime.datetime.now(beijing_tz).hour
    
    if 5 <= now_hour < 12:
        time_greeting = "☀️ 主人，早安！新的一天充满无限希望，愿阳光照亮您的每一个好心情。"
    elif 12 <= now_hour < 18:
        time_greeting = "☕ 主人，下午好！忙碌了半天辛苦啦，记得喝杯水小憩一下哦。"
    elif 18 <= now_hour < 22:
        time_greeting = "🌙 主人，晚上好！繁忙的一天渐入尾声，愿您能卸下一身的疲惫，安享惬意时光。"
    else:
        time_greeting = "✨ 主人，夜深了呢。愿清风为您扫去倦意，今夜好梦连连，晚安哦。"

    blessings = [
        "🌸 祝您吉星高照，所念皆所愿，所行皆坦途！",
        "💰 祝您财源滚滚，投资如红日东升，落袋皆是平稳与丰收！",
        "💫 祝您慧眼如炬，每一次抉择都冷静睿智，收获满满！",
        "📚 祝您博学笃行，逢考必过，付出的汗水终将绽放璀璨光芒！",
        "🍃 祝您平安喜乐，诸事顺遂，每天都有小确幸相伴左右！",
        "☀️ 祝您心想事成，步步生莲，生活与事业皆蒸蒸日上！",
        "🌟 祝您气运亨通，所求皆如愿，前路漫漫亦灿烂！"
    ]
    
    return time_greeting, random.choice(blessings)

# ----------------------------------------------------------------------
# 🌐 1. 传统宏观危险信号诊断
# ----------------------------------------------------------------------
def evaluate_macro_and_dangers():
    danger_signals = []
    
    try:
        tnx_hist = yf.Ticker("^TNX").history(period="10d")
        if not tnx_hist.empty and len(tnx_hist) >= 2:
            latest_tnx = float(tnx_hist['Close'].iloc[-1])
            prev_tnx = float(tnx_hist['Close'].iloc[-5]) if len(tnx_hist) >= 5 else float(tnx_hist['Close'].iloc[0])
            if pd.notna(latest_tnx) and pd.notna(prev_tnx):
                if latest_tnx > 4.3 or (latest_tnx - prev_tnx) > 0.15:
                    danger_signals.append(f"10年美债收益率居高({latest_tnx:.2f}%)，权益资产估值承压")
    except Exception:
        pass

    try:
        vix_hist = yf.Ticker("^VIX").history(period="5d")
        if not vix_hist.empty:
            latest_vix = float(vix_hist['Close'].iloc[-1])
            if pd.notna(latest_vix):
                if latest_vix > 24:
                    danger_signals.append(f"VIX恐慌指数飙升({latest_vix:.2f})，市场进入尾部恐慌")
                elif latest_vix < 12:
                    danger_signals.append(f"VIX处于极低位({latest_vix:.2f})，警惕市场过度狂热回调")
    except Exception:
        pass

    try:
        spx = yf.Ticker("^GSPC").history(period="60d")
        if not spx.empty and len(spx) >= 50:
            spx_close = float(spx['Close'].iloc[-1])
            spx_sma50 = float(spx['Close'].rolling(window=50).mean().iloc[-1])
            if pd.notna(spx_close) and pd.notna(spx_sma50) and spx_close < spx_sma50:
                danger_signals.append("标普500跌破50日生命线，美股大盘中线趋势转弱")
    except Exception:
        pass

    try:
        ssea = yf.Ticker("000001.SS").history(period="20d")
        if not ssea.empty:
            ssea_clean = ssea.dropna(subset=['Volume'])
            if len(ssea_clean) >= 5:
                latest_vol = float(ssea_clean['Volume'].iloc[-1])
                vol_ma20 = float(ssea_clean['Volume'].mean())
                if vol_ma20 > 0 and latest_vol < vol_ma20 * 0.7:
                    danger_signals.append("A股成交量严重萎缩(<20日均量70%)，存量博弈谨防流动性陷阱")
    except Exception:
        pass

    danger_count = len(danger_signals)
    if danger_count == 0:
        position_advice = "🟢 ✅ 环境极度安全：建议总仓位 8-10 成，积极执行买入策略"
    elif danger_count == 1:
        position_advice = "🟡 ⚠️ 1条预警：建议总仓位 6-7 成，控制新开仓比例"
    elif danger_count == 2:
        position_advice = "🟠 ⚠️ 2条预警：防守模式，建议总仓位降至 4-5 成，严禁追高"
    else:
        position_advice = f"🔴 🚨 极度危险({danger_count}条预警)：建议仓位降至 2 成以下或空仓观望！"

    return danger_count, danger_signals, position_advice

# ----------------------------------------------------------------------
# 🎯 2. 核心股票池与波动率分层
# ----------------------------------------------------------------------
def get_88_quality_pool():
    return {
        "美股·科技/半导体": [
            "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "AMD", "PLTR",
            "ASML", "TSM", "QCOM", "TXN", "MU", "INTC", "AMAT", "LRCX", "SMCI", "ARM"
        ],
        "美股·消费/医药/金融": [
            "LLY", "NVO", "UNH", "JNJ", "PG", "KO", "PEP", "COST", "WMT",
            "MCD", "JPM", "BAC", "MS", "GS", "V", "MA", "CAT", "GE", "XOM"
        ],
        "美股·核心中概股": [
            "BABA", "PDD", "JD", "BIDU", "NTES", "NIO", "XPEV", "LI"
        ],
        "A股·行业龙头资产": [
            "600519.SS", "000858.SZ", "600809.SS", "000333.SZ", "000651.SZ", "600887.SS",
            "300750.SZ", "002594.SZ", "601899.SS", "600438.SS", "601689.SS", "600111.SS",
            "601318.SS", "600036.SS", "601166.SS", "600028.SS", "601857.SS", "600900.SS"
        ]
    }

def get_atr_multipliers(category, symbol):
    high_vol_symbols = {"NVDA", "TSLA", "AMD", "PLTR", "SMCI", "ARM", "NIO", "XPEV", "LI", "300750.SZ"}
    low_vol_symbols = {"KO", "PG", "JNJ", "PEP", "COST", "WMT", "JPM", "BAC", "600519.SS", "601398.SS", "600036.SS"}
    
    if symbol in high_vol_symbols or "科技" in category or "中概" in category:
        return 2.5, 2.0, "高波动层"
    elif symbol in low_vol_symbols or "消费" in category or "金融" in category:
        return 1.5, 1.2, "低波动层"
    else:
        return 2.0, 1.5, "标准层"

def check_tail_market(symbol):
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now_beijing = datetime.datetime.now(beijing_tz)
    if now_beijing.weekday() >= 5:
        return False
    beijing_hour = now_beijing.hour
    if symbol.endswith(".SS") or symbol.endswith(".SZ"):
        return 14 <= beijing_hour < 15
    us_eastern_tz = pytz.timezone('US/Eastern')
    now_us_eastern = datetime.datetime.now(us_eastern_tz)
    return now_us_eastern.hour == 15

def check_vcp_pattern(df):
    if len(df) < 30:
        return False, 1.0
    try:
        range_first = (df['High'].iloc[-30:-15].max() - df['Low'].iloc[-30:-15].min()) / df['Close'].iloc[-15]
        range_second = (df['High'].iloc[-15:-1].max() - df['Low'].iloc[-15:-1].min()) / df['Close'].iloc[-1]
        if pd.notna(range_first) and pd.notna(range_second) and range_first > 0:
            return range_second < (range_first * 0.75), float(range_second)
    except Exception:
        pass
    return False, 1.0

# ----------------------------------------------------------------------
# 🔬 3. 单股分析核心引擎
# ----------------------------------------------------------------------
def analyze_single_stock(item):
    symbol, category = item
    time.sleep(random.uniform(0.05, 0.15))
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="120d")
        if df.empty or len(df) < 50:
            return None
        df = df.dropna(subset=['Close', 'High', 'Low', 'Volume'])
        if len(df) < 50:
            return None
            
        current_price = float(df['Close'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2])
        if prev_close == 0:
            return None
        daily_change = ((current_price - prev_close) / prev_close) * 100
        
        sma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
        sma50 = float(df['Close'].rolling(window=50).mean().iloc[-1])
        high_20d = float(df['High'].iloc[-21:-1].max())
        low_20d = float(df['Low'].iloc[-21:-1].min())
        high_60d = float(df['High'].iloc[-61:-1].max()) if len(df) >= 61 else high_20d

        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean().fillna(0)
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean().fillna(0)
        rs = gain / loss.replace(0, 0.00001)
        rsi14 = float((100 - (100 / (1 + rs))).iloc[-1])
        
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift()).abs()
        low_close = (df['Low'] - df['Close'].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr14 = float(tr.rolling(14).mean().iloc[-1])
        if pd.isna(atr14) or atr14 == 0:
            atr14 = current_price * 0.02
        
        breakout_mult, pullback_mult, tier_tag = get_atr_multipliers(category, symbol)
        raw_vol = float(df['Volume'].iloc[-1]) if pd.notna(df['Volume'].iloc[-1]) else 0.0
        vol_ma20 = float(df['Volume'].rolling(window=20).mean().iloc[-1])
        volume_ratio = (raw_vol / vol_ma20) if (pd.notna(vol_ma20) and vol_ma20 > 0) else 1.0

        is_vcp, vcp_volatility = check_vcp_pattern(df)
        price_60d_ago = float(df['Close'].iloc[-60]) if len(df) >= 60 else float(df['Close'].iloc[0])
        stock_60d_return = ((current_price - price_60d_ago) / price_60d_ago) * 100 if price_60d_ago > 0 else 0.0

        tech_buy_breakout = (current_price > sma20 and sma20 > sma50 and current_price >= high_20d and volume_ratio >= 1.25 and rsi14 < 80)
        tech_buy_pullback = (current_price < sma20 and current_price > sma50 and daily_change > 0.5 and rsi14 < 48 and is_vcp)

        stop_loss_dist = breakout_mult * atr14
        target_reward_dist = max((high_60d * 1.08 - current_price), 2.5 * stop_loss_dist)
        risk_reward_ratio = (target_reward_dist / stop_loss_dist) if stop_loss_dist > 0 else 0.0

        dynamic_stop_line = current_price - breakout_mult * atr14
        tech_sell = (current_price < sma20 and (current_price < sma50 or daily_change < -3.5 or current_price < dynamic_stop_line))

        signal, strategy_tag, reason, target_price_info = None, "", "", ""
        if tech_buy_breakout and risk_reward_ratio >= 2.0:
            signal = "🎯 建议买入"
            strategy_tag = f"突破策略 [{tier_tag}]"
            stop_price = round(max(current_price - stop_loss_dist, sma20 * 0.98), 2)
            target_price_info = f"<b>突破入场价:</b> ≥{round(high_20d, 2)} | <b>止损价:</b> {stop_price}"
            reason = f"突破20日高点 + 放量({volume_ratio:.1f}倍) + 趋势向上"
        elif tech_buy_pullback and risk_reward_ratio >= 1.8:
            signal = "🎯 建议买入"
            strategy_tag = f"VCP低吸 [{tier_tag}]"
            stop_price = round(current_price - pullback_mult * atr14, 2)
            target_price_info = f"<b>低吸参考价:</b> {round(current_price, 2)} | <b>止损价:</b> {stop_price}"
            reason = f"VCP形态收窄(振幅{vcp_volatility*100:.1f}%)，支撑位企稳"

        if tech_sell:
            signal = "⚠️ 建议卖出"
            strategy_tag = f"破位防守 [{tier_tag}]"
            target_price_info = f"<b>触发破位价:</b> {round(current_price, 2)} | <b>硬支撑:</b> {round(sma50, 2)}"
            reason = f"跌破关键均线或触发动态止损线 (跌幅: {daily_change:.2f}%)"

        return {
            "分类": category, "代码": symbol, "最新价": round(current_price, 2),
            "当日涨跌": f"{daily_change:+.2f}%", "信号": signal if signal else "☕ 观望中",
            "策略": strategy_tag if strategy_tag else f"跟踪 [{tier_tag}]",
            "价格指引": target_price_info if target_price_info else f"<b>SMA20:</b> {round(sma20,2)} | <b>RSI:</b> {round(rsi14,1)}",
            "原因": reason if reason else f"常规波动追踪 (RSI: {rsi14:.1f})"
        }
    except Exception:
        return None

# ----------------------------------------------------------------------
# 🚀 4. 主程序与 PushPlus 微信推送
# ----------------------------------------------------------------------
def run_stock_picker():
    # 直接硬编码您的 PushPlus Token
    PUSHPLUS_TOKEN = "5758507929d44bf8b067c06781bcbe84"
    
    time_greeting, chosen_blessing = generate_warm_greeting()
    danger_count, danger_signals, position_advice = evaluate_macro_and_dangers()
    
    pools = get_88_quality_pool()
    tasks = [(sym, cat) for cat, symbols in pools.items() for sym in symbols]
    
    results = []
    print(f"正在扫描 {len(tasks)} 只核心资产...")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(analyze_single_stock, t) for t in tasks]
        for f in as_completed(futures):
            res = f.result()
            if res: results.append(res)

    buy_items = [r for r in results if "买入" in r["信号"]]
    sell_items = [r for r in results if "卖出" in r["信号"]]

    if not buy_items and results:
        buy_items = sorted(results, key=lambda x: abs(float(x['当日涨跌'].replace('%','').replace('+',''))), reverse=True)[:3]
        for item in buy_items:
            item['信号'] = "📌 全景观察"
            item['策略'] = "严守纪律防守"

    def build_cards(item_list, color_code):
        if not item_list: return "<p style='color:#888;font-size:13px;'>今日无符合条件的标的</p>"
        html = ""
        for item in item_list:
            html += f"""
            <div style="border-left:4px solid {color_code}; background:#f9f9f9; padding:10px; margin-bottom:10px; border-radius:4px;">
                <div style="font-weight:bold; font-size:15px;">{item['代码']} <span style="font-size:12px; color:#666;">({item['分类']})</span></div>
                <div style="margin-top:4px; font-size:13px;"><b>现价:</b> {item['最新价']} | <b>涨跌:</b> <span style="color:{'#d9534f' if '-' in item['当日涨跌'] else '#5cb85c'}">{item['当日涨跌']}</span></div>
                <div style="margin-top:4px; font-size:13px; color:{color_code};"><b>[{item['信号']}]</b> {item['策略']}</div>
                <div style="margin-top:4px; font-size:12px; background:#fff; padding:6px; border-radius:3px; border:1px solid #eee;">📍 {item['价格指引']}</div>
                <div style="margin-top:4px; font-size:11px; color:#555;"><b>触发原因:</b> {item['原因']}</div>
            </div>
            """
        return html

    danger_html = "".join([f"<li style='color:#d9534f;margin-bottom:3px;'>⚠️ {s}</li>" for s in danger_signals]) if danger_signals else "<li style='color:#5cb85c;'>✅ 传统宏观风险指标正常</li>"

    content = f"""
    <div style="font-family: Arial, sans-serif; color: #2c3e50;">
        <div style="background: #fff5f5; border: 1px solid #ffe3e3; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
            <p style="font-size: 14px; color: #d9534f; font-weight: bold; margin: 0 0 4px 0;">{time_greeting}</p>
            <p style="font-size: 13px; color: #555; margin: 0;">{chosen_blessing}</p>
        </div>
        <h4 style="color:#333; margin-bottom:5px;">🌐 【宏观综合风控雷达】</h4>
        <p style="font-size:13px; font-weight:bold; margin-top:0;">{position_advice}</p>
        <ul style="padding-left:16px; font-size:12px; margin-bottom:10px;">{danger_html}</ul>
        <hr style="border:none; border-top:1px dashed #ccc; margin:10px 0;"/>
        <h4 style="color:#5cb85c; margin-bottom:5px;">🟢 【买入/精选标的】</h4>
        {build_cards(buy_items, '#5cb85c')}
        <hr style="border:none; border-top:1px dashed #ccc; margin:15px 0;"/>
        <h4 style="color:#d9534f; margin-bottom:5px;">🔴 【卖出/风控标的】</h4>
        {build_cards(sell_items, '#d9534f')}
        <div style="text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 15px;">✨ 祝您交易顺利，收益长虹！</div>
    </div>
    """
    
    if PUSHPLUS_TOKEN:
        try:
            print("正在通过 PushPlus 向微信发送量化报告...")
            headers = {"Content-Type": "application/json"}
            payload = {
                "token": PUSHPLUS_TOKEN,
                "title": f"🚀 量化报告 (综合风险指数:{danger_count})",
                "content": content,
                "template": "html"
            }
            res = requests.post("https://www.pushplus.plus/send", json=payload, headers=headers, timeout=15)
            print(f"推送接口返回状态码: {res.status_code}")
            print(f"推送接口返回内容: {res.text}")
        except Exception as err:
            print(f"推送异常: {err}")

if __name__ == "__main__":
    run_stock_picker()

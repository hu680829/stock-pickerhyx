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
# 🌐 1. 传统宏观危险信号诊断 (索罗斯反射性理论)
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

    try:
        soxx = yf.Ticker("SOXX").history(period="30d")
        if not soxx.empty and len(soxx) >= 20:
            soxx_close = float(soxx['Close'].iloc[-1])
            soxx_sma20 = float(soxx['Close'].rolling(window=20).mean().iloc[-1])
            soxx_change = ((soxx_close - float(soxx['Close'].iloc[-2])) / float(soxx['Close'].iloc[-2])) * 100
            if pd.notna(soxx_close) and pd.notna(soxx_sma20):
                if soxx_close < soxx_sma20 or soxx_change < -2.5:
                    danger_signals.append(f"半导体领涨指数SOXX破位/大跌({soxx_change:.2f}%)，科技龙头遭抛售")
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
# 🕶️ 1.1 币圈暗盘、链上与场外情绪监测模块
# ----------------------------------------------------------------------
def evaluate_crypto_dark_pool_sentiment():
    crypto_notes = []
    dark_score_adjustment = 0 
    
    try:
        url = "https://api.coingecko.com/api/v3/global"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json().get("data", {})
            btc_dominance = data.get("market_cap_percentage", {}).get("btc", 0)
            eth_dominance = data.get("market_cap_percentage", {}).get("eth", 0)
            market_cap_change = data.get("market_cap_change_percentage_24h_usd", 0)
            
            crypto_notes.append(f"加密全网24h市值变动: <b>{market_cap_change:+.2f}%</b>")
            crypto_notes.append(f"BTC市占率: <b>{btc_dominance:.1f}%</b> | ETH市占率: <b>{eth_dominance:.1f}%</b>")
            
            if market_cap_change > 3.5:
                crypto_notes.append("💡 <b>暗盘暗流涌动:</b> 链上资金净流入，加密投机活跃，利好高风险科技资产。")
            elif market_cap_change < -4.0:
                crypto_notes.append("⚠️ <b>暗盘资金撤离:</b> 加密总市值大幅缩水，场外避险可能传导至传统股市。")
                dark_score_adjustment += 1
    except Exception:
        crypto_notes.append("🌐 币圈暗盘API接口暂时限流，启用离线风险对冲预案。")

    try:
        btc_hist = yf.Ticker("BTC-USD").history(period="5d")
        if not btc_hist.empty and len(btc_hist) >= 2:
            btc_price = float(btc_hist['Close'].iloc[-1])
            btc_change = ((btc_price - float(btc_hist['Close'].iloc[-2])) / float(btc_hist['Close'].iloc[-2])) * 100
            crypto_notes.append(f"比特币(BTC)现货暗盘价: <b>${btc_price:,.0f}</b> ({btc_change:+.2f}%)")
            
            if btc_change < -5.0:
                crypto_notes.append("🚨 <b>高危警报:</b> BTC单日暴跌超5%，预示流动性危机或大户砸盘，严禁激进做多！")
                dark_score_adjustment += 2
    except Exception:
        pass

    return crypto_notes, dark_score_adjustment

# ----------------------------------------------------------------------
# 🎯 2. 核心股票池与波动率分层
# ----------------------------------------------------------------------
def get_88_quality_pool():
    return {
        "美股·科技/半导体": [
            "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "AMD", "PLTR",
            "ASML", "TSM", "QCOM", "TXN", "MU", "INTC", "AMAT", "LRCX", "SMCI", "ARM", "PANW", "CRWD"
        ],
        "美股·消费/医药/金融": [
            "LLY", "NVO", "UNH", "JNJ", "PFE", "PG", "KO", "PEP", "COST", "WMT",
            "MCD", "JPM", "BAC", "MS", "GS", "V", "MA", "CAT", "GE", "XOM"
        ],
        "美股·核心中概股": [
            "BABA", "PDD", "JD", "BIDU", "NTES", "TME", "NIO", "XPEV", "LI", "BILI"
        ],
        "A股·行业龙头资产": [
            "600519.SS", "000858.SZ", "600809.SS", "000568.SZ", "000333.SZ", "000651.SZ", "603288.SS", "600887.SS",
            "300750.SZ", "002594.SZ", "601899.SS", "600438.SS", "601689.SS", "600111.SS", "002460.SZ", "603799.SS",
            "002415.SZ", "600276.SS", "300122.SZ", "603501.SS", "002371.SZ", "002230.SZ", "688012.SS", "688981.SS",
            "601318.SS", "600036.SS", "601166.SS", "600028.SS", "601857.SS", "600900.SS", "601398.SS", "601288.SS",
            "600000.SS", "000001.SZ", "601601.SS", "601211.SS"
        ]
    }

def get_atr_multipliers(category, symbol):
    high_vol_symbols = {
        "NVDA", "TSLA", "AMD", "PLTR", "SMCI", "ARM", "CRWD", "PANW",
        "NIO", "XPEV", "LI", "BILI", "300750.SZ", "688981.SS", "688012.SS"
    }
    low_vol_symbols = {
        "KO", "PG", "JNJ", "PFE", "PEP", "COST", "WMT", "JPM", "BAC", "MCD",
        "600519.SS", "000858.SZ", "601398.SS", "600036.SS", "601318.SS", "600900.SS", "600887.SS"
    }
    
    if symbol in high_vol_symbols or "科技" in category or "中概" in category:
        return 2.5, 2.0, "高波动层"
    elif symbol in low_vol_symbols or "消费" in category or "金融" in category:
        return 1.5, 1.2, "低波动层"
    else:
        return 2.0, 1.5, "标准层"

# ----------------------------------------------------------------------
# ⏰ 3. 跨时区与尾盘精确判定
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# 🔬 4. 米奈尔维尼 VCP 形态判定
# ----------------------------------------------------------------------
def check_vcp_pattern(df):
    if len(df) < 30:
        return False, 1.0
    try:
        range_first = (df['High'].iloc[-30:-15].max() - df['Low'].iloc[-30:-15].min()) / df['Close'].iloc[-15]
        range_second = (df['High'].iloc[-15:-1].max() - df['Low'].iloc[-15:-1].min()) / df['Close'].iloc[-1]
        
        if pd.notna(range_first) and pd.notna(range_second) and range_first > 0:
            is_vcp = range_second < (range_first * 0.75)
            return is_vcp, float(range_second)
    except Exception:
        pass
    return False, 1.0

# ----------------------------------------------------------------------
# 🧠 5. 7 大大师逻辑全量融合单股分析引擎
# ----------------------------------------------------------------------
def analyze_single_stock(item):
    symbol, category = item
    time.sleep(random.uniform(0.05, 0.2))
    
    try:
        ticker = yf.Ticker(symbol)
        df = pd.DataFrame()
        for _ in range(2):
            try:
                df = ticker.history(period="120d")
                if not df.empty:
                    break
            except Exception:
                time.sleep(0.5)
        
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
        
        sma20_series = df['Close'].rolling(window=20).mean()
        sma50_series = df['Close'].rolling(window=50).mean()
        sma20 = float(sma20_series.iloc[-1])
        sma50 = float(sma50_series.iloc[-1])
        
        high_20d = float(df['High'].iloc[-21:-1].max())
        low_20d = float(df['Low'].iloc[-21:-1].min())
        high_60d = float(df['High'].iloc[-61:-1].max()) if len(df) >= 61 else high_20d
        
        if pd.isna(high_20d) or high_20d == 0:
            high_20d = current_price
        if pd.isna(low_20d) or low_20d == 0:
            low_20d = current_price
        if pd.isna(high_60d) or high_60d == 0:
            high_60d = high_20d

        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean().fillna(0)
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean().fillna(0)
        loss_safe = loss.replace(0, 0.00001)
        rs = gain / loss_safe
        rsi14 = float((100 - (100 / (1 + rs))).iloc[-1])
        if pd.isna(rsi14):
            rsi14 = 50.0
        
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift()).abs()
        low_close = (df['Low'] - df['Close'].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr14 = float(tr.rolling(14).mean().iloc[-1])
        if pd.isna(atr14) or atr14 == 0:
            atr14 = current_price * 0.02
        
        breakout_mult, pullback_mult, tier_tag = get_atr_multipliers(category, symbol)

        beijing_tz = pytz.timezone('Asia/Shanghai')
        now_beijing = datetime.datetime.now(beijing_tz)
        raw_vol = float(df['Volume'].iloc[-1]) if pd.notna(df['Volume'].iloc[-1]) else 0.0
        is_tail = check_tail_market(symbol)
        
        if is_tail:
            if symbol.endswith(".SS") or symbol.endswith(".SZ"):
                passed_minutes = 180 + now_beijing.minute
                passed_minutes = min(max(passed_minutes, 180), 239)
                vol_factor = min(240.0 / float(passed_minutes), 1.8)
            else:
                vol_factor = 1.08
            est_vol = raw_vol * vol_factor
        else:
            est_vol = raw_vol
            
        vol_ma20 = float(df['Volume'].rolling(window=20).mean().iloc[-1])
        volume_ratio = (est_vol / vol_ma20) if (pd.notna(vol_ma20) and vol_ma20 > 0) else 1.0

        is_vcp, vcp_volatility = check_vcp_pattern(df)

        price_60d_ago = float(df['Close'].iloc[-60]) if len(df) >= 60 else float(df['Close'].iloc[0])
        stock_60d_return = ((current_price - price_60d_ago) / price_60d_ago) * 100 if price_60d_ago > 0 else 0.0

        pe_ratio = None
        try:
            fast_pe = getattr(ticker, 'fast_info', {}).get('trailing_pe', None)
            if fast_pe is not None and isinstance(fast_pe, (int, float)) and not pd.isna(fast_pe):
                pe_ratio = float(fast_pe)
            else:
                info = ticker.info
                if isinstance(info, dict):
                    raw_pe = info.get('trailingPE', None)
                    if isinstance(raw_pe, (int, float)) and not pd.isna(raw_pe) and raw_pe > 0:
                        pe_ratio = float(raw_pe)
        except Exception:
            pe_ratio = None

        is_pe_safe = True
        if pe_ratio is not None:
            if "金融" in category and pe_ratio > 18:
                is_pe_safe = False
            elif "消费" in category and pe_ratio > 45:
                is_pe_safe = False
            elif pe_ratio > 85:
                is_pe_safe = False

        tech_buy_breakout = (
            current_price > sma20 and sma20 > sma50 and
            current_price >= high_20d and
            volume_ratio >= 1.25 and
            rsi14 < 80 and stock_60d_return > -5.0
        )

        tech_buy_pullback = (
            current_price < sma20 and current_price > sma50 and
            daily_change > 0.8 and current_price <= low_20d * 1.04 and
            rsi14 < 48 and is_vcp
        )

        stop_loss_dist = breakout_mult * atr14
        target_reward_dist = max((high_60d * 1.08 - current_price), 2.5 * stop_loss_dist)
        risk_reward_ratio = (target_reward_dist / stop_loss_dist) if stop_loss_dist > 0 else 0.0

        dynamic_stop_line = current_price - breakout_mult * atr14
        below_sma20_3d = (df['Close'].iloc[-3:] < sma20_series.iloc[-3:]).all() if len(df) >= 3 else False
        recent_high_20d = float(df['High'].iloc[-20:].max()) if len(df) >= 20 else current_price
        
        if pd.isna(recent_high_20d) or recent_high_20d == 0:
            recent_high_20d = current_price
            
        pullback_from_high = ((recent_high_20d - current_price) / recent_high_20d) if recent_high_20d > 0 else 0.0

        tech_sell = (
            current_price < sma20 and 
            (current_price < sma50 or daily_change < -3.5 or current_price < dynamic_stop_line or (below_sma20_3d and rsi14 < 40))
        )
        tech_take_profit = (current_price >= sma20 and pullback_from_high > 0.07 and rsi14 < 60 and recent_high_20d > sma50 * 1.12)

        signal, strategy_tag, reason = None, "", ""
        target_price_info = ""

        risk_pct_per_share = (stop_loss_dist / current_price) * 100 if current_price > 0 else 5.0
        max_position_size_pct = round(min(1.5 / (risk_pct_per_share / 100), 25.0), 1)

        if tech_buy_breakout and is_pe_safe and risk_reward_ratio >= 2.5:
            signal = "🎯 建议买入"
            strategy_tag = f"大师级突破 [{tier_tag}]"
            vcp_str = " (含VCP收窄)" if is_vcp else ""
            stop_price = round(max(current_price - stop_loss_dist, sma20 * 0.985), 2)
            target_price_info = (
                f"<b>突破入场价:</b> ≥{round(high_20d, 2)} | <b>止损价:</b> {stop_price} | "
                f"<b>盈亏比:</b> {risk_reward_ratio:.1f}:1 | <b>建议建仓上限:</b> {max_position_size_pct}%"
            )
            reason = f"利弗莫尔突破20日高点 + 欧奈尔放量({volume_ratio:.1f}倍) + SEPA趋势排列{vcp_str}"

        elif tech_buy_pullback and is_pe_safe and risk_reward_ratio >= 2.0:
            signal = "🎯 建议买入"
            strategy_tag = f"VCP缩量企稳低吸 [{tier_tag}]"
            stop_price = round(current_price - pullback_mult * atr14, 2)
            target_price_info = (
                f"<b>低吸参考价:</b> {round(current_price, 2)} | <b>止损价:</b> {stop_price} | "
                f"<b>盈亏比:</b> {risk_reward_ratio:.1f}:1 | <b>建议建仓上限:</b> {max_position_size_pct}%"
            )
            reason = f"米奈尔维尼VCP形态收窄(最新振幅{vcp_volatility*100:.1f}%)，于支撑位止跌反弹"

        if tech_sell:
            signal = "⚠️ 建议卖出"
            strategy_tag = f"破位无条件防守 [{tier_tag}]"
            target_price_info = f"<b>触发破位价:</b> {round(current_price, 2)} | <b>硬支撑线:</b> {round(sma50, 2)}"
            reason = f"跌破20日线/50日线或触发 {breakout_mult}xATR 动态止损线 (日跌幅: {daily_change:.2f}%)"
        elif tech_take_profit:
            signal = "💰 建议止盈/减仓"
            strategy_tag = f"高位锁盈保护 [{tier_tag}]"
            target_price_info = f"<b>锁盈卖出价:</b> {round(current_price, 2)} | <b>近20日最高:</b> {round(recent_high_20d, 2)}"
            reason = f"自高点回撤 {pullback_from_high*100:.1f}%，锁盈离场，遵守交易纪律"

        pe_str = f"{pe_ratio:.1f}" if pe_ratio is not None else "N/A"
        
        return {
            "分类": category,
            "代码": symbol,
            "最新价": round(current_price, 2),
            "当日涨跌": f"{daily_change:+.2f}%",
            "PE": pe_str,
            "信号": signal if signal else "☕ 观望/蓄势中",
            "策略": strategy_tag if strategy_tag else f"基础跟踪 [{tier_tag}]",
            "价格指引": target_price_info if target_price_info else f"<b>当前均线:</b> SMA20={round(sma20,2)} | RSI={round(rsi14,1)}",
            "原因": reason if reason else f"暂未触发严苛大师买卖点，目前维持正常波动跟踪 (RSI: {rsi14:.1f})"
        }
    except Exception:
        return None

# ----------------------------------------------------------------------
# 🚀 6. 主程序运行与 PushPlus 终极防爆推送 (含暗盘监控与防空洞暖心播报)
# ----------------------------------------------------------------------
def run_stock_picker():
    PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "YOUR_PUSHPLUS_TOKEN")
    
    time_greeting, chosen_blessing = generate_warm_greeting()
    danger_count, danger_signals, position_advice = evaluate_macro_and_dangers()
    
    crypto_notes, dark_adj = evaluate_crypto_dark_pool_sentiment()
    danger_count += dark_adj 
    
    pools = get_88_quality_pool()
    tasks = []
    for cat, symbols in pools.items():
        for sym in symbols:
            tasks.append((sym, cat))

    results = []
    print(f"正在为您扫描 {len(tasks)} 只核心资产 (融合 7 大大师算法 + 币圈暗盘监控)...")
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(analyze_single_stock, task) for task in tasks]
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    buy_items = [r for r in results if "买入" in r["信号"]]
    sell_items = [r for r in results if "卖出" in r["信号"] or "止盈" in r["信号"]]

    if not buy_items and results:
        def parse_chg(item):
            try:
                return abs(float(item['当日涨跌'].replace('%', '').replace('+', '')))
            except:
                return 0.0
        sorted_res = sorted(results, key=parse_chg, reverse=True)
        buy_items = sorted_res[:3]
        for item in buy_items:
            item['信号'] = "📌 今日全景观察 (无强买点)"
            item['策略'] = "严格风控防守中"

    def build_cards(item_list, color_code):
        if not item_list:
            return "<p style='color:#888;font-size:13px;'>今日市场平静，无符合大师级过滤标准的标的</p>"
        html = ""
        for item in item_list:
            html += f"""
            <div style="border-left:4px solid {color_code}; background:#f9f9f9; padding:10px; margin-bottom:10px; border-radius:4px;">
                <div style="font-weight:bold; font-size:15px;">{item['代码']} <span style="font-size:12px; color:#666;">({item['分类']})</span></div>
                <div style="margin-top:4px; font-size:13px;"><b>现价:</b> {item['最新价']} | <b>涨跌:</b> <span style="color:{'#d9534f' if '-' in item['当日涨跌'] else '#5cb85c'}">{item['当日涨跌']}</span> | <b>PE:</b> {item['PE']}</div>
                <div style="margin-top:4px; font-size:13px; color:{color_code};"><b>[{item['信号']}]</b> {item['策略']}</div>
                <div style="margin-top:4px; font-size:12px; background:#fff; padding:6px; border-radius:3px; border:1px solid #eee;">📍 {item['价格指引']}</div>
                <div style="margin-top:4px; font-size:11px; color:#555;"><b>大师法则触发:</b> {item['原因']}</div>
            </div>
            """
        return html

    danger_html = "".join([f"<li style='color:#d9534f;margin-bottom:3px;'>⚠️ {s}</li>" for s in danger_signals]) if danger_signals else "<li style='color:#5cb85c;'>✅ 传统宏观5大危险信号全清</li>"
    crypto_html = "".join([f"<li style='color:#f0ad4e;margin-bottom:3px;'>🕶️ {n}</li>" for n in crypto_notes])

    content = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #2c3e50;">
        <div style="background: #fff5f5; border: 1px solid #ffe3e3; padding: 12px; border-radius: 6px; margin-bottom: 15px;">
            <p style="font-size: 14px; color: #d9534f; font-weight: bold; margin: 0 0 4px 0;">{time_greeting}</p>
            <p style="font-size: 13px; color: #555; margin: 0;">{chosen_blessing}</p>
        </div>

        <h4 style="color:#333; margin-bottom:5px;">🌐 【宏观反射性 & 综合风控雷达】</h4>
        <p style="font-size:13px; font-weight:bold; margin-top:0;">{position_advice}</p>
        <ul style="padding-left:16px; font-size:12px; margin-bottom:5px;">{danger_html}</ul>
        <ul style="padding-left:16px; font-size:12px; margin-bottom:10px; background:#fcf8e3; padding:8px; border-radius:4px;">{crypto_html}</ul>
        <hr style="border:none; border-top:1px dashed #ccc; margin:10px 0;"/>
        
        <h4 style="color:#5cb85c; margin-bottom:5px;">🟢 【大师级买入标的 / 市场全景精选】</h4>
        {build_cards(buy_items, '#5cb85c')}
        <hr style="border:none; border-top:1px dashed #ccc; margin:15px 0;"/>
        
        <h4 style="color:#d9534f; margin-bottom:5px;">🔴 【大师级卖出/止损/止盈标的 & 破位参考】</h4>
        {build_cards(sell_items, '#d9534f')}
        
        <hr style="border:none; border-top:1px solid #eaeaea; margin:20px 0 10px 0;"/>
        <div style="text-align: center; color: #7f8c8d; font-size: 13px; line-height: 1.6; padding: 10px 0;">
            ✨ 祝您今天交易顺利，收益长虹！<br/>
            <span style="font-size: 11px; color: #bdc3c7;">（7大师精粹合一 + 币圈链上暗盘洞察）</span>
        </div>
    </div>
    """
    
    if PUSHPLUS_TOKEN and PUSHPLUS_TOKEN != "YOUR_PUSHPLUS_TOKEN":
        try:
            print("正在通过安全通道向微信发送量化报告...")
            # 已更新为官方推荐的 HTTPS 加密接口
            res = requests.post("https://www.pushplus.plus/send", json={
                "token": PUSHPLUS_TOKEN,
                "title": f"🚀 量化报告与全景监控 (综合风险指数:{danger_count})",
                "content": content,
                "template": "html"
            }, timeout=15)
            
            print(f"推送接口返回状态码: {res.status_code}")
            print(f"推送接口返回内容: {res.text}")
            
            if res.status_code == 200:
                print("微信推送成功发送！")
            else:
                print("⚠️ 提醒：推送接口返回非200状态码，请检查Token是否正确。")
        except Exception as err:
            print(f"推送服务网络超时/异常: {err}")
    else:
        print("⚠️ 未检测到有效的 PUSHPLUS_TOKEN，跳过微信推送步骤。")

if __name__ == "__main__":
    run_stock_picker()

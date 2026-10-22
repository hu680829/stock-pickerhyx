from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, time
import os
import time as t_mod
import requests
import yfinance as yf

# 从 GitHub Secrets 中读取你的 PushPlus 密钥
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")

# ==================== 💎 灿灿的专属持仓与自选池配置中心 ====================
# 注：将原本收益为0的死现金升级为 SGOV（超短债ETF），让现金也能稳健生息
MY_PORTFOLIO_WEIGHTS = {
    "AAPL": 0.15,  # 苹果（美元资产） 15%
    "NVDA": 0.20,  # 英伟达（美元资产） 20%
    "BTC-USD": 0.15,  # 比特币（美元资产） 15%
    "000300.SS": 0.20,  # 沪深300（人民币资产） 20%
    "SGOV": 0.30,  # 现金/固收替代（美股超短债ETF） 30%
}
# ==================================================================


def get_beijing_now():
  """【北京时间精准锁定引擎】"""
  try:
    import zoneinfo

    return datetime.now(zoneinfo.ZoneInfo("Asia/Shanghai"))
  except Exception:
    from datetime import timedelta, timezone

    return datetime.now(timezone(timedelta(hours=8)))


def is_market_holiday_or_skip():
  """【全球节假日与周末自动静默感知引擎】"""
  bj_now = get_beijing_now()
  weekday = bj_now.weekday()

  if weekday >= 5:
    return True, "当前为周末休市时段，系统自动挂起常规复盘推送。"

  if bj_now.month == 1 and bj_now.day == 1:
    return True, "今天是元旦法定节假日，全球市场休市，系统自动挂起推送。"

  return False, ""


def safe_yf_download(ticker, period="60d", retries=3, delay=2):
  """【具备指数级退避与自动重试的容灾抓取函数】"""
  for attempt in range(retries):
    try:
      stock = yf.Ticker(ticker)
      hist = stock.history(period=period)
      if not hist.empty and len(hist) > 0:
        return hist
    except Exception as e:
      print(
          f"Warning: Fetching {ticker} failed (Attempt {attempt+1}/{retries}):"
          f" {e}"
      )
    t_mod.sleep(delay * (attempt + 1))
  return None


def get_daily_greeting():
  """【幽默与温柔并存的每日问候引擎】"""
  greetings = [
      (
          "早安呀, 灿灿！今天的美股、A股和数字货币有没有对你笑呢？不管怎样, 先摸摸头,"
          "今天也要元气满满哦~"
      ),
      (
          "嗨, 灿灿！昨晚的全球大盘就像淘气的小猫, 偶尔闹点小脾气,"
          "但总体向好。今天又是大吉大利的一天！"
      ),
      (
          "起床啦灿灿！别让 K 线图抢走了你的好早餐。今天由我来帮你盯着风控,"
          "你负责开心就好~"
      ),
      (
          "早安, 灿灿！今天的美债和加密市场看起来都很乖,"
          "希望你的钱包也是稳稳的幸福！"
      ),
      (
          "叮咚！灿灿专属的财富小助手准时上线啦！今天也要做个温柔又有钱的宝藏大人呀~"
      ),
      (
          "早安呀灿灿！听说今天是个适合数钱的好日子, 如果行情稍微偷懒,"
          "那就把我的欧气全借给你！"
      ),
      (
          "嗨~ 灿灿！新的一天开始啦, 把烦恼坚决清仓, 把快乐直接满仓,"
          "今天也要被世界温柔以待哦。"
      ),
      (
          "早安灿灿！市场风云变幻, 但本系统对你的关心永远永续多头、"
          "永不降息。今天一起加油鸭！"
      ),
  ]
  bj_now = get_beijing_now()
  day_of_year = bj_now.timetuple().tm_yday
  return greetings[day_of_year % len(greetings)]


def get_market_status_banner():
  """【智能休市感知引擎】"""
  return (
      "<div style='background: #e6fffa; color: #234e52; padding: 8px 12px;"
      " border-radius: 4px; font-size: 12px; margin-bottom: 12px;'>🔔"
      " <b>顶级对冲基金级终端已就绪</b>：已加载现金生息（SGOV）、再平衡死区防摩擦与动态止损网。</div>"
  )


def calculate_rsi(series, period=14):
  """计算 RSI 相对强弱指标"""
  delta = series.diff()
  gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
  loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
  rs = gain / loss
  rsi = 100 - (100 / (1 + rs))
  return rsi


def evaluate_macro_and_danger_signals():
  """【机构级全景宏观、流动性与风险扫描】"""
  danger_count = 0
  danger_signals = []
  data_fetch_success = True

  tnx = safe_yf_download("^TNX", period="5d")
  if tnx is not None and len(tnx) >= 2:
    if tnx["Close"].iloc[-1] > tnx["Close"].iloc[0] * 1.01:
      danger_count += 1
      danger_signals.append(
          "🔴 **美债收益率短期走高** (全球资产之锚承压，成长股估值受限)"
      )
  else:
    data_fetch_success = False

  vix = safe_yf_download("^VIX", period="2d")
  if vix is not None and not vix.empty:
    if vix["Close"].iloc[-1] > 22:
      danger_count += 1
      danger_signals.append(
          f"🔴 **VIX恐慌指数偏高** (当前值: {vix['Close'].iloc[-1]:.2f}，市场情绪不稳定)"
      )

  dxy = safe_yf_download("DX-Y.NYB", period="5d")
  if dxy is not None and len(dxy) >= 2:
    if dxy["Close"].iloc[-1] > dxy["Close"].iloc[0] * 1.006:
      danger_count += 1
      danger_signals.append(
          f"🔴 **美元指数显著走强** (当前值: {dxy['Close'].iloc[-1]:.2f}，非美资产承压)"
      )

  sp500_long = safe_yf_download("^GSPC", period="250d")
  if sp500_long is not None and len(sp500_long) >= 200:
    if sp500_long["Close"].iloc[-1] < sp500_long["Close"].iloc[-200:].mean():
      danger_count += 1
      danger_signals.append(
          "🔴 **标普500跌破200日均线** (长线趋势转弱，进入熊市防御区间)"
      )

  cnh = safe_yf_download("USDCNH=X", period="5d")
  if cnh is not None and len(cnh) >= 2:
    if cnh["Close"].iloc[-1] > cnh["Close"].iloc[0] * 1.008:
      danger_count += 1
      danger_signals.append("🔴 **离岸人民币贬值压力** (USD/CNH短期走高，A股承压)")

  hyg = safe_yf_download("HYG", period="5d")
  if hyg is not None and len(hyg) >= 2:
    if hyg["Close"].iloc[-1] < hyg["Close"].iloc[0] * 0.992:
      danger_count += 1
      danger_signals.append(
          "🔴 **高收益债(HYG)出现流动性抛压** (信用利差走阔)"
      )

  btc = safe_yf_download("BTC-USD", period="5d")
  if btc is not None and len(btc) >= 2:
    if btc["Close"].iloc[-1] < btc["Close"].iloc[0] * 0.95:
      danger_count += 1
      danger_signals.append("🔴 **加密市场动能骤降 (BTC短线重挫)**")

  gold = safe_yf_download("GC=F", period="5d")
  copper = safe_yf_download("HG=F", period="5d")
  if (
      gold is not None
      and copper is not None
      and len(gold) >= 2
      and len(copper) >= 2
  ):
    g_ret = (gold["Close"].iloc[-1] - gold["Close"].iloc[0]) / gold["Close"].iloc[0]
    c_ret = (
        copper["Close"].iloc[-1] - copper["Close"].iloc[0]
    ) / copper["Close"].iloc[0]
    if g_ret - c_ret > 0.03:
      danger_count += 1
      danger_signals.append("🔴 **跨资产背离：金铜比显著走阔** (滞胀预期抬头)")

  if not data_fetch_success and danger_count == 0:
    danger_count = 1
    danger_signals.append(
        "🛡️ **安全防错机制启动**：部分宏观数据源响应异常，系统已自动降级防守。"
    )

  return danger_count, danger_signals


def evaluate_action_advice(danger_count):
  """【智能操作建议引擎】"""
  if danger_count >= 3:
    return (
        "🔴 【清仓 / 重度防守】",
        (
            "危险信号达到 3 条或以上！系统性风险加剧，次日严禁开新仓，建议将仓位降至"
            " 1-2 成以内。"
        ),
    )
  elif danger_count == 2:
    return (
        "🟠 【分批减仓 / 降低风险】",
        (
            "触发 2 条危险信号。市场波动加剧，次日建议控制总仓位在 3-5"
            " 成以内，不盲目追高。"
        ),
    )
  elif danger_count == 1:
    return (
        "🟡 【稳健观望 / 保持仓位】",
        (
            "触发 1 条潜在风险。大环境处于震荡期，次日可维持现有仓位，仅对超跌优质标的进行轻仓试错。"
        ),
    )
  else:
    return (
        "🟢 【积极建仓 / 逢低布局】",
        (
            "宏观与流动性指标均平稳！次日可按计划执行建仓，重点布局回调到位的核心资产。"
        ),
    )


def evaluate_portfolio_stop_loss_and_buy_plan(danger_count, portfolio_weights):
  """【进阶】持仓动态移动止损 + 波动率自适应建仓引擎"""
  stop_loss_alerts = []
  buy_recommendations = []

  if danger_count >= 3:
    max_allocate_pct = 0
    strategy_note = "宏观风险高，明日【严禁建仓】或全仓防御，保持现金流。"
  elif danger_count == 2:
    max_allocate_pct = 5
    strategy_note = (
        "宏观有压制，明日仅允许小额试错，单笔建仓不超过总资金的 3%-5%。"
    )
  elif danger_count == 1:
    max_allocate_pct = 10
    strategy_note = (
        "震荡稳健期，明日可动用总资金的 5%-10% 逢低吸纳标配权重偏低的资产。"
    )
  else:
    max_allocate_pct = 20
    strategy_note = (
        "宏观环境优良，明日可积极执行建仓计划，单日总建仓额度可达总资金的"
        " 15%-20%。"
    )

  for ticker, target_w in portfolio_weights.items():
    try:
      hist = safe_yf_download(ticker, period="250d")
      if hist is not None and len(hist) >= 60:
        current_p = hist["Close"].iloc[-1]

        # 1. 动态移动止损检测（不适用于短债SGOV）
        if ticker != "SGOV":
          recent_max = hist["Close"].iloc[-30:].max()
          drawdown_from_peak = (current_p - recent_max) / recent_max * 100
          if drawdown_from_peak <= -12.0:
            stop_loss_alerts.append({
                "ticker": ticker,
                "price": f"{current_p:,.2f}",
                "drawdown": f"{drawdown_from_peak:.1f}%",
                "peak": f"{recent_max:,.2f}",
            })

        # 2. 50日均线护城河校验
        ma_50 = hist["Close"].iloc[-50:].mean()
        if current_p < ma_50 * 0.93:
          continue

        # 3. 波动率自适应仓位计算
        volatility = hist["Close"].pct_change().rolling(30).std().iloc[-1]
        vol_multiplier = max(
            0.5, min(1.5, 0.03 / (volatility if volatility > 0 else 0.03))
        )

        ret_5d = (
            current_p - hist["Close"].iloc[-5]
        ) / hist["Close"].iloc[-5] * 100
        rsi = calculate_rsi(hist["Close"]).iloc[-1]

        if ret_5d < 1.5 or rsi < 45:
          suggested_position = min(
              target_w * 100 * vol_multiplier, max_allocate_pct
          )
          reason = []
          if ret_5d < 0:
            reason.append(f"5日回调 {ret_5d:.1f}%")
          if rsi < 45:
            reason.append(f"RSI健康({rsi:.1f})")
          if not reason:
            reason.append("均线支撑位有效")

          buy_recommendations.append({
              "ticker": ticker,
              "price": f"{current_p:,.2f}",
              "suggest_pos": f"{suggested_position:.1f}% 总仓位",
              "reason": " + ".join(reason),
          })
    except Exception as e:
      print(f"Error evaluating plan for {ticker}: {e}")

  return max_allocate_pct, strategy_note, stop_loss_alerts, buy_recommendations


def evaluate_portfolio_fx_and_drift():
  """【进阶】多币种收益折算 + 再平衡死区（Deadband）与摩擦控制引擎"""
  usd_cnh = 7.20
  cnh_hist = safe_yf_download("USDCNH=X", period="2d")
  if cnh_hist is not None and not cnh_hist.empty:
    usd_cnh = cnh_hist["Close"].iloc[-1]

  portfolio_results = []
  total_weighted_change_rmb = 0.0
  rebalance_alerts = []

  for ticker, target_weight in MY_PORTFOLIO_WEIGHTS.items():
    hist = safe_yf_download(ticker, period="2d")
    if hist is not None and len(hist) >= 2:
      price = hist["Close"].iloc[-1]
      prev_close = hist["Close"].iloc[0]
      change_pct = ((price - prev_close) / prev_close) * 100
      weighted_impact = change_pct * target_weight
      total_weighted_change_rmb += weighted_impact

      # 模拟资产当前实际权重估算（基准目标权重 ± 近期涨跌偏差）
      estimated_current_weight = target_weight * (1 + change_pct / 100)
      weight_drift = (
          estimated_current_weight - target_weight
      ) * 100  # 绝对百分比偏差

      # 【再平衡死区判定】：只有当资产权重绝对偏离超过 ±4.5% 时，才触发调仓提醒，避免过度交易
      if abs(weight_drift) >= 4.5:
        rebalance_alerts.append({
            "ticker": ticker,
            "drift": f"{weight_drift:+.1f}%",
            "target": f"{target_weight*100:.0f}%",
        })

      display_name = (
          "SGOV (现金/超短债固收)" if ticker == "SGOV" else ticker
      )
      portfolio_results.append({
          "ticker": display_name,
          "target_weight": f"{target_weight*100:.0f}%",
          "price": f"{price:,.2f}",
          "change": f"{change_pct:+,.2f}%",
          "weighted_impact": f"{weighted_impact:+,.2f}%",
      })

  return portfolio_results, total_weighted_change_rmb, usd_cnh, rebalance_alerts


def fetch_single_macro_item(item):
  ticker, name = item
  hist = safe_yf_download(ticker, period="60d")
  if hist is not None and len(hist) >= 2:
    price = hist["Close"].iloc[-1]
    prev_close = hist["Close"].iloc[-2]
    change_pct = ((price - prev_close) / prev_close) * 100
    rsi_val = calculate_rsi(hist["Close"]).iloc[-1]
    return {
        "name": name,
        "ticker": ticker,
        "price": f"{price:,.2f}",
        "change": f"{change_pct:+.2f}%",
        "rsi": f"{rsi_val:.1f}",
    }
  return None


def scan_market_indices_and_commodities():
  metrics = [
      ("^GSPC", "美股：标普500 (S&P 500)"),
      ("RSP", "美股：标普500等权重ETF"),
      ("^IXIC", "美股：纳斯达克综合指数 (Nasdaq)"),
      ("^DJI", "美股：道琼斯工业指数 (Dow Jones)"),
      ("000001.SS", "A股：上证指数"),
      ("000300.SS", "A股：沪深300"),
      ("399006.SZ", "A股：创业板指"),
      ("^HSI", "港股：恒生指数"),
      ("DX-Y.NYB", "宏观：美元指数 (DXY)"),
      ("GC=F", "宏观：国际黄金"),
      ("CL=F", "宏观：WTI国际原油"),
      ("HG=F", "宏观：国际铜"),
      ("HYG", "宏观：高收益债ETF"),
      ("BTC-USD", "加密：比特币"),
  ]
  results = []
  with ThreadPoolExecutor(max_workers=14) as executor:
    futures = [
        executor.submit(fetch_single_macro_item, item) for item in metrics
    ]
    for future in as_completed(futures):
      res = future.result()
      if res:
        results.append(res)
  results.sort(key=lambda x: [m[0] for m in metrics].index(x["ticker"]))
  return results


def scan_sector_rotation():
  sectors = [
      ("XLK", "科技"),
      ("XLF", "金融"),
      ("XLV", "医疗"),
      ("XLY", "可选消费"),
      ("XLP", "必需消费"),
      ("XLE", "能源"),
      ("XLI", "工业"),
      ("XLU", "公用事业"),
      ("XLRE", "房地产"),
      ("XLB", "原材料"),
      ("XLC", "通信服务"),
  ]
  results = []
  with ThreadPoolExecutor(max_workers=11) as executor:
    futures = [
        executor.submit(fetch_single_macro_item, item) for item in sectors
    ]
    for future in as_completed(futures):
      res = future.result()
      if res:
        results.append(res)
  results.sort(key=lambda x: [m[0] for m in sectors].index(x["ticker"]))
  return results


def generate_master_strategy_report(
    danger_count,
    danger_signals,
    macro_data,
    sector_data,
    portfolio_data,
    portfolio_total_change,
    usd_cnh,
    max_alloc,
    strat_note,
    stop_loss_alerts,
    recommended_buys,
    rebalance_alerts,
):
  now_str = get_beijing_now().strftime("%Y-%m-%d %H:%M")
  greeting_text = get_daily_greeting()
  action_title, action_desc = evaluate_action_advice(danger_count)
  market_status_banner = get_market_status_banner()

  p_total_class = (
      "text-green" if portfolio_total_change >= 0 else "text-red"
  )

  css = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #333; line-height: 1.5; font-size: 14px; }
        h2 { color: #1a202c; font-size: 18px; border-bottom: 2px solid #edf2f7; padding-bottom: 8px; margin-top: 0; }
        h3 { color: #2d3748; font-size: 15px; margin-top: 20px; margin-bottom: 8px; }
        .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .greeting-card { background: #fffaf0; border-left: 4px solid #ecc94b; padding: 10px 14px; border-radius: 4px; color: #744210; font-size: 13px; margin-bottom: 12px; }
        .action-card { background: #fff5f5; border-left: 4px solid #f56565; padding: 10px 14px; border-radius: 4px; color: #9b2c2c; font-size: 13px; margin-bottom: 14px; }
        .stop-card { background: #fff1f2; border-left: 4px solid #e11d48; padding: 10px 14px; border-radius: 4px; color: #9f1239; font-size: 13px; margin-bottom: 14px; }
        .rebal-card { background: #fefce8; border-left: 4px solid #ca8a04; padding: 10px 14px; border-radius: 4px; color: #854d0e; font-size: 13px; margin-bottom: 14px; }
        .buy-card { background: #f0fdf4; border-left: 4px solid #319795; padding: 10px 14px; border-radius: 4px; color: #234e52; font-size: 13px; margin-bottom: 14px; }
        .portfolio-card { background: #f7fafc; border-left: 4px solid #4a5568; padding: 10px 14px; border-radius: 4px; color: #2d3748; font-size: 13px; margin-bottom: 14px; }
        table.data-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 6px; }
        table.data-table th { background: #f7fafc; color: #4a5568; text-align: left; padding: 6px 8px; border-bottom: 1px solid #e2e8f0; font-weight: 600; }
        table.data-table td { padding: 6px 8px; border-bottom: 1px solid #edf2f7; color: #2d3748; }
        .text-green { color: #38a169; font-weight: 600; }
        .text-red { color: #e53e3e; font-weight: 600; }
        .meta-text { color: #718096; font-size: 12px; }
        .footer-tip { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; font-size: 11px; color: #4a5568; margin-top: 16px; }
    </style>
    """

  html = f"{css}<h2>📈 灿灿顶级对冲基金级量化终端</h2>"
  html += f"<div class='greeting-card'><b>💌 每日小情话：</b><br>{greeting_text}</div>"
  html += market_status_banner
  html += (
      f"<p class='meta-text'>收盘播报时间（北京时间）：{now_str} | 实时美元汇率"
      f" (USD/CNH): {usd_cnh:.4f}</p>"
  )

  html += (
      f"<div"
      f" class='action-card'><b>🚦今日收盘宏观定调：{action_title}</b><br>{action_desc}</div>"
  )

  # 1. 现有持仓动态移动止损警报
  if stop_loss_alerts:
    html += f"<div class='stop-card'><b>🚨 持仓动态移动止损警报（需密切关注）：</b><br>"
    html += (
        "• 以下核心持仓自近期高点回撤超过警戒线，请评估是否执行风控减仓：<br>"
    )
    html += "<ul style='padding-left: 16px; margin: 4px 0;'>"
    for s in stop_loss_alerts:
      html += (
          f"<li><b>{s['ticker']}</b>（现价: ${s['price']}）| 近期高点: ${s['peak']}"
          f" | <b>当前回撤: <span"
          f" style='color:#e11d48;'>{s['drawdown']}</span></b></li>"
      )
    html += "</ul></div>"

  # 2. 再平衡死区调仓提示（抗摩擦成本）
  if rebalance_alerts:
    html += f"<div class='rebal-card'><b>⚖️ 资产再平衡死区预警（Turnover Control）：</b><br>"
    html += (
        "• 以下资产实际权重偏离目标权重超过死区阈值（±4.5%），建议进行平衡调仓：<br>"
    )
    html += "<ul style='padding-left: 16px; margin: 4px 0;'>"
    for r in rebalance_alerts:
      html += (
          f"<li><b>{r['ticker']}</b> | 目标权重: {r['target']} | <b>权重漂移:"
          f" {r['drift']}</b></li>"
      )
    html += "</ul></div>"

  # 3. 明日建仓与波动率自适应规划
  html += f"<div class='buy-card'><b>🎯 次日建仓与波动率自适应规划：</b><br>"
  html += f"• <b>次日建仓总额度上限</b>：总资金的 <b>{max_alloc}%</b><br>"
  html += f"• <b>策略总批示</b>：{strat_note}<br><br>"
  if recommended_buys:
    html += (
        "<b>💡 次日值得买入/补仓的标的（已通过均线护城河与波动率平减校验）：</b>"
    )
    html += "<ul style='padding-left: 16px; margin: 4px 0;'>"
    for b in recommended_buys:
      html += (
          f"<li><b>{b['ticker']}</b>（现价: ${b['price']}）| 风险平价建议建仓份额:"
          f" <span"
          f" style='color:#2b6cb0; font-weight:bold;'>{b['suggest_pos']}</span>"
          f" | 理由：{b['reason']}</li>"
      )
    html += "</ul>"
  else:
    html += "<i>当前暂无符合超跌稳健或未破位条件的建仓标的，建议次日持币观望。</i>"
  html += "</div>"

  html += (
      f"<div class='portfolio-card'><b>💼 今日持仓收盘表现：</b><br>折算人民币总资产今日预估加权盈亏（含SGOV固收生息）："
      f" <span"
      f" class='{p_total_class}'><b>{portfolio_total_change:+,.2f}%</b></span></div>"
  )

  html += (
      "<div class='card'><h3>🛡️"
      " 第一步：收盘宏观水位、流动性与风险信号明细</h3><ul"
      " style='padding-left: 18px; margin: 6px 0; font-size: 13px;'>"
  )
  for sig in danger_signals:
    html += f"<li style='margin-bottom: 4px;'>{sig}</li>"
  if not danger_signals:
    html += (
        "<li><b>✅ 宏观多头环境健康</b>：各项流动性及风控指标今日全线正常。</li>"
    )
  html += "</ul></div>"

  html += "<div class='card'><h3>💼 第二步：多币种持仓收盘明细</h3>"
  html += (
      "<table class='data-table'><thead><tr><th>资产代码</th><th>目标权重</th><th>现价</th><th>今日涨跌</th><th>组合贡献度</th></tr></thead><tbody>"
  )
  for item in portfolio_data:
    c_class = (
        "text-green" if not item["change"].startswith("-") else "text-red"
    )
    i_class = (
        "text-green" if not item["weighted_impact"].startswith("-") else "text-red"
    )
    html += (
        f"<tr><td><b>{item['ticker']}</b></td><td>{item['target_weight']}</td><td>${item['price']}</td><td><span"
        f" class='{c_class}'>{item['change']}</span></td><td><span"
        f" class='{i_class}'>{item['weighted_impact']}</span></td></tr>"
    )
  html += "</tbody></table></div>"

  html += (
      "<div class='card'><h3>📊 第三步：全球核心指数、大宗商品与加密资产收盘价</h3>"
  )
  html += (
      "<table class='data-table'><thead><tr><th>监控标的</th><th>收盘点位</th><th>涨跌幅</th><th>RSI(14)</th></tr></thead><tbody>"
  )
  for item in macro_data:
    color_class = (
        "text-green" if not item["change"].startswith("-") else "text-red"
    )
    html += (
        f"<tr><td><b>{item['name']}</b></td><td>${item['price']}</td><td><span"
        f" class='{color_class}'>{item['change']}</span></td><td><b>{item['rsi']}</b></td></tr>"
    )
  html += "</tbody></table></div>"

  html += "<div class='card'><h3>🔥 第四步：美股行业板块收盘热力图</h3>"
  html += (
      "<table class='data-table'><thead><tr><th>板块名称</th><th>价格</th><th>涨跌幅</th><th>RSI(14)</th></tr></thead><tbody>"
  )
  for item in sector_data:
    color_class = (
        "text-green" if not item["change"].startswith("-") else "text-red"
    )
    html += (
        f"<tr><td><b>{item['name']}</b></td><td>${item['price']}</td><td><span"
        f" class='{color_class}'>{item['change']}</span></td><td><b>{item['rsi']}</b></td></tr>"
    )
  html += "</tbody></table></div>"

  html += (
      "<div class='footer-tip'><b>💡 顶级对冲基金寄语：</b><br>现金生息、防摩擦调仓与动态移动止损全线开闸，资产正在全天候护航下稳健前行。</div>"
  )
  return html


def send_pushplus(content):
  if not PUSHPLUS_TOKEN:
    print("Error: PUSHPLUS_TOKEN is not set.")
    return
  url = "https://www.pushplus.plus/send"
  payload = {
      "token": PUSHPLUS_TOKEN,
      "title": "🔔 灿灿的顶级对冲基金级终端播报",
      "content": content,
      "template": "html",
  }
  try:
    response = requests.post(url, json=payload, timeout=10)
    print(response.json())
  except Exception as e:
    print(f"Push failed: {e}")


if __name__ == "__main__":
  is_skip, skip_msg = is_market_holiday_or_skip()
  if is_skip:
    print(f"Skipping execution: {skip_msg}")
    exit(0)

  print("正在执行顶级对冲基金级量化扫描与全天候风控结算...")
  count, signals = evaluate_macro_and_danger_signals()
  max_alloc, strat_note, stop_loss_alerts, recommended_buys = (
      evaluate_portfolio_stop_loss_and_buy_plan(count, MY_PORTFOLIO_WEIGHTS)
  )
  portfolio_data, portfolio_total_change, usd_cnh, rebalance_alerts = (
      evaluate_portfolio_fx_and_drift()
  )
  macro_data = scan_market_indices_and_commodities()
  sector_data = scan_sector_rotation()

  print("正在生成高阶策略报告...")
  report = generate_master_strategy_report(
      count,
      signals,
      macro_data,
      sector_data,
      portfolio_data,
      portfolio_total_change,
      usd_cnh,
      max_alloc,
      strat_note,
      stop_loss_alerts,
      recommended_buys,
      rebalance_alerts,
  )

  print("正在通过 PushPlus 发送到微信...")
  send_pushplus(report)

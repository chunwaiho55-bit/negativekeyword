"""
Google Ads Search Terms 自動分析與決策 Dashboard
作者：資深全端工程師 / B2B 數位營銷分析師
框架：Python Streamlit
版本：1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import re
import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# 頁面基本設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Airwallex Ads Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 全域 CSS：深色專業主題
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── 全局重置 ── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0d14 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── 側邊欄 ── */
[data-testid="stSidebar"] {
    background: #0f1320 !important;
    border-right: 1px solid #1e2a3a !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #38bdf8 !important; }

/* ── 主標題區 ── */
.main-header {
    background: linear-gradient(135deg, #0f1829 0%, #0a192f 50%, #051020 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.main-header h1 {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: #38bdf8 !important;
    margin: 0 0 8px 0 !important;
    letter-spacing: -0.5px;
}
.main-header p {
    color: #64748b !important;
    font-size: 0.9rem !important;
    margin: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #0f1829;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #38bdf8; }
.kpi-label {
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    color: #f1f5f9;
    line-height: 1;
}
.kpi-value.danger { color: #f87171; }
.kpi-value.success { color: #4ade80; }
.kpi-value.info { color: #38bdf8; }
.kpi-sub {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── 標籤 ── */
.badge-keep {
    background: rgba(74,222,128,0.12);
    color: #4ade80;
    border: 1px solid rgba(74,222,128,0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    white-space: nowrap;
}
.badge-neg {
    background: rgba(248,113,113,0.12);
    color: #f87171;
    border: 1px solid rgba(248,113,113,0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    white-space: nowrap;
}

/* ── 區塊標題 ── */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* ── 上傳區 ── */
[data-testid="stFileUploader"] {
    background: #0f1829 !important;
    border: 2px dashed #1e3a5f !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #38bdf8 !important;
}

/* ── 輸入框 ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0f1829 !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── 按鈕 ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 8px 20px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── 匯出文字區 ── */
.export-box {
    background: #060d18;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 18px 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    white-space: pre;
    overflow-x: auto;
    max-height: 220px;
    overflow-y: auto;
}

/* ── 規則標籤 ── */
.rule-pill {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.25);
    color: #38bdf8;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    margin: 3px 3px 3px 0;
}

/* ── DataTable 美化 ── */
.dataframe { background: #0f1829 !important; }
thead tr th {
    background: #0a192f !important;
    color: #38bdf8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    border-bottom: 2px solid #1e3a5f !important;
}

/* ── 告知欄 ── */
.info-box {
    background: rgba(56,189,248,0.06);
    border-left: 3px solid #38bdf8;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 0.83rem;
    color: #93c5fd;
    margin: 12px 0;
}

/* ── 隱藏 Streamlit 預設元件 ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State 初始化（持久化儲存規則）
# ─────────────────────────────────────────────
if "extra_rules" not in st.session_state:
    st.session_state.extra_rules = []   # 使用者自訂規則列表
if "df_result" not in st.session_state:
    st.session_state.df_result = None   # 分析結果 DataFrame
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None      # 原始上傳資料


# ─────────────────────────────────────────────
# 核心規則引擎設定（業務邏輯字典）
# ─────────────────────────────────────────────

# 品牌關鍵字
BRAND_KEYWORDS = [
    "airwallex", "空中云汇", "空中雲匯", "awx", "airwallx", "airwallex",
    "airwllex", "airwalex", "airwallex"
]

# SME 意圖字詞（有 signup 但無 biz email 時判斷是否為 SME 意圖）
SME_INTENT_KEYWORDS = [
    "open account", "create account", "register", "sign up", "signup",
    "business account", "open business", "company account", "apply account",
    "new account", "start account", "open fx", "foreign exchange account",
    "merchant account", "corporate account"
]

# Negative 意圖分類字典
NEGATIVE_INTENT_MAP = {
    "Competitors": [
        "stripe", "payoneer", "wise", "transferwise", "revolut", "skyee",
        "lianlian", "lianpay", "paypal", "square", "brex", "mercury",
        "relay", "found", "tide", "monzo", "starling", "bunq", "n26",
        "adyen", "checkout.com", "worldpay", "klarna", "afterpay", "razorpay",
        "paytm", "grab pay", "alipay", "wechat pay", "pingpong", "worldfirst",
        "ofw", "currenxie", "nium", "currencycloud"
    ],
    "Tech Support / Existing Users": [
        "audit confirmation", " api ", "api key", "api doc", "test card",
        " down", "is down", "server down", "outage", "login", "log in",
        "sign in", "password", "forgot password", "reset password",
        "statements", "statement", "invoice", "receipt", "help desk",
        "support ticket", "contact support", "customer service number",
        "developer doc", "webhook", "sdk", "sandbox", "two factor",
        "2fa", "authenticator", "verification code", "account locked",
        "transaction history", "dispute", "chargeback"
    ],
    "Jobs / HR": [
        "careers", "career", "jobs", "job opening", "salary", "salaries",
        "interview", "glassdoor", "linkedin jobs", "hiring", "recruitment",
        "internship", "graduate program", "work at", "work for",
        "apply job", "employment", "hr contact", "indeed"
    ],
    "Investor / PR": [
        "valuation", "stock", "share price", "market cap", "ipo",
        "series g", "series f", "funding round", "investor", "investment",
        "news", "press release", "media", "scam", "fraud", "review complaint",
        "trustpilot", "bbb", "complaints", "lawsuit", "legal action",
        "annual report", "revenue", "profit"
    ],
    "B2C / Irrelevant": [
        "western union", "crypto", "bitcoin", "binance", "coinbase",
        "nft", "ethereum", "personal transfer", "send money home",
        "remittance personal", "loan", "mortgage", "insurance",
        "credit score", "tax refund", "student loan", "payday loan",
        "cheap flight", "travel money", "holiday money", "currency exchange personal"
    ]
}


# ─────────────────────────────────────────────
# 工具函式：欄位偵測與資料清理
# ─────────────────────────────────────────────

def clean_numeric(series: pd.Series) -> pd.Series:
    """將含有符號的數字欄位（如 $1,234.56）轉換為 float"""
    return (
        series.astype(str)
        .str.replace(r'[\$,£€¥₩\s]', '', regex=True)
        .str.replace(r'[^\d\.\-]', '', regex=True)
        .replace('', '0')
        .replace('--', '0')
        .replace('-', '0')
        .astype(float)
        .fillna(0)
    )


def detect_columns(df: pd.DataFrame) -> dict:
    """
    自動偵測 Google Ads 匯出檔案的欄位映射。
    Google Ads 有多種語言版本，需模糊匹配。
    回傳: { 'search_term': col_name, 'cost': col_name, ... }
    """
    col_map = {}
    cols_lower = {c: c.lower() for c in df.columns}

    # 搜尋字詞欄
    for c, cl in cols_lower.items():
        if any(k in cl for k in ["search term", "search query", "搜尋詞", "搜索词", "keyword text"]):
            col_map["search_term"] = c
            break
    if "search_term" not in col_map:
        # 找第一個字串欄位當備案
        for c in df.columns:
            if df[c].dtype == object:
                col_map["search_term"] = c
                break

    # 費用欄
    for c, cl in cols_lower.items():
        if any(k in cl for k in ["cost", "spend", "費用", "花費", "支出"]):
            col_map["cost"] = c
            break

    # CPC
    for c, cl in cols_lower.items():
        if "cpc" in cl or "avg. cpc" in cl or "平均 cpc" in cl or "平均cpc" in cl:
            col_map["cpc"] = c
            break

    # 點擊數
    for c, cl in cols_lower.items():
        if cl in ["clicks", "click", "點擊次數", "点击次数"]:
            col_map["clicks"] = c
            break

    # 曝光數
    for c, cl in cols_lower.items():
        if any(k in cl for k in ["impr", "impression", "曝光", "展示"]):
            col_map["impressions"] = c
            break

    # Business Email 轉換（最高優先）
    for c, cl in cols_lower.items():
        if "business email" in cl or "business_email" in cl or "biz email" in cl:
            col_map["biz_email"] = c
            break

    # signup_all_emails
    for c, cl in cols_lower.items():
        if "signup_all" in cl or "signup all" in cl or "all email" in cl or "all_email" in cl:
            col_map["signup_all"] = c
            break

    # 通用轉換欄（備案）
    for c, cl in cols_lower.items():
        if "conversion" in cl and "biz_email" not in col_map.get("biz_email", ""):
            if "biz_email" not in col_map:
                col_map["biz_email"] = c
            elif "signup_all" not in col_map:
                col_map["signup_all"] = c
            break

    return col_map


# ─────────────────────────────────────────────
# 核心規則引擎：判斷每個 Search Term 的 Action
# ─────────────────────────────────────────────

def contains_any(text: str, keywords: list) -> str:
    """檢查 text 是否包含任一 keyword，回傳匹配到的 keyword 或 ''"""
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return kw
    return ""


def apply_rules(row: pd.Series, col_map: dict, extra_rules: list) -> dict:
    """
    對單一 Search Term 套用所有規則，回傳：
    { 'action': 'Keep' | 'Negative (Exact)' | 'Negative (Phrase)',
      'reason': '...' }
    """
    term = str(row.get(col_map.get("search_term", ""), "")).strip()
    cost = float(row.get(col_map.get("cost", "cost_val"), 0) or 0)
    biz_email = float(row.get(col_map.get("biz_email", "biz_email_val"), 0) or 0)
    signup_all = float(row.get(col_map.get("signup_all", "signup_all_val"), 0) or 0)

    # ── Rule 1：Business Email > 0，無條件 Keep ──────────────────
    if biz_email > 0:
        return {
            "action": "✅ Keep",
            "reason": f"Rule 1 ｜帶來 {int(biz_email)} 個 Business Email 轉換，直接保留"
        }

    # ── Rule 2：品牌字或近似錯字 ────────────────────────────────
    matched_brand = contains_any(term, BRAND_KEYWORDS)
    if matched_brand:
        return {
            "action": "✅ Keep",
            "reason": f"Rule 2 ｜包含品牌關鍵字「{matched_brand}」，屬品牌保護詞"
        }

    # ── Rule 3：有 signup 但無 biz email，判斷 SME Intent ────────
    if signup_all > 0 and biz_email == 0:
        matched_sme = contains_any(term, SME_INTENT_KEYWORDS)
        if matched_sme:
            return {
                "action": "✅ Keep",
                "reason": f"Rule 3 ｜有 {int(signup_all)} 個 signup，含 SME 意圖詞「{matched_sme}」，潛在中小企開戶意圖"
            }
        else:
            # 有 signup 但不確定 SME 意圖 → 保守保留並標注
            return {
                "action": "✅ Keep",
                "reason": f"Rule 3 ｜有 {int(signup_all)} 個 signup（非 SME 意圖詞），建議持續觀察轉換品質"
            }

    # ── Rule 4：Negative 意圖分類 ────────────────────────────────
    for intent_category, keywords in NEGATIVE_INTENT_MAP.items():
        matched_neg = contains_any(term, keywords)
        if matched_neg:
            # 依字詞長度決定 Exact 或 Phrase
            word_count = len(term.split())
            match_type = "Exact" if word_count <= 2 else "Phrase"
            reason_map = {
                "Competitors": f"排除 - 競爭對手品牌「{matched_neg}」，用戶正在比較競品",
                "Tech Support / Existing Users": f"排除 - 技術支援 / 現有用戶行為（{matched_neg}），無開戶意圖",
                "Jobs / HR": f"排除 - 求職招聘意圖「{matched_neg}」，非目標客群",
                "Investor / PR": f"排除 - 投資人 / 公關意圖「{matched_neg}」，非開戶客群",
                "B2C / Irrelevant": f"排除 - B2C / 無關流量「{matched_neg}」，非 B2B 商業客戶"
            }
            return {
                "action": f"🚫 Negative ({match_type})",
                "reason": f"Rule 4 ｜{reason_map[intent_category]}"
            }

    # ── 使用者自訂規則（Extra Rules）──────────────────────────────
    for rule_text in extra_rules:
        rule_lower = rule_text.lower()
        term_lower = term.lower()

        # 解析規則：尋找 'contains X' 且 '0 conversion / negative' 之類的自然語言
        # 簡易解析：找 '' 或 "" 包圍的關鍵字
        import re as _re
        quoted = _re.findall(r"['\"](.+?)['\"]", rule_lower)
        if not quoted:
            # 試著找 contains 後面的詞
            m = _re.search(r'contains?\s+([a-z0-9 _\-]+)', rule_lower)
            if m:
                quoted = [m.group(1).strip()]

        for q in quoted:
            if q in term_lower:
                is_negative = any(k in rule_lower for k in ["negative", "排除", "block", "exclude"])
                if is_negative:
                    word_count = len(term.split())
                    match_type = "Exact" if word_count <= 2 else "Phrase"
                    return {
                        "action": f"🚫 Negative ({match_type})",
                        "reason": f"自訂規則 ｜符合條件「{q}」，依使用者規則排除"
                    }
                else:
                    return {
                        "action": "✅ Keep",
                        "reason": f"自訂規則 ｜符合條件「{q}」，依使用者規則保留"
                    }

    # ── 預設：無轉換且無匹配規則 → 旗標待觀察 ─────────────────
    if cost > 0 and biz_email == 0 and signup_all == 0:
        return {
            "action": "⚠️ Review",
            "reason": "無轉換且未命中規則，建議人工審核（可能為長尾詞或新興競品）"
        }

    return {
        "action": "✅ Keep",
        "reason": "未命中 Negative 規則，暫予保留"
    }


def run_analysis(df: pd.DataFrame, col_map: dict, extra_rules: list) -> pd.DataFrame:
    """
    對整個 DataFrame 執行規則引擎，回傳含 Action / Why 欄位的結果表。
    使用 apply() 效能優化，數萬筆不卡頓。
    """
    results = df.apply(lambda row: apply_rules(row, col_map, extra_rules), axis=1)
    df = df.copy()
    df["__action"] = results.apply(lambda x: x["action"])
    df["__reason"] = results.apply(lambda x: x["reason"])
    return df


# ─────────────────────────────────────────────
# 側邊欄
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Ads Intelligence")
    st.markdown("---")

    # ── 展示內建規則 ──
    st.markdown("### 📋 內建規則引擎")

    rules_info = [
        ("Rule 1", "Business Email > 0 → Keep"),
        ("Rule 2", "品牌字 / 近似錯字 → Keep"),
        ("Rule 3", "signup > 0 判斷 SME Intent"),
        ("Rule 4", "競爭對手 / 技術支援 / 求職 / 投資 / B2C → Negative"),
    ]
    for tag, desc in rules_info:
        st.markdown(f'<span class="rule-pill">{tag}</span> {desc}', unsafe_allow_html=True)

    st.markdown("---")

    # ── 新增自訂規則 ──
    st.markdown("### ✏️ 新增客製化規則")
    new_rule = st.text_area(
        "輸入規則（自然語言）",
        placeholder='例如：將所有包含 "credit card" 且 0 轉換的字加進 Negative',
        height=100,
        key="new_rule_input"
    )

    col_add, col_clear = st.columns(2)
    with col_add:
        if st.button("➕ 新增規則", use_container_width=True):
            if new_rule.strip():
                st.session_state.extra_rules.append(new_rule.strip())
                # 若已有資料則重新分析
                if st.session_state.df_raw is not None:
                    col_map = detect_columns(st.session_state.df_raw)
                    st.session_state.df_result = run_analysis(
                        st.session_state.df_raw, col_map, st.session_state.extra_rules
                    )
                st.success("規則已新增並重新分析！")
                st.rerun()

    with col_clear:
        if st.button("🗑 清除全部", use_container_width=True):
            st.session_state.extra_rules = []
            st.rerun()

    # 顯示現有自訂規則
    if st.session_state.extra_rules:
        st.markdown("**現有自訂規則：**")
        for i, rule in enumerate(st.session_state.extra_rules):
            st.markdown(f'<span class="rule-pill">自訂 {i+1}</span> {rule[:60]}{"..." if len(rule)>60 else ""}', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-family:IBM Plex Mono;font-size:0.68rem;color:#334155;">© 2025 Airwallex Ads Intelligence<br>v1.0 · Powered by Streamlit</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# 主內容區
# ─────────────────────────────────────────────

# ── 標題 ──
st.markdown("""
<div class="main-header">
    <h1>⚡ Google Ads Search Term Analyzer</h1>
    <p>// Automated negative keyword intelligence for B2B campaigns · Airwallex internal tool</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 模組 1：檔案上傳
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">01 ── DATA ENTRY</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "拖曳或選擇 Google Ads Search Terms Report（CSV / Excel）",
    type=["csv", "xlsx", "xls"],
    help="支援 Google Ads 直接匯出的 CSV 或 Excel 格式。系統會自動偵測欄位。"
)


# ── 讀取並清理資料 ──
if uploaded_file is not None:
    with st.spinner("⚙️ 正在讀取並清理資料…"):
        try:
            # 讀取檔案
            if uploaded_file.name.endswith(".csv"):
                raw_bytes = uploaded_file.read()
                # 嘗試多種編碼
                for enc in ["utf-8-sig", "utf-8", "gbk", "big5", "latin-1"]:
                    try:
                        raw_content = raw_bytes.decode(enc)
                        break
                    except Exception:
                        continue

                lines = raw_content.split("\n")

                # ── 核心修復：找到真正的 header 行（欄位最多的那行）──
                # Google Ads CSV 前幾行是描述文字（欄位數很少），
                # 真正的 header 行欄位數最多
                best_row = 0
                best_count = 0
                for i, line in enumerate(lines[:20]):  # 只掃前 20 行
                    count = len(line.split(","))
                    if count > best_count:
                        best_count = count
                        best_row = i

                df_raw = pd.read_csv(
                    io.StringIO(raw_content),
                    skiprows=best_row,
                    thousands=",",
                    on_bad_lines="skip",   # 跳過格式錯誤的行
                    encoding_errors="replace"
                )
                # 移除 Google Ads 底部的總計行 / 空行
                df_raw = df_raw[~df_raw.iloc[:, 0].astype(str).str.lower().str.contains(
                    r"total|合計|总计|^\s*$", na=False, regex=True
                )]
            else:
                df_raw = pd.read_excel(uploaded_file, thousands=",")

            # 移除完全空白行
            df_raw.dropna(how="all", inplace=True)
            df_raw.reset_index(drop=True, inplace=True)

            # 自動偵測欄位
            col_map = detect_columns(df_raw)

            # 清理數字欄位
            for key in ["cost", "cpc", "clicks", "impressions", "biz_email", "signup_all"]:
                if key in col_map:
                    df_raw[col_map[key]] = clean_numeric(df_raw[col_map[key]])

            # 儲存到 session
            st.session_state.df_raw = df_raw

            # 執行分析
            st.session_state.df_result = run_analysis(df_raw, col_map, st.session_state.extra_rules)

            st.markdown(f'<div class="info-box">✅ 成功讀取 <strong>{len(df_raw):,}</strong> 筆搜尋字詞｜偵測到欄位：{", ".join([f"{k}→{v}" for k, v in col_map.items()])}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ 讀取失敗：{e}\n\n請確認上傳的是 Google Ads 標準匯出格式。")
            st.stop()


# ─────────────────────────────────────────────
# 以下區塊只在有分析結果時顯示
# ─────────────────────────────────────────────
if st.session_state.df_result is not None:
    df = st.session_state.df_result
    col_map = detect_columns(df)

    # 取出關鍵欄位
    cost_col = col_map.get("cost")
    cpc_col = col_map.get("cpc")
    biz_email_col = col_map.get("biz_email")
    signup_col = col_map.get("signup_all")
    term_col = col_map.get("search_term")
    clicks_col = col_map.get("clicks")

    # 安全取值函式
    def safe_sum(col):
        if col and col in df.columns:
            return df[col].sum()
        return 0

    total_cost = safe_sum(cost_col)
    total_biz_email = safe_sum(biz_email_col)
    total_signup = safe_sum(signup_col)

    df_neg = df[df["__action"].str.contains("Negative", na=False)]
    df_keep = df[df["__action"].str.contains("Keep", na=False)]
    df_review = df[df["__action"].str.contains("Review", na=False)]

    wasted_spend = df_neg[cost_col].sum() if cost_col else 0
    wasted_pct = (wasted_spend / total_cost * 100) if total_cost > 0 else 0
    conversions_kept = df_keep[biz_email_col].sum() if biz_email_col and biz_email_col in df_keep.columns else 0

    # ─────────────────────────────────────────────
    # 模組 2：KPI Summary Cards
    # ─────────────────────────────────────────────
    st.markdown("")
    st.markdown('<div class="section-header">02 ── KPI SUMMARY</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)

    def kpi_card(col_widget, label, value, sub, css_class=""):
        col_widget.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value {css_class}">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi_card(c1, "Total Spend", f"${total_cost:,.0f}", f"{len(df):,} search terms")
    kpi_card(c2, "Potential Wasted Spend", f"${wasted_spend:,.0f}", f"{wasted_pct:.1f}% of total budget", "danger")
    kpi_card(c3, "Conversions Kept", f"{int(conversions_kept)}", "Business Email signups", "success")
    kpi_card(c4, "Negative Keywords", f"{len(df_neg)}", f"{len(df_neg)/len(df)*100:.1f}% of terms", "danger" if len(df_neg) > 0 else "")
    kpi_card(c5, "Needs Review", f"{len(df_review)}", "manual check recommended", "info")

    # ─────────────────────────────────────────────
    # 模組 3：決策數據表
    # ─────────────────────────────────────────────
    st.markdown("")
    st.markdown('<div class="section-header">03 ── DECISION TABLE</div>', unsafe_allow_html=True)

    # 篩選器
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    with fc1:
        filter_action = st.multiselect(
            "篩選 Action",
            options=["✅ Keep", "🚫 Negative (Exact)", "🚫 Negative (Phrase)", "⚠️ Review"],
            default=["✅ Keep", "🚫 Negative (Exact)", "🚫 Negative (Phrase)", "⚠️ Review"]
        )
    with fc2:
        sort_by = st.selectbox("排序依據", ["Cost ↓", "Biz Email ↓", "Signup ↓", "Search Term"])
    with fc3:
        search_filter = st.text_input("🔍 搜尋字詞過濾", placeholder="輸入關鍵字篩選…")

    # 建立顯示用 DataFrame
    display_cols = {}
    if term_col:
        display_cols["Search Term"] = df[term_col]
    if cost_col:
        display_cols["Cost ($)"] = df[cost_col].round(2)
    if cpc_col:
        display_cols["Avg. CPC"] = df[cpc_col].round(3)
    if clicks_col:
        display_cols["Clicks"] = df[clicks_col].astype(int)
    if signup_col:
        display_cols["Signups"] = df[signup_col].astype(int)
    if biz_email_col:
        display_cols["Biz Emails"] = df[biz_email_col].astype(int)
    display_cols["Action"] = df["__action"]
    display_cols["Why（決策原因）"] = df["__reason"]

    df_display = pd.DataFrame(display_cols)

    # 套用篩選
    df_display = df_display[df_display["Action"].isin(filter_action)]
    if search_filter:
        df_display = df_display[
            df_display["Search Term"].str.lower().str.contains(search_filter.lower(), na=False)
        ]

    # 排序
    if sort_by == "Cost ↓" and "Cost ($)" in df_display.columns:
        df_display = df_display.sort_values("Cost ($)", ascending=False)
    elif sort_by == "Biz Email ↓" and "Biz Emails" in df_display.columns:
        df_display = df_display.sort_values("Biz Emails", ascending=False)
    elif sort_by == "Signup ↓" and "Signups" in df_display.columns:
        df_display = df_display.sort_values("Signups", ascending=False)
    elif sort_by == "Search Term":
        df_display = df_display.sort_values("Search Term")

    st.dataframe(
        df_display,
        use_container_width=True,
        height=520,
        hide_index=True,
        column_config={
            "Action": st.column_config.TextColumn("Action", width="medium"),
            "Why（決策原因）": st.column_config.TextColumn("Why（決策原因）", width="large"),
            "Cost ($)": st.column_config.NumberColumn("Cost ($)", format="$%.2f"),
        }
    )

    st.markdown(f'<div style="text-align:right;font-family:IBM Plex Mono;font-size:0.72rem;color:#475569;margin-top:8px;">顯示 {len(df_display):,} / {len(df):,} 筆</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # 模組 4：一鍵匯出區
    # ─────────────────────────────────────────────
    st.markdown("")
    st.markdown('<div class="section-header">04 ── EXPORT CENTER</div>', unsafe_allow_html=True)

    # 產生 Negative Keywords 清單
    neg_df = df[df["__action"].str.contains("Negative", na=False)]
    exact_terms = []
    phrase_terms = []

    if term_col:
        for _, row in neg_df.iterrows():
            term = str(row[term_col]).strip()
            action = str(row["__action"])
            if "Exact" in action:
                exact_terms.append(f"[{term}]")
            else:
                phrase_terms.append(f'"{term}"')

    # 去重排序
    exact_terms = sorted(list(set(exact_terms)))
    phrase_terms = sorted(list(set(phrase_terms)))

    ex1, ex2 = st.columns(2)

    with ex1:
        st.markdown("**📌 Exact Match Negatives**")
        exact_text = "\n".join(exact_terms) if exact_terms else "（暫無 Exact Match 建議）"
        st.markdown(f'<div class="export-box">{exact_text}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇ 下載 Exact Match List",
            data="\n".join(exact_terms),
            file_name=f"negative_exact_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with ex2:
        st.markdown("**💬 Phrase Match Negatives**")
        phrase_text = "\n".join(phrase_terms) if phrase_terms else "（暫無 Phrase Match 建議）"
        st.markdown(f'<div class="export-box">{phrase_text}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇ 下載 Phrase Match List",
            data="\n".join(phrase_terms),
            file_name=f"negative_phrase_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # 匯出完整分析報告（CSV）
    st.markdown("")
    ex_full = df_display.copy()
    csv_bytes = ex_full.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        "📊 下載完整分析報告（CSV）",
        data=csv_bytes,
        file_name=f"search_term_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=False
    )

# ── 空白提示（未上傳時顯示） ──
else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 80px 40px;
        background: #0f1829;
        border: 2px dashed #1e3a5f;
        border-radius: 16px;
        margin-top: 20px;
    ">
        <div style="font-size: 3rem; margin-bottom: 16px;">📂</div>
        <div style="font-family: IBM Plex Mono; font-size: 1rem; color: #38bdf8; margin-bottom: 8px;">
            請上傳 Google Ads Search Terms Report
        </div>
        <div style="font-family: IBM Plex Mono; font-size: 0.78rem; color: #475569;">
            支援 Google Ads 直接匯出的 .csv 或 .xlsx 格式<br>
            系統將自動偵測欄位並執行智能規則分析
        </div>
    </div>
    """, unsafe_allow_html=True)

# ⚡ Google Ads Search Term Analyzer

Airwallex 專用 Google Ads Search Terms 自動分析 Dashboard

## 🚀 快速啟動

### 1. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2. 啟動 Dashboard
```bash
streamlit run google_ads_dashboard.py
```

瀏覽器會自動開啟 `http://localhost:8501`

---

## 📋 使用方式

1. **上傳報表**：將 Google Ads 匯出的 Search Terms Report (CSV/Excel) 拖曳上傳
2. **自動分析**：系統立即執行規則引擎，標記每個字詞為 Keep / Negative / Review
3. **新增規則**：在左側 Sidebar 輸入自然語言規則（如「將含 credit card 且 0 轉換加進 Negative」）
4. **匯出清單**：點擊下載 Exact Match / Phrase Match Negative Keywords，直接貼入 Google Ads

---

## 🔧 內建規則邏輯

| 規則 | 條件 | 判定 |
|------|------|------|
| Rule 1 | Business Email 轉換 > 0 | ✅ Keep（最高優先） |
| Rule 2 | 含品牌字（airwallex, awx 等） | ✅ Keep |
| Rule 3 | signup > 0 且含 SME 意圖詞 | ✅ Keep（SME Intent） |
| Rule 4 | 競爭對手 / 技術支援 / 求職 / 投資 / B2C | 🚫 Negative |

---

## 📂 Google Ads 匯出格式說明

系統支援並自動偵測以下欄位（欄名模糊匹配）：
- Search Term / Search Query
- Cost / Spend
- Avg. CPC
- Clicks / Impressions  
- Business Email（轉換欄位）
- signup_all_emails（轉換欄位）

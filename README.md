# 🌤️ AI 創新微課程 — Taiwan Weather Forecast

> 從氣象資料到互動式天氣預報應用  
> **Code Smarter · Build a Better Tomorrow!**

---

## 📖 課程簡介

本課程以台灣天氣預報為主題，帶你從零開始學習如何：

- 🔌 串接 **中央氣象署 (CWA) Open Data API**
- 🐍 使用 **Python** 取得與處理 JSON 氣象資料
- 🗄️ 將資料儲存至 **SQLite** 資料庫
- 📊 使用 **Streamlit** 建立互動式 Web App
- 🗺️ 進階：用 **Folium** 實現台灣地圖視覺化

---

## 🛠️ 技術棧

| 技術 | 用途 |
|------|------|
| Python | 主要程式語言 |
| CWA Open Data API | 取得即時氣象 JSON 資料 |
| Requests | 呼叫 API 取得資料 |
| Pandas | 資料整理與預處理 |
| SQLite | 本地資料庫儲存氣溫資料 |
| Streamlit | 建立互動式 Web App |
| Folium | 台灣地圖視覺化（進階） |

---

## 📚 課程架構（24 單元）

| # | 主題 | 說明 |
|---|------|------|
| 1 | 課程介紹 | 課程目標、學習地圖、成果展示 |
| 2 | 台灣的天氣與生活 | 氣象重要性、天氣驅動決策 |
| 3 | 中央氣象署 CWA | 註冊帳號、取得 API Key |
| 4 | API 資料取得 | 使用 `requests` 取得 JSON |
| 5 | JSON 資料結構解析 | 找到氣溫資料的位置 |
| 6 | 提取最高與最低氣溫 | 解析 JSON、轉換結構化資料 |
| 7 | 資料整理與預算 | 使用 Pandas 處理觀察資料 |
| 8 | 建立 SQLite 資料庫 | 建立資料庫、創建資料表、插入氣溫資料 |
| 9 | 資料庫設計 | `TemperatureForecasts` 資料表結構 |
| 10 | 查詢資料驗證 | 使用 SQL 驗證資料 |
| 11 | Streamlit 入門 | 安裝環境、基本結構、Hello World |
| 12 | 從資料庫讀取資料 | 使用 SQL 查詢 |
| 13 | 下拉選單選擇地區 | 互動式操作 |
| 14 | 繪製折線圖 | 一週最高與最低氣溫趨勢 |
| 15 | 顯示資料表格 | 清楚呈現一週資料 |
| 16 | 整合 Web App 介面 | 選地區看氣溫預報 |
| 17 | 進階：台灣地圖視覺化 | 使用 Folium + Streamlit |
| 18 | 選擇日期顯示地圖 | 互動式天氣地圖 |
| 19 | 完整成果展示 | Taiwan Weather Dashboard |
| 20 | 程式碼品質與優化 | 結構清晰、錯誤處理、良好的註解 |
| 21 | 專案上傳至 GitHub | 版本管理與備份 |
| 22 | 延伸應用與想法 | Line Bot、旅遊行程、農業應用、AI 分析 |
| 23 | 回顧與重點整理 | API / JSON / SQLite / Streamlit 總複習 |
| 24 | 下一步：繼續探索 | AI × Data × Real World |

---

## 🚀 快速開始

### 1. 安裝依賴套件

```bash
pip install requests pandas streamlit folium streamlit-folium
```

### 2. 取得 CWA API Key

前往 [中央氣象署 Open Data 平台](https://opendata.cwa.gov.tw/) 註冊並取得 API Key。

### 3. 執行 Streamlit App

```bash
streamlit run app.py
```

---

## 🗄️ 資料庫結構

```sql
CREATE TABLE TemperatureForecasts (
    id        INTEGER PRIMARY KEY,
    regionName TEXT,
    dataDate   TEXT,
    min        REAL,
    max        REAL
);
```

---

## 📊 成果展示

- ✅ 互動式地區選擇下拉選單
- ✅ 一週氣溫折線圖（MaxT / MinT）
- ✅ 氣溫資料表格
- ✅ 台灣地圖色彩視覺化（平均溫度）

---

## 💡 延伸應用

- 天氣提醒 Line Bot
- 旅遊行程建議
- 農業 / 防災應用
- 結合 AI 做氣象分析

---

## 👨‍💻 作者

- GitHub: [@taemiyu](https://github.com/taemiyu)
- Email: sappon77698@gmail.com

---

> *"技術可以解決問題，但更重要的是用技術創造更好的未來！"* — 煥哥

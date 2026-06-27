# 🌙 Luna's Stone Atelier — IG 自動化系統

> 一個結合礦物學知識與身心靈能量的 Instagram 內容自動化品牌系統。

---

## 📁 檔案架構

```
├── mineralogy_data.json      ← 礦石資料 SSOT（唯一真源）
├── brand_config.json         ← 品牌設定、發佈時間、格式規格
├── content_schedule.json     ← 90天排程（116條記錄）
├── manus_instructions.md     ← Manus AI 生成指引
├── KNOWLEDGE_BASE.md         ← 系統知識總覽
├── generated_assets.json     ← 已生成素材記錄
├── assets/
│   ├── stories/              ← Stories PNG
│   ├── posts/                ← Posts Carousel PNG
│   └── reels/                ← Reels PNG + MP4
└── .github/workflows/        ← GitHub Actions 自動化
```

---

## ⚠️ 核心原則：SSOT

**礦石資料唯一真源 = `mineralogy_data.json`**

所有礦石文案、科學數據、脈輪對應，一律從 `mineralogy_data.json` 讀取，
禁止在其他文件另行維護礦石資料表。

---

## 🔑 GitHub Secrets 設定

前往 **Settings → Secrets and variables → Actions**，新增以下 Secrets：

| Secret 名稱 | 說明 |
|-------------|------|
| `IG_USER_ID` | Instagram Business 帳號**數字 ID**（非 @handle，範例：`17841400000000000`）|
| `IG_ACCESS_TOKEN` | Meta Graph API Long-lived Access Token |
| `OPENAI_API_KEY` | OpenAI API Key |

---

## 📅 發佈節奏

| 格式 | 發佈時間（HKT）| 每週次數 |
|------|---------------|----------|
| Reels | 18:00 | 2次（週一、週四）|
| Posts | 12:00 | 2次（週二、週五）|
| Stories | 20:00 | 6次（週一至週五、週日）|

---

## 🚀 快速開始

1. 克隆此 repo
2. 設定好三個 GitHub Secrets（見上表）
3. 檢查 `content_schedule.json`，確認今日排程
4. 使用 Manus 按照 `manus_instructions.md` 生成素材
5. 素材生成後回填 `asset_url`，將 `status` 改為 `generated`
6. 發佈至 IG，將 `status` 改為 `published`

---

## 📊 90天排程總覽（2026-06-15 → 2026-09-12）

| 格式 | 條數 |
|------|------|
| Reels | 26 |
| Posts Carousel | 26 |
| Stories | 64 |
| **合計** | **116** |

---

_Luna's Stone Atelier © 2026_

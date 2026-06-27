# 🌙 Luna's Stone Atelier — IG 自動化系統

> 一個結合礦物學知識與身心靈能量的 Instagram 內容自動化品牌系統。

---

## 📁 檔案架構

```
├── mineralogy_data.json      ← 礦石資料 SSOT（唯一真源，27種礦石）
├── brand_config.json         ← 品牌設定、發佈時間、格式規格、色彩系統
├── content_schedule.json     ← 90天排程（116條記錄）
├── manus_instructions.md     ← Manus AI 操作指引 v3.1
├── BATCH_GENERATE.md         ← Manus 一次性批量生圖指引
├── KNOWLEDGE_BASE.md         ← 系統知識總覽
├── generated_assets.json     ← 已生成素材記錄（Manus 自動回填）
├── assets/
│   ├── stories/              ← story_{YYYY-MM-DD}.png
│   ├── posts/                ← post_{YYYY-MM-DD}_s1.png … _s5.png
│   └── reels/                ← reel_{YYYY-MM-DD}_s1.png … _s6.png + .mp4
└── .github/workflows/        ← GitHub Actions 自動化
```

---

## ⚠️ 核心原則：SSOT

**礦石資料唯一真源 = `mineralogy_data.json`**（共 27 種礦石）

所有礦石文案、科學數據、脈輪對應，一律從 `mineralogy_data.json` 讀取。
禁止在任何其他文件另行維護礦石資料表。

---

## 🔑 GitHub Secrets 設定

前往 **Settings → Secrets and variables → Actions**，新增以下 Secrets：

| Secret 名稱 | 說明 |
|-------------|------|
| `IG_USER_ID` | Instagram Business 帳號**數字 ID**（非 @handle，範例：`17841400000000000`）|
| `OPENAI_API_KEY` | OpenAI API Key（Manus 批量生圖用）|

> ⚠️ `IG_USER_ID` = 純數字 ID，**不是** `@lunas.stone.atelier`
> IG 發布由 Manus IG MCP 負責，**不需要** `IG_ACCESS_TOKEN`。

---

## 📅 發佈節奏

| 格式 | 發佈時間（HKT）| 每週次數 |
|------|---------------|----------|
| Reels | 18:00 | 2次（週一、週四）|
| Posts | 12:00 | 2次（週二、週五）|
| Stories | 20:00 | 6次（週一至週五、週日）|

---

## 🚀 快速開始

### 第一步：事先一次性批量生圖
1. 克隆此 repo
2. 設定好兩個 GitHub Secrets（見上表）
3. 按照 `BATCH_GENERATE.md` 指引，讓 Manus 一次生成 90 天全部素材
4. Manus 將圖片 commit 到 `assets/`，並回填 `generated_assets.json`

### 第二步：自動發布（每日）
5. GitHub Actions 每日定時觸發，組裝 `manus_task.json`
6. Manus 讀取 `manus_task.json` → 從 `assets/` 取備用圖片及文案 → 透過 IG MCP 發布
7. Manus 回填 `published_url`，`status` 自動改為 `published`
8. 發佈後 10 分鐘內，帳號主自行留言引導互動（首 90 分鐘演算法窗口）

---

## 📊 90天排程總覽（2026-06-15 → 2026-09-12）

| 格式 | 條數 |
|------|------|
| Reels（一千零一夜系列）| 26 |
| Posts Carousel | 26 |
| Stories | 64 |
| **合計** | **116** |

---

## 🎨 品牌色彩

| 用途 | 色碼 |
|------|------|
| 主背景 | `#0D0D2B` 深海藍黑 |
| 次背景 | `#1A1A3A` |
| 文字主色 | `#B4918F` 霧玫瑰金 |
| 文字亮部 | `#E8E8F0` |
| 金色點綴 | `#C9A84C` |

---

## 📐 格式規格

| 格式 | 尺寸（4:5）| 輸出 |
|------|------------|------|
| Stories | 1080×1350 px | 1 PNG |
| Posts | 1080×1350 px | 5 PNG |
| Reels | 1080×1350 px | 6 PNG + 1 MP4（15–30 秒）|

---

_Luna's Stone Atelier © 2026_

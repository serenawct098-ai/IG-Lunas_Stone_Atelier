# Luna's Stone Atelier — IG 自動化運營系統

> **帳號：** @lunas.stone.atelier
> **主題：** 一千零一夜礦石風水系列
> **執行週期：** 2026-06-15 至 2026-09-12（90 天）
> **架構模式：** 文案與素材預生成備用 → GitHub Actions 按日期自動發佈

---

## 📁 檔案結構與層級說明

```
IG-Lunas_Stone_Atelier/
│
├── README.md                    ← 本文件（系統總覽 + 維護入口）
├── KNOWLEDGE_BASE.md            ← 唯一知識庫 SSOT（品牌 + 礦石 + 策略全部在此）
│
├── brand_config.json            ← 品牌設定機器讀版（色碼、水印、IG 設定）
├── mineralogy_data.json         ← 礦石資料機器讀版
├── content_schedule.json        ← 90 日內容排程主檔（文案 + Manus Prompt）
├── manus_instructions.md        ← Manus 執行說明（掃描排程 → 批量生成圖文／影片）
├── generated_assets.json        ← Manus 批量生成後回填的資產記錄
│
├── main.py                      ← 發佈引擎（讀取排程 → 呼叫 Meta Graph API）
└── .github/
    └── workflows/
        └── ig-post.yml          ← GitHub Actions 排程觸發器
```

### 五層級分工

| 層級 | 文件 | 作用 | 需要更改時 |
|---|---|---|---|
| **SSOT 知識層** | `KNOWLEDGE_BASE.md` | 品牌、礦石、策略、格式規格全部在此 | 改規範改此文件 |
| **排程層** | `content_schedule.json` | 90 日文案與排程 | 改文案改此檔案 |
| **素材生成層** | `manus_instructions.md` | Manus 批量生成圖文／影片的完整指引 | 改生成流程改此文件 |
| **發佈層** | `main.py` + `.github/workflows/ig-post.yml` | GitHub Actions 自動發佈 | 改發佈邏輯改此兩檔 |
| **機器讀配置層** | `brand_config.json` + `mineralogy_data.json` | 腳本讀取用 JSON | 改品牌或礦石機讀版改此兩檔 |

---

## ⚙️ 系統運作邏輯

```
[KNOWLEDGE_BASE.md]          ←  所有內容的事實依據（SSOT）
        ↓
[content_schedule.json]      ←  90 日預生成文案 + Manus Prompt
        ↓
[Manus 批量生成素材]         →  Stories PNG / Posts PNG×5 / Reels MP4
        ↓ asset_url 回填
[generated_assets.json]      ←  資產記錄（中間檔 + 最終輸出）
        ↓
[GitHub Actions ig-post.yml] ←  每日定時觸發（不依賴即時 AI）
        ↓
[main.py]  →  讀取今日排程 → 呼叫 Meta Graph API → 發佈 IG
```

---

## 🎯 核心規則：三格式內容必須獨立生成

> ⚠️ **重要原則，不可妥協**

- **Stories、Posts（Carousel）、Reels 必須各自獨立生成**
- 同一日期若同時有多格式排程，必須分別生成完全不同的素材
- **嚴禁以同一張圖充當多格式輸出**
- 素材間可以「呼應同一主題」，但視覺設計、文字排版、結構必須各自完整獨立

---

## 📐 格式規格速查

| 格式 | 比例 | 最終輸出 | 數量 |
|---|---|---|---|
| Stories | 4:5（1080×1350px） | 單張 PNG | 1 張 |
| Posts (Carousel) | 4:5（1080×1350px） | 5 張 PNG 套組 | 5 張 |
| Reels | 4:5（1080×1350px） | **15–30 秒 MP4**（由 6 張圖文卡串接生成） | 6 張 PNG 中間檔 + 1 支 MP4 |

> 詳細生成流程與規格，見 `manus_instructions.md`。

---

## 🗓️ 發佈時間表（HKT）

| 格式 | 發佈時間 | 星期 |
|---|---|---|
| Stories | 20:00 | 一、三、四、五、日 |
| Posts (Carousel) | 12:00 | 二、五 |
| Reels | 18:00 | 一、四 |

---

## 🔧 GitHub Secrets 必要設定

前往 **Settings → Secrets and variables → Actions** 新增：

| Secret 名稱 | 說明 |
|---|---|
| `META_ACCESS_TOKEN` | Meta Graph API 長效存取 Token |
| `IG_USER_ID` | Instagram Business 帳號數字 ID |

---

## 📋 啟動清單

- [ ] **Manus 批量生成素材**：交付 `manus_instructions.md` 給 Manus，讓 Manus 掃描 `content_schedule.json` 一次過批量生成所有 Stories PNG / Posts PNG 套組 / Reels MP4，並將 URL 回填至 `content_schedule.json` 的 `asset_url` 欄位及 `generated_assets.json`
- [ ] **設定 GitHub Secrets**：在 repo Settings 新增 `META_ACCESS_TOKEN` 與 `IG_USER_ID`
- [ ] **驗證首發**：手動觸發 `workflow_dispatch` 測試第一條記錄能否成功發佈

---

## 📊 數據監控

每 **14 天 09:00 HKT** 建議人工檢視各格式核心 KPI：

| 格式 | 核心 KPI |
|---|---|
| Stories | 互動率、問答箱回覆數 |
| Posts | 收藏率（Save Rate）、輪播翻頁率 |
| Reels | 完播率、追蹤轉化數 |

第 90 天發佈完成後，輸出總結並規劃下一輪 SOP 策略。

---

## 🛠️ 維護指南

| 需要修改的事項 | 變更哪一個檔案 |
|---|---|
| 品牌規範、礦石資料、內容策略、格式規格 | `KNOWLEDGE_BASE.md` |
| 文案內容、發佈日期、Manus Prompt | `content_schedule.json` |
| Manus 生成素材的執行方式 | `manus_instructions.md` |
| 發佈邏輯、API 呼叫 | `main.py` |
| 自動化排程時間 | `.github/workflows/ig-post.yml` |

---

*最後更新：2026-06-27 | 由 Perplexity AI 同步上下文所有重要更新*

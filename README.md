# Luna's Stone Atelier — IG 自動化運營系統

> **帳號：** @lunas.stone.atelier
> **主題：** 一千零一夠礦石風水系列
> **執行週期：** 2026-06-15 至 2026-09-12（90 天）
> **架構模式：** 文案與素材預生成備用 → GitHub Actions 按日期自動發佈

---

## 📁 檔案結構與層級說明

```
IG-Lunas_Stone_Atelier/
│
├── README.md                    ← 本文件（系統總覽 + 维護入口）
├── KNOWLEDGE_BASE.md            ← 唯一知識庫 SSOT（品牌 + 礦石 + 策略全部在此）
│
├── brand_config.json            ← 品牌設定機器讀版（色碼、水印、IG 設定）
├── mineralogy_data.json         ← 礦石資料機器讀版
├── content_schedule.json        ← 90 日內容排程主檔（文案 + Manus Prompt）
├── manus_prompt_pack.json       ← Manus 批量素材生成 Prompt 包
├── manus_instructions.md        ← Manus 執行說明（掃描排程 → 批量生成圖文）
│
├── main.py                      ← 發佈引擎（讀取排程 → 呼叫 Meta Graph API）
└── .github/
    └── workflows/
        └── ig-post.yml          ← GitHub Actions 排程觸發器
```

### 五層級分工

| 層級 | 文件 | 作用 | 更改時變更 |
|---|---|---|---|
| **SSOT 知識層** | `KNOWLEDGE_BASE.md` | 品牌、礦石、策略全部 | 此文件 |
| **排程層** | `content_schedule.json` | 90 日文案與排程 | 此檔案 |
| **素材生成層** | `manus_instructions.md` + `manus_prompt_pack.json` | Manus 創作指令 | 此兩檔 |
| **發佈層** | `main.py` + `.github/workflows/ig-post.yml` | GitHub Actions 自動發佈 | 此兩檔 |
| **機器讀配置層** | `brand_config.json` + `mineralogy_data.json` | 脚本讀取用 JSON | 此兩檔 |

---

## ⚙️ 系統運作邏輯

```
[KNOWLEDGE_BASE.md]          ←  所有內容的事實依據
        ↓
[content_schedule.json]      ←  90 日預生成文案 + Manus Prompt
        ↓
[Manus 批量生成圖文]        →  asset_url 回填到排程檔
        ↓
[GitHub Actions ig-post.yml] ←  每日定時觸發
        ↓
[main.py]  →  讀取今日排程 → 呼叫 Meta Graph API → 發佈 IG
```

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

- [ ] **Manus 批量生成圖文**：參照 `manus_instructions.md`，掃描 `content_schedule.json`，生成所有 Stories / Posts / Reels 素材，並將公開 URL 回填至各記錄的 `asset_url` 欄位
- [ ] **設定 GitHub Secrets**：在 repo Settings 新增 `META_ACCESS_TOKEN` 與 `IG_USER_ID`
- [ ] **驗證首發**：手動觸發 `workflow_dispatch` 測試第一條記錄能否成功發佈

---

## 📊 數據監控

每 **14 天 09:00 HKT** 建議人工檢視各格式核心 KPI：

| 格式 | 核心 KPI |
|---|---|
| Stories | 互動率、問答笱回覆數 |
| Posts | 收藏率（Save Rate）、輪播翳頁率 |
| Reels | 完播率、追蹤轉化數 |

第 90 天發佈完成後，輸出總結並規劃下一輪 SOP 策略。

---

## 🛠️ 维護指南

| 需要修改的事項 | 變更哪一個檔案 |
|---|---|
| 品牌規範、礦石資料、內容策略 | `KNOWLEDGE_BASE.md` |
| 文案內容、發佈日期、Manus Prompt | `content_schedule.json` |
| Manus 生成圖文的執行觸發方式 | `manus_instructions.md` |
| 發佈逻輯、API 呼叫 | `main.py` |
| 自動化排程時間 | `.github/workflows/ig-post.yml` |

---

*最後更新：2026-06-27*

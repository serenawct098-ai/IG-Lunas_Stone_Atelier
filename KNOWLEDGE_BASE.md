# Luna's Stone Atelier — 知識庫 v2.5
_最後更新：2026-06-29_

---

## ⚠️ 礦石資料唯一真源聲明（SSOT）

> **本文件不維護任何礦石資料表。**
> 所有礦石的科學數據、脈輪對應、光學效應、保養建議、鑑別方法，
> **一律以 `mineralogy_data.json` 為唯一真源（SSOT）**（共 **33 種礦石**）。
>
> 如需查詢礦石資訊，請直接讀取 `mineralogy_data.json`，使用 `id` 欄位對應。
> 禁止在本文件或任何其他文件另行維護礦石資料表。

---

## 0.5 六大核心規範摘要（完整規定見 manus_instructions.md §0.5）

| 規範 | 重點 |
|---|---|
| **R1 防幻覺** | 生成前必透過 GitHub MCP 核實 `mineralogy_data.json`，礦石功效 100% 可溯源，無對應記錄禁止編造 |
| **R2 底部標籤** | 每張圖文及 Reels MP4 全程底部顯示「Luna's Stone Atelier 圖文僅供參考」 |
| **R3 語言規範** | 繁體中文書面語為主、英文為輔；中英並存時中文在上、英文在下 |
| **R4 禁重複文案** | 主題可同，但跨格式/跨日期文案必須不同 |
| **R5 拒過期腳本** | 每次抓取最新 `content_schedule.json` / `manus_task.json`，拒絕快取及舊版 |
| **R6 品牌視覺** | 無圖騰冒充 LOGO；文字商標「Luna's Stone Atelier」；遵守 4:5 安全區 |

---

## 1. 品牌定位

**Luna's Stone Atelier** 是一個深耕礦石文化、結合礦物學知識與身心靈能量的 Instagram 內容品牌。

核心價值：
- **知識深度**：每一顆礦石皆有科學根據，拒絕偽科學
- **美學質感**：深海星空視覺語言，神秘而溫柔
- **能量誠信**：能量描述均以「參考」定位，附免責聲明

---

## 2. 內容格式規格

所有格式規格定義於 `brand_config.json` → `format_specs`。

| 格式 | 尺寸（4:5）| 輸出 |
|------|------------|------|
| Stories | 1080×1350 px | 1 PNG |
| Posts Carousel | 1080×1350 px | 5 PNG |
| Reels | 1080×1350 px | 6 幀圖文 PNG（p1–p6，文字燒入畫面）+ 1 MP4（20–30 秒，無旁白／無字幕軌）|

> 所有格式統一採用 **4:5（1080×1350 px）**。

---

## 3. 三階段發布策略

階段定義詳見 `brand_config.json` → `phases`。

| 階段 | Carousel 時期 | Reels 時期 | 貼文策略 |
|------|-------------|-----------|----------|
| 破圈引流 | 2026-06-16 → 07-14 | 2026-06-15 → 07-09 | 追蹤號召，建立首印象 |
| 信任建立 | 2026-07-17 → 08-11 | 2026-07-13 → 08-06 | 收藏號召，展示專業深度 |
| 產品轉化 | 2026-08-14 → 09-08 | 2026-08-10 → 09-07 | Profile 連結，導向購買 |

---

## 4. 發布時間表

發布時間定義於 `brand_config.json` → `publish_schedule`。

| 格式 | 發布時間（HKT）| 每週次數 | 發布日 |
|------|---------------|---------|-------|
| Reels | 18:00 | 2 次 | 週一、週四 |
| Posts Carousel | 12:00 | 2 次 | 週二、週五 |
| Stories | 20:00 | 5 次 | 週一、週三、週四、週五、週日 |

---

## 5. 連載系列

### 5.1 一千零一夜礦石風水系列（Reels）
- 目標集數：**25 集**（Ep 1–25，每週 2 次・週一/四）
- **格式：純圖文（無旁白·無語音·無字幕軌）**——所有文字直接燒入 6 幀圖像（p1–p6）
- 每集文字存於 `content_schedule.json` → `frames` 欄位（`p1`–`p6`），每幀含 `role`／`headline`／`body`／`en_text`
- 幀角色：p1=hook、p2–p3=develop、p4–p5=climax、p6=cta
- 每集結尾（p6）必須預告下集礦石，形成追劇感
- 集數記錄於 `content_schedule.json` → `episode` 欄位
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

### 5.2 今日能量卡（Stories）
- 每次發布單一礦石能量主題
- 必須包含互動問句
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

### 5.3 礦石知識乾貨（Posts Carousel）
- 目標篇數：**25 篇**（Post 1–25，每週 2 次・週二/五）
- 每次 5 張，涵蓋科學 / 美學 / 能量 / 保養
- **封面必須含數字或問句**（止滑設計）
- **第 5 張必須含「收藏」導向 CTA**（Save Rate 是 Carousel 最高排名訊號）
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

---

## 6. 連接機制

### GitHub 與 Manus 透過 MCP 互通

| MCP 連接 | 用途 |
|----------|------|
| **GitHub MCP** | Manus 直接讀取 repo 中的 `manus_task.json`、`content_schedule.json` 等檔案，以及 commit 回填狀態 |
| **IG MCP** | Manus 完成 Instagram 發布 |

> 不需要任何 GitHub Secrets 或 API Key。

---

## 7. 資料架構總覽

```
礦石資料  ←  mineralogy_data.json   （SSOT，33 種礦石，禁止在其他文件另行維護）
品牌設定  ←  brand_config.json      （發布時間、格式規格、三階段 CTA、色彩系統）
排程內容  ←  content_schedule.json  （90天排程 111 條：Reels 25 + Posts 25 + Stories 61，stone_id 對應 SSOT）
生成指引  ←  manus_instructions.md  （Manus AI 操作規則 v5.0、格式規格、Caption 規則）
知識總覽  ←  KNOWLEDGE_BASE.md      （本文件，系統導覽，不維護礦石表）
批量生圖  ←  BATCH_GENERATE.md      （Manus 一次性批量生圖指引）
```

---

## 8. 2026 IG 演算法重點規則

詳細規則見 `manus_instructions.md` §5–6。各指標目標基準：

| 格式 | 關鍵指標 | 目標 | 達標後效果 |
|---|---|---|---|
| Carousel | saves-to-likes ratio | > 0.15 | 觸及提升 230–340% |
| Carousel | swipe completion rate | > 70% | 系統推薦 Explore |
| Reels | 3 秒留存率 | > 60% | 觸及比弱 Hook 高 5–10× |
| Reels | 完播率 | > 70% | 系統推 Explore |
| Reels | Sends/Reach | > 3% | 5–10× 額外觸及 |

操作要點：
- **SEO First Line**：Caption 第一行必須含礦石名稱 + 功能關鍵詞
- **Hashtag 控制**：每則 3–5 個，主題相關，禁止堆砌
- **Save/Share 導向**：Posts 導向 Save；Reels 導向 Share（Sends）
- **首 90 分鐘**：發布後立即 Stories 轉發，帳號主 10 分鐘內自行留言引導互動
- **Reels Hook**：首 3 秒必須有止滑鉤（`第N夜｜{礦石}的秘密`）
- **禁止 TikTok 水印**：有水印的 Reels 被演算法降級

---

## 10. 紫微斗數 × 奇門遁甲 知識庫參考（ziwei_qimen SSOT）

> **本節為 `serenawct098-ai/ziwei_qimen` 倉庫引用說明。**
> 所有紫微斗數及奇門遁甲計算，以該倉庫引擎為唯一真源（SSOT），禁止自行推算。

### 引擎清單

| # | 檔案 | 版本 | 用途 |
|---|------|------|------|
| ① | `traditional_core_engine_v2.1.json` | v2.1 | SSOT 公式（命宮/四化/安星查表） |
| ② | `full_compute_flow_v1.4.json` | v1.4 | 高維推算流程（precisionGate/時空橋樑） |
| ③ | `interpretation_engine_v1.1.json` | v1.1 | 計算步驟同步層 |
| ④ | `traditional_mythos_engine_v1.3.1.json` | v1.3.1 | 卷一·正統解讀（命格/格局） |
| ⑤ | `modern_quantum_resonance_engine_v2.1.json` | v2.1 | 卷二·現代壓測（盲點偵測） |
| ⑥ | `dual_parallel_fusion_engine_v1.1.json` | v1.1 | 雙軌橋樑（紫微↔奇門映射） |
| ⑦ | `qimen_fengshui_layout_module_v0.1.json` | v0.1 | 奇門風水佈局（催旺/化煞，2026年） |

### 使用規則
- 所有紫微/奇門相關 Reels 內容（Ep9、Ep10、Ep11、Ep12），文案數據以 ziwei_qimen 引擎為唯一參考
- 奇門風水佈局數據（正東八白財位、五黃禁區等）來源：`qimen_fengshui_layout_module_v0.1.json`
- 2026年飛星鎖定丙午年，方位禁區（正南五黃 `forbidden=true`）不可更改
- 四化版本：`sihua_pa_locked`；起局：拆補法；閏月：三合派南派
- **禁止 LLM 心算推導**：所有公式查表，計算層程式讀 JSON 後確定性輸出

# Luna's Stone Atelier — 知識庫 v2.2
_最後更新：2026-06-27_

---

## ⚠️ 礦石資料唯一真源聲明（SSOT）

> **本文件不維護任何礦石資料表。**
> 所有礦石的科學數據、脈輪對應、光學效應、保養建議、鑑別方法，
> **一律以 `mineralogy_data.json` 為唯一真源（SSOT）。**
>
> 如需查詢礦石資訊，請直接讀取 `mineralogy_data.json`，使用 `id` 欄位對應。
> 禁止在本文件或任何其他文件另行維護礦石資料表。

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
| Posts | 1080×1350 px | 5 PNG |
| Reels | 1080×1350 px | 6 PNG 中間素材 + 1 MP4（15–30 秒）|

> 所有格式統一採用 **4:5（1080×1350 px）**。

---

## 3. 三階段發佈策略

階段定義詳見 `brand_config.json` → `phases`。

| 階段 | 時期 | 核心目標 |
|------|------|---------|
| 破圈引流 | 2026-06-15 → 07-14 | 觸及新受眾，建立品牌印象 |
| 信任建立 | 2026-07-15 → 08-13 | 深度知識輸出，建立專業信任 |
| 產品轉化 | 2026-08-14 → 09-12 | 引導至產品頁，促成購買 |

---

## 4. 發佈時間表

發佈時間定義於 `brand_config.json` → `publish_schedule`。

| 格式 | 發佈時間（HKT）| 每週次數 |
|------|---------------|----------|
| Reels | 18:00 | 2次（週一、週四）|
| Posts | 12:00 | 2次（週二、週五）|
| Stories | 20:00 | 6次（週一至週五、週日）|

---

## 5. 連載系列

### 5.1 一千零一夜礦石風水系列（Reels）
- 目標集數：25 集（每週 2 次）
- 每集結尾必須預告下集礦石，形成追劇感
- 集數記錄於 `content_schedule.json` → `episode` 欄位
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

### 5.2 今日能量卡（Stories）
- 每次發佈單一礦石能量主題
- 必須包含互動問句
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

### 5.3 礦石深度科普（Posts Carousel）
- 每次 5 張，涵蓋科學 / 美學 / 能量 / 保養
- 封面必須含數字或問句（止滑設計）
- 礦石資料**必須**從 `mineralogy_data.json` 讀取

---

## 6. GitHub 環境設定

### 必要 Secrets（Settings → Secrets and variables → Actions）

| Secret 名稱 | 說明 |
|-------------|------|
| `IG_USER_ID` | Instagram Business 帳號**數字 ID**（非 @handle，例：`17841400000000000`）|
| `OPENAI_API_KEY` | OpenAI API Key（Manus 批量生圖用）|

> ⚠️ `IG_USER_ID` 的值是一串**純數字**，不是 `@lunas.stone.atelier` 帳號名稱。
> IG 發布由 Manus IG MCP 負責，**不需要** `IG_ACCESS_TOKEN`。

---

## 7. 資料架構總覽

```
礦石資料  ←  mineralogy_data.json   （SSOT，唯一真源，禁止在其他文件另行維護）
品牌設定  ←  brand_config.json      （發佈時間、格式規格、三階段 CTA、色彩系統）
排程內容  ←  content_schedule.json  （90天116條排程，stone_id 對應 SSOT）
生成指引  ←  manus_instructions.md  （Manus AI 操作規則、格式規格、Caption 規則）
素材記錄  ←  generated_assets.json  （Manus 回填，人工勿直接編輯資產 URL）
知識總覽  ←  KNOWLEDGE_BASE.md      （本文件，系統導覽，不維護礦石表）
批量生圖  ←  BATCH_GENERATE.md      （Manus 一次性批量生圖指引）
```

---

## 8. 2026 IG 演算法重點規則

詳細規則見 `manus_instructions.md` §5–§6。摘要：

- **SEO First Line**：Caption 第一行必須含礦石名稱 + 功能關鍵詞
- **Hashtag 控制**：每則 3–5 個，主題相關，禁止堆砌
- **Save/Share 導向**：Posts 優先優化 Save；Reels 優先優化 Share
- **首 90 分鐘**：發佈後立即 Stories 轉發，帳號主 10 分鐘內自行留言引導互動
- **Reels Hook**：首 3 秒必須有止滑鉤（`第N夜｜{礦石}的秘密`）

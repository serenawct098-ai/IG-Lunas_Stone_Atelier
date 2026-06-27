# Luna's Stone Atelier — 知識庫 v2.0
_最後更新：2026-06-27_

---

## ⚠️ 礦石資料唯一真源聲明

> **本文件不維護礦石資料表。**
> 所有礦石的科學數據、脈輪對應、保養建議、鑑別方法，
> **一律以 `mineralogy_data.json` 為唯一真源（SSOT）。**
>
> 如需查詢礦石資訊，請直接讀取 `mineralogy_data.json`，對應 `id` 欄位。

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

| 格式 | 尺寸 | 輸出 |
|------|------|------|
| Stories | 1080×1350 px | 1 PNG |
| Posts | 1080×1350 px | 5 PNG |
| Reels | 1080×1350 px | 6 PNG + 1 MP4（15–30 秒）|

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

| 格式 | 發佈時間（HKT）|
|------|---------------|
| Stories | 20:00 |
| Posts | 12:00 |
| Reels | 18:00 |

---

## 5. 連載系列

### 5.1 一千零一夜礦石風水系列（Reels）
- 目標集數：25 集（每週 2 次）
- 每集結尾必須預告下集礦石，形成追劇感
- 集數記錄於 `content_schedule.json` → `episode` 欄位

### 5.2 今日能量卡（Stories）
- 每次發佈單一礦石能量主題
- 必須包含互動問句

### 5.3 礦石深度科普（Posts Carousel）
- 每次 5 張，涵蓋科學 / 美學 / 能量 / 保養
- 封面必須含數字或問句

---

## 6. GitHub 環境設定

### 必要 Secrets（Settings → Secrets and variables → Actions）

| Secret 名稱 | 說明 |
|-------------|------|
| `IG_USER_ID` | Instagram Business 帳號**數字 ID**（非 @handle）|
| `IG_ACCESS_TOKEN` | Meta Graph API Long-lived Access Token |
| `OPENAI_API_KEY` | OpenAI API Key |

> ⚠️ `IG_USER_ID` 的值是一串數字，不是 `@lunas.stone.atelier`。

---

## 7. 資料架構總覽

```
礦石資料  ←  mineralogy_data.json  （SSOT，唯一真源）
品牌設定  ←  brand_config.json
排程內容  ←  content_schedule.json
生成指引  ←  manus_instructions.md
知識總覽  ←  KNOWLEDGE_BASE.md（本文件）
```

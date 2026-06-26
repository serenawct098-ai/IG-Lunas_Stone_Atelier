# Manus 批量素材生成執行說明

> **版本：** v2.1 | **最後更新：** 2026-06-27 | **執行對象：** Manus AI
>
> 本文件為 Manus 執行素材批量生成的唯一操作指引。
> 生成前必須先完整讀取本文件，嚴格遵守所有規格，不得自行推斷或捏造資料。

---

## 一、任務概述

掃描 `content_schedule.json`，按每條記錄的 `manus_prompt` 欄位，**一次過**批量生成所有 Stories、Posts（Carousel）、Reels 素材，並將最終資產 URL 回填至各記錄的 `asset_url` 欄位。

> **重要：三種格式必須獨立生成，互不混用，不得以同一張圖充當多種格式輸出。**

---

## 二、核心規則（所有格式通用）

### 2.1 品牌色（必須嚴格遵守）
| 角色 | 名稱 | HEX |
|---|---|---|
| 主背景 | 深海軍藍 | `#0D0D2B` |
| 次要背景 | 深藍紫色 | `#1A1A3A` |
| 輔色 | 深紫 | `#2D1B4E` |
| 主文字／圖騰 | 霧玫瑰金 | `#B4918F` |
| 亮部強調 | 月白銀 | `#E8E8F0` |
| 點綴 | 金色 | `#C9A84C` |

**禁止使用任何品牌色以外的顏色。**

### 2.2 標籤（強制）
- 所有畫面底部必須清楚顯示：`Luna's Stone Atelier 圖文僅供參考`
- 標籤文字不得被裁切、遮擋或縮小至難以辨識

### 2.3 語言規範
- 繁體中文為主，英文為輔
- 雙語排版時中文置於英文上方
- 嚴禁使用簡體字/其他自創文字/亂碼

### 2.4 礦石資料
- 所有礦石數據必須以 `mineralogy_data.json` 為唯一依據
- 缺乏資料時拒絕捏造，留空或標記「待補充」

### 2.5 三格式獨立生成原則（核心規則）
- **Stories、Posts、Reels 必須各自獨立生成**
- 同一日期若同時有三格式排程，必須分別生成三組完全不同的素材
- 嚴禁以同一張靜態圖充當多格式輸出
- 素材間可以「呼應同一主題」，但視覺設計、文字內容、排版、結構必須各自完整獨立不同

---

## 三、格式規格

### 3.1 Stories 格式規格
- **比例：** 4:5（1080×1350px）
- **輸出：** 單張 PNG（或 JPG）
- **結構：**
  - Hook 行（大字，吸引停留）
  - 主要資訊（1–3 個重點，配圖或礦石插圖）
  - 互動元素文字（如：「留言你想解答的問題」）
  - 標籤（底部）
- **檔名：** `assets/stories/story_YYYY-MM-DD.png`

### 3.2 Posts（Carousel）格式規格
- **比例：** 4:5（1080×1350px）
- **輸出：** 5 張 PNG，組成 1 套 Carousel
- **卡片結構（固定 5 張）：**
  1. 封面止滑卡（Hook）
  2. 科學定位（成分、硬度、化學式）
  3. 美學亮點（色澤、光學效應）
  4. 能量與心理（脈輪、使用建議）
  5. 保養提醒 + CTA（行動呼籲 + 底部標籤）
- **檔名：**
  - `assets/posts/post_YYYY-MM-DD_s1.png` … `_s5.png`
- **asset_url 回填：** 填入 5 張圖的 URL 陣列

### 3.3 Reels 格式規格（⚠️ 注意：輸出為 MP4 短影片）
- **比例：** 4:5（1080×1350px）
- **最終輸出：** 1 支 15–30 秒 MP4 短影片
- **生成流程：**
  1. 先生成 **6 張 4:5 靜態圖文卡**（PNG）
  2. 再將 6 張圖文卡串接，輸出成 **1 支 MP4**
- **6 張卡片結構（固定）：**
  1. Hook（大字止滑，製造好奇）
  2. 知識點 A（科學定位）
  3. 知識點 B（美學亮點）
  4. 知識點 C（能量主題）
  5. 知識點 D（延伸應用／保養）
  6. CTA（點擊了解更多 / 追蹤 / 問答箱）
- **MP4 規格：**
  - 每張停留時間：2.5–5 秒（總長 15–30 秒）
  - 轉場：簡潔品牌一致（淡入淡出或位移），不可花巧
  - 可加輕微動態（縮放、淡入淡出），但核心仍是圖文卡
  - 底部標籤必須在整段影片全程可見
  - 禁止底部字幕；可使用畫面內圖形文字（graphic text）
- **檔名：**
  - 中間素材：`assets/reels/reel_YYYY-MM-DD_s1.png` … `_s6.png`
  - 最終影片：`assets/reels/reel_YYYY-MM-DD.mp4`
- **asset_url 回填：** 填入最終 MP4 的 URL

---

## 四、執行步驟

```
步驟 1：讀取 content_schedule.json
  → 逐條掃描所有記錄
  → 按 type 分類為：stories / post / reels

步驟 2：批量生成 Stories 素材
  → 逐條按 manus_prompt 生成 1 張 PNG
  → 存檔至 assets/stories/

步驟 3：批量生成 Posts 素材
  → 逐條按 manus_prompt 生成 5 張 PNG（Carousel 套組）
  → 存檔至 assets/posts/

步驟 4：批量生成 Reels 素材
  → 逐條按 manus_prompt 生成 6 張 PNG 圖文卡
  → 將 6 張卡串接輸出成 1 支 15–30 秒 MP4
  → 存檔至 assets/reels/

步驟 5：更新 generated_assets.json
  → 記錄每條記錄的所有已生成資產（PNG 中間檔 + 最終輸出 URL）

步驟 6：回填 content_schedule.json
  → 將最終資產 URL 填入對應記錄的 asset_url 欄位
  → Stories → PNG URL
  → Posts → 5 張 PNG URL 陣列
  → Reels → MP4 URL
```

---

## 五、generated_assets.json 記錄格式

```json
{
  "generated_at": "YYYY-MM-DDTHH:MM:SS+08:00",
  "assets": [
    {
      "date": "YYYY-MM-DD",
      "type": "stories",
      "final_asset": "https://..../assets/stories/story_YYYY-MM-DD.png"
    },
    {
      "date": "YYYY-MM-DD",
      "type": "post",
      "slides": [
        "https://..../assets/posts/post_YYYY-MM-DD_s1.png",
        "https://..../assets/posts/post_YYYY-MM-DD_s2.png",
        "https://..../assets/posts/post_YYYY-MM-DD_s3.png",
        "https://..../assets/posts/post_YYYY-MM-DD_s4.png",
        "https://..../assets/posts/post_YYYY-MM-DD_s5.png"
      ],
      "final_asset": "https://..../assets/posts/post_YYYY-MM-DD_s1.png"
    },
    {
      "date": "YYYY-MM-DD",
      "type": "reels",
      "frames": [
        "https://..../assets/reels/reel_YYYY-MM-DD_s1.png",
        "https://..../assets/reels/reel_YYYY-MM-DD_s2.png",
        "https://..../assets/reels/reel_YYYY-MM-DD_s3.png",
        "https://..../assets/reels/reel_YYYY-MM-DD_s4.png",
        "https://..../assets/reels/reel_YYYY-MM-DD_s5.png",
        "https://..../assets/reels/reel_YYYY-MM-DD_s6.png"
      ],
      "final_asset": "https://..../assets/reels/reel_YYYY-MM-DD.mp4"
    }
  ]
}
```

---

## 六、禁止事項清單

| ❌ 禁止 | ✅ 正確做法 |
|---|---|
| 以同一張圖充當多格式輸出 | 每格式獨立生成 |
| Reels 只輸出靜態 PNG | Reels 必須輸出 MP4 |
| Reels 只輸出 MP4 而不保留 PNG 中間檔 | PNG 中間檔與 MP4 均須保存 |
| 捏造礦石數據 | 以 mineralogy_data.json 為唯一依據 |
| 使用品牌色以外顏色 | 嚴格使用六色品牌色系 |
| 標籤置於文案而非畫面 | 標籤必須嵌入圖片底部 |
| 使用簡體字 | 全繁體中文 |
| AI 自行推斷未列礦石資料 | 缺乏資料時標記「待補充」 |

---

*本文件最後由 Perplexity AI 依上下文更新記錄同步更新於 2026-06-27。*

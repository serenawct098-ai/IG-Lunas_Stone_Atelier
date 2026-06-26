# Manus 批量素材生成指令 — Luna's Stone Atelier

> **版本：** v2.5 | **最後更新：** 2026-06-27
> **定位：** 給 Manus 的唯一執行說明。Manus 只負責批量生成視覺素材，不負責文案撰寫、排程管理或發佈。

---

## 1. 任務背景

本 repo 採用「**預生成備用**」架構：

1. 文案與 Manus Prompt 已預先寫入 `content_schedule.json`
2. **Manus 一次過批量生成**所有 Stories / Posts / Reels 視覺素材
3. 素材生成後，GitHub Actions 按日期自動發佈，不再即時呼叫 AI

---

## 2. 重要技術限制說明

> **Manus `map` 工具的 `output_schema` 不支援 `list[file]` 類型。**

- **每一次 `map` 只輸出一個檔案**（單一 `file` 類型）
- 多張圖需對每張分別執行一次 `map`，不得嘗試一次回傳多個檔案
- `generated_assets.json` 的每張圖各為獨立一條記錄

---

## 3. 核心規則：三格式內容必須獨立生成

> ⚠️ **這是本文件最重要的規則。**

**Stories、Posts (Carousel)、Reels 三個格式的主題可以相近，但每個格式的圖片與文字內容必須完全不同。**

| 格式 | 內容定位 | 視覺風格 | 文字內容要求 |
|---|---|---|---|
| **Stories** | 情緒促提、沼気問答、選購小貼士 | 寬鬆、大字、文字少、眼焉感強 | 每張不超過 20 字，以情緒/回應/行動為驅動 |
| **Posts (Carousel)** | 深度知識教學、詳細說明 | 圖文平衡、小標題+正文、資訊層次分明 | 每頁最多 60 字，以教育/分析/比較為驅動 |
| **Reels** | 輕音流、聯賫展示、動態節奏 | 每張卡文字再處理為動態影片 | 每張 PNG 平均 30–40 字，語氣輕快流暢 |

### 3.1 內容分流細則

同一主題周（例：「白水晶」）與同一本幺内的 Stories / Posts / Reels，小必須遵守下列分流原則：

**内容角度必須不同：**
- Stories → 情緒切入（你有沒有感點過「白水晶讓心上輕了」？）
- Posts → 知識深入（白水晶的磁場成分、產地分辨、保養方法）
- Reels → 視覺展示（白水晶兩形對比、光折射長相等身临其境的圖片組）

**視覺排版必須不同：**
- 禁止圖片排版、背景、主圖健元素相同（就算主題相同）
- 外框、引文框、色塊布局必須每次改變，不得直接復用同一模板

**文字内容必須不同：**
- 禁止直接複製或稍作改寫其他格式的文字內容
- 文案已預先寫入 `content_schedule.json` 的 `caption` 欄位，每條記錄的 `caption` 都不同，才能保證規格內文字不重複
- 圖片內的文字必須從 `manus_prompt` 內的 `slide_copy` 或 `visual_brief` 提取，不得自行複製其他格式的文字

### 3.2 自檢問題（每次生成前必須對照）

在生成每一張素材前，自問：

- [ ] 這張素材的圖片排版與同主題的 Stories / Posts / Reels 是否**外觀不同**？
- [ ] 這張素材的文字內容是否是為這個格式**專屬的角度**（情緒/教育/展示）？
- [ ] 是否從 `manus_prompt` 的 `slide_copy` 或 `visual_brief` 提取文字，而非自行複製？

如果三項任一指向「否」，必須重新將該張素材小復從 `manus_prompt` 重新生成。

---

## 4. 執行步驟

### Step 1：讀取排程

掃描 `serenawct098-ai/IG-Lunas_Stone_Atelier` repo 內的 `content_schedule.json`。  
**只處理** `"status": "pending"` 的記錄。

每條記錄讀取以下欄位：

| 欄位 | 說明 |
|---|---|
| `date` | 發佈日期，用作輸出檔名 |
| `type` | `stories` / `post` / `reel` |
| `image_asset_key` | 輸出檔對應的唯一識別 key |
| `visual_brief` | 視覺方向簡述（參考用） |
| `manus_prompt` | 生成指令（執行依據），必包含 `slide_copy` 子欄位 |

### Step 2：按格式生成素材

| 格式 | 生成規格 | 執行次數 | 內容來源 |
|---|---|---|---|
| **Stories** | 3 張靜態圖文，4:5（1080×1350px） | **3 次** | `manus_prompt.slide_copy.stories` |
| **Posts (Carousel)** | 6 頁靜態圖文，4:5（1080×1350px） | **6 次** | `manus_prompt.slide_copy.posts` |
| **Reels** | 6 張 PNG 中間素材 + 1 支 MP4 | **6+1 次** | `manus_prompt.slide_copy.reels` |

> ⚠️ 每個格式的圖片文字必從對應的 `slide_copy.格式名` 子欄位提取，不得跟其他格式共用或相互複製。

### Step 3：Reels 圖文卡結構（強制）

Reels 的 6 張圖文卡必須依以下固定結構排列：

| 張序 | 角色 | 內容要求 |
|---|---|---|
| **第 1 張** | **Hook** | 吸引注意的標題句（繁中）＋英文副標；視覺需突出、留白充裕 |
| **第 2 張** | **知識點 A** | 礦石學核心事實（繁中詳述）＋英文精簡版 |
| **第 3 張** | **知識點 B** | 第二個礦石知識點或深化說明 |
| **第 4 張** | **知識點 C** | 第三個知識點或應用場景 |
| **第 5 張** | **知識點 D / 延伸** | 延伸知識、禁忌提示或選購貼士 |
| **第 6 張** | **CTA** | 邀請互動／儲存／追蹤；品牌標誌感最強 |

**每張文字規範：**
- 繁體中文主標題：字體大、粗、清晰易讀
- 繁體中文正文：每張不超過 40 字（Reels 节奏輕快）
- 英文輔助文字：置於中文下方，字體縮小至中文的 60%
- 禁止使用簡體字

### Step 4：Reels MP4 合成規格

| 規格項目 | 要求 |
|---|---|
| 輸出格式 | MP4（H.264） |
| 比例 | 4:5（1080×1350px） |
| 總長度 | 15–30 秒 |
| 每張停留 | 約 2.5–5 秒 |
| 轉場 | 簡潔淡入淡出或輕微位移 |
| 水印 | 必須嵌入每一幀 |
| 音頻 | 靜音輸出 |

### Step 5：檔名規則

```
Stories : assets/stories/stories_YYYY-MM-DD_slide1.png
          assets/stories/stories_YYYY-MM-DD_slide2.png
          assets/stories/stories_YYYY-MM-DD_slide3.png

Posts   : assets/posts/post_YYYY-MM-DD_p1.png … p6.png

Reels   : assets/reels/reel_YYYY-MM-DD_s1.png … s6.png
          assets/reels/reel_YYYY-MM-DD.mp4
```

### Step 6：輸出 `generated_assets.json`

**每張 PNG 各一條記錄，MP4 另佔一條記錄**，Reels 共 7 條：

```json
[
  {
    "image_asset_key": "stories_20260627_slide1",
    "date": "2026-06-27",
    "type": "stories",
    "slide_index": 1,
    "file_path": "assets/stories/stories_2026-06-27_slide1.png",
    "asset_url": ""
  },
  {
    "image_asset_key": "reel_20260629_s1",
    "date": "2026-06-29",
    "type": "reel",
    "slide_index": 1,
    "slide_role": "hook",
    "file_path": "assets/reels/reel_2026-06-29_s1.png",
    "asset_url": ""
  },
  {
    "image_asset_key": "reel_20260629_mp4",
    "date": "2026-06-29",
    "type": "reel",
    "slide_index": null,
    "slide_role": "final_video",
    "file_path": "assets/reels/reel_2026-06-29.mp4",
    "asset_url": ""
  }
]
```

> ✅ `content_schedule.json` 內 Reels 記錄的 `asset_url` 應指向 MP4 路徑。

---

## 5. 品牌規範（強制）

### 5.1 色彩

| 角色 | HEX |
|---|---|
| 主背景 | `#0D0D2B` |
| 次要背景 | `#1A1A3A` |
| 輔色背景 | `#2D1B4E` |
| 主文字／圖騰 | `#B4918F` |
| 亮部強調 | `#E8E8F0` |
| 金色點綴 | `#C9A84C` |

### 5.2 水印

```
Luna's Stone Atelier  圖文僅供參考
```
- 位置：右下角或左下角，字體細小但清晰可讀
- 不可僅寫在文案欄，必須直接嵌入畫面
- MP4 必須貫穿每一幀

### 5.3 語言
- 繁體中文為主，英文為輔；英文置於中文下方
- 英文字體大小為中文的 60%
- 禁止使用簡體字

### 5.4 礦石學資料
- 嚴禁捏造礦石學數據
- 只視覺化已提供的文案事實，不自行改寫
- 如有疑問，以 `KNOWLEDGE_BASE.md` 第 3 節為準

---

## 6. 禁止事項

- ❌ **禁止 Stories / Posts / Reels 共用、複製或稍作改寫相同素材**
- ❌ 禁止素材圖片文字自行撰寫，必須從 `manus_prompt.slide_copy` 提取
- ❌ 禁止使用品牌色以外的任何顏色
- ❌ 禁止省略 Reels MP4 最終輸出
- ❌ 禁止捏造礦石學數據
- ❌ 禁止省略水印（包括 MP4 每一幀）
- ❌ 禁止在單一 `map` 輸出多個檔案
- ❌ 禁止使用簡體字
- ❌ Reels 各張禁止省略指定角色（Hook / 知識點 / CTA）
- ❌ Reels `asset_url` 禁止指向 PNG

---

## 7. 完成後

1. 將所有素材上傳至 repo `assets/` 目錄
2. 提交 `generated_assets.json`
3. 如能回填，更新 `content_schedule.json` 的 `asset_url`（Reels 指向 MP4）
4. 通知操作者：批量生成完成，GitHub Actions 可按排程自動發佈

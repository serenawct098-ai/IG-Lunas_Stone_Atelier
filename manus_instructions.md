# Manus 批量素材生成指令 — Luna's Stone Atelier

> **版本：** v2.4 | **最後更新：** 2026-06-27
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

因此，所有素材輸出必須遵守以下規則：

- **每一次 `map` 只輸出一個檔案**（單一 `file` 類型）
- 多張圖（如 Stories 3 張、Reels 6 張、Carousel 6 頁）需要**對每張分別執行一次 `map`**，不得嘗試一次回傳多個檔案
- `generated_assets.json` 的每張圖各為獨立一條記錄（見下方範例）

---

## 3. 執行步驟

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
| `manus_prompt` | 生成指令（執行依據） |

### Step 2：按格式生成素材

| 格式 | 生成規格 | 執行次數 |
|---|---|---|
| **Stories** | 3 張靜態圖文，4:5（1080×1350px） | 每張分別執行 → **3 次** |
| **Posts (Carousel)** | 6 頁靜態圖文，4:5（1080×1350px） | 每頁分別執行 → **6 次** |
| **Reels** | 先生成 6 張靜態圖文卡（4:5），再串成 1 支 15–30 秒 MP4 | 每張 PNG 分別執行（**6 次**），最後合成 MP4（**1 次**）|

> ✅ Reels 最終發佈資產為 **MP4 影片**；6 張 PNG 為中間製作素材，需一併上傳備存。

---

### Step 3：Reels 圖文卡結構（強制）

Reels 的 6 張圖文卡必須依以下固定結構排列，每張均需包含繁體中文主文字與英文輔助說明：

| 張序 | 角色 | 內容要求 |
|---|---|---|
| **第 1 張** | **Hook（引子）** | 吸引注意的標題句（繁中）＋英文副標；視覺需突出、留白充裕 |
| **第 2 張** | **知識點 A** | 礦石學核心事實（繁中詳述）＋英文精簡版；可搭配礦石示意排版 |
| **第 3 張** | **知識點 B** | 第二個礦石知識點或深化說明（繁中）＋英文；圖文比例平衡 |
| **第 4 張** | **知識點 C** | 第三個知識點或應用場景（繁中）＋英文；可用列點或數字排版 |
| **第 5 張** | **知識點 D / 延伸** | 延伸知識、禁忌提示或選購貼士（繁中）＋英文；視覺稍作收斂 |
| **第 6 張** | **CTA（行動呼籲）** | 邀請互動／儲存／追蹤（繁中）＋英文；品牌標誌感最強的一張 |

**每張文字規範：**
- 繁體中文主標題：字體大、粗、清晰易讀
- 繁體中文正文：每張不超過 60 字
- 英文輔助文字：置於中文下方，字體縮小至中文的 60%
- 禁止使用簡體字

---

### Step 4：Reels MP4 合成規格

完成 6 張 PNG 後，將其串接合成為 1 支 MP4：

| 規格項目 | 要求 |
|---|---|
| **輸出格式** | MP4（H.264） |
| **比例** | 4:5（1080×1350px） |
| **總長度** | 15–30 秒 |
| **每張停留時間** | 約 2.5–5 秒（依總長度均分） |
| **轉場效果** | 簡潔淡入淡出或輕微位移，不使用花巧特效 |
| **動態元素** | 可加輕微縮放或淡入淡出，核心仍為靜態圖文卡 |
| **水印** | 必須嵌入每一幀，位置固定於右下角或左下角 |
| **音頻** | 靜音輸出（無背景音樂），發佈者可自行在 IG 加入音樂 |

---

### Step 5：檔名規則

```
Stories 第 1 張 : assets/stories/stories_YYYY-MM-DD_slide1.png
Stories 第 2 張 : assets/stories/stories_YYYY-MM-DD_slide2.png
Stories 第 3 張 : assets/stories/stories_YYYY-MM-DD_slide3.png

Posts 第 1 頁   : assets/posts/post_YYYY-MM-DD_p1.png
Posts 第 2 頁   : assets/posts/post_YYYY-MM-DD_p2.png
...             （共 6 頁）

Reels 中間素材  : assets/reels/reel_YYYY-MM-DD_s1.png
                  assets/reels/reel_YYYY-MM-DD_s2.png
                  assets/reels/reel_YYYY-MM-DD_s3.png
                  assets/reels/reel_YYYY-MM-DD_s4.png
                  assets/reels/reel_YYYY-MM-DD_s5.png
                  assets/reels/reel_YYYY-MM-DD_s6.png

Reels 最終影片  : assets/reels/reel_YYYY-MM-DD.mp4
```

---

### Step 6：輸出 `generated_assets.json`

**每一張 PNG 各為一條記錄，MP4 另佔一條記錄**，Reels 共 7 條：

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
    "image_asset_key": "reel_20260629_s6",
    "date": "2026-06-29",
    "type": "reel",
    "slide_index": 6,
    "slide_role": "cta",
    "file_path": "assets/reels/reel_2026-06-29_s6.png",
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

> ✅ `content_schedule.json` 內 Reels 記錄的 `asset_url` 應指向 **MP4 路徑**，而非 PNG。

---

## 4. 品牌規範（強制）

### 4.1 色彩（嚴禁使用任何以外顏色）

| 角色 | HEX |
|---|---|
| 主背景 | `#0D0D2B` |
| 次要背景 | `#1A1A3A` |
| 輔色背景 | `#2D1B4E` |
| 主文字／圖騰 | `#B4918F` |
| 亮部強調 | `#E8E8F0` |
| 金色點綴 | `#C9A84C` |

### 4.2 水印（強制出現於每一張畫面及影片每一幀）

```
Luna's Stone Atelier  圖文僅供參考
```

- 位置：右下角或左下角，字體細小但清晰可讀
- 不可僅寫在文案欄，必須直接嵌入畫面
- MP4 影片中水印必須貫穿全片每一幀

### 4.3 語言

- 繁體中文為主，英文為輔
- 雙語排版時，中文置於英文上方
- **英文字體大小為中文的 60%**
- 禁止使用簡體字

### 4.4 礦石學資料

- **嚴禁捏造礦石學數據**
- 只視覺化已提供的文案事實，不自行改寫
- 如對任何礦石資料有疑問，以 `KNOWLEDGE_BASE.md` 第 3 節為準

---

## 5. 禁止事項

- ❌ 禁止使用品牌色以外的任何顏色
- ❌ 禁止省略 Reels MP4 最終輸出（必須同時上傳 6 張 PNG 中間素材 + 1 支 MP4）
- ❌ 禁止捏造、修改礦石學數據
- ❌ 禁止省略水印聲明（包括 MP4 每一幀）
- ❌ 禁止引入其他專案的視覺風格
- ❌ 禁止在單一 `map` 輸出中回傳多個檔案（每次只輸出一個 `file`）
- ❌ 禁止使用簡體字
- ❌ Reels 各張禁止省略指定角色（Hook / 知識點 / CTA）
- ❌ `content_schedule.json` 的 Reels `asset_url` 禁止指向 PNG，必須指向 MP4

---

## 6. 完成後

1. 將所有素材上傳至 repo `assets/` 目錄（PNG 中間素材 + MP4 最終影片）
2. 提交 `generated_assets.json`（每張 PNG 各一條記錄 + MP4 獨立一條，Reels PNG 記錄需含 `slide_role` 欄位）
3. 如能回填，更新 `content_schedule.json` 的 `asset_url` 欄位（Reels 指向 MP4）
4. 通知操作者：批量生成完成，GitHub Actions 可按排程自動發佈

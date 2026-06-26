# Manus 批量素材生成指令 — Luna's Stone Atelier

> **版本：** v2.3 | **最後更新：** 2026-06-27
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

### Step 2：按格式生成素材（每張分別一次執行）

| 格式 | 生成規格 | 執行次數 |
|---|---|---|
| **Stories** | 3 張靜態圖文，4:5（1080×1350px） | 每張分別執行→ **3 次** |
| **Posts (Carousel)** | 6 頁靜態圖文，4:5（1080×1350px） | 每頁分別執行→ **6 次** |
| **Reels** | 6 張靜態圖文，4:5（1080×1350px） | 每張分別執行→ **6 次** |

> ⚠️ Reels 改為 **6 張具深度文字內容的靜態圖文序列**，不再生成動態影片（MP4）。

### Step 3：Reels 圖文結構（強制）

Reels 的 6 張圖必須依以下固定結構排列，每張均需包含繁體中文主文字與英文輔助說明：

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

### Step 4：檔名規則

```
Stories 第 1 張 : assets/stories/stories_YYYY-MM-DD_slide1.png
Stories 第 2 張 : assets/stories/stories_YYYY-MM-DD_slide2.png
Stories 第 3 張 : assets/stories/stories_YYYY-MM-DD_slide3.png

Posts 第 1 頁   : assets/posts/post_YYYY-MM-DD_p1.png
Posts 第 2 頁   : assets/posts/post_YYYY-MM-DD_p2.png
...             （共 6 頁）

Reels 第 1 張   : assets/reels/reel_YYYY-MM-DD_s1.png
Reels 第 2 張   : assets/reels/reel_YYYY-MM-DD_s2.png
Reels 第 3 張   : assets/reels/reel_YYYY-MM-DD_s3.png
Reels 第 4 張   : assets/reels/reel_YYYY-MM-DD_s4.png
Reels 第 5 張   : assets/reels/reel_YYYY-MM-DD_s5.png
Reels 第 6 張   : assets/reels/reel_YYYY-MM-DD_s6.png
```

### Step 5：輸出 `generated_assets.json`

**每一張圖各為一條獨立記錄**，不得將多個檔案共用一條：

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
    "image_asset_key": "reel_20260629_s2",
    "date": "2026-06-29",
    "type": "reel",
    "slide_index": 2,
    "slide_role": "knowledge_a",
    "file_path": "assets/reels/reel_2026-06-29_s2.png",
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
  }
]
```

如能取得公開 URL，請回填各條的 `asset_url` 欄位，並同步更新 `content_schedule.json` 內對應記錄的 `asset_url`。

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

### 4.2 水印（強制出現於每一張畫面）

```
Luna's Stone Atelier  圖文僅供參考
```

- 位置：右下角或左下角，字體細小但清晰可讀
- 不可僅寫在文案欄，必須直接嵌入畫面

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
- ❌ 禁止生成 MP4 影片作為 Reels 素材（已改為 6 張靜態圖文）
- ❌ 禁止捏造、修改礦石學數據
- ❌ 禁止省略水印聲明
- ❌ 禁止引入其他專案的視覺風格
- ❌ 禁止在單一 `map` 輸出中回傳多個檔案（每次只輸出一個 `file`）
- ❌ 禁止使用簡體字
- ❌ Reels 各張禁止省略指定角色（Hook / 知識點 / CTA）

---

## 6. 完成後

1. 將所有素材上傳至 repo `assets/` 目錄
2. 提交 `generated_assets.json`（每張圖各一條記錄，Reels 記錄需含 `slide_role` 欄位）
3. 如能回填，更新 `content_schedule.json` 的 `asset_url` 欄位
4. 通知操作者：批量生成完成，GitHub Actions 可按排程自動發佈

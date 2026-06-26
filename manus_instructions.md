# Manus 批量素材生成指令 — Luna's Stone Atelier

> **版本：** v2.1 | **最後更新：** 2026-06-27
> **定位：** 給 Manus 的唯一執行說明。Manus 只負責批量生成視覺素材，不負責文案撰寫、排程管理或發佈。

---

## 1. 任務背景

本 repo 採用「**預生成備用**」架構：

1. 文案與 Manus Prompt 已預先寫入 `content_schedule.json`
2. **Manus 一次過批量生成**所有 Stories / Posts / Reels 視覺素材
3. 素材生成後，GitHub Actions 按日期自動發佈，不再即時呼叫 AI

---

## 2. 執行步驟

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

| 格式 | 生成規格 |
|---|---|
| **Stories** | 3 張靜態圖，比例 4:5（1080×1350px） |
| **Posts (Carousel)** | 6 頁靜態圖，比例 4:5（1080×1350px） |
| **Reels** | 15–30 秒動態影片，比例 4:5（1080×1350px），**必須為真正動態影片，不得以靜態圖充當** |

### Step 3：輸出檔名規則

```
Stories : assets/stories/stories_YYYY-MM-DD_slide1.png
          assets/stories/stories_YYYY-MM-DD_slide2.png
          assets/stories/stories_YYYY-MM-DD_slide3.png

Posts   : assets/posts/post_YYYY-MM-DD_p1.png
          assets/posts/post_YYYY-MM-DD_p2.png
          ...（共 6 頁）

Reels   : assets/reels/reel_YYYY-MM-DD.mp4
```

### Step 4：輸出資產清單

生成 `generated_assets.json`，格式如下：

```json
[
  {
    "image_asset_key": "stories_20260627",
    "date": "2026-06-27",
    "type": "stories",
    "files": [
      "assets/stories/stories_2026-06-27_slide1.png",
      "assets/stories/stories_2026-06-27_slide2.png",
      "assets/stories/stories_2026-06-27_slide3.png"
    ],
    "asset_url": ""
  }
]
```

如能取得公開 URL，請回填 `content_schedule.json` 各記錄的 `asset_url` 欄位。

---

## 3. 品牌規範（強制）

### 3.1 色彩（嚴禁使用任何以外顏色）

| 角色 | HEX |
|---|---|
| 主背景 | `#0D0D2B` |
| 次要背景 | `#1A1A3A` |
| 輔色背景 | `#2D1B4E` |
| 主文字／圖騰 | `#B4918F` |
| 亮部強調 | `#E8E8F0` |
| 金色點綴 | `#C9A84C` |

### 3.2 水印（強制出現於每一張畫面）

```
Luna's Stone Atelier  圖文僅供參考
```

- 位置：右下角或左下角，字體細小但清晰可讀
- 不可僅寫在文案欄，必須直接嵌入畫面

### 3.3 語言

- 繁體中文為主，英文為輔
- 雙語排版時，中文置於英文上方

### 3.4 礦石學資料

- **嚴禁捏造礦石學數據**
- 只視覺化已提供的文案事實，不自行改寫
- 如對任何礦石資料有疑問，以 `KNOWLEDGE_BASE.md` 第 3 節為準

---

## 4. 禁止事項

- ❌ 禁止使用品牌色以外的任何顏色
- ❌ 禁止以靜態圖充當 Reels 影片素材
- ❌ 禁止捏造、修改礦石學數據
- ❌ 禁止省略水印聲明
- ❌ 禁止引入其他專案的視覺風格

---

## 5. 完成後

1. 將所有素材上傳至 repo `assets/` 目錄
2. 提交 `generated_assets.json`
3. 如能回填，更新 `content_schedule.json` 的 `asset_url` 欄位
4. 通知操作者：批量生成完成，GitHub Actions 可按排程自動發佈

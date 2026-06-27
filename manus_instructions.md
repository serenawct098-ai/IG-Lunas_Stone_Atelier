# Manus 操作指引 v3.0
_最後更新：2026-06-27_

---

## 0. 礦石資料唯一真源（SSOT）

> **所有礦石文案、科學數據、脈輪對應、保養資訊，必須以 `mineralogy_data.json` 為唯一來源。**
> 禁止自行編寫或引用其他文件中的礦石資料表。讀取時使用 `stone_id` 欄位對應 `mineralogy_data.json` 的 `id` 欄位。

---

## 1. 生成流程總覽

```
content_schedule.json
        │
        ▼
讀取當日記錄（status = "pending"）
        │
        ├─ type = stories  ──→ 生成 1 PNG
        ├─ type = posts    ──→ 生成 5 PNG Carousel
        └─ type = reels    ──→ 生成 6 PNG → 串接 1 MP4
        │
        ▼
 asset_url(s) 回填 content_schedule.json
        │
        ▼
發佈 IG（API / 手動）→ status 改為 "published"
```

---

## 2. 格式規格（嚴格遵守）

| 格式 | 尺寸 | 輸出 | 時長 |
|------|------|------|------|
| Stories | 1080×1350 px | **1 PNG** | — |
| Posts Carousel | 1080×1350 px | **5 PNG** | — |
| Reels | 1080×1350 px | **6 PNG 中間素材 + 1 MP4** | 15–30 秒 |

---

## 3. 品牌色彩系統

```
主背景：#0D0D2B（深海藍黑）
次背景：#1A1A3A
文字主色：#B4918F（霧玫瑰金）
文字亮部：#E8E8F0
金色點綴：#C9A84C
```

---

## 4. 各格式生成規則

### 4.1 Stories
1. Hook 大字（`今日能量：{stone_zh}`）
2. 礦石寫實插圖（居中，含細節紋理）
3. 三點資訊：脈輪 / 主題關鍵詞 / 能量使用建議一句
4. 互動文字：`「你的{stone_zh}故事？」`
5. 底部免責聲明：`Luna's Stone Atelier 圖文僅供參考`

### 4.2 Posts Carousel（5 張）
| 張 | 內容 |
|---|---|
| 1/5 | 封面止滑卡：大標題含數字或問句 + 礦石全貌插圖 + 頁碼 |
| 2/5 | 科學定位：化學式 / 莫氏硬度 / 分類（讀 `mineralogy_data.json`）|
| 3/5 | 美學亮點：色澤 / 光學效應 / 天然特徵辨別 |
| 4/5 | 能量與心理：脈輪 / 主題 / 使用建議 |
| 5/5 | 保養提醒 + CTA：淨化方式 / 禁忌 / 呼籲追蹤 |

封面第一行文字**必須**含數字或問句（提升止滑率）。
底部每張必須顯示：`Luna's Stone Atelier 圖文僅供參考`

### 4.3 Reels（6 PNG → 1 MP4）
| 張 | 內容 |
|---|---|
| 1/6 | Hook 止滑（首 3 秒決定留存）：`「第N夜｜{stone_zh}的秘密」` + 礦石特寫 |
| 2/6 | 知識點A 科學定位 |
| 3/6 | 知識點B 美學亮點 |
| 4/6 | 知識點C 能量主題 |
| 5/6 | 知識點D 保養禁忌 |
| 6/6 | CTA Cliffhanger：`「下集預告：{next_stone_zh}」` + 追蹤號召 |

**MP4 規格：**
- 每張停留 2.5–5 秒（總長 15–30 秒）
- 轉場：淡入淡出
- 底部標籤全程可見
- **禁止**底部字幕條（Caption Bar），改用 Graphic Text
- `asset_url` 回填為最終 MP4 的 URL

---

## 5. Caption 寫作規則（IG 2026 演算法）

1. **SEO First Line**：第一行必須含目標關鍵詞（礦石名稱 + 功能），這是搜尋收錄的核心
2. **Hashtag 控制**：每則 3–5 個，主題相關，避免堆砌
3. **CTA 必備**：每則均須包含行動號召，按階段調整措辭（見 `brand_config.json` phases）
4. **互動誘導**：Stories 必須有問句，Posts 以「滑動查看」引導，Reels 以「下集預告」引導追蹤

---

## 6. 首 90 分鐘互動策略

發佈後 90 分鐘是 IG 演算法評估窗口，Manus 需協助以下操作：
- 發佈後立即於 Stories 轉發貼文（製造初始流量）
- 準備 3 條「引導互動」留言範本，由帳號主在發佈後 10 分鐘內自行留言
- 監控首 90 分鐘 Save/Share 數字，Save 導向優先（Posts > Reels > Stories）

---

## 7. 檔案命名規範

```
assets/stories/story_{YYYY-MM-DD}.png
assets/posts/post_{YYYY-MM-DD}_s1.png … _s5.png
assets/reels/reel_{YYYY-MM-DD}_s1.png … _s6.png
assets/reels/reel_{YYYY-MM-DD}.mp4
```

---

## 8. 狀態管理

`content_schedule.json` 中每條記錄的 `status` 欄位：

| 值 | 意義 |
|---|---|
| `pending` | 待生成 |
| `generated` | 素材已生成，待發佈 |
| `published` | 已發佈至 IG |
| `error` | 生成或發佈失敗，需人工介入 |

生成完成後將 `asset_url`（或 `asset_urls` 陣列）回填，並將 `status` 改為 `generated`。

---

## 9. 免責聲明規範

所有素材底部**必須**顯示以下文字：

> Luna's Stone Atelier 圖文僅供參考

禁止省略或更改措辭。

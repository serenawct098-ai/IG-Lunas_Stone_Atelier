# Manus 操作指引 v4.0
_最後更新：2026-06-27_

---

## 0. 礦石資料唯一真源（SSOT）

> **所有礦石文案、科學數據、脈輪對應、保養資訊，必須以 `mineralogy_data.json` 為唯一來源。**
> 禁止自行編寫或引用其他文件中的礦石資料表。讀取時使用 `stone_id` 欄位對應 `mineralogy_data.json` 的 `id` 欄位。

---

## 1. 系統架構與 Manus 角色

### 1.1 兩個工作模式

| 模式 | 觸發方式 | Manus 的工作 |
|---|---|---|
| **批量生圖模式** | 手動執行（一次性 / 更新時）| 讀取 `content_schedule.json` 全部 pending 項目 → 批量生成所有圖片/MP4 → 存入 `assets/` → 回填 `asset_url` → status 改為 `generated` |
| **發布模式** | GitHub Actions 每日定時觸發 | 讀取 `manus_task.json` → 從 `assets/` 取備用圖片及文案 → 透過 IG MCP 發布至 Instagram → 回報完成（status 改為 `published`）|

### 1.2 發布模式詳細流程

```
【GitHub Actions 定時觸發】
        │
        ▼
  main.py 組裝 manus_task.json
  （含 asset_paths、caption、hashtags、cta）
        │
        ▼
  Manus 讀取 manus_task.json
        │
        ├─ 從 assets/ 取備用圖片（已事先批量生成）
        ├─ 套用文案、caption、hashtags
        │
        ▼
  透過 IG MCP 發布至 Instagram
        │
        ▼
  回填 published_url → status 改為 "published"
  回報完成至 GitHub
```

> ⚠️ **Manus 在發布模式下不負責生圖。** 若 `asset_path` 對應檔案不存在，須立即報錯（`status = "error"`），不得嘗試即時生成。

---

## 2. 格式規格（嚴格遵守）

> **所有格式統一採用 4:5（1080×1350 px）。**

| 格式 | 尺寸 | 輸出 | 時長 |
|------|------|------|------|
| Stories | 1080×1350 px（4:5）| **1 PNG** | — |
| Posts Carousel | 1080×1350 px（4:5）| **5 PNG** | — |
| Reels | 1080×1350 px（4:5）| **6 PNG 中間素材 + 1 MP4** | 15–30 秒 |

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

## 4. 各格式生成規則（批量生圖模式用）

### 4.1 Stories（1080×1350 px，4:5）
1. Hook 大字（`今日能量：{stone_zh}`）
2. 礦石寫實插圖（居中，含細節紋理）
3. 三點資訊：脈輪 / 主題關鍵詞 / 能量使用建議一句
4. 互動文字：`「你的{stone_zh}故事？」`
5. 底部免責聲明：`Luna's Stone Atelier 圖文僅供參考`

### 4.2 Posts Carousel（1080×1350 px，4:5，共 5 張）

**2026 演算法硬規則 — Carousel：**
- **封面第一行必須含數字或問句**，配合情緒觸點（警告/好奇/衝突感），目標：0.3 秒止滑
- **每頁設計必須製造「不完整感」**，讓讀者必須翻下一頁才能完整理解（提升 swipe completion rate）
- **目標 saves-to-likes ratio > 0.15**，達標後觸及提升 230–340%
- **封底 CTA 必須包含「收藏」導向文字**（收藏率是 Feed 最強排名訊號）

| 張 | 內容 |
|---|---|
| 1/5 | 封面止滑卡：大標題含數字或問句 + 礦石全貌插圖 + 頁碼 |
| 2/5 | 科學定位：化學式 / 莫氏硬度 / 分類（讀 `mineralogy_data.json`）|
| 3/5 | 美學亮點：色澤 / 光學效應 / 天然特徵辨別 |
| 4/5 | 能量與心理：脈輪 / 主題 / 使用建議 |
| 5/5 | 保養提醒 + CTA：淨化方式 / 禁忌 / 呼籲追蹤 + 收藏號召 |

底部每張必須顯示：`Luna's Stone Atelier 圖文僅供參考`

### 4.3 Reels（1080×1350 px，4:5，6 PNG → 1 MP4）

**2026 演算法硬規則 — Reels：**
- **首 3 秒 Hook 決定一切**：60%+ 3 秒留存率目標，觸及比弱 Hook 高 5–10×
- **15–30 秒最佳格式**：目標完播率 70%+，達標後系統推 Explore
- **DM 分享（Sends）是 #1 破圈訊號**：Sends/Reach 超過 3% 帶來 5–10× 額外觸及
- **重播率（Replay）是高質訊號**：設計「值得重看的細節」（快速列舉、神秘感、資訊密度高）
- **禁止 TikTok 水印**：有水印的 Reels 被演算法降級（Aggregator Penalty）
- **字幕提升完播率**：2026 年 IG 確認字幕有助更多完整觀看
- **Series 連載設計**：每集結尾必須有下集鉤子（series_hook），推動追蹤

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

1. **SEO First Line（硬規則）**：Caption 第一行必須含目標關鍵詞（礦石名稱 + 功能），這是 IG 2026 搜尋收錄的核心分類訊號
2. **Shares 優先導向**：Caption 內容必須令人想轉發——提問、反常識、實用清單是最高轉發觸發格式
3. **Hashtag 控制（硬規則）**：每則 **3–5 個精準相關標籤**，禁止使用 30 個舊式做法（過多稀釋訊號）
4. **CTA 必備**：每則均須包含行動號召，按階段調整措辭（見 `brand_config.json` phases）
5. **互動誘導**：Stories 必須有問句，Posts 以「收藏 / 左滑查看」引導，Reels 以「下集預告」引導追蹤
6. **Carousel Caption 必須含「收藏」號召**：儲存率（Save Rate）是 Carousel 最重要排名訊號

---

## 6. 首 90 分鐘互動策略（2026 演算法關鍵窗口）

發布後 **首 90 分鐘** 是 IG 演算法評估窗口，頭 1 小時加速分發決定觸及上限：

- 發布後立即於 Stories 轉發貼文（製造初始流量）
- 準備 **3 條「引導互動」留言範本**，由帳號主在發布後 10 分鐘內自行留言
- **主動回覆所有留言**（發布後前 90 分鐘）——早期互動直接觸發演算法加速分發
- 監控首 90 分鐘 Save/Share 數字：
  - Carousel：目標 saves-to-likes ratio > 0.15
  - Reels：目標 3 秒留存率 > 60%，完播率 > 70%，Sends/Reach > 3%

---

## 7. 演算法指標基準（2026）

| 格式 | 關鍵指標 | 目標基準 | 達標後效果 |
|---|---|---|---|
| Carousel | saves-to-likes ratio | > 0.15 | 觸及提升 230–340% |
| Carousel | swipe completion rate | > 70% | 系統推薦 Explore |
| Reels | 3 秒留存率 | > 60% | 觸及比弱 Hook 高 5–10× |
| Reels | 完播率 | > 70% | 系統推 Explore |
| Reels | Sends/Reach | > 3% | 5–10× 額外觸及 |
| 全格式 | 首 90 分鐘 Save 數量 | 越高越好 | 決定整體觸及上限 |

---

## 8. 檔案命名規範

```
assets/stories/story_{YYYY-MM-DD}.png
assets/posts/post_{YYYY-MM-DD}_s1.png … _s5.png
assets/reels/reel_{YYYY-MM-DD}_s1.png … _s6.png
assets/reels/reel_{YYYY-MM-DD}.mp4
```

---

## 9. 狀態管理

`content_schedule.json` 中每條記錄的 `status` 欄位：

| 值 | 意義 |
|---|---|
| `pending` | 待生成（批量生圖模式處理）|
| `generated` | 素材已存入 `assets/`，待 GitHub Actions 觸發發布 |
| `published` | 已透過 IG MCP 發布至 Instagram |
| `error` | 生成或發布失敗，需人工介入 |

生成完成後將 `asset_url`（或 `asset_urls` 陣列）回填，並將 `status` 改為 `generated`。

---

## 10. 免責聲明規範

所有素材底部**必須**顯示以下文字：

> Luna's Stone Atelier 圖文僅供參考

禁止省略或更改措辭。

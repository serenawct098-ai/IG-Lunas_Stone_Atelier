# 🎨 一次性批量生圖指引

> 此文件說明如何用 Manus 一次生成 90 天全部素材，存入 GitHub assets/ 備用。
> 完成後，每日發布只需 Manus 取圖發布，消耗最小 token。

---

## 框架邏輯

```
一次性操作（開始或更新時）
        ↓
   Manus 讀 content_schedule.json
   對每一條 pending 記錄：
     • 根據 stone_id 讀取 mineralogy_data.json（SSOT）
     • 按 format_spec 生成圖片
     • 存入 assets/{type}/{filename}
        ↓
   commit 到 GitHub repo
        ↓
   備用完成！GitHub Actions 每次發布時直接取用
```

---

## 檔案命名規則

| 格式 | 路徑格式 | 範例 |
|------|----------|------|
| Stories | `assets/stories/story_{YYYY-MM-DD}.png` | `assets/stories/story_2026-07-01.png` |
| Posts | `assets/posts/post_{YYYY-MM-DD}_s1.png` … `_s5.png` | `assets/posts/post_2026-07-02_s1.png` |
| Reels | `assets/reels/reel_{YYYY-MM-DD}_s1.png` … `_s6.png` + `.mp4` | `assets/reels/reel_2026-07-05.mp4` |

---

## 素材規格（全部統一 4:5）

| 格式 | 尺寸 | 輸出 |
|------|------|------|
| Stories | **1080×1350 px（4:5）** | 1 PNG |
| Posts Carousel | **1080×1350 px（4:5）** | 5 PNG（封面必須含數字或問句）|
| Reels | **1080×1350 px（4:5）** | 6 PNG 中間素材 + 1 MP4（15–30 秒）|

> 所有格式統一 **4:5（1080×1350 px）**，禁止使用其他尺寸。

---

## 品牌色彩

| 用途 | 色碼 |
|------|------|
| 主背景 | `#0D0D2B` |
| 次背景 | `#1A1A3A` |
| 文字主色 | `#B4918F` |
| 文字亮部 | `#E8E8F0` |
| 金色點綴 | `#C9A84C` |

---

## 礦石資料來源

一律從 `mineralogy_data.json` 讀取（SSOT）。**禁止自行輸入礦石資料。**

---

## 完成後 commit 格式

```
assets: batch generate [Phase 1] 2026-06-15 to 2026-07-14 (30 entries)
```

---

## 備用完成後的發布流程

```
GitHub Actions 定時觸發
        ↓
   main.py 找今日任務
   解析 assets/ 備用素材路徑
   寫入 manus_task.json（assets_ready: true）
        ↓
   Manus 讀取 manus_task.json
   從 assets/ 取備用圖片及文案
   透過 IG MCP 發布至 Instagram
   回填 published_url → status 改為 published
```

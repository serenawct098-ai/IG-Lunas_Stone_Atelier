# IG月華星礦坊 - 90 天 Carousel Posts 自動發布 Playbook

> **執行模式：** Manus 排程自動執行 (`--run-as-new-task`)
> **觸發時間：** 每週二、五 12:00 HKT (Cron: `0 0 4 * * 2,5` UTC)
> **目標：** 90天內發布 26 篇高收藏、高轉發 Carousel 貼文

## 1. 任務上下文 (Context)
此 Playbook 用於指導 Manus 在每次排程觸發時，自動完成 IG 圖文的內容生成、圖片準備與發布。必須嚴格遵循《品牌基礎規範 v1.0》與《礦物學知識庫 v1.0》。

## 2. 執行步驟 (Execution Steps)

### Step 1: 確定當前貼文主題
讀取 `/home/ubuntu/Serena-my-prompts/IG-LunasStoneAtelier/90_days_content_plan.json`，根據當前日期尋找對應的貼文主題。若找不到完全匹配的日期，取下一個未發布的主題。

### Step 2: 內容生成 (Caption & 乾貨摘要)
根據主題與《礦物學知識庫 v1.0》生成文案，必須包含：
- **第1行：** 爆點標題（與封面呼應，加emoji）
- **第2-3行：** 1-2句引子，製造好奇
- **空行**
- **乾貨摘要（3點，每點1句）：**
  ✦ 點1
  ✦ 點2
  ✦ 點3
- **空行**
- **CTA：** 「💾 收藏留底 | 👇 留言你最想了解哪種礦石」
- **空行**
- **Hashtags（分三層）：**
  - 大眾（100萬+）：#水晶 #風水 #礦石 #crystals #fengshui
  - 中眾（10-100萬）：#水晶能量 #礦石收藏 #開運水晶 #crystalhealing
  - 精準（1-10萬）：與主題高度相關（如 #黃水晶功效）

### Step 3: 圖片準備 (Carousel 1-5頁)
使用 `generate` 工具或調用 Python 繪圖腳本，嚴格遵循色彩規範：
- 主色（背景）：`#1A1A3A`
- 主文字/邊框：`#B4918F`
- 輔色：`#002D00`, `#F5F5DC`
- Logo：`Lunas_Stone_Atelier_Transparent_Like_Fig3.png`
- Watermark：`Luna's Stone Atelier`

**頁面結構：**
- **P1 (封面)：** 吸睛大標題 + 礦石特寫 + 「👉 左滑看全部」
- **P2-P4 (內頁)：** 每頁文字 <80 字，極簡列點/表格，附礦石圖，標示頁碼 (2/5, 3/5, 4/5)
- **P5 (封底)：** 文案「💾 收藏起來，需要時翻出嚟！➕ 追蹤我，每週更新礦石開運知識」

### Step 4: 發布至 Instagram
調用 Instagram MCP 工具 `create_instagram`：
- `type`: "post"
- `caption`: 填入 Step 2 生成的文案
- `media`: 填入 Step 3 生成的 5 張圖片 URL/路徑
- 確認發布。

### Step 5: 數據監控 (每 14 天)
若當前為第 14, 28, 42, 56, 70, 84 天，調用 `get_post_list` 與 `get_post_insights` 收集：
- 收藏數 (Saves) - 首要 KPI
- 分享數 (Shares)
- 觸及人數 (Reach)
將數據彙整寫入 `/home/ubuntu/Serena-my-prompts/IG-LunasStoneAtelier/performance_report.md`。

### Step 6: 結束通知 (第 90 天)
發布最後一篇貼文後，向使用者發送通知：
「✅ 90天Carousel Posts SOP已完成！共發布26篇，最高收藏帖子：[X]篇，平均收藏率[X]%。建議下一步：將高收藏帖子改編為Reels或限時動態再利用。」

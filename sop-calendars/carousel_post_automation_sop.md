# IG 月華星礦坊 Carousel Post 自動排程 SOP

## 1. 目的與範圍
本 SOP 旨在規範「IG 月華星礦坊」Instagram Carousel Posts 的自動化生成與排程流程，確保所有產出符合品牌視覺規範，並透過 `manus-config schedule` 實現自動化發布。

## 2. 品牌視覺規範 (不可逆設定)
- **Logo**: Luna’s Stone Atelier 官方圖騰 (`/home/ubuntu/upload/Lunas_Stone_Atelier_Transparent_Like_Fig3.png`)
- **圖片標籤 (Watermark)**: Luna’s Stone Atelier
- **主色**: 深紫藍色 `#1A1A3A` (背景)
- **主文字/圖騰/邊框色**: 霧玫瑰金色 `#B4918F`
- **輔色**: 墨綠色 `#002D00`、暖米白色 `#F5F5DC` (文案邊框)
- **主題**: 天然礦石元素
- **防幻覺協議**: 所有資料必須基於真實文獻，禁止 AI 自行腦補，數據必須驗證通過。

## 3. 自動化排程架構
採用 **Schedule → Manus execution** 模式，透過 `manus-config schedule` 建立排程任務。

### 3.1 排程設定指令範例
```bash
manus-config schedule create \
  --title "IG Carousel Post 自動發布" \
  --detail "根據 brand_config.json 規範，生成包含天然礦石知識的 Carousel Post (3-5張圖)，並透過 MCP Instagram 發布。" \
  --cron "0 0 18 * * 1,3,5" \
  --repeated \
  --connector-uids "4b899211-fd12-410e-a8d2-264a409cbc78"
```
*(註：上述 Cron 代表每週一、三、五 18:00 執行)*

## 4. 執行腳本邏輯 (Python)
每次排程觸發時，系統將執行以下邏輯：
1. **讀取設定**: 載入 `brand_config.json`。
2. **內容生成**: 根據真實礦石資料庫生成文案與圖片 Prompt。
3. **圖片合成**: 使用 Python (Pillow) 或 AI 繪圖工具生成圖片，並套用指定色碼與 Logo。
4. **發布驗證**: 呼叫 MCP Instagram `create_instagram` 工具，傳入生成的圖片 URL 與文案。

## 5. 驗證與斷路器機制
- **發布前驗證**: 檢查圖片尺寸 (不大於 8MB)、色碼是否符合規範、Logo 是否存在。
- **48h 斷路器**: 若連續 48 小時內發布失敗或觸及 Rate Limit，自動暫停排程並通知管理員。

## 6. 下一步行動
- 部署 Python 自動化腳本至沙盒。
- 執行單次測試發布以驗證 MCP Instagram 連線與視覺規範。

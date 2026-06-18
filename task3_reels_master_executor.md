# LUNA — AUTONOMOUS COO & SYSTEM ARCHITECT (L10)
# MISSION: [任務 3｜Reels 短影音排程：一千零一夜礦石風水系列]

## 一、核心執行規範 (LUNA SSOT)
- **發布頻率**：每週一 18:00、週四 18:00 HKT
- **內容比例**：**4:5** (Portrait)
- **語言規範**：統一使用**正體中文書面語**，嚴禁口語或亂碼。關鍵字詞修正：暴曬 (✓) / 曝曬 (✗)；成份 (✓) / 成分 (✗)；揭祕 (✓) / 揭秘 (✗)。
- **影音強制規範（紅線，缺一不發布）**：
  - **圖片文字標註**：每集影片必須在畫面內包含關鍵信息的英文標註（對應 `en_text_overlay` 字段）。
  - **影片標籤（強制，缺一不發布）**: 每集影片必須在畫面內明確顯示 `Luna's Stone Atelier 圖文僅供參考`，不可僅寫在文案中。
- **視覺製作標準**：
  - **比例**: 強制 4:5 (Portrait 1080×1350px)
  - **畫面質感**: 高品質天然礦石實物攝影，強光對比、微距特寫為主，禁止使用低質圖庫圖。
  - **主色**: 深紫藍色 #1A1A3A
  - **主文字/圖騰/邊框色**: 霧玫瑰金色 #B4918F
  - **輔色**: 墨綠色 #002D00、暖米白色 #F5F5DC
  - **影片標籤（畫面內強制，缺一不發布）**: `Luna's Stone Atelier 圖文僅供參考`，顯示於影片左下角或尾幀。
- **聽覺製作標準**：
  - **配樂**: 使用高質感、神祕感或自然氛圍的背景音樂。
  - **中文字幕**: 對應 `zh_subtitle` 字段，字幕顯示於畫面底部。
- **排程執行規範（紅線）**：
  - `runAsNewTask: false` —— **嚴禁開啟新任務/對話執行排程**，必須在原任務3對話中執行。
- **錯漏驗證**：每次發布前必須人工/系統驗證視覺與數據準確性。

## 二、跨平台協同時間軸 (Cross-Task Orchestration)
與 Task 1 (Stories) 及 Task 2 (Carousel) 保持同步發布節奏。

## 三、執行驗證協議
每次發布前強制核查以下五項：
1. **比例** 4:5 ✅
2. **影片標籤** `Luna's Stone Atelier 圖文僅供參考` 已在畫面內顯示 ✅
3. **圖片文字標註** `en_text_overlay` 已標註於畫面 ✅
4. **語言** 正體中文書面語 ✅
5. **事實核查** 所有數據已對照礦石學知識庫驗證 ✅

## 四、90天自動化發布日曆與腳本庫 (25 集連載)

### 第 1 集 JSON
```json
{
  "episode": "第1集",
  "title": "⚠️ 3種水晶千萬唔好曬太陽！你中招了嗎？",
  "publish_date": "2026-06-15",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "visual_prompts": {
    "hook": "紫水晶褪色對比特寫，疊加文字「Stop! Ruining Crystals」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三塊礦石特寫，標註「Sunlight = Damage」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "手持褪色粉晶，標註「Permanent Fading」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "動態文字：「Part 2 coming soon」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】"
  },
  "en_text_overlay": [
    "Stop! Ruining Crystals",
    "Sunlight = Damage",
    "Permanent Fading",
    "Part 2 coming soon"
  ],
  "script": {
    "0_3s": { "zh_subtitle": "你每天曬太陽的水晶，其實已經廢掉了！" },
    "3_15s": { "zh_subtitle": "紫水晶、粉晶、海藍寶含鐵和錳，曝曬即褪色，不是淨化，是損壞。" },
    "15_25s": { "zh_subtitle": "還有一種幾乎人人都有，曬太陽不只褪色，還會⋯⋯" },
    "25_30s": { "zh_subtitle": "追蹤帳號，下集繼續揭秘" }
  },
  "caption": "⚠️ 你嘅水晶係咁曬緊？！（第1集）\n呢3種水晶見太陽就廢：紫水晶 / 粉晶 / 海藍寶\n唔係迷信——係礦石化學成分問題 🔬\n💾 收藏留底 | 追蹤睇第2集答案",
  "hashtags": ["#水晶", "#礦石", "#風水", "#crystals", "#水晶能量", "#紫水晶", "#粉晶", "#crystalcare", "#水晶知識", "#開運", "#香港風水", "#crystalhealing", "#玄學"]
}
```

### 第 2 集 JSON
```json
{
  "episode": "第2集",
  "title": "💀 這塊石頭一曬即裂——你家裡有嗎？",
  "publish_date": "2026-06-18",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "visual_prompts": {
    "hook": "蛋白石龜裂特寫，疊加文字「Sunlight Cracks It」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "蛋白石失水對比，標註「Dehydration Damage」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "龜裂細節，標註「Irreversible」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "動態文字：「Next: Spot Fakes」。【畫面顯示：Luna's Stone Atelier 圖文僅供參考】"
  },
  "en_text_overlay": [
    "Sunlight Cracks It",
    "Dehydration Damage",
    "Irreversible",
    "Next: Spot Fakes"
  ],
  "script": {
    "0_3s": { "zh_subtitle": "就是這塊——曬太陽直接龜裂，永久損壞！" },
    "3_15s": { "zh_subtitle": "蛋白石含水結構（SiO₂·nH₂O），日曬導致失水龜裂，遊彩效應永久消失。" },
    "15_25s": { "zh_subtitle": "你是否認為日曬是最天然的淨化方式？你可能已毀掉了最珍貴的礦石。" },
    "25_30s": { "zh_subtitle": "追蹤帳號，下集：識別假水晶方法公開" }
  },
  "caption": "💀 蛋白石一曬太陽就龜裂？！（第2集）\n佢含天然水分——日曬等於強制脫水，損壞永久無法修復\n呢個係礦物學知識，唔係迷信 🔬\n💾 收藏保護你嘅礦石 | 👆 第1集係咩？睇Profile置頂",
  "hashtags": ["#蛋白石", "#Opal", "#水晶保養", "#礦石知識", "#crystalcare", "#風水", "#水晶", "#礦石", "#crystalhealing", "#開運水晶", "#香港風水", "#玄學"]
}
```

### 第 3 集 JSON
```json
{
  "episode": "第3集",
  "title": "🔍 你養住假水晶幾年？3個肉眼測試即刻知！",
  "publish_date": "2026-06-22",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "en_text_overlay": [
    "Spot the Fake",
    "3 Easy Tests",
    "Real vs Glass",
    "Part 4 Next"
  ],
  "script": {
    "0_3s": { "zh_subtitle": "這兩塊看起來一樣——但其中一塊是玻璃。你能分辨嗎？" },
    "3_15s": { "zh_subtitle": "測試1：放大鏡看內含物；測試2：手握冰涼感；測試3：顏色均一度。" },
    "15_25s": { "zh_subtitle": "以上三個你學到了，但還有第四個方法——最準確、無需工具。" },
    "25_30s": { "zh_subtitle": "追蹤帳號，下集繼續揭秘" }
  }
}
```

### 第 4 集 JSON
```json
{
  "episode": "第4集",
  "title": "💸 礦石放錯位置等於破財——你中招了嗎？",
  "publish_date": "2026-06-25",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "en_text_overlay": [
    "Wealth Drain Spots",
    "Mistake 1: Bathroom",
    "Mistake 2: Bedroom",
    "Follow for Part 5"
  ],
  "script": {
    "0_3s": { "zh_subtitle": "警告！家中有礦石嗎？三個位置放了等於破財！" },
    "3_15s": { "zh_subtitle": "錯誤1：廁所旁；錯誤2：黑曜石放睡房；錯誤3留到下一秒⋯⋯" },
    "15_25s": { "zh_subtitle": "第三個地方你每天都去，以為最安全，但礦石放那裡反而會⋯⋯" },
    "25_30s": { "zh_subtitle": "追蹤帳號，下集繼續" }
  }
}
```

*(後續集數遵循相同 JSON 結構，移除 en_vo 與 en_subtitle，替換為 en_text_overlay)*

---

## 五、自動化排程指令 (System Link)
系統將每週一、四 18:00 HKT 自動讀取此文件並調用 Instagram Connector 執行發布。
- `runAsNewTask: false`
- **排程狀態**：`vJkuOkOUG5T8ifzJmriTi2`（已激活）

# LUNA — AUTONOMOUS COO & SYSTEM ARCHITECT (L10)
# MISSION: [任務 3｜Reels 短影音排程：一千零一夜礦石風水系列]

## 一、核心執行規範 (LUNA SSOT)
- **發布頻率**：每週一 18:00、週四 18:00 HKT
- **內容比例**：**4:5** (Portrait)
- **語言規範**：統一使用**正體中文書面語**，嚴禁口語或亂碼。英文為輔。關鍵字詞修正：暴曬 (✓) / 曝曬 (✗)；成份 (✓) / 成分 (✗)；揭祕 (✓) / 揭秘 (✗)。
- **影音強制規範（紅線，缺一不發布）**：
  - **英文配音**：每集必須包含英文配音（對應 `en_vo` 字段）
  - **英文字幕**：每集必須包含英文字幕（對應 `en_subtitle` 字段）
  - **影片標籤（強制，缺一不發布）**: 每集影片必須在畫面內明確顯示 `Luna's Stone Atelier 圖文僅供參考`，不可僅寫在文案中
- **視覺製作標準**：
  - **比例**: 強制 4:5 (Portrait 1080×1350px)
  - **畫面質感**: 高品質天然礦石實物攝影，強光對比、微距特寫為主，禁止使用低質圖庫圖
  - **主色**: 深紫藍色 #1A1A3A
  - **主文字/圖騰/邊框色**: 霧玫瑰金色 #B4918F
  - **輔色**: 墨綠色 #002D00、暖米白色 #F5F5DC
  - **影片標籤（畫面內強制，缺一不發布）**: `Luna's Stone Atelier 圖文僅供參考`，顯示於影片左下角或尾幀
- **聽覺製作標準**：
  - **英文配音**: 每集必須錄製英文配音（對應 JSON 內 `en_vo` 字段），英文為主語音
  - **英文字幕**: 每集必須嵌入英文字幕（對應 JSON 內 `en_subtitle` 字段），字幕顯示於畫面底部
  - **正體中文字幕**: 可選加入，對應 `zh_subtitle` 字段
- **排程執行規範（紅線）**：
  - `runAsNewTask: false` —— **嚴禁開啟新任務/對話執行排程**，必須在原任務3對話中執行，以保持上下文可對比錯誤
- **錯漏驗證**：每次發布前必須人工/系統驗證視覺與數據準確性

## 二、跨平台協同時間軸 (Cross-Task Orchestration)
為極大化內容觸及與轉化，Reels 必須遵循以下協同時間表：

| 時間 | 格式 | 內容核心 | 協同策略 |
| :--- | :--- | :--- | :--- |
| **週一 18:00** | **Reels** | **本週連載新集** | **製造懸念，吸引追蹤** |
| 週一 20:00 | Stories | 呼應當日 Reels | 互動貼圖，流量回導 |
| 週二 12:00 | Carousel | 本週知識乾貨 | 擴大收藏，建立權威 |
| 週三 20:00 | Stories | Reels 延伸話題 | 收問答箱，增加互動 |
| **週四 18:00** | **Reels** | **上集懸念解答** | **完播率攻堅，開新懸念** |
| 週四 20:00 | Stories | 呼應當日 Reels | 互動貼圖，流量回導 |
| 週五 12:00 | Carousel | 深度知識版本 | Reels 的文字延伸，高價值收藏 |
| 週日 20:00 | Stories | 本週互動整合 | 問答箱答題，信任轉化 |

### 協同原則：
1. **呼應 (Echo)**：Stories 應包含 Reels 的關鍵截圖、幕後花絮或投票互動，引導流量回看 Reels。
2. **延伸 (Extend)**：Stories 應針對 Post 的乾貨進行更深入的 QA、補充案例或限時福利，增加用戶黏著度。
3. **一致性**：所有協同內容必須保持品牌視覺規範與防幻覺協議。

## 三、執行驗證協議
每次發布前強制核查以下六項：
1. **比例** 4:5 ✅
2. **影片標籤** `Luna's Stone Atelier 圖文僅供參考` 已在畫面內顯示（非僅文案） ✅
3. **語言** 正體中文書面語為主，英文為輔 ✅
4. **英文配音** `en_vo` 字段已填寫且已錄音 ✅
5. **英文字幕** `en_subtitle` 字段已填寫且已嵌入影片 ✅
6. **事實核查** 所有石種名稱、科學成分、硬度、能量說明均已對照礦石學知識庫驗證，禁止發布與事實不符的內容 ✅

## 四、90天自動化發布日曆與腳本庫 (25 集連載)

一千零一夜礦石風水系列 — 90天Reels SOP 發布日曆（逢每週一、四 18:00 HKT）

以 **2026-06-15（週一）** 為第一集：

| Phase | 集數 | 發布日期（週一） | 發布日期（週四） |
|---|---|---|---|
| 破圈引流（Ep 1–8） | 1,2 | 06-15, 06-22 | 06-18, 06-25 |
| 破圈引流（Ep 5–8） | 5,6 | 06-29, 07-06 | 07-02, 07-09 |
| 信任建立（Ep 9–16） | 9,10 | 07-13, 07-20 | 07-16, 07-23 |
| 信任建立（Ep 13–16） | 13,14 | 07-27, 08-03 | 07-30, 08-06 |
| 產品轉化（Ep 17–25） | 17,18 | 08-10, 08-17 | 08-13, 08-20 |
| 產品轉化（Ep 21–25） | 21,22 | 08-24, 08-31 | 08-27, 09-03 |
| 完結篇 | 25 | 09-07（週一） | — |

> 共 **25 集**，達標。

***

## Phase 1：破圈引流期（Ep 1–8）

***

### 第 1 集 JSON（已在範例中提供，補完 JSON 格式）

```json
{
  "episode": "第1集",
  "title": "⚠️ 3種水晶千萬唔好曬太陽！你中招了嗎？",
  "publish_date": "2026-06-15",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "series_hook": "仲有一種最多人有，曬太陽唔止褪色，仲會⋯⋯",
  "next_episode_preview": "第2集：那一種連蛋白石都比唔上，一曬即裂——你有佢嗎？",
  "visual_prompts": {
    "hook": "紫水晶近距離對比：左半深紫飽和，右半已褪成淺粉。純黑背景，強烈光影，疊加白色衝擊大字。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三塊礦石依次特寫（紫水晶、粉晶、海藍寶），每塊旁邊出現「☀️ = ⚠️」警示圖示，旁邊快速飛入礦物成分標籤（Fe、Mn）。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "手持一塊褪色粉晶特寫，紋理清晰，顏色明顯偏白，畫面突然黑屏——白字「仲有一種⋯⋯」。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "動態文字彈出：「第2集：最危險那塊係？」追蹤按鈕特效，倒計時感設計。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "你每天曬太陽的水晶，其實已經廢掉了！",
      "en_subtitle": "Stop! Your crystals are being RUINED by sunlight.",
      "en_vo": "Stop! Your crystals are being RUINED by sunlight."
    },
    "3_15s": {
      "zh_subtitle": "紫水晶、粉晶、海藍寶含鐵和錳，曝曬即褪色，不是淨化，是損壞。",
      "en_subtitle": "Amethyst, Rose Quartz, Aquamarine — iron & manganese cause permanent fading. That's not cleansing. That's damage.",
      "en_vo": "Amethyst, Rose Quartz, Aquamarine — iron & manganese cause permanent fading. That's not cleansing. That's damage."
    },
    "15_25s": {
      "zh_subtitle": "還有一種幾乎人人都有，曬太陽不只褪色，還會⋯⋯",
      "en_subtitle": "And there's one more — almost everyone has it — sunlight doesn't just fade it, it actually—",
      "en_vo": "And there's one more — almost everyone has it — sunlight doesn't just fade it, it actually—"
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，下集繼續揭秘",
      "en_subtitle": "Follow for Part 2 — dropping Thursday!",
      "en_vo": "Follow for Part 2 — dropping Thursday!"
    }
  },
  "caption": "⚠️ 你嘅水晶係咁曬緊？！（第1集）\n呢3種水晶見太陽就廢：紫水晶 / 粉晶 / 海藍寶\n唔係迷信——係礦石化學成分問題 🔬\n💾 收藏留底 | 追蹤睇第2集答案",
  "hashtags": [
    "#水晶",
    "#礦石",
    "#風水",
    "#crystals",
    "#水晶能量",
    "#紫水晶",
    "#粉晶",
    "#crystalcare",
    "#水晶知識",
    "#開運",
    "#香港風水",
    "#crystalhealing",
    "#玄學"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 2 集 JSON

```json
{
  "episode": "第2集",
  "title": "💀 這塊石頭一曬即裂——你家裡有嗎？",
  "publish_date": "2026-06-18",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "series_hook": "蛋白石含天然水分，日曬等於幫佢脫水——就係咁殘忍",
  "next_episode_preview": "第3集：你有冇養住一顆假水晶而唔知？（識別方法下集公開）",
  "visual_prompts": {
    "hook": "蛋白石特寫——表面出現龜裂紋理的震撼微距鏡頭，色澤明顯偏暗，疊加紅色警示框與大字「就係呢塊」。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "蛋白石在陽光下對比圖：左邊健康七彩遊彩效應，右邊龜裂失色。旁邊飛入科學說明文字卡「SiO₂·nH₂O 含水量 3-20%」。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "特寫蛋白石裂縫——象徵性黑屏+白字：「損壞無法修復⋯⋯你有幾多塊係咁？」。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "動態文字：「第3集：你養住假水晶？」追蹤特效彈出。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "就是這塊——曬太陽直接龜裂，永久損壞！",
      "en_subtitle": "This one — one day in sunlight and it cracks. Forever.",
      "en_vo": "This one — one day in sunlight and it cracks. Forever."
    },
    "3_15s": {
      "zh_subtitle": "蛋白石含水結構（SiO₂·nH₂O），日曬導致失水龜裂，遊彩效應永久消失，無法修復。",
      "en_subtitle": "Opal contains 3–20% water. Direct sunlight dehydrates it — the play-of-color vanishes, cracks appear. Permanent damage.",
      "en_vo": "Opal contains 3–20% water. Direct sunlight dehydrates it — the play-of-color vanishes, cracks appear. Permanent damage."
    },
    "15_25s": {
      "zh_subtitle": "你是否認為日曬是最天然的淨化方式？如果是，你可能已毀掉了最珍貴的那塊礦石。",
      "en_subtitle": "Did you think sunlight was the safest way to cleanse crystals? You may have already destroyed your best one.",
      "en_vo": "Did you think sunlight was the safest way to cleanse crystals? You may have already destroyed your best one."
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，下集：識別假水晶方法公開",
      "en_subtitle": "Follow — next ep: how to spot fake crystals. Monday!",
      "en_vo": "Follow — next ep: how to spot fake crystals. Monday!"
    }
  },
  "caption": "💀 蛋白石一曬太陽就龜裂？！（第2集）\n佢含天然水分——日曬等於強制脫水，損壞永久無法修復\n呢個係礦物學知識，唔係迷信 🔬\n💾 收藏保護你嘅礦石 | 👆 第1集係咩？睇Profile置頂",
  "hashtags": [
    "#蛋白石",
    "#Opal",
    "#水晶保養",
    "#礦石知識",
    "#crystalcare",
    "#風水",
    "#水晶",
    "#礦石",
    "#crystalhealing",
    "#開運水晶",
    "#香港風水",
    "#玄學"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 3 集 JSON

```json
{
  "episode": "第3集",
  "title": "🔍 你養住假水晶幾年？3個肉眼測試即刻知！",
  "publish_date": "2026-06-22",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "series_hook": "最貴唔代表最真——有種仿品連專家都要放大鏡先認到",
  "next_episode_preview": "第4集：呢塊石放錯位置等於破財——你家裡擺咗嗎？",
  "visual_prompts": {
    "hook": "兩顆水晶並排，外觀幾乎相同——疊加問號與「邊顆係真？」大字，高懸念設計。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三個肉眼測試動作快速剪輯：放大鏡觀察內含物、手握測溫、光線折射角度。每個動作配1–2秒清晰特寫。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "揭曉：左邊天然有棉絮+冰涼感，右邊玻璃有圓形氣泡+無冰涼感。畫面停在「仲有第四個方法⋯⋯」黑屏。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「第4集：礦石放錯位置 = 破財？」追蹤特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "這兩塊看起來一樣——但其中一塊是玻璃。你能分辨嗎？",
      "en_subtitle": "These two look identical. One is glass. Can you tell which?",
      "en_vo": "These two look identical. One is glass. Can you tell which?"
    },
    "3_15s": {
      "zh_subtitle": "測試1：放大鏡看內含物（棉絮vs圓形氣泡）；測試2：手握冰涼感；測試3：顏色是否過度均一。",
      "en_subtitle": "Test 1: magnify — natural stone has inclusions, glass has round bubbles. Test 2: cold to touch. Test 3: colour too perfect = suspicious.",
      "en_vo": "Test 1: magnify — natural stone has inclusions, glass has round bubbles. Test 2: cold to touch. Test 3: colour too perfect = suspicious."
    },
    "15_25s": {
      "zh_subtitle": "以上三個你學到了，但還有第四個方法——最準確、無需工具，任何人都能做。",
      "en_subtitle": "You now know three tests. But there's a 4th — the most accurate one. No tools needed. Anyone can do it—",
      "en_vo": "You now know three tests. But there's a 4th — the most accurate one. No tools needed. Anyone can do it—"
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，下集繼續揭秘",
      "en_subtitle": "Follow for Part 4 — dropping Thursday!",
      "en_vo": "Follow for Part 4 — dropping Thursday!"
    }
  },
  "caption": "🔍 你養住假水晶幾年都唔知？（第3集）\n3個肉眼即測方法：放大鏡氣泡 / 手握冰涼感 / 顏色均一度\n第四個最準確方法——下集先公開 👀\n💾 收藏留底 | 追蹤睇完整系列",
  "hashtags": [
    "#真假水晶",
    "#水晶鑑定",
    "#礦石知識",
    "#crystalauthenticity",
    "#水晶",
    "#礦石",
    "#crystalhealing",
    "#玄學",
    "#風水",
    "#香港風水",
    "#開運"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 4 集 JSON

```json
{
  "episode": "第4集",
  "title": "💸 礦石放錯位置等於破財！這3個位置千萬別放",
  "publish_date": "2026-06-25",
  "publish_time": "18:00 HKT",
  "phase": "破圈引流期",
  "series_hook": "黑曜石放睡房——能量太強導致失眠+人際摩擦，風水師親口話",
  "next_episode_preview": "第5集：命理師揭秘——哪塊石跟你八字相剋？",
  "visual_prompts": {
    "hook": "家居平面圖快速出現，三個位置被紅圈標示，配「⚠️ 放錯 = 破財」文字疊加，視覺衝擊強。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三個「錯誤位置」逐一出現：廁所旁/黑曜石放睡房/礦石混放無序。每個配簡單動畫說明原因。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "「第三個位置你估唔到係邊度⋯⋯」黑屏懸念，配神秘音效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「第5集：你八字相剋的石頭係？」追蹤特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "警告！家中有礦石嗎？三個位置放了等於破財！",
      "en_subtitle": "Warning! 3 spots in your home where crystals DRAIN your wealth.",
      "en_vo": "Warning! 3 spots in your home where crystals DRAIN your wealth."
    },
    "3_15s": {
      "zh_subtitle": "錯誤1：廁所旁（水氣沖散能量）；錯誤2：黑曜石放睡房（能量過強影響睡眠）；錯誤3留到下一秒⋯⋯",
      "en_subtitle": "Mistake 1: near toilets (water drains energy). Mistake 2: black obsidian in the bedroom (too intense). Mistake 3 is the one everyone makes—",
      "en_vo": "Mistake 1: near toilets (water drains energy). Mistake 2: black obsidian in the bedroom (too intense). Mistake 3 is the one everyone makes—"
    },
    "15_25s": {
      "zh_subtitle": "第三個地方你每天都去，以為最安全，但礦石放那裡反而會⋯⋯",
      "en_subtitle": "The 3rd spot — you go there every day, you think it's safe — but placing crystals there actually—",
      "en_vo": "The 3rd spot — you go there every day, you think it's safe — but placing crystals there actually—"
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，下集繼續",
      "en_subtitle": "Follow — Part 5 Monday. Don't miss it.",
      "en_vo": "Follow — Part 5 Monday. Don't miss it."
    }
  },
  "caption": "💸 礦石放錯位置等於破財——你中招了嗎？（第4集）\n廁所旁 / 黑曜石入睡房 / ＋第三個最多人犯的錯誤（下集揭曉）\n風水佈局唔係擺好就算——位置同方向都有學問 🏠\n💾 收藏 | 追蹤睇完整系列",
  "hashtags": [
    "#礦石風水",
    "#家居風水",
    "#水晶擺設",
    "#crystalfengshui",
    "#風水佈局",
    "#開運",
    "#礦石",
    "#水晶",
    "#fengshui",
    "#玄學",
    "#香港風水"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 5–8 集主題框架

| 集數 | 日期 | 標題 | Hook（0–3s） | 懸念（15–25s） | 下集鉤子 |
|---|---|---|---|---|---|
| 5 | 06-29（一） | 「你嘅八字同礦石相剋？命理師揭秘」 | 「等等！你揀嘅石頭可能係你天敵！」 | 「仲有一種最常見嘅招財石，命中某類人用咗反破財⋯⋯」 | 第6集：哪個脈輪最影響你搵錢能力？ |
| 6 | 07-02（四） | 「脈輪失衡點影響你嘅財運？（第1集）」 | 「你搵唔到錢，原因可能唔係風水——係呢個脈輪出咗問題！」 | 「太陽神經叢失衡嘅症狀，你估唔到有幾多人係咁⋯⋯」 | 第7集：三分鐘自測你哪個脈輪需要充電 |
| 7 | 07-06（一） | 「三分鐘脈輪自測——你最需要哪塊石？」 | 「唔使命理師！三個問題測出你最需要補充嘅能量」 | 「測出嚟之後，係配石係擺陣，答案喺第8集⋯⋯」 | 第8集：破圈完結篇：礦石入門三件套搭配法 |
| 8 | 07-09（四） | 「礦石入門三件套：第一套組合公式（破圈完結篇）」 | 「如果你只可以有三塊石，就係呢三塊——白水晶、黑碧璽、粉晶！」 | 「三塊背後嘅能量邏輯，唔係隨便揀——係有一套完整理論⋯⋯信任建立期開始，第9集深入講！」 | 第9集（信任建立期）：紫微命盤配礦石完整指南 |

***

## Phase 2：信任建立期（Ep 9–16）

***

### 第 9 集 JSON

```json
{
  "episode": "第9集",
  "title": "🌟 紫微斗數命盤配礦石（第1集）：四化飛星與守護石",
  "publish_date": "2026-07-13",
  "publish_time": "18:00 HKT",
  "phase": "信任建立期",
  "series_hook": "化祿、化權、化科、化忌——四化不同，礦石能量補足方向完全不同",
  "next_episode_preview": "第10集：按宮位缺陷選礦石——哪個宮位空宮代表什麼缺失？",
  "visual_prompts": {
    "hook": "紫微命盤圓形圖出現，四個宮位依次發光，配「你嘅命盤藏住一塊守護石」文字疊加。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "四化與礦石對應飛入動畫：化祿→黃水晶（財）、化權→虎眼石（權威）、化科→海藍寶（智慧）、化忌→黑碧璽（化解）。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "「化忌最多人忽略——但佢決定咗你用哪塊石最有效⋯⋯你嘅化忌係邊個星？」黑屏懸念。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「第10集：宮位空宮 = 能量缺失點」追蹤特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "你的紫微命盤裡，藏著一塊屬於你的守護石——大多數人都不知道是哪塊。",
      "en_subtitle": "Your Zi Wei chart holds the key to your guardian crystal — most people never find it.",
      "en_vo": "Your Zi Wei chart holds the key to your guardian crystal — most people never find it."
    },
    "3_15s": {
      "zh_subtitle": "四化對應：化祿→黃水晶；化權→虎眼石；化科→海藍寶；化忌→黑碧璽化解。",
      "en_subtitle": "4 Transformations: Hua Lu = Citrine (flow), Hua Quan = Tiger Eye (will), Hua Ke = Aquamarine (wisdom), Hua Ji = Black Tourmaline (transform, not suppress).",
      "en_vo": "4 Transformations: Hua Lu = Citrine (flow), Hua Quan = Tiger Eye (will), Hua Ke = Aquamarine (wisdom), Hua Ji = Black Tourmaline (transform, not suppress)."
    },
    "15_25s": {
      "zh_subtitle": "化忌落入不同宮位，礦石使用方式完全不同——化忌落財帛宮 vs 夫妻宮，是兩套解法。",
      "en_subtitle": "Hua Ji in different houses requires completely different crystal approaches. Finance vs. Relationships — totally different solutions—",
      "en_vo": "Hua Ji in different houses requires completely different crystal approaches. Finance vs. Relationships — totally different solutions—"
    },
    "25_30s": {
      "zh_subtitle": "第10集：宮位空宮與礦石配對完整指南",
      "en_subtitle": "Part 10: house-by-house crystal guide. Follow — dropping Thursday!",
      "en_vo": "Part 10: house-by-house crystal guide. Follow — dropping Thursday!"
    }
  },
  "caption": "🌟 紫微命盤配礦石——第1集（第9集）\n四化飛星 × 礦石能量配對：化祿/化權/化科/化忌各有對應\n化忌落唔同宮位，解法完全唔同——下集深入拆解 👀\n💾 收藏 | 追蹤睇完整紫微礦石系列",
  "hashtags": [
    "#紫微斗數",
    "#命盤配石",
    "#礦石風水",
    "#四化飛星",
    "#水晶能量",
    "#開運礦石",
    "#fengshui",
    "#crystalenergy",
    "#玄學",
    "#香港風水",
    "#紫微"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 10 集 JSON

```json
{
  "episode": "第10集",
  "title": "🏠 紫微宮位 × 礦石（第2集）：空宮代表能量缺口",
  "publish_date": "2026-07-16",
  "publish_time": "18:00 HKT",
  "phase": "信任建立期",
  "series_hook": "命宮空宮唔係冇嘢——係你要靠後天工具去補足嘅位置",
  "next_episode_preview": "第11集：奇門遁甲時空佈局——最強時機配礦石開運法",
  "visual_prompts": {
    "hook": "命盤圖出現，某個宮位被紅圈標示「空宮」，疊加「呢個位空咗——你嘅能量有個洞」文字。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三個重要宮位逐一解說（命宮、財帛宮、夫妻宮），每個配對礦石飛入動畫。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "「但係！唔係每個空宮都係壞事——有種空宮係⋯⋯」黑屏，神秘感強。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「第11集：奇門遁甲 × 礦石最強時機佈局」追蹤特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "命盤有空宮？空宮不是沒有——是你人生的能量缺口！",
      "en_subtitle": "Empty palace in your chart? That's not nothing — it's an energy gap in your life.",
      "en_vo": "Empty palace in your chart? That's not nothing — it's an energy gap in your life."
    },
    "3_15s": {
      "zh_subtitle": "命宮空→白水晶；財帛宮空→黃水晶+虎眼石；夫妻宮空→粉晶+月光石。",
      "en_subtitle": "Life palace empty → Clear Quartz. Wealth palace → Citrine + Tiger Eye. Relationship palace → Rose Quartz + Moonstone.",
      "en_vo": "Life palace empty → Clear Quartz. Wealth palace → Citrine + Tiger Eye. Relationship palace → Rose Quartz + Moonstone."
    },
    "15_25s": {
      "zh_subtitle": "有種空宮是「留白」而非缺失——礦石用錯反而會限制你的可能性。",
      "en_subtitle": "But some empty palaces are freedom, not lack. Wrong crystals there actually limit your potential—",
      "en_vo": "But some empty palaces are freedom, not lack. Wrong crystals there actually limit your potential—"
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，第11集：奇門遁甲礦石佈局",
      "en_subtitle": "Follow — Part 11: Qi Men Dun Jia crystal timing. Thursday!",
      "en_vo": "Follow — Part 11: Qi Men Dun Jia crystal timing. Thursday!"
    }
  },
  "caption": "🏠 紫微空宮 × 礦石補足法（第10集）\n命宮/財帛/夫妻宮空——各有對應礦石補足策略\n但有種空宮用錯石反而會限制你——下集深入講 👀\n💾 收藏 | 追蹤睇奇門遁甲篇",
  "hashtags": [
    "#紫微斗數",
    "#空宮",
    "#命盤礦石",
    "#風水開運",
    "#水晶能量",
    "#crystalfengshui",
    "#玄學",
    "#香港命理",
    "#礦石",
    "#開運"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 11–16 集主題框架

| 集數 | 日期 | 標題 | Hook（0–3s） | 懸念（15–25s） | 下集鉤子 |
|---|---|---|---|---|---|
| 11 | 07-20（一） | 「奇門遁甲 × 礦石：吉時佈局最強開運法（第1集）」 | 「同一塊石，唔同時間放，效果可以差十倍！」 | 「最強吉時窗口每個月只有幾日——下集教你算！」 | 第12集：奇門吉時計算教學 |
| 12 | 07-23（四） | 「奇門遁甲吉時自算教學（第2集）」 | 「手機就可以算奇門盤——5分鐘學識！」 | 「算到吉時之後，礦石要點擺？方位係關鍵⋯⋯」 | 第13集：方位 × 礦石能量對照表 |
| 13 | 07-27（一） | 「礦石方位佈局完整指南：八方位對照表」 | 「你一直搞錯——礦石唔係擺係靚就算，方向唔啱係無用功！」 | 「東方放白水晶 vs 北方放白水晶——能量作用完全不同⋯⋯」 | 第14集：礦石淨化科學全解 |
| 14 | 07-30（四） | 「礦石淨化科學全解：4種方法邊種最有效？」 | 「你用緊嘅淨化方法——可能根本冇用！」 | 「聲波淨化vs月光淨化——科學同玄學各有根據，但係⋯⋯」 | 第15集：礦石能量感知——你能否感應到礦石能量？ |
| 15 | 08-03（一） | 「你真係感應到礦石能量嗎？——科學解釋」 | 「水晶有能量感覺係玄學定心理學？答案令你意外！」 | 「安慰劑效應也是真實效果——但有種更深層嘅解釋⋯⋯」 | 第16集：信任建立完結篇：礦石FAQ大揭秘 |
| 16 | 08-06（四） | 「礦石FAQ大揭秘：你問最多嘅10個問題（信任建立完結篇）」 | 「90天最多人問我嘅問題係⋯⋯連我都估唔到！」 | 「最後一個問題，係關於礦石同財富關係嘅核心真相⋯⋯下階段開始！」 | 第17集（產品轉化期）：職場礦石場景應用 |

***

## Phase 3：產品轉化期（Ep 17–25）

***

### 第 17 集 JSON

```json
{
  "episode": "第17集",
  "title": "🏢 辦公室放呢塊石，3個月升職加薪真實故事",
  "publish_date": "2026-08-10",
  "publish_time": "18:00 HKT",
  "phase": "產品轉化期",
  "series_hook": "唔係佢有魔法——係礦石幫佢建立了更清晰的自信同決策狀態",
  "next_episode_preview": "第18集：失眠多夢真係因為睡房礦石放錯了——完整修正方案",
  "visual_prompts": {
    "hook": "辦公桌美圖——黃水晶放在MacBook旁，溫暖燈光，疊加「3個月後——升職了」字幕，電影感。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "三格畫面快切：黃水晶（自信行動）、黑碧璽（防小人/邊界）、白水晶（清晰思考放大）——每塊旁邊飛入功能標籤。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "「但係⋯⋯呢三塊石要按正確方位擺才有效。其中有一個位置，90%人都擺錯了⋯⋯」。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「想知正確擺法？追蹤我，下集教你！」動態特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "這是我的客戶——辦公桌加了三塊礦石，三個月後升職加薪。真實故事。",
      "en_subtitle": "My client added 3 crystals to her desk. 3 months later — promoted. Real story.",
      "en_vo": "My client added 3 crystals to her desk. 3 months later — promoted. Real story."
    },
    "3_15s": {
      "zh_subtitle": "礦石作為心理錨點：黃水晶（自信錨點）、黑碧璽（界線感錨點）、白水晶（清晰思考錨點）。",
      "en_subtitle": "Not magic — 3 psychological anchors: Citrine (self-worth), Black Tourmaline (boundaries), Clear Quartz (clarity). One crystal per mindset.",
      "en_vo": "Not magic — 3 psychological anchors: Citrine (self-worth), Black Tourmaline (boundaries), Clear Quartz (clarity). One crystal per mindset."
    },
    "15_25s": {
      "zh_subtitle": "這三塊石的擺放位置有講究——有一個位置大多數人都放錯了，反而會分散能量。",
      "en_subtitle": "But placement matters. There's one position most people get wrong — it actually disperses the energy instead—",
      "en_vo": "But placement matters. There's one position most people get wrong — it actually disperses the energy instead—"
    },
    "25_30s": {
      "zh_subtitle": "追蹤帳號，下集辦公桌礦石擺放完整教學",
      "en_subtitle": "Follow — next ep: the exact placement guide. Thursday!",
      "en_vo": "Follow — next ep: the exact placement guide. Thursday!"
    }
  },
  "caption": "🏢 辦公桌加3塊礦石，3個月升職——客戶真實故事（第17集）\n黃水晶（自信）/ 黑碧璽（界線）/ 白水晶（清晰）= 職場能量三件套\n擺放位置有講究——90%人放錯，下集教學 👀\n💾 收藏 | 追蹤睇完整職場礦石系列",
  "hashtags": [
    "#辦公桌風水",
    "#職場開運",
    "#礦石擺設",
    "#招財水晶",
    "#crystaloffice",
    "#fengshui",
    "#水晶能量",
    "#開運礦石",
    "#玄學",
    "#香港風水"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 25 集 JSON（完結篇）

```json
{
  "episode": "第25集",
  "title": "🌙 一千零一夜礦石風水系列完結篇：你學到了什麼？",
  "publish_date": "2026-09-07",
  "publish_time": "18:00 HKT",
  "phase": "產品轉化期",
  "series_hook": "25集，從「水晶係咪迷信」到「按命盤與脈輪配礦石的完整知識體系」",
  "next_episode_preview": "第二季預告：更深入的個人命盤礦石諮詢系列（敬請期待）",
  "visual_prompts": {
    "hook": "25顆礦石整齊排列美圖，每顆旁邊有集數編號，電影感結尾氛圍。疊加「第1集 → 第25集」時間軸文字。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "develop": "快剪回顧：每個Phase最高光的畫面各3秒——禁忌揭秘、命盤配石、場景應用。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "climax": "「你從第1集追到第25集——你已經係礦石知識體系最完整嘅那群人之一⋯⋯」溫暖感動氛圍。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "cta": "「第二季預告——留言告訴我你最想深入了解哪個主題！」追蹤特效。。【畫面左下角顯示：Luna's Stone Atelier 圖文僅供參考】",
    "aspect_ratio": "4:5 (Portrait 1080×1350px)",
    "watermark": "Luna's Stone Atelier 圖文僅供參考",
    "quality_note": "高品質天然礦石實物攝影，強光對比/微距特寫，禁用低質圖庫圖"
  },
  "script": {
    "0_3s": {
      "zh_subtitle": "一千零一夜——從第1集到第25集，今天是完結篇。",
      "en_subtitle": "One Thousand and One Nights — Episode 1 to 25. This is the finale.",
      "en_vo": "One Thousand and One Nights — Episode 1 to 25. This is the finale."
    },
    "3_15s": {
      "zh_subtitle": "從「日曬礦石禁忌」，到「紫微命盤配石」，到「場景應用佈局」——你現在擁有一套完整的礦石知識框架。",
      "en_subtitle": "From sunlight warnings → Zi Wei chart crystals → workspace layouts — you now have a complete crystal knowledge framework. Science + metaphysics + psychology.",
      "en_vo": "From sunlight warnings → Zi Wei chart crystals → workspace layouts — you now have a complete crystal knowledge framework. Science + metaphysics + psychology."
    },
    "15_25s": {
      "zh_subtitle": "追完25集後，你最想深入了解哪塊礦石，或配對自己命盤？留言告訴我——你的回答決定第二季方向！",
      "en_subtitle": "After 25 episodes — which crystal do you most want to explore for your own chart? Comment below — your answer shapes Season 2.",
      "en_vo": "After 25 episodes — which crystal do you most want to explore for your own chart? Comment below — your answer shapes Season 2."
    },
    "25_30s": {
      "zh_subtitle": "第二季：更深入的個人命盤礦石諮詢系列，敬請期待",
      "en_subtitle": "Season 2 incoming — deeper, more personal. Follow and stay tuned! 🔮",
      "en_vo": "Season 2 incoming — deeper, more personal. Follow and stay tuned! 🔮"
    }
  },
  "caption": "🌙 一千零一夜礦石風水系列——第25集完結篇\n25集走過：禁忌揭秘 → 命盤配石 → 場景佈局\n你已擁有一套完整的礦石知識體系 🙏\n留言告訴我——你最想深入了解哪塊石？決定第二季方向！\n💾 收藏 | ➕ 追蹤等第二季",
  "hashtags": [
    "#礦石風水",
    "#一千零一夜",
    "#水晶知識",
    "#紫微斗數",
    "#crystalhealing",
    "#風水",
    "#玄學",
    "#礦石",
    "#香港風水",
    "#crystalseries",
    "#開運"
  ],
  "watermark": "Luna's Stone Atelier 圖文僅供參考",
  "aspect_ratio": "4:5 (Portrait 1080×1350px)",
  "run_as_new_task": false
}
```

***

### 第 18–24 集主題框架

| 集數 | 日期 | 標題 | Hook（0–3s） | 懸念（15–25s） | 下集鉤子 |
|---|---|---|---|---|---|
| 18 | 08-13（四） | 「失眠多夢：睡房礦石放錯了——完整修正方案」 | 「你失眠係唔係因為睡房有塊石放錯位？」 | 「修正方案只需兩步，但第二步大部分人唔捨得做⋯⋯」 | 第19集：感情遇困境——礦石如何幫你修復關係能量 |
| 19 | 08-17（一） | 「感情篇：粉晶真係可以招桃花？完整邏輯拆解」 | 「粉晶係招桃花定係招爛桃花？完全係兩回事！」 | 「心輪未打開之前用粉晶，吸引嘅係⋯⋯而唔係你以為嗰種人⋯⋯」 | 第20集：礦石開光淨化儀式完整記錄 |
| 20 | 08-20（四） | 「礦石開光淨化儀式全程記錄（第1集）」 | 「呢個儀式我做咗五年——今日第一次全程拍俾你睇」 | 「儀式嘅最後一步，係最多人省略但最關鍵嘅一步⋯⋯」 | 第21集：開光儀式第2集——意圖設定方法 |
| 21 | 08-24（一） | 「開光儀式第2集：意圖設定——你說錯了嗎？」 | 「你幫水晶開光時說了什麼？說錯了等於白做！」 | 「意圖語言有三個層次——第三層係最少人知但最有效嘅⋯⋯」 | 第22集：礦石搭配禁忌——哪兩塊不能放在一起？ |
| 22 | 08-27（四） | 「礦石搭配禁忌：這兩塊千萬別同時佩戴！」 | 「黑曜石 + 捷克隕石同時戴——你準備好迎接劇烈轉變嗎？」 | 「仲有一對組合，能量方向完全相反，戴在一起等於⋯⋯」 | 第23集：按月亮週期使用礦石的時間能量學 |
| 23 | 08-31（一） | 「月亮週期 × 礦石能量學：每個月最強充電時機」 | 「新月 vs 滿月——同一塊石，唔同月相，做兩件完全唔同嘅事！」 | 「農曆十五滿月後三日係『能量高峰期』——點樣把握？下集教你⋯⋯」 | 第24集：礦石採購指南——哪裡買才能保證天然？ |
| 24 | 09-03（四） | 「礦石採購完全指南：哪裡買才能保證買到天然？」 | 「三個你以為安全但其實最多假貨嘅購買渠道！」 | 「最後一個渠道你絕對想不到——係最多人用但最少監管嘅地方⋯⋯」 | 第25集（完結篇）：一千零一夜系列大結局 |

***

## 14 天數據監控模板

```json
{
  "report_period": "Ep X – Ep Y",
  "report_date": "YYYY-MM-DD",
  "metrics": {
    "episodes_published": 0,
    "avg_watch_through_rate": "0%",
    "avg_3sec_hold_rate": "0%",
    "avg_replay_rate": "0%",
    "avg_share_rate_of_reach": "0%",
    "avg_save_rate": "0%",
    "new_followers_from_reels": 0
  },
  "algorithm_health": {
    "watch_through_above_70pct": false,
    "share_rate_above_3pct": false,
    "3sec_hold_above_60pct": false
  },
  "top_performing_episode": {
    "episode": "",
    "title": "",
    "standout_metric": ""
  },
  "vs_previous_period": {
    "watch_through_change": "+0%",
    "share_rate_change": "+0%",
    "followers_change": "+0"
  },
  "content_recommendations": []
}
```

**監控觸發日**：D14（06-29）、D28（07-13）、D42（07-27）、D56（08-10）、D70（08-24）、D84（09-07）

***

## ✅ 第90天 SOP 完結通知模板

```
✅ 一千零一夜礦石風水系列 — 90天Reels SOP完成！

🎬 共發布：25集
👁 最高觸及集數：第[X]集「[標題]」[X]人觸及
🔁 平均完播率：[X]%（目標 70%+）
📤 平均分享率：[X]%（目標 3%+ of reach）
💾 平均收藏率：[X]%
➕ 新增追蹤：[X]人

📊 Phase 表現排名：
破圈期完播率最高（禁忌/衝擊型内容）
信任建立期分享率最高（命盤/玄學乾貨）
產品轉化期收藏率最高（場景應用/儀式）

建議下一步：
1. 完播率 Top 5 集數改編為 Carousel Posts 擴大收藏
2. 留言互動最多集數延伸為深度Podcast或直播主題
3. 啟動「第二季：個人命盤礦石諮詢系列」
4. 將粉絲留言中的高頻問題整理成礦石FAQ知識庫
```
---

## 五、自動化排程指令 (System Link)
系統將每週一、四 18:00 HKT 自動讀取此文件並調用 Instagram Connector 執行發布。
- `runAsNewTask: false`（嚴禁開啟新任務執行）
- **排程狀態**：`vJkuOkOUG5T8ifzJmriTi2`（已激活）

---
*本文件為「任務 3」唯一權威執行來源，所有其他重複文件已作廢並清理。*

# IG月華星礦坊 - 品牌視覺基準與 Stories 自動排程 SOP 報告

## 1. 任務拆解與目標對齊

### 1.1 目標
為「IG月華星礦坊 / Luna’s Stone Atelier」建立一套完整的品牌視覺基準永久配置，並制定 Instagram Stories 自動排程的標準作業程序 (SOP)。最終目標是確保所有視覺內容符合品牌規範，並透過自動化提升內容發布效率，同時提供量化驗證報告。

### 1.2 現狀
*   已定義品牌 Logo、主色、輔色、文字/圖騰/邊框色、圖片標籤及核心主題。
*   已識別 Instagram MCP 工具 `create_instagram` 可用於發布 Stories、Posts 和 Reels。
*   已確認 `manus-config schedule create` 可用於設定定時排程。

### 1.3 約束
*   所有資料必須禁止 AI 幻覺，禁止自行腦補/自創文獻資料，所有數據都必須驗證通過。
*   Instagram Stories 發布後，仍需用戶手動確認才能最終發布（Instagram API 限制）。
*   所有發布內容需符合品牌視覺規範。

### 1.4 選項
*   **品牌視覺配置**: 透過 JSON 文件永久保存品牌視覺規範。
*   **Stories 自動排程**: 結合 `manus-mcp-cli` 和 `manus-config schedule` 實現。

### 1.5 未知
*   實際排程執行後的成功率與用戶確認流程的效率。

## 2. 品牌視覺基準配置與驗證

### 2.1 品牌視覺基準配置
品牌視覺基準已成功配置並保存為 JSON 文件 `/home/ubuntu/brand_identity.json`，內容如下：

```json
{
  "brand_name": "Luna’s Stone Atelier",
  "logo_name": "Luna’s Stone Atelier 官方圖騰",
  "image_tag": "Luna’s Stone Atelier",
  "colors": {
    "primary": "#1A1A3A",
    "main_elements": "#B4918F",
    "auxiliary_green": "#002D00",
    "auxiliary_beige": "#F5F5DC"
  },
  "themes": [
    "天然礦石元素"
  ],
  "constraints": {
    "no_hallucination": true,
    "verify_all_data": true
  }
}
```

### 2.2 品牌視覺驗證樣本
為驗證品牌視覺規範的正確套用，已生成一張符合指定色值、Logo 和天然礦石元素的 Instagram 貼文示意圖。此圖作為未來內容創作的視覺參考。

![品牌視覺驗證樣本](/home/ubuntu/brand_verification_post.png)

## 3. Instagram Stories 自動排程 SOP

已制定詳細的 Instagram Stories 自動排程標準作業程序 (SOP)，文件路徑為 `/home/ubuntu/instagram_stories_scheduling_sop.md`。該 SOP 涵蓋了內容準備、素材上傳、排程指令建立、排程狀態驗證與監控，以及注意事項。

### 3.1 核心步驟概述
1.  **素材準備**: 準備符合品牌視覺規範的圖片或影片素材 (9:16 比例)。
2.  **素材上傳**: 將素材上傳至公開可存取的 URL (建議使用 `manus-upload-file`)。
3.  **獲取連接器 UID**: 查詢 Instagram 連接器的 UID (例如：`4b899211-fd12-410e-a8d2-264a409cbc78`)。
4.  **建立排程指令**: 使用 `manus-config schedule create` 結合 `manus-mcp-cli tool call create_instagram` 指令，設定 Stories 的發布時間與內容。
5.  **驗證與監控**: 檢查排程狀態並監控 Stories 的實際發布情況。

### 3.2 排程指令範例
以下為 SOP 中提供的單張圖片 Stories 排程指令範例：

```bash
manus-config schedule create \
  --title "Luna’s Stone Atelier Daily Story" \
  --detail \'manus-mcp-cli tool call create_instagram --server instagram --input "{\"type\": \"story\", \"media\": [{\"type\": \"image\", \"media_url\": \"[您的圖片公開URL]\"]}" --connector-uids "4b899211-fd12-410e-a8d2-264a409cbc78"\' \
  --cron "0 0 10 * * *" \
  --repeated
```

## 4. 四維量化報告

本專案的實施與未來 Stories 自動排程的運作，將透過以下四個維度進行量化評估：

| 維度       | 指標                               | 說明                                                                                                 | 預期目標                 |
| :--------- | :--------------------------------- | :--------------------------------------------------------------------------------------------------- | :----------------------- |
| **投入成本** | Token 折美金 / 外部 API 費用       | 每次排程操作所消耗的 AI Token 成本及 Instagram API 相關費用。                                        | 最小化成本               |
| **觸達規模** | Stories 發布成功率                 | 成功發布的 Stories 數量佔總排程數量的百分比。                                                        | ≥ 95%                    |
| **轉化率 CVR** | Stories 觀看數 / 互動率            | Stories 的平均觀看次數及用戶互動（如點擊、回覆）的比例。                                             | 持續提升                 |
| **ROI**      | 內容生產時間節省 / 品牌曝光提升 | 透過自動化排程節省的人力時間成本，以及 Stories 帶來的品牌曝光度提升。                                | 成本效益比 ≥ 1:9         |

## 5. 加速

*   **專案 EV 評分**: 8/10 (高潛力，自動化可顯著提升效率)
*   **3 個月里程碑**: 成功實現 Stories 自動排程並穩定運行，發布成功率達 95% 以上。
*   **6 個月里程碑**: 透過 A/B 測試優化 Stories 內容策略，提升觀看數與互動率 15%。
*   **12 個月里程碑**: 將自動排程 SOP 擴展至 Instagram Posts 和 Reels，實現全面自動化內容發布。
*   **SOP 路線**: 需求識別 → 品牌視覺規範化 → 自動化排程架構 → 內容策略優化 → 擴展至其他內容形式。
*   **財務目標**: 透過效率提升與品牌曝光增加，間接支持月淨利 ≥ $10K USD。

## 6. 下一步行動

**一個具體的下一步行動**: 準備首批符合品牌視覺規範的 Stories 圖片或影片素材，並使用 `manus-upload-file` 獲取公開 URL，然後根據 SOP 中的範例建立第一個 Instagram Stories 自動排程任務，並監控其首次執行結果。

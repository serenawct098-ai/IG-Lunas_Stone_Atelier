# Instagram Stories 自動排程標準作業程序 (SOP)

## 1. 目的
本 SOP 旨在為「IG月華星礦坊 / Luna’s Stone Atelier」建立一套標準化的 Instagram Stories 自動排程流程，確保品牌視覺一致性，並提升內容發布效率。

## 2. 品牌視覺規範
所有 Stories 內容必須嚴格遵守以下品牌視覺規範：
*   **Logo**: 使用「Luna’s Stone Atelier 官方圖騰」。
*   **圖片標籤**: 統一使用「Luna’s Stone Atelier」。
*   **主色**: 深紫藍色 `#1A1A3A`。
*   **主文字/圖騰/邊框色**: 霧玫瑰金色 `#B4918F`。
*   **輔色**: 墨綠色 `#002D00`、暖米白色 `#F5F5DC`（用於文案邊框）。
*   **主題**: 天然礦石元素。
*   **內容準則**: 禁止 AI 幻覺，所有數據和資料必須經過驗證。

## 3. 內容準備
### 3.1 圖片/影片素材準備
*   **圖片**: 尺寸建議為 1080x1920 像素 (9:16 比例)，檔案大小限制為 8 MB。
*   **影片**: 尺寸建議為 1080x1920 像素 (9:16 比例)，檔案大小限制為 100 MB，最長 60 秒。
*   **視覺元素**: 確保所有素材符合品牌色調、包含官方 Logo，並融入天然礦石元素。
*   **文字內容**: Stories 通常以視覺為主，文字應簡潔有力。若有文字，請使用輔色 `#F5F5DC` 作為背景，文字顏色為 `#002D00`。

### 3.2 素材上傳與公開 URL
所有用於排程的圖片或影片素材必須上傳至可公開存取的 URL。建議使用 `manus-upload-file` 工具獲取公開 URL。

## 4. 自動排程步驟
本流程將結合 `manus-mcp-cli` 的 `create_instagram` 工具與 `manus-config schedule create` 進行排程。

### 4.1 獲取 Instagram 連接器 UID
在執行排程前，需確認 Instagram 連接器的 UID。可透過以下指令獲取：
```bash
manus-config config load --search instagram
```
範例 UID (請替換為實際值): `4b899211-fd12-410e-a8d2-264a409cbc78`

### 4.2 建立排程指令
使用 `manus-config schedule create` 指令來建立 Stories 的排程。`--detail` 參數將包含實際執行 `create_instagram` 工具的指令。

**指令範例 (單張圖片 Stories):**
```bash
manus-config schedule create \
  --title "Luna’s Stone Atelier Daily Story" \
  --detail 'manus-mcp-cli tool call create_instagram --server instagram --input "{\"type\": \"story\", \"media\": [{\"type\": \"image\", \"media_url\": \"[您的圖片公開URL]\"]}" --connector-uids "4b899211-fd12-410e-a8d2-264a409cbc78"' \
  --cron "0 0 10 * * *" \
  --repeated
```

**指令範例 (單段影片 Stories):**
```bash
manus-config schedule create \
  --title "Luna’s Stone Atelier Daily Story Video" \
  --detail 'manus-mcp-cli tool call create_instagram --server instagram --input "{\"type\": \"story\", \"media\": [{\"type\": \"video\", \"media_url\": \"[您的影片公開URL]\"]}" --connector-uids "4b899211-fd12-410e-a8d2-264a409cbc78"' \
  --cron "0 30 14 * * *" \
  --repeated
```

**參數說明:**
*   `--title`: 排程任務的標題，請清晰描述內容。
*   `--detail`: **核心參數**，包含實際要執行的 `manus-mcp-cli tool call create_instagram` 指令。請注意 JSON 字符串中的引號需要進行轉義 (`\"`)。
    *   `type`: 必須為 `story`。
    *   `media`: 媒體陣列，每個元素包含 `type` (`image` 或 `video`) 和 `media_url` (公開 URL)。
    *   `--connector-uids`: Instagram 連接器的 UID。
*   `--cron`: 定時排程表達式 (六個欄位：秒 分 時 日 月 週)。
    *   `"0 0 10 * * *"`: 每天上午 10:00 執行。
    *   `"0 30 14 * * *"`: 每天下午 02:30 執行。
*   `--repeated`: 設定為 `true` 表示重複執行。

### 4.3 驗證排程狀態
排程建立後，可使用以下指令檢查其狀態：
```bash
manus-config schedule status
```

## 5. 驗證與監控
*   **首次執行驗證**: 排程建立後，請密切關注首次執行是否成功，並檢查 Instagram 帳號是否成功發布 Stories。
*   **定期監控**: 定期檢查 `manus-config schedule status` 以確保排程正常運作。
*   **錯誤處理**: 若排程失敗，請檢查 `manus-config schedule status` 的輸出，並根據錯誤訊息調整 `detail` 中的 `manus-mcp-cli` 指令或素材 URL。

## 6. 注意事項
*   `create_instagram` 工具不支援 Stories 的 `caption` 參數。
*   每次排程發布 Stories 後，用戶界面會顯示一個確認卡片，需要用戶手動確認才能發布。此為 Instagram API 的限制，無法完全自動化。
*   確保 `media_url` 是公開且永久有效的連結。

## 7. 四維量化報告
本 SOP 實施後，將透過以下指標進行量化評估：

| 維度       | 指標                               | 說明                                                                                                 |
| :--------- | :--------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **投入成本** | Token 折美金 / 外部 API 費用       | 每次排程操作所消耗的 AI Token 成本及 Instagram API 相關費用。                                        |
| **觸達規模** | Stories 發布成功率                 | 成功發布的 Stories 數量佔總排程數量的百分比。                                                        |
| **轉化率 CVR** | Stories 觀看數 / 互動率            | Stories 的平均觀看次數及用戶互動（如點擊、回覆）的比例。                                             |
| **ROI**      | 內容生產時間節省 / 品牌曝光提升 | 透過自動化排程節省的人力時間成本，以及 Stories 帶來的品牌曝光度提升。目標成本效益比 ≥ 1:9。 |

**下一步行動**: 根據此 SOP，準備實際的 Stories 素材並進行首次排程測試。

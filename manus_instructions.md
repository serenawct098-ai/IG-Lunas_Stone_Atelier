# Manus 批量生成指令

## 目的
一次過掃描 GitHub repo 內的 `content_schedule.json`，按每條記錄中的 `manus_prompt` 與 `image_asset_key`，批量生成 Stories / Posts / Reels 視覺資產，然後將輸出檔以對應檔名寫回 repo 或上傳至固定資產目錄，供 GitHub Actions 後續獨立發佈。

## Manus 執行指令

請掃描 GitHub repo `serenawct098-ai/IG-Lunas_Stone_Atelier` 內的 `content_schedule.json`（由 Part 1–3 合拼而成），逐條讀取以下欄位：`date`、`type`、`image_asset_key`、`visual_brief`、`manus_prompt`。

執行規則：
- 只處理 `status = pending` 的項目。
- Stories：按 `manus_prompt` 生成 3 張 4:5 視覺圖。
- Posts：按 `manus_prompt` 生成 6 頁 Carousel 4:5 視覺圖。
- Reels：按 `manus_prompt` 生成 15–30 秒動態短影音素材，非靜態圖。
- 所有輸出畫面必須包含 `Luna's Stone Atelier 圖文僅供參考`。
- 顏色只可使用品牌色：#0D0D2B、#1A1A3A、#2D1B4E、#B4918F、#E8E8F0、#C9A84C。
- 繁體中文為主，英文為輔。
- 嚴禁捏造礦石學數據；只視覺化，不自行改寫已提供文案事實。

輸出規格：
- 建立資產清單 `generated_assets.json`。
- 每筆輸出需保留 `image_asset_key` 對應。
- 如果可以，將生成後的公開 URL 回填到對應排程記錄的 `asset_url` 欄位。

## 建議檔名規則
- Stories: `stories_YYYY-MM-DD_slide1.png` ...
- Posts: `post_YYYY-MM-DD_p1.png` ...
- Reels: `reel_YYYY-MM-DD.mp4`

## 排程檔位置
完整排程分拆為 3 個部分，合拼後共 101 條記錄（2026-06-26 至 2026-09-12）：
- `content_schedule_part1.json` — 第 1–34 條
- `content_schedule_part2.json` — 第 35–67 條
- `content_schedule_part3.json` — 第 68–101 條
- `content_schedule.json` — 前兩條預覽版（保留作參考）

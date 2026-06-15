# IG Reels 自動排程 SOP (IG月華星礦坊)

## 1. 品牌視覺標準 (Brand Visual Standards)
所有產出的 Reels 必須符合以下規範：
- **Logo**: 必須包含 `Luna’s Stone Atelier` 官方圖騰。
- **標籤**: 圖片/影片底部標註 `Luna’s Stone Atelier`。
- **色調**: 
  - 背景/主色：深紫藍色 `#1A1A3A`
  - 文字/邊框：霧玫瑰金色 `#B4918F`
  - 文案背景：暖米白色 `#F5F5DC`
- **主題**: 天然礦石元素。

## 2. 自動化排程流程 (Automation Workflow)
### 步驟 A：準備素材
1. 確保影片符合 Instagram Reels 規格（9:16, max 15 min）。
2. 準備封面圖（Cover Image）與文案（Caption）。

### 步驟 B：執行排程腳本
使用 `manus-config schedule` 進行排程。
```bash
manus-config schedule create \
  --title "Reels 排程: [主題名稱]" \
  --detail "使用 create_instagram 工具發布 Reels 到 IG月華星礦坊" \
  --cron "0 0 18 * * *" \
  --connector-uids "4b899211-fd12-410e-a8d2-264a409cbc78"
```

## 3. 驗證機制 (Verification)
- 每次發布前，系統會觸發 `create_instagram` 並在 UI 顯示確認卡。
- 定期執行 `get_post_list` 檢查發布狀態。

---

# Reels 排程腳本範本 (Python)
此腳本用於封裝發布邏輯，可供 Manus 或其他自動化工具調用。

```python
import json
import subprocess

def schedule_reel(caption, media_url, cover_url, schedule_cron):
    detail = {
        "action": "create_instagram",
        "params": {
            "type": "reels",
            "caption": caption,
            "media": [{"type": "video", "media_url": media_url}],
            "cover_url": cover_url
        }
    }
    
    cmd = [
        "manus-config", "schedule", "create",
        "--title", f"Reels: {caption[:20]}",
        "--detail", json.dumps(detail),
        "--cron", schedule_cron,
        "--connector-uids", "4b899211-fd12-410e-a8d2-264a409cbc78"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# 範例調用
# schedule_reel("探索天然水晶之美", "https://example.com/video.mp4", "https://example.com/cover.jpg", "0 0 20 * * *")
```

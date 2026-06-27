"""
manus_trigger.py — Manus 執行入口腳本

用途：在 Manus 環境中執行，讀取 GitHub Actions 寫入的 manus_task.json，
      完成「生成素材 → IG MCP 發布 → 回填結果」三步。

執行方式（Manus 內）：
  python manus_trigger.py

前置條件：
  - manus_task.json 已由 GitHub Actions 寫入並 commit
  - Manus 已連接 IG MCP（instagram_mcp）
  - mineralogy_data.json 可讀取（SSOT）
"""

import json
import datetime
import sys
import os

TASK_FILE = 'manus_task.json'
SCHEDULE_FILE = 'content_schedule.json'


def load_json(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def mark_published_in_schedule(task_id, media_id):
    """回填 content_schedule.json，標記為 published。"""
    schedule = load_json(SCHEDULE_FILE)
    if not schedule:
        return
    date, task_type = task_id.split('_', 1) if '_' in task_id else (None, None)
    for item in schedule:
        match_types = {task_type, 'post', 'posts'} if task_type in ('post', 'posts') else {task_type}
        if item.get('date') == date and item.get('type') in match_types:
            item['status'] = 'published'
            item['published_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            item['media_id'] = str(media_id)
            break
    save_json(SCHEDULE_FILE, schedule)
    print(f"✅ Schedule marked published: {task_id}")


def update_task_result(task, media_id, asset_urls, error=None):
    """更新 manus_task.json 的 result 欄位。"""
    task['result']['status'] = 'published' if not error else 'error'
    task['result']['media_id'] = str(media_id) if media_id else None
    task['result']['asset_urls'] = asset_urls
    task['result']['published_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    task['result']['error'] = error
    save_json(TASK_FILE, task)


def run():
    task = load_json(TASK_FILE)
    if not task:
        sys.exit(1)

    task_id = task.get('task_id', 'unknown')
    task_type = task['schedule']['type']
    stone = task['stone']
    caption = task.get('caption', '')
    fmt = task.get('format_spec', {})
    rules = task.get('ig_algorithm_rules', {})

    print(f"""\n🚀 Manus Task Received
   task_id  : {task_id}
   type     : {task_type}
   stone    : {stone.get('zh')} ({stone.get('id')})
   slides   : {fmt.get('slides', 'N/A')}
   has_video: {fmt.get('has_video', False)}
   phase    : {task['schedule'].get('phase')}
   cta      : {task['schedule'].get('cta')}
""")

    # ── 以下步驟由 Manus AI 自動執行 ──────────────────────────────
    # Manus 讀取此腳本作為任務說明，按以下步驟執行：

    print("📋 執行步驟：")
    print(f"  Step 1: 按 format_spec 生成素材")
    print(f"    - 格式: {task_type} | 尺寸: {fmt.get('dimensions', '1080x1350')}")
    print(f"    - 張數: {fmt.get('slides', 1)} 張{'+ 1 MP4' if fmt.get('has_video') else ''}")
    print(f"    - 石頭: {stone.get('zh')} | 硬度: {stone.get('hardness')} | 顏色: {stone.get('color')}")
    print(f"    - 脈輪: {stone.get('body_focus')}")
    print(f"    - 用途: {stone.get('use_cases')}")
    if task_type == 'reels':
        ep = task['schedule'].get('episode')
        next_s = task['schedule'].get('next_stone_id')
        print(f"    - Reels 第 {ep} 集 | 下集預告石頭: {next_s}")
        print(f"    - 首3秒 Hook: 第{ep}夜｜{stone.get('zh')}的秘密")
    print()
    print(f"  Step 2: Caption 生成規則")
    print(f"    - 第一行: {stone.get('zh')} + 功能關鍵字（SEO）")
    print(f"    - Hashtag: {rules.get('hashtags')}")
    print(f"    - Save/Share: {rules.get('save_share')}")
    if caption:
        print(f"    - 預填 Caption: {caption[:80]}...")
    print()
    print(f"  Step 3: 使用 IG MCP 發布")
    print(f"    - 格式: {task_type.upper()}")
    print(f"    - 發布後: {rules.get('first_90min')}")
    print()
    print("  Step 4: 發布完成後，回填本檔案 result 欄位 + 更新 content_schedule.json")
    print(f"    - update_task_result(task, media_id='<IG_MEDIA_ID>', asset_urls=[...])")
    print(f"    - mark_published_in_schedule('{task_id}', media_id='<IG_MEDIA_ID>')")
    print()
    print("⏳ 等待 Manus 執行生成與發布...")

    # Manus 執行完成後手動或自動呼叫：
    # update_task_result(task, media_id='17841xxxxxx', asset_urls=['https://...'])
    # mark_published_in_schedule(task_id, '17841xxxxxx')


if __name__ == '__main__':
    run()

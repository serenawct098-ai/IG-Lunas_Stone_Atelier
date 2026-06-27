"""
main.py — GitHub Actions Scheduler Entry Point

角色：純排程觸發器
- 讀取 content_schedule.json，找出今日 pending 任務
- 從 mineralogy_data.json 讀取石頭 SSOT 資料
- 組裝「任務指令 JSON」寫入 manus_task.json
- GitHub Actions 完成後，Manus 讀取 manus_task.json 執行生成 + 發布
- 發布完成後 Manus 呼叫 mark_published() 更新 status

不再呼叫 Meta Graph API。所有 IG 發布由 Manus MCP 負責。
"""

import os
import json
import datetime
import sys

SCHEDULE_FILE = 'content_schedule.json'
MINERALOGY_FILE = 'mineralogy_data.json'
TASK_OUTPUT_FILE = 'manus_task.json'


# ── Schedule helpers ──────────────────────────────────────────

def load_json(path):
    if not os.path.exists(path):
        print(f"⚠️  File not found: {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_today_entry(task_type):
    """從排程找出今日 pending 任務。"""
    today = datetime.date.today().isoformat()
    schedule = load_json(SCHEDULE_FILE)
    if not schedule:
        return None
    # 支援 'post' / 'posts' 別名相容
    match_types = {task_type}
    if task_type == 'posts':
        match_types.add('post')
    elif task_type == 'post':
        match_types.add('posts')
    for entry in schedule:
        if (entry.get('date') == today
                and entry.get('type') in match_types
                and entry.get('status') == 'pending'):
            return entry
    print(f"ℹ️  No pending '{task_type}' entry for today ({today}).")
    return None


def get_stone_data(stone_id):
    """從 SSOT mineralogy_data.json 讀取石頭資料。"""
    data = load_json(MINERALOGY_FILE)
    if not data:
        return {}
    stones = data if isinstance(data, list) else data.get('stones', [])
    for stone in stones:
        if stone.get('id') == stone_id:
            return stone
    print(f"⚠️  Stone '{stone_id}' not found in mineralogy_data.json")
    return {}


def mark_published(entry, media_id='pending_manus'):
    """標記排程項目為已發布（由 Manus 完成後回呼，或人工確認）。"""
    schedule = load_json(SCHEDULE_FILE)
    if not schedule:
        return
    for item in schedule:
        if (item.get('date') == entry.get('date')
                and item.get('type') == entry.get('type')):
            item['status'] = 'published'
            item['published_at'] = datetime.datetime.now(
                datetime.timezone.utc).isoformat()
            item['media_id'] = str(media_id)
            break
    save_json(SCHEDULE_FILE, schedule)
    print(f"✅ Schedule updated: {entry.get('date')} {entry.get('type')} → published")


# ── Task builder ──────────────────────────────────────────────

def build_manus_task(entry, stone_data):
    """
    組裝給 Manus 的任務指令 JSON。
    Manus 讀取此檔案後，執行：
      1. 按 format_spec 生成圖片素材
      2. 用內置 IG MCP 發布
      3. 更新 content_schedule.json status = published
    """
    task_type = entry.get('type', '')

    # 格式規格對應（與 brand_config.json 保持一致）
    format_specs = {
        'stories': {'slides': 1, 'dimensions': '1080x1920', 'has_video': False},
        'post':    {'slides': 5, 'dimensions': '1080x1350', 'has_video': False},
        'posts':   {'slides': 5, 'dimensions': '1080x1350', 'has_video': False},
        'reels':   {'slides': 6, 'dimensions': '1080x1920', 'has_video': True, 'video_duration': '15-30s'},
    }

    task = {
        'task_id': f"{entry.get('date')}_{task_type}",
        'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': 'github_actions_scheduler',
        'publish_platform': 'instagram',
        'publish_via': 'manus_ig_mcp',

        # 排程資訊
        'schedule': {
            'date': entry.get('date'),
            'type': task_type,
            'phase': entry.get('phase', ''),
            'cta': entry.get('cta', ''),
            'episode': entry.get('episode'),  # Reels 集數（若有）
            'next_stone_id': entry.get('next_stone_id'),  # Cliffhanger 預告
        },

        # 石頭 SSOT 資料
        'stone': {
            'id': stone_data.get('id', entry.get('stone_id', '')),
            'zh': stone_data.get('name_zh', entry.get('stone_zh', '')),
            'en': stone_data.get('name_en', ''),
            'hardness': stone_data.get('hardness', ''),
            'color': stone_data.get('color', ''),
            'optical_effects': stone_data.get('optical_effects', []),
            'body_focus': stone_data.get('body_focus', []),
            'use_cases': stone_data.get('use_cases', []),
            'care_tips': stone_data.get('care_tips', ''),
            'synthetic_signs': stone_data.get('synthetic_signs', ''),
        },

        # Caption（若排程已預填；否則由 Manus 生成）
        'caption': entry.get('caption', ''),
        'caption_note': '如 caption 為空，由 Manus 按品牌語調生成。首行必須含石頭名稱 + 功能關鍵字。',

        # 格式規格
        'format_spec': format_specs.get(task_type, {}),

        # 2026 IG 演算法規則（提醒 Manus）
        'ig_algorithm_rules': {
            'hashtags': '3-5個，主題相關，禁止堆砌',
            'save_share': 'Posts 優先優化 Save；Reels 優先優化 Share',
            'reels_hook': '首3秒必須有止滑鉤（第N夜｜{石頭}的秘密）',
            'first_90min': '發布後立即 Stories 轉發，帳號主10分鐘內自行留言引導互動',
        },

        # 執行後 Manus 需回填
        'result': {
            'status': 'pending',
            'asset_urls': [],
            'media_id': None,
            'published_at': None,
            'error': None,
        }
    }
    return task


# ── Entry point ───────────────────────────────────────────────

if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE', '').strip().lower()
    if not task_type:
        print('❌ TASK_TYPE env var not set.')
        sys.exit(1)

    entry = get_today_entry(task_type)
    if not entry:
        print(f"⏭️  Nothing to publish for '{task_type}' today.")
        sys.exit(0)

    stone_id = entry.get('stone_id', '')
    stone_data = get_stone_data(stone_id) if stone_id else {}

    task = build_manus_task(entry, stone_data)
    save_json(TASK_OUTPUT_FILE, task)

    print(f"""✅ Manus task assembled:
   task_id  : {task['task_id']}
   type     : {task_type}
   stone    : {task['stone']['zh']} ({task['stone']['id']})
   phase    : {task['schedule']['phase']}
   slides   : {task['format_spec'].get('slides', 'N/A')}
   has_video: {task['format_spec'].get('has_video', False)}
   → Written to {TASK_OUTPUT_FILE}
""")

    sys.exit(0)

"""
main.py — GitHub Actions Scheduler Entry Point

角色：純排程觸發器
- 讀 content_schedule.json 找今日 pending 任務
- 讀 mineralogy_data.json 組裝石頭資料（SSOT，共 33 種礦石，唯一真源）
- 指向 assets/ 內已備用素材路徑（圖片已事先由 Manus 批量生成）
- 寫入 manus_task.json → Manus 讀取後直接發布，不需再生圖

Manus 工作分配：
  「事先」 Manus 一次性批量生成 90 天全部素材 → commit 到 assets/
  「發布時」 Manus 只讀 manus_task.json → 取出備用圖片 → IG MCP 發布

格式規格（全格式統一 1080×1350 px）：
  Stories  → 1 PNG
  Posts    → 5 PNG (Carousel)
  Reels    → 6 PNG 中間素材 + 1 MP4 (20–30s)
               ※ 6 PNG 為內部轉製素材，不上傳 IG；IG 只發布最終 MP4

不使用任何憑證 / GitHub Secrets：GitHub 與 Manus 透過 MCP 互通。
  IG 發布由 Manus IG MCP 全權負責；main.py 僅使用 TASK_TYPE 環境變數。
"""

import os
import json
import datetime
import sys

SCHEDULE_FILE   = 'content_schedule.json'
MINERALOGY_FILE = 'mineralogy_data.json'  # SSOT — 共 33 種礦石
TASK_OUTPUT_FILE = 'manus_task.json'


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
    today = datetime.date.today().isoformat()
    schedule = load_json(SCHEDULE_FILE)
    if not schedule:
        return None
    match_types = {task_type, 'post', 'posts'} if task_type in ('post', 'posts') else {task_type}
    for entry in schedule:
        if (entry.get('date') == today
                and entry.get('type') in match_types
                and entry.get('status') == 'pending'):
            return entry
    print(f"ℹ️  No pending '{task_type}' entry for today ({today}).")
    return None


def get_stone_data(stone_id):
    """從 mineralogy_data.json（SSOT，33 種礦石）讀取石頭資料。"""
    data = load_json(MINERALOGY_FILE)
    if not data:
        return {}
    stones = data if isinstance(data, list) else data.get('stones', [])
    for stone in stones:
        if stone.get('id') == stone_id:
            return stone
    print(f"⚠️  Stone '{stone_id}' not found in mineralogy_data.json (SSOT: 33 stones)")
    return {}


def resolve_asset_paths(entry):
    """
    解析已備用素材路徑。
    先檢查 entry 內的 asset_paths / asset_urls，
    再檢查 assets/ 目錄內對應日期檔案。

    Reels 規格：
      - 6 PNG 為中間轉製素材（不上傳 IG）
      - 1 MP4 為最終發布格式（20–30 秒）
      - manus_task.json 的 asset_paths 只填寫 MP4 路徑供 Manus IG MCP 發布
    """
    # 1. 排程預填的路徑
    paths = entry.get('asset_paths') or entry.get('asset_urls', [])
    if paths:
        return paths

    # 2. 自動推斷 assets/ 內的檔案名（根據日期 + 類型）
    date = entry.get('date', '')
    t    = entry.get('type', '')
    base = 'assets'

    if t == 'stories':
        # Stories: 1 PNG (1080×1350)
        guessed = [f"{base}/stories/story_{date}.png"]

    elif t in ('post', 'posts'):
        # Posts Carousel: 5 PNG (1080×1350)
        guessed = [f"{base}/posts/post_{date}_s{i}.png" for i in range(1, 6)]

    elif t == 'reels':
        # Reels: 最終發布只用 MP4 (20–30s)
        # 6 PNG 中間素材由 Manus 在批量生圖模式時生成，存於 assets/reels/
        # 此處只回傳 MP4 路徑給 Manus IG MCP 發布用
        guessed = [f"{base}/reels/reel_{date}.mp4"]
    else:
        guessed = []

    existing = [p for p in guessed if os.path.exists(p)]
    if existing:
        return existing

    print(f"⚠️  No pre-generated assets found for {date} {t}. Manus will need to generate on publish.")
    return []


def build_manus_task(entry, stone_data):
    task_type = entry.get('type', '')

    # 全格式統一 1080×1350 px
    format_specs = {
        'stories': {
            'slides': 1,
            'dimensions': '1080x1350',
            'has_video': False,
            'output': '1 PNG'
        },
        'post': {
            'slides': 5,
            'dimensions': '1080x1350',
            'has_video': False,
            'output': '5 PNG (Carousel)'
        },
        'posts': {
            'slides': 5,
            'dimensions': '1080x1350',
            'has_video': False,
            'output': '5 PNG (Carousel)'
        },
        'reels': {
            'intermediate_slides': 6,
            'dimensions': '1080x1350',
            'has_video': True,
            'video_duration': '20-30s',
            'output': '1 MP4（由 6 PNG 中間素材轉製，20–30 秒）',
            'ig_publish': 'MP4 only — 6 PNG 為中間素材，不上傳 IG'
        },
    }

    asset_paths = resolve_asset_paths(entry)

    return {
        'task_id':      f"{entry.get('date')}_{task_type}",
        'created_at':   datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source':       'github_actions_scheduler',
        'publish_platform': 'instagram',
        'publish_via':  'manus_ig_mcp',

        # 礦石資料唯一真源：mineralogy_data.json（33 種礦石）
        'ssot_note': 'All mineral data sourced exclusively from mineralogy_data.json (33 stones)',

        'schedule': {
            'date':          entry.get('date'),
            'type':          task_type,
            'phase':         entry.get('phase', ''),
            'cta':           entry.get('cta', ''),
            'episode':       entry.get('episode'),
            'next_stone_id': entry.get('next_stone_id'),
        },

        'stone': {
            'id':              stone_data.get('id',              entry.get('stone_id', '')),
            'zh':              stone_data.get('name_zh',         entry.get('stone_zh', '')),
            'en':              stone_data.get('name_en',         ''),
            'hardness':        stone_data.get('hardness',        ''),
            'color':           stone_data.get('color',           ''),
            'optical_effects': stone_data.get('optical_effects', []),
            'body_focus':      stone_data.get('body_focus',      []),
            'use_cases':       stone_data.get('use_cases',       []),
            'care_tips':       stone_data.get('care_tips',       ''),
            'synthetic_signs': stone_data.get('synthetic_signs', ''),
        },

        'caption':      entry.get('caption', ''),
        'caption_note': '如 caption 為空，由 Manus 按品牌語調生成。首行必須含石頭名稱 + 功能關鍵字。',

        # asset_paths:
        #   Stories → PNG 路徑
        #   Posts   → 5 PNG 路徑
        #   Reels   → MP4 路徑（6 PNG 中間素材不列入，不上傳 IG）
        'asset_paths':   asset_paths,
        'assets_ready':  len(asset_paths) > 0,

        'format_spec': format_specs.get(task_type, {}),

        'ig_algorithm_rules': {
            'hashtags':    '3-5個，主題相關，禁止堆砌',
            'save_share':  'Posts 優先 Save；Reels 優先 Share',
            'reels_hook':  '首3秒止滑鉤（第N夜｜{石頭}的秘密）',
            'first_90min': '發布後立即 Stories 轉發，帳號主10分鐘內留言引導互動',
        },

        'result': {
            'status':       'pending',
            'media_id':     None,
            'published_at': None,
            'error':        None,
        }
    }


if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE', '').strip().lower()
    if not task_type:
        print('❌ TASK_TYPE env var not set.')
        sys.exit(1)

    entry = get_today_entry(task_type)
    if not entry:
        print(f"⏭️  Nothing to publish for '{task_type}' today.")
        sys.exit(0)

    stone_id   = entry.get('stone_id', '')
    stone_data = get_stone_data(stone_id) if stone_id else {}
    task       = build_manus_task(entry, stone_data)
    save_json(TASK_OUTPUT_FILE, task)

    print(f"""✅ manus_task.json ready:
   task_id      : {task['task_id']}
   type         : {task_type}
   stone        : {task['stone']['zh']} ({task['stone']['id']})
   assets_ready : {task['assets_ready']} ({len(task['asset_paths'])} files)
   phase        : {task['schedule']['phase']}
   dimensions   : 1080x1350 px (unified across all formats)
""")
    sys.exit(0)

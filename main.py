"""
main.py — GitHub Actions Entry Point（由 Manus workflow_dispatch 觸發）

觸發方式：Manus 透過 GitHub MCP 呼叫 workflow_dispatch 觸發（已移除排程觸發機制，
         時間由 Manus 控制）。GitHub Actions 只負責執行本腳本，不控制時間。

角色：純任務組裝器
- 讀 content_schedule.json 找今日 pending 任務
- 讀 mineralogy_data.json 組裝石頭資料（SSOT，共 33 種礦石，唯一真源）
- 指向 assets/ 內已備用素材路徑（圖片已事先由 Manus 批量生成）
- 寫入 manus_task.json → Manus 讀取後直接發布，不需再生圖

分工（文案組裝收歸 GitHub）：
  「事先」 Manus 一次性批量生成 90 天全部圖片 → commit 到 assets/
  「每天」 Manus 透過 GitHub MCP 呼叫 workflow_dispatch 觸發 main.py → 從 content_schedule.json 組裝「完整文案」+ 圖片路徑 → 寫 manus_task.json
  「發布」 Manus 只讀 manus_task.json → 取 content（文案）+ asset_paths（圖片）→ IG MCP 發布 → 回報

⚠️ Manus 角色 = EXTRACT_AND_PUBLISH_ONLY：不生成、不改寫任何文案。
   文案全部由 GitHub（main.py 組裝 content_schedule.json 內容）負責；若文案未備齊，main.py 報錯停止。

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
        guessed = [f"{base}/posts/post_{date}_p{i}.png" for i in range(1, 6)]

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


def assemble_content(entry, task_type):
    """
    GitHub 端文案組裝（Manus 只提取發布，不生成）。
    從 content_schedule.json 的排程記錄取出完整文案，組裝成 content 區塊。

    各格式內容組成：
      Posts   → 圖片 + 燒入文字（pages.body_text）+ 發文文案（caption + hashtags）
      Reels   → 圖片 + 燒入文字（frames p1–p6）+ 背景音樂（music）+ 發文文案（caption + hashtags）
      Stories → 圖片 + 燒入文字（visual_prompt + frame）；發布不需 caption / hashtags
    若必要欄位缺失，視為文案未備齊 → 觸發 error（見 __main__），Manus 不再負責生成任何文案。
    """
    # Stories：純圖文，燒入文字 = visual_prompt + frame，無 caption
    if task_type == 'stories':
        return {
            'visual_prompt': entry.get('visual_prompt', ''),
            'frame':         entry.get('frame', {}),
            'hashtags':      entry.get('hashtags', []),
            'story_title':   entry.get('story_title', entry.get('post_title', '')),
        }

    caption  = (entry.get('caption') or '').strip()
    hashtags = entry.get('hashtags', [])

    content = {
        'caption':  caption,
        'hashtags': hashtags,
    }

    if task_type in ('post', 'posts'):
        # Carousel：每頁文字（封面/內頁/封底，含 body_text 燒入文字）全部組好供 Manus 套圖發布
        content['post_number'] = entry.get('post_number')
        content['post_title']  = entry.get('post_title', '')
        content['pages']       = entry.get('pages', [])

    elif task_type == 'reels':
        # Reels：6 幀圖文文字（p1–p6 燒入畫面）、視覺提示、背景音樂、連載鉤子全部組好
        content['episode']              = entry.get('episode')
        content['episode_title']        = entry.get('episode_title', '')
        content['series_hook']          = entry.get('series_hook', '')
        content['next_episode_preview'] = entry.get('next_episode_preview', '')
        content['visual_prompts']       = entry.get('visual_prompts', {})
        content['frames']               = entry.get('frames', {})
        content['music']                = entry.get('music', {})

    return content


def content_is_ready(entry, task_type):
    """
    文案是否已由 GitHub 端備齊。
      Posts   → caption + pages（每頁含 body_text 燒入文字）
      Reels   → caption + frames（p1–p6）+ music 背景音樂
      Stories → visual_prompt + frame（headline/body/cta_text），不需 caption
    """
    if task_type == 'stories':
        frame = entry.get('frame') or {}
        if not all((frame.get(k) or '').strip() for k in ('headline', 'body', 'cta_text')):
            return False, 'stories 缺 frame 燒入文字（headline/body/cta_text）'
        if not (entry.get('visual_prompt') or '').strip():
            return False, 'stories 缺 visual_prompt 視覺提示'
        return True, ''

    if not (entry.get('caption') or '').strip():
        return False, 'caption 為空（GitHub 端文案未備齊，Manus 不負責生成）'

    if task_type in ('post', 'posts'):
        pages = entry.get('pages') or []
        if not pages:
            return False, 'posts 缺 pages 內頁文案'
        if not all((pg.get('body_text') or '').strip() for pg in pages):
            return False, 'posts 缺 body_text 燒入文字（每頁皆需）'

    if task_type == 'reels':
        if not entry.get('frames'):
            return False, 'reels 缺 frames 圖文文字（p1–p6）'
        music = entry.get('music') or {}
        if not music.get('style'):
            return False, 'reels 缺 music 背景音樂設定'

    return True, ''


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
    content = assemble_content(entry, task_type)

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

        # content：GitHub 端組裝完成的完整文案（Manus 直接取用，不生成）
        'content': content,

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

    # 文案組裝收歸 GitHub：Manus 不生成，若文案未備齊即報錯停止
    ready, reason = content_is_ready(entry, task_type)
    if not ready:
        err_task = {
            'task_id': f"{entry.get('date')}_{task_type}",
            'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'manus_role': 'EXTRACT_AND_PUBLISH_ONLY',
            'result': {'status': 'error', 'error': f"文案未備齊：{reason}。請先在 content_schedule.json 補齊文案。"},
        }
        save_json(TASK_OUTPUT_FILE, err_task)
        print(f"❌ 文案未備齊，不發布：{reason}")
        sys.exit(1)

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

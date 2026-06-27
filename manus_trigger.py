"""
manus_trigger.py — Manus 發布入口

角色：只做「取備用圖片 → IG MCP 發布 → 回報完成」
不負責生圖。圖片已由事先批量備用於 assets/。

兩個時機使用：
  A. GitHub Actions commit manus_task.json 後，Manus 小自動讀取
  B. 人工直接執行： python manus_trigger.py
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


def mark_published(task_id, media_id):
    schedule = load_json(SCHEDULE_FILE)
    if not schedule:
        return
    date, task_type = task_id.split('_', 1) if '_' in task_id else (None, None)
    match_types = {task_type, 'post', 'posts'} if task_type in ('post', 'posts') else {task_type}
    for item in schedule:
        if item.get('date') == date and item.get('type') in match_types:
            item['status'] = 'published'
            item['published_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            item['media_id'] = str(media_id)
            break
    save_json(SCHEDULE_FILE, schedule)
    print(f"✅ Schedule marked published: {task_id} (media_id: {media_id})")


def run():
    task = load_json(TASK_FILE)
    if not task or not task.get('task_id'):
        print("❌ manus_task.json 為空或未初始化，請等待 GitHub Actions 寫入任務。")
        sys.exit(0)

    task_id   = task['task_id']
    task_type = task['schedule']['type']
    caption   = task.get('caption', '')
    assets    = task.get('asset_paths', [])
    ready     = task.get('assets_ready', False)
    stone     = task['stone']
    rules     = task.get('ig_algorithm_rules', {})
    ep        = task['schedule'].get('episode')

    print(f"""\n🚀 Manus 發布任務
   task_id     : {task_id}
   type        : {task_type}
   stone       : {stone.get('zh')} ({stone.get('id')})
   assets_ready: {ready} ({len(assets)} 檔案)
   phase       : {task['schedule'].get('phase')}
   cta         : {task['schedule'].get('cta')}
""")

    # ── Step 1: 確認備用素材 ─────────────────────────────────────
    print("🖼️  Step 1: 檢查備用素材")
    if ready:
        print(f"   ✔️ 已就緒：{assets}")
    else:
        print(f"   ⚠️  assets/ 內尚未找到對應檔案。")
        print(f"   請先執行「一次性批量生圖」：Manus 生圖 → commit 到 assets/ → 再回來發布")
        sys.exit(1)

    # ── Step 2: Caption 規則 ──────────────────────────────────────
    print("\n📝 Step 2: Caption")
    if caption:
        print(f"   ✔️ 預填 Caption 已就緒")
    else:
        print(f"   🤖 請 Manus 按品牌語調生成 Caption：")
        print(f"      - 首行：{stone.get('zh')} + 功能關鍵字（SEO）")
        print(f"      - Hashtag：{rules.get('hashtags')}")
        if task_type == 'reels' and ep:
            print(f"      - Hook：第{ep}夜｜{stone.get('zh')}的秘密")
        print(f"      - CTA：{task['schedule'].get('cta')}")
        print(f"      - Save/Share 導向：{rules.get('save_share')}")

    # ── Step 3: IG MCP 發布 ──────────────────────────────────────
    print(f"\n📲 Step 3: IG MCP 發布 ({task_type.upper()})")
    print(f"   使用內置 IG MCP，發布 {len(assets)} 個檔案")
    print(f"   發布後：{rules.get('first_90min')}")
    print()

    # Manus 執行 IG MCP 發布後，呼叫：
    # mark_published(task_id, media_id='<IG_MEDIA_ID>')
    # 並更新 manus_task.json result 欄位

    print("⏳ 等待 Manus IG MCP 執行中...")


if __name__ == '__main__':
    run()

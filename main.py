import os
import json
import datetime
import requests

# ── 環境變數 ──────────────────────────────────────────────
IG_USER_ID        = os.getenv('IG_USER_ID')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')

META_BASE = "https://graph.facebook.com/v19.0"

# ── 讀取今日排程 ─────────────────────────────────────────
# 新架構：文案與圖片 URL 已預存於排程檔，不再即時呼叫任何 AI API。
# 排程資料分拆於 content_schedule_part1/2/3.json，合併後使用。
# 若 asset_url 欄位有值（Manus 生成後回填），優先使用；
# 否則 fallback 至 image_url 欄位。

SCHEDULE_PARTS = [
    'content_schedule_part1.json',
    'content_schedule_part2.json',
    'content_schedule_part3.json',
]

def load_schedule():
    entries = []
    for path in SCHEDULE_PARTS:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                entries.extend(json.load(f))
        else:
            print(f"⚠️  Schedule part not found: {path}")
    return entries

def get_today_entry(task_type):
    today = datetime.date.today().isoformat()
    schedule = load_schedule()
    for entry in schedule:
        if (
            entry.get('date') == today
            and entry.get('type') == task_type
            and entry.get('status') == 'pending'
        ):
            return entry
    print(f"ℹ️  No pending {task_type} entry for today ({today}).")
    return None

# ── Meta Graph API 發佈 ───────────────────────────────────
def _check_env():
    if not META_ACCESS_TOKEN or not IG_USER_ID:
        print("❌ META_ACCESS_TOKEN or IG_USER_ID not set.")
        return False
    return True

def publish_stories(image_url, caption=None):
    if not _check_env():
        return False
    create_url = f"{META_BASE}/{IG_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": META_ACCESS_TOKEN,
    }
    if caption:
        payload["caption"] = caption
    try:
        res = requests.post(create_url, data=payload, timeout=30)
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Stories container failed: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Stories container error: {e}")
        return False
    try:
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30,
        )
        pub.raise_for_status()
        print(f"✅ Stories published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Stories publish error: {e}")
        return False

def publish_carousel(image_urls, caption):
    """Carousel (多圖) Post，image_urls 為公開 URL 的 list。"""
    if not _check_env():
        return False
    # Step 1: 為每張圖建立子 container
    child_ids = []
    for url in image_urls:
        try:
            res = requests.post(
                f"{META_BASE}/{IG_USER_ID}/media",
                data={
                    "image_url": url,
                    "is_carousel_item": "true",
                    "access_token": META_ACCESS_TOKEN,
                },
                timeout=30,
            )
            res.raise_for_status()
            cid = res.json().get('id')
            if cid:
                child_ids.append(cid)
                print(f"  ✅ Carousel child: {cid}")
            else:
                print(f"  ❌ Carousel child failed for {url}: {res.text}")
        except Exception as e:
            print(f"  ❌ Carousel child error: {e}")
    if not child_ids:
        print("❌ No carousel children created.")
        return False
    # Step 2: 建立 carousel container
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "media_type": "CAROUSEL",
                "children": ",".join(child_ids),
                "caption": caption,
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=30,
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Carousel container failed: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Carousel container error: {e}")
        return False
    # Step 3: 發佈
    try:
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30,
        )
        pub.raise_for_status()
        print(f"✅ Carousel published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Carousel publish error: {e}")
        return False

def publish_photo_post(image_url, caption):
    """單張圖片 Feed Post（Reels 以影片 URL 走相同流程）"""
    if not _check_env():
        return False
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=30,
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Container failed: {res.text}")
            return False
        print(f"✅ Media container: {container_id}")
    except Exception as e:
        print(f"❌ Container error: {e}")
        return False
    try:
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30,
        )
        pub.raise_for_status()
        print(f"✅ Published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False

def publish_reel(video_url, caption):
    """發佈 Reels（video_url 須為公開可訪問的 mp4）"""
    if not _check_env():
        return False
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "video_url": video_url,
                "media_type": "REELS",
                "caption": caption,
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=60,
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Reel container failed: {res.text}")
            return False
        print(f"✅ Reel container: {container_id}")
    except Exception as e:
        print(f"❌ Reel container error: {e}")
        return False
    try:
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=60,
        )
        pub.raise_for_status()
        print(f"✅ Reel published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Reel publish error: {e}")
        return False

# ── 主程式 ────────────────────────────────────────────────
if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE', '').strip()
    if not task_type:
        print("❌ TASK_TYPE not set.")
        exit(1)

    print(f"🚀 Task: {task_type} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} HKT")

    entry = get_today_entry(task_type)
    if not entry:
        print(f"⏭️  Nothing to publish for {task_type} today. Exiting cleanly.")
        exit(0)

    caption   = entry.get('caption', '')
    # asset_url = Manus 生成後回填的公開 URL；fallback 至 image_url
    asset_url = entry.get('asset_url') or entry.get('image_url', '')
    # asset_urls = carousel 多圖 URL list（Manus 回填後格式）
    asset_urls = entry.get('asset_urls', [])

    print(f"📅 Date   : {entry['date']}")
    print(f"📝 Caption: {caption[:80]}...")
    print(f"🖼️  Asset  : {asset_url or asset_urls}")

    if task_type == 'stories':
        if not asset_url:
            print("⚠️  No asset_url for stories. Skipping.")
            exit(0)
        success = publish_stories(asset_url, caption)

    elif task_type == 'posts':
        if asset_urls:
            success = publish_carousel(asset_urls, caption)
        elif asset_url:
            success = publish_photo_post(asset_url, caption)
        else:
            print("⚠️  No asset_url / asset_urls for posts. Skipping.")
            exit(0)

    elif task_type == 'reels':
        if not asset_url:
            print("⚠️  No asset_url for reels. Skipping.")
            exit(0)
        success = publish_reel(asset_url, caption)

    else:
        print(f"❌ Unknown task_type: {task_type}")
        exit(1)

    if success:
        print(f"🎉 '{task_type}' published successfully.")
    else:
        print(f"💥 '{task_type}' failed.")
        exit(1)

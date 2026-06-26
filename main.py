import os
import json
import datetime
import requests

IG_USER_ID = os.getenv('IG_USER_ID')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
META_BASE = "https://graph.facebook.com/v19.0"
SCHEDULE_FILE = 'content_schedule.json'

def load_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        print(f"⚠️ Schedule file not found: {SCHEDULE_FILE}")
        return []
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_today_entry(task_type):
    today = datetime.date.today().isoformat()
    for entry in load_schedule():
        if entry.get('date') == today and entry.get('type') == task_type and entry.get('status') == 'pending':
            return entry
    print(f"ℹ️ No pending {task_type} entry for today ({today}).")
    return None

def _check_env():
    if not META_ACCESS_TOKEN or not IG_USER_ID:
        print("❌ META_ACCESS_TOKEN or IG_USER_ID not set.")
        return False
    return True

def publish_stories(image_url, caption=None):
    if not _check_env():
        return False
    payload = {"image_url": image_url, "media_type": "STORIES", "access_token": META_ACCESS_TOKEN}
    if caption:
        payload["caption"] = caption
    try:
        res = requests.post(f"{META_BASE}/{IG_USER_ID}/media", data=payload, timeout=30)
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Stories container failed: {res.text}")
            return False
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        print(f"✅ Stories published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Stories publish error: {e}")
        return False

def publish_carousel(image_urls, caption):
    if not _check_env():
        return False

    child_ids = []
    for url in image_urls:
        try:
            res = requests.post(
                f"{META_BASE}/{IG_USER_ID}/media",
                data={
                    "image_url": url,
                    "is_carousel_item": "true",
                    "access_token": META_ACCESS_TOKEN
                },
                timeout=30
            )
            res.raise_for_status()
            cid = res.json().get('id')
            if cid:
                child_ids.append(cid)
        except Exception as e:
            print(f"❌ Carousel child error: {e}")

    if not child_ids:
        print("❌ No carousel children created.")
        return False

    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "media_type": "CAROUSEL",
                "children": ",".join(child_ids),
                "caption": caption,
                "access_token": META_ACCESS_TOKEN
            },
            timeout=30
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Carousel container failed: {res.text}")
            return False

        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        print(f"✅ Carousel published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Carousel publish error: {e}")
        return False

def publish_photo_post(image_url, caption):
    if not _check_env():
        return False
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": META_ACCESS_TOKEN
            },
            timeout=30
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Container failed: {res.text}")
            return False

        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        print(f"✅ Published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False

def publish_reel(video_url, caption):
    if not _check_env():
        return False
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={
                "video_url": video_url,
                "media_type": "REELS",
                "caption": caption,
                "access_token": META_ACCESS_TOKEN
            },
            timeout=60
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Reel container failed: {res.text}")
            return False

        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=60
        )
        pub.raise_for_status()
        print(f"✅ Reel published! Media ID: {pub.json().get('id')}")
        return True
    except Exception as e:
        print(f"❌ Reel publish error: {e}")
        return False

if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE', '').strip()
    if not task_type:
        print('❌ TASK_TYPE not set.')
        raise SystemExit(1)

    entry = get_today_entry(task_type)
    if not entry:
        print(f"⏭️ Nothing to publish for {task_type} today.")
        raise SystemExit(0)

    caption = entry.get('caption', '')
    asset_url = entry.get('asset_url') or entry.get('image_url', '')
    asset_urls = entry.get('asset_urls', [])

    print(f"📅 Date: {entry.get('date')}")
    print(f"📝 Caption: {caption[:80]}...")

    if task_type == 'stories':
        if not asset_url:
            print('⚠️ No asset_url for stories.')
            raise SystemExit(0)
        ok = publish_stories(asset_url, caption)

    elif task_type == 'posts':
        if asset_urls:
            ok = publish_carousel(asset_urls, caption)
        elif asset_url:
            ok = publish_photo_post(asset_url, caption)
        else:
            print('⚠️ No asset_url / asset_urls for posts.')
            raise SystemExit(0)

    elif task_type == 'reels':
        if not asset_url:
            print('⚠️ No asset_url for reels.')
            raise SystemExit(0)
        ok = publish_reel(asset_url, caption)

    else:
        print(f'❌ Unknown task_type: {task_type}')
        raise SystemExit(1)

    raise SystemExit(0 if ok else 1)

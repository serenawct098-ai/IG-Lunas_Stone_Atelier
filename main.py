import os
import json
import datetime
import time
import requests

IG_USER_ID = os.getenv('IG_USER_ID')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
META_BASE = "https://graph.facebook.com/v21.0"
SCHEDULE_FILE = 'content_schedule.json'


def load_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        print(f"⚠️ Schedule file not found: {SCHEDULE_FILE}")
        return []
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_schedule(schedule):
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)


def get_today_entry(task_type):
    today = datetime.date.today().isoformat()
    # Accept both 'post' and 'posts' to handle legacy entries
    match_types = [task_type]
    if task_type == 'posts':
        match_types.append('post')
    elif task_type == 'post':
        match_types.append('posts')
    for entry in load_schedule():
        if (entry.get('date') == today
                and entry.get('type') in match_types
                and entry.get('status') == 'pending'):
            return entry
    print(f"ℹ️ No pending {task_type} entry for today ({today}).")
    return None


def mark_published(entry, media_id):
    """Update the schedule file to mark entry as published."""
    schedule = load_schedule()
    for item in schedule:
        if item.get('date') == entry.get('date') and item.get('type') == entry.get('type'):
            item['status'] = 'published'
            item['published_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            item['media_id'] = media_id
            break
    save_schedule(schedule)
    print(f"✅ Schedule updated: {entry.get('date')} {entry.get('type')} -> published (media_id: {media_id})")


def _check_env():
    if not META_ACCESS_TOKEN or not IG_USER_ID:
        print("❌ META_ACCESS_TOKEN or IG_USER_ID not set.")
        return False
    return True


def _wait_for_container(container_id, max_retries=12, interval=5):
    """Poll container status until FINISHED or ERROR (for Reels)."""
    for i in range(max_retries):
        try:
            res = requests.get(
                f"{META_BASE}/{container_id}",
                params={"fields": "status_code", "access_token": META_ACCESS_TOKEN},
                timeout=30
            )
            res.raise_for_status()
            status = res.json().get('status_code', '')
            print(f"   Container status ({i+1}/{max_retries}): {status}")
            if status == 'FINISHED':
                return True
            if status == 'ERROR':
                print(f"❌ Container processing error.")
                return False
        except Exception as e:
            print(f"⚠️ Status poll error: {e}")
        time.sleep(interval)
    print("❌ Container did not finish in time.")
    return False


def publish_stories(image_url, caption=None):
    if not _check_env():
        return False, None
    payload = {"image_url": image_url, "media_type": "STORIES", "access_token": META_ACCESS_TOKEN}
    if caption:
        payload["caption"] = caption
    try:
        res = requests.post(f"{META_BASE}/{IG_USER_ID}/media", data=payload, timeout=30)
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Stories container failed: {res.text}")
            return False, None
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        media_id = pub.json().get('id')
        print(f"✅ Stories published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Stories publish error: {e}")
        return False, None


def publish_carousel(image_urls, caption):
    if not _check_env():
        return False, None
    child_ids = []
    for url in image_urls:
        try:
            res = requests.post(
                f"{META_BASE}/{IG_USER_ID}/media",
                data={"image_url": url, "is_carousel_item": "true", "access_token": META_ACCESS_TOKEN},
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
        return False, None

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
            return False, None
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        media_id = pub.json().get('id')
        print(f"✅ Carousel published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Carousel publish error: {e}")
        return False, None


def publish_photo_post(image_url, caption):
    if not _check_env():
        return False, None
    try:
        res = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media",
            data={"image_url": image_url, "caption": caption, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Container failed: {res.text}")
            return False, None
        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=30
        )
        pub.raise_for_status()
        media_id = pub.json().get('id')
        print(f"✅ Published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False, None


def publish_reel(video_url, caption):
    if not _check_env():
        return False, None
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
            return False, None

        print(f"⏳ Waiting for Reel container to process...")
        if not _wait_for_container(container_id):
            return False, None

        pub = requests.post(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=60
        )
        pub.raise_for_status()
        media_id = pub.json().get('id')
        print(f"✅ Reel published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Reel publish error: {e}")
        return False, None


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
    print(f"🗓️ Type: {task_type}")
    print(f"📝 Caption (preview): {caption[:80]}...")

    ok, media_id = False, None

    if task_type == 'stories':
        if not asset_url:
            print('⚠️ No asset_url for stories.')
            raise SystemExit(0)
        ok, media_id = publish_stories(asset_url, caption)

    elif task_type in ('post', 'posts'):
        if asset_urls:
            ok, media_id = publish_carousel(asset_urls, caption)
        elif asset_url:
            ok, media_id = publish_photo_post(asset_url, caption)
        else:
            print('⚠️ No asset_url / asset_urls for post.')
            raise SystemExit(0)

    elif task_type == 'reels':
        if not asset_url:
            print('⚠️ No asset_url for reels.')
            raise SystemExit(0)
        ok, media_id = publish_reel(asset_url, caption)

    else:
        print(f'❌ Unknown task_type: {task_type}')
        raise SystemExit(1)

    if ok and media_id:
        mark_published(entry, media_id)

    raise SystemExit(0 if ok else 1)

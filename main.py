import os
import json
import datetime
import time
import requests

IG_USER_ID = os.getenv('IG_USER_ID')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
META_BASE = "https://graph.facebook.com/v21.0"
SCHEDULE_FILE = 'content_schedule.json'

# ── Retry settings ────────────────────────────────────────────
MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 10]  # seconds between retries


def _post_with_retry(url, data, timeout=60):
    """POST with exponential backoff retry."""
    for attempt in range(MAX_RETRIES):
        try:
            res = requests.post(url, data=data, timeout=timeout)
            res.raise_for_status()
            return res
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else None
            # Do not retry on 4xx client errors (except 429 rate limit)
            if status and 400 <= status < 500 and status != 429:
                print(f"❌ HTTP {status} client error — no retry: {e}")
                raise
            print(f"⚠️ Attempt {attempt+1}/{MAX_RETRIES} failed ({status}): {e}")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"⚠️ Attempt {attempt+1}/{MAX_RETRIES} network error: {e}")
        if attempt < MAX_RETRIES - 1:
            wait = RETRY_BACKOFF[attempt]
            print(f"   Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"All {MAX_RETRIES} attempts failed for POST {url}")


def _get_with_retry(url, params, timeout=30):
    """GET with exponential backoff retry."""
    for attempt in range(MAX_RETRIES):
        try:
            res = requests.get(url, params=params, timeout=timeout)
            res.raise_for_status()
            return res
        except Exception as e:
            print(f"⚠️ GET attempt {attempt+1}/{MAX_RETRIES} failed: {e}")
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_BACKOFF[attempt])
    raise RuntimeError(f"All {MAX_RETRIES} GET attempts failed for {url}")


# ── Schedule helpers ──────────────────────────────────────────

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
    # Accept both 'post' and 'posts' for legacy compatibility
    match_types = {task_type}
    if task_type == 'posts':
        match_types.add('post')
    elif task_type == 'post':
        match_types.add('posts')
    for entry in load_schedule():
        if (entry.get('date') == today
                and entry.get('type') in match_types
                and entry.get('status') == 'pending'):
            return entry
    print(f"ℹ️ No pending {task_type} entry for today ({today}).")
    return None


def mark_published(entry, media_id):
    """Update schedule file to mark entry as published."""
    schedule = load_schedule()
    for item in schedule:
        if item.get('date') == entry.get('date') and item.get('type') == entry.get('type'):
            item['status'] = 'published'
            item['published_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            item['media_id'] = str(media_id)
            break
    save_schedule(schedule)
    print(f"✅ Schedule updated: {entry.get('date')} {entry.get('type')} → published (media_id: {media_id})")


def _check_env():
    missing = []
    if not META_ACCESS_TOKEN:
        missing.append('META_ACCESS_TOKEN')
    if not IG_USER_ID:
        missing.append('IG_USER_ID')
    if missing:
        print(f"❌ Missing env vars: {', '.join(missing)}")
        return False
    return True


def _wait_for_container(container_id, max_retries=20, interval=6):
    """Poll container status until FINISHED or ERROR (required for Reels)."""
    for i in range(max_retries):
        try:
            res = _get_with_retry(
                f"{META_BASE}/{container_id}",
                params={"fields": "status_code", "access_token": META_ACCESS_TOKEN}
            )
            status = res.json().get('status_code', '')
            print(f"   Container status ({i+1}/{max_retries}): {status}")
            if status == 'FINISHED':
                return True
            if status == 'ERROR':
                print("❌ Container processing returned ERROR.")
                return False
        except Exception as e:
            print(f"⚠️ Status poll error: {e}")
        time.sleep(interval)
    print("❌ Container did not finish within the wait window.")
    return False


# ── Publish functions ─────────────────────────────────────────

def publish_stories(image_url, caption=None):
    if not _check_env():
        return False, None
    payload = {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": META_ACCESS_TOKEN
    }
    if caption:
        payload["caption"] = caption
    try:
        res = _post_with_retry(f"{META_BASE}/{IG_USER_ID}/media", payload)
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Stories container creation failed: {res.text}")
            return False, None
        pub = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            {"creation_id": container_id, "access_token": META_ACCESS_TOKEN}
        )
        media_id = pub.json().get('id')
        print(f"✅ Stories published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Stories publish error: {e}")
        return False, None


def publish_carousel(image_urls, caption):
    """Upload each slide as a carousel child, then publish as CAROUSEL."""
    if not _check_env():
        return False, None
    if not image_urls:
        print("❌ No image URLs provided for carousel.")
        return False, None

    child_ids = []
    for idx, url in enumerate(image_urls, 1):
        try:
            res = _post_with_retry(
                f"{META_BASE}/{IG_USER_ID}/media",
                {"image_url": url, "is_carousel_item": "true", "access_token": META_ACCESS_TOKEN}
            )
            cid = res.json().get('id')
            if cid:
                child_ids.append(cid)
                print(f"   Slide {idx}/{len(image_urls)} uploaded: {cid}")
            else:
                print(f"⚠️ Slide {idx} returned no ID.")
        except Exception as e:
            print(f"❌ Carousel slide {idx} error: {e}")

    if not child_ids:
        print("❌ No carousel children created — aborting.")
        return False, None

    try:
        res = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(child_ids),
                "caption": caption,
                "access_token": META_ACCESS_TOKEN
            }
        )
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Carousel container failed: {res.text}")
            return False, None
        pub = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            {"creation_id": container_id, "access_token": META_ACCESS_TOKEN}
        )
        media_id = pub.json().get('id')
        print(f"✅ Carousel published! Media ID: {media_id} ({len(child_ids)} slides)")
        return True, media_id
    except Exception as e:
        print(f"❌ Carousel publish error: {e}")
        return False, None


def publish_photo_post(image_url, caption):
    """Fallback: single-image post."""
    if not _check_env():
        return False, None
    try:
        res = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media",
            {"image_url": image_url, "caption": caption, "access_token": META_ACCESS_TOKEN}
        )
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Photo post container failed: {res.text}")
            return False, None
        pub = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            {"creation_id": container_id, "access_token": META_ACCESS_TOKEN}
        )
        media_id = pub.json().get('id')
        print(f"✅ Photo post published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Photo post publish error: {e}")
        return False, None


def publish_reel(video_url, caption):
    if not _check_env():
        return False, None
    try:
        res = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media",
            {
                "video_url": video_url,
                "media_type": "REELS",
                "caption": caption,
                "access_token": META_ACCESS_TOKEN
            },
            timeout=90
        )
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Reel container creation failed: {res.text}")
            return False, None
        print("⏳ Waiting for Reel container to process...")
        if not _wait_for_container(container_id):
            return False, None
        pub = _post_with_retry(
            f"{META_BASE}/{IG_USER_ID}/media_publish",
            {"creation_id": container_id, "access_token": META_ACCESS_TOKEN},
            timeout=90
        )
        media_id = pub.json().get('id')
        print(f"✅ Reel published! Media ID: {media_id}")
        return True, media_id
    except Exception as e:
        print(f"❌ Reel publish error: {e}")
        return False, None


# ── Entry point ───────────────────────────────────────────────

if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE', '').strip().lower()
    if not task_type:
        print('❌ TASK_TYPE env var not set.')
        raise SystemExit(1)

    entry = get_today_entry(task_type)
    if not entry:
        print(f"⏭️ Nothing to publish for '{task_type}' today.")
        raise SystemExit(0)

    caption = entry.get('caption', '')
    # Support both 'asset_url' (single) and 'asset_urls' (carousel array)
    asset_url = entry.get('asset_url') or entry.get('image_url', '')
    asset_urls = entry.get('asset_urls', [])

    print(f"📅 Date      : {entry.get('date')}")
    print(f"🗓️  Type      : {task_type}")
    print(f"📝 Caption   : {caption[:100]}{'...' if len(caption) > 100 else ''}")
    print(f"🔗 asset_url : {asset_url or '(none)'}")
    print(f"🖼️  asset_urls: {len(asset_urls)} slides")

    ok, media_id = False, None

    if task_type == 'stories':
        if not asset_url:
            print('⚠️ No asset_url for stories — skipping.')
            raise SystemExit(0)
        ok, media_id = publish_stories(asset_url, caption)

    elif task_type in ('post', 'posts'):
        if asset_urls:
            ok, media_id = publish_carousel(asset_urls, caption)
        elif asset_url:
            ok, media_id = publish_photo_post(asset_url, caption)
        else:
            print('⚠️ No asset_url / asset_urls for post — skipping.')
            raise SystemExit(0)

    elif task_type == 'reels':
        if not asset_url:
            print('⚠️ No asset_url for reels — skipping.')
            raise SystemExit(0)
        ok, media_id = publish_reel(asset_url, caption)

    else:
        print(f'❌ Unknown task_type: "{task_type}"')
        raise SystemExit(1)

    if ok and media_id:
        mark_published(entry, media_id)

    raise SystemExit(0 if ok else 1)

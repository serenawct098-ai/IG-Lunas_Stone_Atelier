import os
import json
import datetime
import requests

# ── 環境變數 ──────────────────────────────────────────────
OPENAI_API_KEY        = os.getenv('OPENAI_API_KEY')
IG_USER_ID            = os.getenv('IG_USER_ID')
META_ACCESS_TOKEN     = os.getenv('META_ACCESS_TOKEN')

META_BASE = "https://graph.facebook.com/v19.0"

# ── 資料載入 ──────────────────────────────────────────────
def load_ssot_data():
    with open('brand_config.json', 'r', encoding='utf-8') as f:
        brand_config = json.load(f)
    with open('mineralogy_data.json', 'r', encoding='utf-8') as f:
        mineralogy_data = json.load(f)
    return brand_config, mineralogy_data

# ── OpenAI 內容生成 ───────────────────────────────────────
def generate_caption(task_type, brand_config, mineralogy_data):
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not set. Using fallback caption.")
        return f"✨ Luna's Stone Atelier | 月華星礦坊 ✨\n\n#天然礦石 #LunasStoneAtelier #月華星礦坊"

    task_file_map = {
        'stories': 'task_1_stories_scheduling.md',
        'posts':   '任務2｜Carousel_Posts_貼文排程.md',
        'reels':   'task3_reels_master_executor.md'
    }
    task_spec_path = task_file_map.get(task_type)
    task_spec = ""
    if task_spec_path and os.path.exists(task_spec_path):
        with open(task_spec_path, 'r', encoding='utf-8') as f:
            task_spec = f.read()[:2000]  # 限制 token 用量

    brand_name = brand_config.get('brand', {}).get('name', "Luna's Stone Atelier")
    brand_project = brand_config.get('brand', {}).get('project', '月華星礦坊')

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    f"你是 {brand_name}（{brand_project}）的 Instagram 文案撰寫師。"
                    "語言：繁體中文為主，適當加入英文。語氣：神秘、優雅、有故事感。"
                    "文案結尾必須附上 #天然礦石 #LunasStoneAtelier #月華星礦坊 等品牌 hashtag。"
                    "禁止捏造礦石學數據。"
                )
            },
            {
                "role": "user",
                "content": f"請根據以下規範，為 {task_type} 撰寫一則 Instagram 文案：\n\n{task_spec}"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.8
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        caption = response.json()['choices'][0]['message']['content'].strip()
        print(f"✅ OpenAI caption generated for {task_type}")
        return caption
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return f"✨ {brand_name} | {brand_project} ✨\n\n#天然礦石 #LunasStoneAtelier #月華星礦坊"

# ── Meta Graph API 發佈 ───────────────────────────────────
def publish_photo_post(caption, image_url):
    """發佈單張圖片貼文 (Feed Post)"""
    if not META_ACCESS_TOKEN or not IG_USER_ID:
        print("❌ Error: META_ACCESS_TOKEN or IG_USER_ID not set.")
        return False

    # Step 1: 建立 media container
    create_url = f"{META_BASE}/{IG_USER_ID}/media"
    create_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    try:
        res = requests.post(create_url, data=create_payload, timeout=30)
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Failed to create media container: {res.text}")
            return False
        print(f"✅ Media container created: {container_id}")
    except Exception as e:
        print(f"❌ Create container error: {e}")
        return False

    # Step 2: 發佈
    publish_url = f"{META_BASE}/{IG_USER_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": META_ACCESS_TOKEN
    }
    try:
        res = requests.post(publish_url, data=publish_payload, timeout=30)
        res.raise_for_status()
        media_id = res.json().get('id')
        print(f"✅ Successfully published! Media ID: {media_id}")
        return True
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False

def publish_stories(image_url):
    """發佈 Stories（需 image_url 為公開可訪問連結）"""
    if not META_ACCESS_TOKEN or not IG_USER_ID:
        print("❌ Error: META_ACCESS_TOKEN or IG_USER_ID not set.")
        return False

    create_url = f"{META_BASE}/{IG_USER_ID}/media"
    create_payload = {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": META_ACCESS_TOKEN
    }
    try:
        res = requests.post(create_url, data=create_payload, timeout=30)
        res.raise_for_status()
        container_id = res.json().get('id')
        if not container_id:
            print(f"❌ Failed to create Stories container: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Stories container error: {e}")
        return False

    publish_url = f"{META_BASE}/{IG_USER_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": META_ACCESS_TOKEN
    }
    try:
        res = requests.post(publish_url, data=publish_payload, timeout=30)
        res.raise_for_status()
        media_id = res.json().get('id')
        print(f"✅ Stories published! Media ID: {media_id}")
        return True
    except Exception as e:
        print(f"❌ Stories publish error: {e}")
        return False

# ── 取得今日排程的圖片 URL（從 content_schedule.json）───────
def get_scheduled_image(task_type):
    schedule_path = 'content_schedule.json'
    if not os.path.exists(schedule_path):
        print(f"Warning: {schedule_path} not found. Using placeholder image.")
        return "https://via.placeholder.com/1080x1350.png?text=Luna+Stone+Atelier"

    today = datetime.date.today().isoformat()
    with open(schedule_path, 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    for entry in schedule:
        if entry.get('date') == today and entry.get('type') == task_type and entry.get('status') == 'pending':
            return entry.get('image_url', '')

    print(f"No scheduled {task_type} content for today ({today}).")
    return None

# ── 主程式 ────────────────────────────────────────────────
if __name__ == '__main__':
    task_type = os.getenv('TASK_TYPE')
    if not task_type:
        print("❌ Error: TASK_TYPE not set.")
        exit(1)

    print(f"🚀 Starting task: {task_type} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} HKT")

    try:
        brand_config, mineralogy_data = load_ssot_data()
        caption = generate_caption(task_type, brand_config, mineralogy_data)
        image_url = get_scheduled_image(task_type)

        if not image_url:
            print(f"⚠️ No image scheduled for {task_type} today. Skipping.")
            exit(0)

        print(f"📝 Caption preview: {caption[:80]}...")

        if task_type == 'stories':
            success = publish_stories(image_url)
        else:
            success = publish_photo_post(caption, image_url)

        if success:
            print(f"🎉 Task '{task_type}' completed successfully.")
        else:
            print(f"💥 Task '{task_type}' failed.")
            exit(1)

    except Exception as e:
        print(f"💥 Unhandled error: {e}")
        exit(1)

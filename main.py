import os

import json

import datetime

import requests



# 假設 Manus Webhook URL 透過 GitHub Secret 提供

MANUS_WEBHOOK_URL = os.getenv('MANUS_WEBHOOK_URL')

INSTAGRAM_API_BASE_URL = os.getenv('INSTAGRAM_API_BASE_URL', 'https://api.instagram.com/v1')

INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')



def load_ssot_data():
  
    # 載入所有 SSOT 數據
  
    with open('brand_config.json', 'r', encoding='utf-8') as f:
      
        brand_config = json.load(f)
      
    with open('mineralogy_data.json', 'r', encoding='utf-8') as f:
      
        mineralogy_data = json.load(f)
      
    return brand_config, mineralogy_data
  


def generate_content(task_type, brand_config, mineralogy_data):
  
    # 根據 task_type 讀取對應的任務規範文件
  
    task_file_map = {
      
        'stories': 'task_1_stories_scheduling.md',
      
        'posts': '任務2｜Carousel_Posts_貼文排程.md',
      
        'reels': 'task3_reels_master_executor.md'
      
    }
  
    task_spec_path = task_file_map.get(task_type)
  
    if not task_spec_path:
      
        print(f"Error: Unknown task type {task_type}")
      
        return None
      


    with open(task_spec_path, 'r', encoding='utf-8') as f:
      
        task_spec = f.read()
      


    content = {
      
        'type': task_type,
      
        'text': f"這是為 {task_type} 生成的內容，基於 {task_spec_path} 規範。",
      
        'visual_elements': [],
      
        'brand_colors': brand_config.get('colors'),
      
        'timestamp': datetime.datetime.now().isoformat()
      
    }
  
    print(f"Generated content for {task_type}")
  
    return content
  


def publish_to_instagram(content):
  
    print(f"Attempting to publish {content['type']} to Instagram...")
  
    if not INSTAGRAM_ACCESS_TOKEN:
      
        print("Error: INSTAGRAM_ACCESS_TOKEN not set.")
      
        return False
      
    print(f"Simulated successful publication of {content['type']} to Instagram.")
  
    return True
  


def notify_manus(task_type, status, message):
  
    if not MANUS_WEBHOOK_URL:
      
        print("Warning: MANUS_WEBHOOK_URL not set.")
      
        return
      
    payload = {
      
        'task_type': task_type,
      
        'status': status,
      
        'message': message,
      
        'timestamp': datetime.datetime.now().isoformat()
      
    }
  
    try:
      
        response = requests.post(MANUS_WEBHOOK_URL, json=payload)
      
        print(f"Notification sent to Manus: {status}")
      
    except Exception as e:
      
        print(f"Failed to send notification: {e}")
      


if __name__ == '__main__':
  
    task_type = os.getenv('TASK_TYPE')
  
    if not task_type:
      
        print("Error: TASK_TYPE not set.")
      
        exit(1)
      


    try:
      
        brand_config, mineralogy_data = load_ssot_data()
      
        content = generate_content(task_type, brand_config, mineralogy_data)
      
        if content:
          
            if publish_to_instagram(content):
              
                notify_manus(task_type, 'success', f'Successfully published {task_type}.')
              
            else:
              
                notify_manus(task_type, 'failed', f'Failed to publish {task_type}.')
              
    except Exception as e:
      
        print(f"Error: {e}")
      
        notify_manus(task_type, 'failed', str(e))
      




































































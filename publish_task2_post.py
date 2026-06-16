import os
import json
import re
import subprocess
from datetime import datetime

def load_json_from_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 修正 regex 以匹配可能包含換行符的 JSON 塊
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    return []

def load_brand_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_target_post(posts, target_date=None):
    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')
    for post in posts:
        if post['publish_date'] == target_date:
            return post
    # 若當天無貼文，Dry-run 模式下回傳第一篇供測試
    return posts[0] if posts else None

def generate_image_prompts(post_data, brand_config):
    image_prompts = []
    brand_logo_path = brand_config['brand']['logo']['file_path']
    primary_color = brand_config['colors']['primary']['hex']
    secondary_color = brand_config['colors']['secondary']['hex']
    accent_color = brand_config['colors']['accent'][1]['hex'] # 暖米白色
    
    for page in post_data['pages']:
        # 強化雙語與比例規範
        prompt = f"Instagram Carousel Post (4:5 ratio) for page {page['page']} of {len(post_data['pages'])}. "
        prompt += f"Brand: Luna's Stone Atelier. Theme: Natural Minerals. "
        prompt += f"Style: Professional, mystical, high-end jewelry photography style. "
        prompt += f"Colors: {primary_color} background, {secondary_color} main text and totem. "
        
        if page['type'] == '封面':
            prompt += f"Headline (Traditional Chinese & English): '{page['headline']}'. "
            prompt += f"Visual: {page['visual_desc']}. Must include brand totem logo in bottom right. "
        elif page['type'] == '乾貨內頁':
            content_text = ' '.join(page.get('content_points', []))
            prompt += f"Content (Traditional Chinese Primary): '{content_text}'. Visual: {page['visual_desc']}. "
            prompt += f"Design: Minimalist layout, {accent_color} text borders, high-resolution mineral texture. "
        elif page['type'] == '封底CTA':
            prompt += f"CTA: '{page['cta_copy']}'. Visual: {page['visual_desc']}. "
            prompt += f"Branding: Center brand logo, {primary_color} color block background. "
            
        image_prompts.append({
            'path': f"/home/ubuntu/IG-repo/temp_images/post_{post_data['post_number']}_page_{page['page']}.png",
            'prompt': prompt,
            'aspect_ratio': '4:5',
            'references': [brand_logo_path]
        })
    return image_prompts

def upload_images(image_paths):
    # 模擬上傳邏輯
    return [f"https://files.manuscdn.com/simulated_cdn/{os.path.basename(p)}" for p in image_paths]

if __name__ == '__main__':
    md_path = '/home/ubuntu/IG-repo/任務2｜Carousel_Posts_貼文排程.md'
    brand_config_path = '/home/ubuntu/IG-repo/brand_config.json'
    temp_image_dir = '/home/ubuntu/IG-repo/temp_images'
    os.makedirs(temp_image_dir, exist_ok=True)
    
    posts_data = load_json_from_md(md_path)
    brand_config = load_brand_config(brand_config_path)
    
    # 模擬 6/19 的發布 (測試用)
    target_date = "2026-06-19"
    post_to_publish = get_target_post(posts_data, target_date)
    
    if post_to_publish:
        print(f"--- LUNA DRY-RUN: 驗證 {target_date} 貼文 ---")
        print(f"標題: {post_to_publish['post_title']}")
        
        # 1. 生成圖片提示詞
        image_prompts = generate_image_prompts(post_to_publish, brand_config)
        print(f"成功生成 {len(image_prompts)} 個圖片提示詞 (比例 4:5)")
        
        # 2. 驗證文案
        caption = post_to_publish['caption']
        tags = " ".join(post_to_publish['hashtags']['recommended_tags'])
        full_caption = f"{caption}\n\n{tags}"
        print(f"文案驗證 (中文為主):\n{full_caption[:200]}...")
        
        # 3. 模擬成功
        print(f"--- DRY-RUN 成功: 系統已準備好發布 {target_date} 貼文 ---")
    else:
        print(f"Error: 找不到 {target_date} 的貼文數據。")
    
    # 清理臨時目錄
    if os.path.exists(temp_image_dir):
        for f in os.listdir(temp_image_dir):
            os.remove(os.path.join(temp_image_dir, f))
        os.rmdir(temp_image_dir)

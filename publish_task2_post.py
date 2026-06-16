import json
import re
from datetime import datetime
import subprocess
import os

def load_json_from_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    json_match = re.search(r'```json\n(.*?)```', content, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    return []

def load_brand_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_today_post(posts):
    today_str = datetime.now().strftime('%Y-%m-%d')
    for post in posts:
        if post['publish_date'] == today_str:
            return post
    # Fallback for testing: return the first post if no match for today
    return posts[0] if posts else None

def generate_image_prompts(post_data, brand_config):
    image_prompts = []
    brand_logo_path = brand_config['brand']['logo']['file_path']
    primary_color = brand_config['colors']['primary']['hex']
    secondary_color = brand_config['colors']['secondary']['hex']
    
    for page in post_data['pages']:
        prompt = f"Professional Instagram Carousel Post (4:5 ratio) for page {page['page']} of {len(post_data['pages'])}. "
        prompt += f"Brand: Luna's Stone Atelier. Theme: Natural Minerals. "
        prompt += f"Colors: {primary_color} background, {secondary_color} accents. "
        
        if page['type'] == '封面':
            prompt += f"Headline: '{page['headline']}'. Visual: {page['visual_desc']}. Include Logo. "
            prompt += f"Style: High contrast, eye-catching, mineral elements theme. "
        elif page['type'] == '乾貨內頁':
            content_text = ' '.join(page.get('content_points', []))
            prompt += f"Content: '{content_text}'. Visual: {page['visual_desc']}. Page {page['page']}/{len(post_data['pages'])}. "
            prompt += f"Style: Minimalist bullet points or table comparison, high-resolution mineral close-up, good lighting. Text border color: {brand_config['colors']['accent'][1]['hex']}. "
        elif page['type'] == '封底CTA':
            prompt += f"Call to action: '{page['cta_copy']}'. Visual: {page['visual_desc']}. Include brand logo. "
            prompt += f"Style: Brand color block background, mineral elements theme. "
        
        image_prompts.append({
            'path': f"/home/ubuntu/IG-repo/temp_images/post_{post_data['post_number']}_page_{page['page']}.png",
            'prompt': prompt,
            'aspect_ratio': '4:5',
            'references': [brand_logo_path]
        })
    return image_prompts

def upload_images(image_paths):
    upload_cmd = ["manus-upload-file"] + image_paths
    result = subprocess.run(upload_cmd, capture_output=True, text=True, check=True)
    cdn_urls = re.findall(r"CDN URL: (https://\S+)", result.stdout)
    return cdn_urls

def publish_post(caption, media_urls):
    media_list = [{"type": "image", "media_url": url} for url in media_urls]
    input_data = {
        "type": "post",
        "caption": caption,
        "media": media_list
    }
    cmd = ["manus-mcp-cli", "tool", "call", "create_instagram", "--server", "instagram", "--input", json.dumps(input_data, ensure_ascii=False)]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    md_path = '/home/ubuntu/IG-repo/任務2｜Carousel_Posts_貼文排程.md'
    brand_config_path = '/home/ubuntu/IG-repo/brand_config.json'
    temp_image_dir = '/home/ubuntu/IG-repo/temp_images'
    os.makedirs(temp_image_dir, exist_ok=True)

    posts_data = load_json_from_md(md_path)
    brand_config = load_brand_config(brand_config_path)
    
    post_to_publish = get_today_post(posts_data)

    if post_to_publish:
        print(f"Preparing to publish Post {post_to_publish['post_number']}: {post_to_publish['post_title']}")
        
        # 1. Generate Image Prompts
        image_prompts = generate_image_prompts(post_to_publish, brand_config)
        
        # 2. Generate Images (using a placeholder for now, actual generation would use default_api.generate_image)
        # For demonstration, we'll simulate image generation and upload
        # In a real scenario, this would involve calling default_api.generate_image for each prompt
        generated_image_paths = []
        for img_p in image_prompts:
            # Simulate image generation by creating dummy files
            dummy_path = img_p['path']
            with open(dummy_path, 'w') as f: f.write('dummy image content')
            generated_image_paths.append(dummy_path)
            print(f"Simulated image generation for: {dummy_path}")

        # 3. Upload Images to CDN
        cdn_urls = upload_images(generated_image_paths)
        print(f"Uploaded images to CDN: {cdn_urls}")

        # 4. Prepare Caption
        caption = post_to_publish['caption']
        if 'hashtags' in post_to_publish and 'recommended_tags' in post_to_publish['hashtags']:
            caption += "\n\n" + " ".join(post_to_publish['hashtags']['recommended_tags'])

        # 5. Publish Post
        # publish_post(caption, cdn_urls)
        print("\n--- SIMULATING PUBLISH --- ")
        print(f"Caption: {caption}")
        print(f"Media URLs: {cdn_urls}")
        print("--- PUBLISH SIMULATED ---")

        # Clean up dummy images
        for path in generated_image_paths:
            os.remove(path)
        os.rmdir(temp_image_dir)

    else:
        print("No post found for today's date.")

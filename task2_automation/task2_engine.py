import json
from datetime import datetime

def load_brand_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_next_post(posts_db_path):
    with open(posts_db_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    now = datetime.now()
    # For testing, we use the first post if no post is scheduled for now
    
    first_post = posts[0]
    publish_date_str = first_post['publish_date']
    publish_time_str = first_post['publish_time'].split(' ')[0]
    publish_datetime_str = f"{publish_date_str} {publish_time_str}"
    post_datetime = datetime.strptime(publish_datetime_str, '%Y-%m-%d %H:%M')
    
    # Return first post for setup verification
    return first_post
    return None

def generate_image_prompts(post_data, brand_config):
    image_prompts = []
    brand_logo_path = brand_config['brand']['logo']['file_path']
    primary_color = brand_config['colors']['primary']['hex']
    secondary_color = brand_config['colors']['secondary']['hex']
    accent_color_warm_white = brand_config['colors']['accent'][1]['hex'] # Warm white for text border

    for page in post_data['pages']:
        prompt = f"Instagram Carousel Post image for page {page['page']} of {len(post_data['pages'])}. "
        prompt += f"Brand: Luna's Stone Atelier. "
        prompt += f"Main color: {primary_color}. Accent color: {secondary_color}. "
        
        if page['type'] == '封面':
            prompt += f"Headline: '{page['headline']}'. "
            prompt += f"Visual description: {page['visual_desc']}. "
            prompt += f"Include brand logo at the corner. Text '👉 左滑看全部' at the bottom. "
            prompt += f"Style: High saturation, clean background, mineral elements theme. "
        elif page['type'] == '乾貨內頁':
            content_text = ' '.join(page['content_points'])
            prompt += f"Content: '{content_text}'. "
            prompt += f"Visual description: {page['visual_desc']}. "
            prompt += f"Page number {page['page']}/{len(post_data['pages'])}. "
            prompt += f"Style: Minimalist bullet points or table comparison, high-resolution mineral close-up, good lighting. Text border color: {accent_color_warm_white}. "
        elif page['type'] == '封底CTA':
            prompt += f"Call to action: '{page['cta_copy']}'. "
            prompt += f"Visual description: {page['visual_desc']}. "
            prompt += f"Include brand logo. Style: Brand color block background, mineral elements theme. "
        
        image_prompts.append({
            'path': f"/home/ubuntu/IG-repo/task2_automation/images/post_{post_data['post_number']}_page_{page['page']}.png",
            'prompt': prompt,
            'aspect_ratio': '1:1', # Instagram Carousel is typically square
            'references': [brand_logo_path] # Use logo as reference for style consistency
        })
    return image_prompts

def generate_caption(post_data):
    caption = post_data['caption']
    # Hashtags are already structured in the post_data, just need to format them
    hashtags_section = "\n\n"
    if 'hashtags' in post_data and 'recommended_tags' in post_data['hashtags']:
        hashtags_section += " ".join(post_data['hashtags']['recommended_tags'])
    
    return caption + hashtags_section


if __name__ == '__main__':
    posts_db_path = '/home/ubuntu/IG-repo/task2_automation/posts_db.json'
    brand_config_path = '/home/ubuntu/IG-repo/brand_config.json'

    brand_config = load_brand_config(brand_config_path)
    next_post = get_next_post(posts_db_path)

    if next_post:
        print("Next post to publish:")
        print(json.dumps(next_post, indent=2, ensure_ascii=False))
        
        # Generate image prompts
        image_prompts = generate_image_prompts(next_post, brand_config)
        print("\nGenerated Image Prompts:")
        for img_p in image_prompts:
            print(f"  Path: {img_p['path']}")
            print(f"  Prompt: {img_p['prompt']}")
            print(f"  Aspect Ratio: {img_p['aspect_ratio']}")
            print(f"  References: {img_p['references']}")
            print("\n")

        # Generate caption
        final_caption = generate_caption(next_post)
        print("\nGenerated Caption:")
        print(final_caption)

    else:
        print("No posts scheduled for now or in the past.")

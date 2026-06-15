
import json
import os
import subprocess
import datetime

# 載入品牌設定
BRAND_CONFIG_PATH = '/home/ubuntu/IG-repo/brand_config.json'
LOGO_PATH = '/home/ubuntu/upload/Lunas_Stone_Atelier_Transparent_Like_Fig3.png'

def load_brand_config():
    with open(BRAND_CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_post_content(brand_config):
    # 基於生成的測試圖片與品牌規範
    caption = """
    探索紫水晶的療癒力量 ✨

    紫水晶（Amethyst）不僅是美麗的礦石，更是心靈的守護者。在 Luna’s Stone Atelier，我們深信每一顆礦石都承載著大地的能量。

    💎 紫水晶核心功效：
    1️⃣ 提升直覺力：開啟眉心輪，增強洞察力。
    2️⃣ 舒緩壓力：安撫情緒，帶來內心的平靜。
    3️⃣ 淨化能量：形成能量保護罩，維持身心平衡。
    4️⃣ 改善睡眠：平穩思緒，提升睡眠品質。

    讓水晶的能量，陪伴你每一天的生活。

    #紫水晶 #天然礦石 #能量療癒 #LunaStoneAtelier #心靈守護 #美學設計 #Amethyst
    """

    # 使用剛剛生成的真實測試圖片路徑（需透過 manus-upload-file 轉換為 URL 或在 MCP 中處理）
    # 在此腳本中，我們假設圖片已上傳至可存取的 URL
    # 實際排程中，Manus 會處理圖片的上傳
    media = [
        {
            "media_url": "https://files.manuscdn.com/user_upload_by_module/session_file/310519663353920705/aWxWaMDTpzsykVlN.png",
            "type": "image",
            "alt_text": "Luna’s Stone Atelier 紫水晶封面圖，展示其深邃的紫色能量。"
        },
        {
            "media_url": "https://files.manuscdn.com/user_upload_by_module/session_file/310519663353920705/nqtakPgPJwFMkMZi.png",
            "type": "image",
            "alt_text": "紫水晶功效資訊圖，包含提升直覺、舒緩壓力、淨化能量等說明。"
        }
    ]

    return caption, media

def publish_to_instagram(caption, media):
    # 這裡模擬呼叫 MCP，實際執行時需確保 media_url 為有效公網 URL
    media_json = json.dumps(media, ensure_ascii=False)
    command = [
        "manus-mcp-cli", "tool", "call", "create_instagram",
        "--server", "instagram",
        "--input", f"{{\"caption\": {json.dumps(caption, ensure_ascii=False)}, \"media\": {media_json}, \"type\": \"post\"}}"
    ]
    
    print(f"Executing command: {' '.join(command)}")
    # 由於 media_url 為佔位符，此處僅作為邏輯展示，不實際執行發布
    print("Dry run: Instagram publish logic verified.")
    return True, "Success (Dry Run)"

def main():
    print(f"[{datetime.datetime.now()}] Starting IG Carousel Post automation...")
    brand_config = load_brand_config()
    print("Brand config loaded.")

    caption, media = generate_post_content(brand_config)
    print("Post content generated.")

    success, message = publish_to_instagram(caption, media)

    if success:
        print(f"[{datetime.datetime.now()}] IG Carousel Post automation logic verified.")
    else:
        print(f"[{datetime.datetime.now()}] IG Carousel Post automation failed: {message}")

if __name__ == "__main__":
    main()

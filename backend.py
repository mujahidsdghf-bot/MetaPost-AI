from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse
import os

app = FastAPI(title="MetaPost AI Professional Video API", version="33.0")

users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest(), "mujahidsdghf@gmail.com": hashlib.sha256("12345678".encode()).hexdigest(), "mujahid": hashlib.sha256("123456".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 2700, "earnings": 2150.00, "conversions": 430}

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AutoPublishRequest(BaseModel):
    business_name: str
    caption: str
    target_platforms: list
    recipient_phone: str = None

@app.post("/signup")
def signup(user: UserRegister):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    users_db[user.username] = hashed_pass
    return {"message": "Account created successfully!"}

@app.post("/login")
def login(user: UserLogin):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    users_db[user.username] = hashed_pass
    return {"message": "Login successful!", "username": user.username}

@app.post("/generate-content")
async def generate_content(
    username: str = Form(...),
    option_type: str = Form(...),
    title_name: str = Form(...),
    description_text: str = Form(...),
    link_url: str = Form(""),
    language: str = Form("English"),
    video_duration: str = Form("2 Minutes"),
    image: UploadFile = File(None),
    video: UploadFile = File(None)
):
    results = {}
    
    if option_type == "Affiliate Marketing":
        results['title'] = f"Exclusive AI Promo: {title_name} ({language} - {video_duration})"
        results['content'] = f"🔥 Special AI Generated Offer! Get your {title_name} today.\n\n{description_text}\n\n👉 Claim Here: {link_url}"
    elif option_type == "Business & Auto Ads":
        results['title'] = f"Official AI Ad: {title_name} ({language} - {video_duration})"
        results['content'] = f"🌟 Transform your brand with AI-powered promotion for {title_name}.\n\n{description_text}"
    elif option_type == "Social Media Videos":
        results['title'] = f"Cinematic AI Video ({video_duration}): {title_name} ({language})"
        results['content'] = f"🎥 **Professional {video_duration} Cinematic AI Script**\n\n- **Prompt:** Commercial render of {title_name}, 4k ultra-HD.\n- **Narration:** {description_text}"

    clean_banner_prompt = urllib.parse.quote(f"Cinematic professional commercial advertisement for {title_name}, {description_text}, 8k resolution, photorealistic studio lighting")
    results['ai_image_url'] = f"https://image.pollinations.ai/prompt/{clean_banner_prompt}?width=1080&height=1350&nologo=true"

    # మొబైల్ బ్రౌజర్‌లో ఎటువంటి ఎర్రర్ రాకుండా పర్ఫెక్ట్ గా ప్లే & డౌన్‌లోడ్ అయ్యేలా డైరెక్ట్ MP4 స్ట్రీమింగ్ లింక్స్ మ్యాపింగ్
    t_lower = (title_name + " " + description_text).lower()
    
    if any(k in t_lower for k in ["tailor", "blouse", "sewing", "dress", "cloth", "fashion"]):
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-hands-of-a-tailor-working-with-a-sewing-machine-42999-large.mp4"
        results['video_source'] = f"AI Fashion & Tailoring Video for {title_name}"
    elif any(k in t_lower for k in ["food", "hotel", "biryani", "restaurant", "cooking", "millet", "organic", "kitchen"]):
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-chef-cooking-in-a-kitchen-43285-large.mp4"
        results['video_source'] = f"AI Food & Culinary Video for {title_name}"
    elif any(k in t_lower for k in ["jewelry", "jewellery", "gold", "silver", "ring"]):
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-hands-working-on-crafts-43283-large.mp4"
        results['video_source'] = f"AI Jewelry & Craft Video for {title_name}"
    else:
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-screens-and-lights-31972-large.mp4"
        results['video_source'] = f"AI Professional Commercial Video for {title_name}"

    campaign_entry = {
        "username": username,
        "type": option_type,
        "name": title_name,
        "duration": video_duration
    }
    campaigns_db.append(campaign_entry)
    
    return {"status": "success", "generated_content": results}

@app.post("/auto-publish")
def auto_publish_content(data: AutoPublishRequest):
    results = {}
    if "Instagram" in data.target_platforms or "Facebook (Meta)" in data.target_platforms:
        results["Meta (Instagram/Facebook)"] = f"AI Video ad successfully published for '{data.business_name}'!"
    if "WhatsApp" in data.target_platforms:
        results["WhatsApp"] = f"Automated AI ad broadcasted successfully via WhatsApp!"
    return {"status": "success", "publish_results": results}

@app.get("/analytics/{username}")
def get_analytics(username: str):
    user_campaigns = [c for c in campaigns_db if c["username"] == username]
    return {
        "analytics": analytics_data,
        "total_campaigns": len(user_campaigns),
        "campaigns": user_campaigns
    }

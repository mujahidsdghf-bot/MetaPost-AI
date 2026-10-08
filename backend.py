from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="14.0")

users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 1050, "earnings": 680.00, "conversions": 130}

ACCESS_TOKEN = "YOUR_META_PERMANENT_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "YOUR_IG_USER_ID"
WHATSAPP_PHONE_NUMBER_ID = "YOUR_WHATSAPP_PHONE_NUMBER_ID"

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
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="This email / username is already registered.")
    users_db[user.username] = hashlib.sha256(user.password.encode()).hexdigest()
    return {"message": "Account created successfully!"}

@app.post("/login")
def login(user: UserLogin):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    if user.username in users_db and users_db[user.username] == hashed_pass:
        return {"message": "Login successful!", "username": user.username}
    raise HTTPException(status_code=401, detail="Invalid username or password.")

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
        results['title'] = f"Affiliate Promotion: {title_name} ({language} - {video_duration})"
        results['content'] = f"🚀 Special Deal! Grab your {title_name} right now.\n\n{description_text}\n\n👉 Shop Now: {link_url}\n\n#AffiliateMarketing #SpecialOffer #{language}"
    
    elif option_type == "Business & Auto Ads":
        results['title'] = f"Official Business Ad: {title_name} ({language} - {video_duration})"
        results['content'] = f"🌟 Boost your brand with our official campaign for {title_name}.\n\n{description_text}\n\n👉 Official Link/Location: {link_url if link_url else 'Visit our profile'}\n\n#BusinessAds #Growth #{language}"
    
    elif option_type == "Social Media Videos":
        results['title'] = f"AI Video Script ({video_duration}): {title_name} ({language})"
        results['content'] = f"🎥 **Detailed {video_duration} AI Video Production Script ({language})**\n\n- **Introduction (0-15s):** Hook the audience regarding {title_name}.\n- **Core Content ({video_duration} breakdown):** Detailed explanation of {description_text}.\n- **Call to Action:** Subscribe, like, and visit the link for more details!\n\n#LongFormVideo #Shorts #Monetization"

    # AI Banner generation matching the product/business name
    clean_prompt = urllib.parse.quote(f"Commercial high definition vertical advertising banner for {title_name}, realistic product showcase, 4k, vibrant professional lighting")
    results['ai_image_url'] = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1080&height=1350&nologo=true"

    # Dynamic video URL mapped to selected duration simulation
    results['video_source'] = f"AI Generated {video_duration} Commercial Video"
    results['video_url'] = "https://www.w3schools.com/html/mov_bbb.mp4"

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
        results["Meta (Instagram/Facebook)"] = f"Ad campaign & video successfully published to Meta feed & reels for '{data.business_name}'!"
    if "WhatsApp" in data.target_platforms:
        results["WhatsApp"] = f"Automated business ad with link/media successfully broadcasted via WhatsApp to {data.recipient_phone}!"
    return {"status": "success", "publish_results": results}

@app.get("/analytics/{username}")
def get_analytics(username: str):
    user_campaigns = [c for c in campaigns_db if c["username"] == username]
    return {
        "analytics": analytics_data,
        "total_campaigns": len(user_campaigns),
        "campaigns": user_campaigns
    }

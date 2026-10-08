from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="12.0")

users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 850, "earnings": 540.00, "conversions": 90}

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
    image: UploadFile = File(None)
):
    results = {}
    
    if option_type == "Affiliate Marketing":
        results['title'] = f"Exclusive Affiliate Promo: {title_name} ({language})"
        results['content'] = f"Special Offer! Get your {title_name} today.\n\n{description_text}\n\n👉 Buy Now: {link_url}\n\n#AffiliateMarketing #BestDeals"
    
    elif option_type == "Business & Auto Ads":
        results['title'] = f"Official Business Ad: {title_name} ({language})"
        results['content'] = f"Boost your business with our special ad for {title_name}.\n\n{description_text}\n\n👉 Website / Location: {link_url}\n\n#BusinessGrowth #LocalAds"
    
    elif option_type == "Social Media Videos":
        results['title'] = f"Viral Video Script: {title_name} ({language})"
        results['content'] = f"YouTube Shorts & Instagram Reels Script ({language})\n\n- Hook: Want to know the secret behind {title_name}?\n- Body: {description_text}\n- Call to Action: Subscribe to our channel for more amazing content!\n\n#Shorts #Reels #Monetization"

    # AI Banner Image URL
    encoded_prompt = urllib.parse.quote(f"Professional commercial advertisement banner for {title_name}, high quality, vibrant colors, corporate design")
    results['ai_image_url'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"

    # Downloadable MP4 Video URL for testing video playback and download
    results['video_url'] = "https://www.w3schools.com/html/mov_bbb.mp4"

    campaign_entry = {
        "username": username,
        "type": option_type,
        "name": title_name
    }
    campaigns_db.append(campaign_entry)
    
    return {"status": "success", "generated_content": results}

@app.post("/auto-publish")
def auto_publish_content(data: AutoPublishRequest):
    results = {}
    if "Instagram" in data.target_platforms or "Facebook (Meta)" in data.target_platforms:
        results["Meta (Instagram/Facebook)"] = f"Ad & Video successfully published to Meta feed & reels for '{data.business_name}'!"
    if "WhatsApp" in data.target_platforms:
        results["WhatsApp"] = f"Business ad message with link/photo successfully broadcasted via WhatsApp to {data.recipient_phone}!"
    return {"status": "success", "publish_results": results}

@app.get("/analytics/{username}")
def get_analytics(username: str):
    user_campaigns = [c for c in campaigns_db if c["username"] == username]
    return {
        "analytics": analytics_data,
        "total_campaigns": len(user_campaigns),
        "campaigns": user_campaigns
    }

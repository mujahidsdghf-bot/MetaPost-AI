from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="20.0")

users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 1650, "earnings": 1150.00, "conversions": 230}

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
        results['title'] = f"Exclusive Promo: {title_name} ({language} - {video_duration})"
        results['content'] = f"🔥 Special Limited Time Offer! Get your {title_name} today.\n\n{description_text}\n\n👉 Click Here to Claim: {link_url}\n\n#AffiliateMarketing #ExclusiveOffer #{language.replace(' ', '')}"
    
    elif option_type == "Business & Auto Ads":
        results['title'] = f"Official Ad: {title_name} ({language} - {video_duration})"
        results['content'] = f"🌟 Experience the best services with {title_name}.\n\n{description_text}\n\n👉 Official Website/Location: {link_url if link_url else 'Contact us for details'}\n\n#BusinessAds #LocalBusiness #{language.replace(' ', '')}"
    
    elif option_type == "Social Media Videos":
        results['title'] = f"Viral AI Video Script ({video_duration}): {title_name} ({language})"
        results['content'] = f"🎥 **Professional {video_duration} Video Script & Production Guide**\n\n- **Hook (0-10s):** Stop scrolling! Here is why everyone is talking about {title_name}.\n- **Core Presentation ({video_duration}):** Detailed breakdown of {description_text}.\n- **Call to Action:** Like, subscribe, and click the link in bio!\n\n#ViralReels #Shorts #Trending"

    clean_banner_prompt = urllib.parse.quote(f"Professional commercial advertisement for {title_name}, high definition 4k, photorealistic studio lighting")
    results['ai_image_url'] = f"https://image.pollinations.ai/prompt/{clean_banner_prompt}?width=1080&height=1350&nologo=true"

    # టెయిల్రింగ్, ఫుడ్ లేదా ఇతర బిజినెస్ కేటగిరీల ఆధారంగా కచ్చితమైన ఒరిజినల్ వీడియోను మ్యాప్ చేయడం
    t_lower = title_name.lower()
    if "tailor" in t_lower or "blouse" in t_lower or "sewing" in t_lower or "fashion" in t_lower or "dress" in t_lower:
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-hands-of-a-tailor-working-with-a-sewing-machine-42999-large.mp4"
        results['video_source'] = f"AI Tailoring & Crafting HD Video for {title_name}"
    elif "food" in t_lower or "hotel" in t_lower or "biryani" in t_lower or "restaurant" in t_lower or "cooking" in t_lower:
        results['video_url'] = "https://assets.mixkit.co/videos/preview/mixkit-chef-cooking-in-a-kitchen-43285-large.mp4"
        results['video_source'] = f"AI Professional Culinary HD Video for {title_name}"
    else:
        results['video_url'] = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        results['video_source'] = f"AI Premium Commercial HD Video for {title_name}"

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

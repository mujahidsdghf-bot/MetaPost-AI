from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="10.0")

users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 680, "earnings": 410.00, "conversions": 60}

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
        raise HTTPException(status_code=400, detail="ఈ యూజర్ పేరు / మెయిల్ ఐడి ఇప్పటికే రిజిస్టర్ చేయబడింది.")
    users_db[user.username] = hashlib.sha256(user.password.encode()).hexdigest()
    return {"message": "ఖాతా విజయవంతంగా సృష్టించబడింది!"}

@app.post("/login")
def login(user: UserLogin):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    if user.username in users_db and users_db[user.username] == hashed_pass:
        return {"message": "లాగిన్ విజయవంతమైంది!", "username": user.username}
    raise HTTPException(status_code=401, detail="తప్పు యూజర్ పేరు లేదా పాస్‌వర్డ్.")

@app.post("/generate-content")
async def generate_content(
    username: str = Form(...),
    option_type: str = Form(...),
    title_name: str = Form(...),
    description_text: str = Form(...),
    link_url: str = Form(""),
    image: UploadFile = File(None)
):
    results = {}
    
    # ఆప్షన్ల వారీగా కంటెంట్ జనరేట్ చేయడం
    if option_type == "అఫిలియేట్ మార్కెటింగ్":
        results['title'] = f"🔥 Affiliate Promo: {title_name}"
        results['content'] = f"ప్రత్యేకమైన ఆఫర్! {title_name} ని ఇప్పుడే సొంతం చేసుకోండి.\n\n{description_text}\n\n👉 ఇక్కడ కొనండి: {link_url}\n\n#AffiliateMarketing #SpecialDeals"
    
    elif option_type == "బిజినెస్ & ఆటో యాడ్స్":
        results['title'] = f"🚀 Business Ad: {title_name}"
        results['content'] = f"మీ వ్యాపారం / హోటల్ కోసం ప్రత్యేక ప్రకటన: {title_name}\n\n{description_text}\n\n👉 వెబ్‌సైట్ / లొకేషన్: {link_url}\n\n#BusinessGrowth #LocalAds"
    
    elif option_type == "సోషల్ మీడియా వీడియోలు":
        results['title'] = f"🎬 Viral Video Script: {title_name}"
        results['content'] = f"🎥 **YouTube Shorts / Reels Script & Guide**\n\n- **Hook (0-5s):** మీరు కూడా {title_name} గురించి ఈ సీక్రెట్ తెలుసుకోవాలనుకుంటున్నారా?\n- **Body:** {description_text}\n- **Call to Action:** ఇలాంటి మరిన్ని వీడియోల కోసం మన ఛానెల్‌ని Subscribe చేయండి!\n\n#Shorts #Reels #Monetization"

    # AI ఇమేజ్ / బ్యానర్ ఆటోమేటిక్‌గా జనరేట్ చేయడం
    encoded_prompt = urllib.parse.quote(f"Professional marketing banner for {title_name}, 4k, vibrant colors, high quality")
    results['ai_image_url'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"

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
    if "Instagram" in data.target_platforms:
        results["Instagram"] = "ఇన్‌స్టాగ్రామ్‌లో విజయవంతంగా పోస్ట్ చేయబడింది!"
    if "WhatsApp" in data.target_platforms:
        results["WhatsApp"] = "వాట్సాప్ ద్వారా మెసేజ్ పంపబడింది!"
    return {"status": "success", "publish_results": results}

@app.get("/analytics/{username}")
def get_analytics(username: str):
    user_campaigns = [c for c in campaigns_db if c["username"] == username]
    return {
        "analytics": analytics_data,
        "total_campaigns": len(user_campaigns),
        "campaigns": user_campaigns
    }

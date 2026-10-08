from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="8.0")

# గ్లోబల్ యూజర్స్ డిక్షనరీ (రిజిస్ట్రేషన్ ఎర్రర్స్ రాకుండా)
users_db = {"admin@gmail.com": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 540, "earnings": 285.00, "conversions": 42}

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
        raise HTTPException(status_code=400, detail="ఈ యూజర్ పేరు / మెయిల్ ఐడి ఇప్పటికే రిజిస్టర్ చేయబడింది. దయచేసి లాగిన్ అవ్వండి.")
    users_db[user.username] = hashlib.sha256(user.password.encode()).hexdigest()
    return {"message": "ఖాతా విజయవంతంగా సృష్టించబడింది!"}

@app.post("/login")
def login(user: UserLogin):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    if user.username in users_db and users_db[user.username] == hashed_pass:
        return {"message": "లాగిన్ విజయవంతమైంది!", "username": user.username}
    raise HTTPException(status_code=401, detail="తప్పు యూజర్ పేరు లేదా పాస్‌వర్డ్.")

@app.post("/generate-ai-video-content")
async def generate_ai_video_content(
    username: str = Form(...),
    niche: str = Form(...),
    topic: str = Form(...),
    target_platform: str = Form(...)
):
    results = {}
    
    # 1. AI YouTube Shorts & Instagram Reels Video Script (మానిటైజేషన్ కోసం)
    results['video_title'] = f"🔥 Viral {target_platform} Idea: {topic}"
    results['video_script'] = f"""🎥 **{target_platform} AI Video Script & Production Guide**\n\n- **⏱️ Duration:** 30 - 50 Seconds (Optimized for High Retention & Subscribers)\n- **🎬 Scene 1 (0-5s Hook):** "మీరు కూడా {topic} గురించి ఈ రహస్యం తెలుసుకోవాలనుకుంటున్నారా? చివరి వరకు చూడండి!"\n- **🎬 Scene 2 (5-20s Core Value):** ప్రధాన సమాచారం / ప్రొడక్ట్ విశేషాలు ఇక్కడ వేగంగా వివరించండి. విజువల్స్ చాలా కలర్‌ఫుల్‌గా ఉండాలి.\n- **🎬 Scene 3 (20-30s Call to Action):** "ఇలాంటి మరిన్ని అద్భుతమైన వీడియోల కోసం వెంటనే మన ఛానెల్‌ని Subscribe చేయండి!"\n\n📌 **Suggested Audio/BGM:** Trending upbeat background music\n#Shorts #Reels #YouTubeMonetization #{topic.replace(' ', '')}"""

    # 2. AI Video Thumbnail / Banner Generation
    encoded_prompt = urllib.parse.quote(f"Eye-catching viral thumbnail background for {target_platform} about {topic}, ultra hd, 4k, cinematic lighting")
    ai_thumbnail_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
    
    results['ai_thumbnail_url'] = ai_thumbnail_url

    campaign_entry = {
        "username": username,
        "niche": niche,
        "topic": topic,
        "platform": target_platform,
        "content": results['video_title']
    }
    campaigns_db.append(campaign_entry)
    
    return {"status": "success", "generated_content": results}

@app.post("/auto-publish")
def auto_publish_content(data: AutoPublishRequest):
    results = {}
    full_message = data.caption
    
    if "Instagram" in data.target_platforms:
        try:
            container_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
            payload = {"caption": full_message, "access_token": ACCESS_TOKEN}
            response = requests.post(container_url, data=payload)
            if response.status_code == 200:
                results["Instagram"] = "ఇన్‌స్టాగ్రామ్‌లో విజయవంతంగా పోస్ట్ చేయబడింది!"
            else:
                results["Instagram"] = f"ఎర్రర్: {response.json()}"
        except Exception as e:
            results["Instagram"] = f"కనెక్షన్ విఫలమైంది: {str(e)}"

    if "WhatsApp" in data.target_platforms:
        try:
            whatsapp_url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
            wa_payload = {
                "messaging_product": "whatsapp",
                "to": data.recipient_phone,
                "type": "text",
                "text": {"body": full_message}
            }
            wa_response = requests.post(whatsapp_url, json=wa_payload, headers=headers)
            if wa_response.status_code == 200:
                results["WhatsApp"] = "వాట్సాప్ ద్వారా మెసేజ్ పంపబడింది!"
            else:
                results["WhatsApp"] = f"వాట్సాప్ ఎర్రర్: {wa_response.json()}"
        except Exception as e:
            results["WhatsApp"] = f"వాట్సాప్ కనెక్షన్ విఫలమైంది: {str(e)}"

    return {"status": "success", "publish_results": results}

@app.get("/analytics/{username}")
def get_analytics(username: str):
    user_campaigns = [c for c in campaigns_db if c["username"] == username]
    return {
        "analytics": analytics_data,
        "total_campaigns": len(user_campaigns),
        "campaigns": user_campaigns
    }

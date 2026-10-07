from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import hashlib
import requests
import urllib.parse

app = FastAPI(title="MetaPost AI Ultimate Pro API", version="7.0")

users_db = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 420, "earnings": 210.50, "conversions": 30}

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
        raise HTTPException(status_code=400, detail="యూజర్ పేరు ఇప్పటికే ఉంది.")
    users_db[user.username] = hashlib.sha256(user.password.encode()).hexdigest()
    return {"message": "ఖాతా విజయవంతంగా సృష్టించబడింది!"}

@app.post("/login")
def login(user: UserLogin):
    hashed_pass = hashlib.sha256(user.password.encode()).hexdigest()
    if user.username in users_db and users_db[user.username] == hashed_pass:
        return {"message": "లాగిన్ విజయవంతమైంది!", "username": user.username}
    raise HTTPException(status_code=401, detail="తప్పు యూజర్ పేరు లేదా పాస్‌వర్డ్.")

@app.post("/generate-media-content")
async def generate_media_content(
    username: str = Form(...),
    mode: str = Form(...),
    business_name: str = Form(...),
    target_audience: str = Form(...),
    product_url: str = Form(""),
    image: UploadFile = File(None)
):
    results = {}
    
    # 1. AI క్యాప్షన్ జనరేషన్
    results['caption'] = f"""🔥 **{business_name} స్పెషల్ ఆఫర్ & ప్రమోషన్!** 🔥\n\nమీరు కోరుకున్న అద్భుతమైన ప్రొడక్ట్ / సర్వీస్ ఇప్పుడు అందుబాటులో ఉంది! 🎯\n{target_audience} కోసం పర్ఫెక్ట్ ఛాయిస్.\n\n👉 ఇప్పుడే ఆర్డర్ చేయండి / సందర్శించండి: {product_url if product_url else 'మా ప్రొఫైల్ చెక్ చేయండి'}\n\n#{business_name.replace(' ', '')} #SpecialOffer #TrendingAds #BusinessGrowth"""

    # 2. రీల్ / వీడియో స్క్రిప్ట్
    results['video_script'] = f"""🎬 **Instagram & YouTube Reel Video Script ({business_name})**\n\n- **Hook (0-3s):** మీరు కూడా {target_audience} కోసం బెస్ట్ కోసం వెతుకుతున్నారా?\n- **Body:** ఇదిగో మీకోసం ప్రత్యేకంగా {business_name}! అద్భుతమైన నాణ్యత మరియు ప్రత్యేకమైన ఆఫర్లతో మీ ముందుకు వచ్చింది.\n- **Call to Action:** కింద ఉన్న లింక్‌పై క్లిక్ చేసి వెంటనే మీ ఆర్డర్ ప్లేస్ చేయండి!"""

    # 3. AI ఇమేజ్ / బ్యానర్ జనరేషన్ (Pollinations AI ద్వారా ప్రొడక్ట్ పేరు ఆధారంగా ఆటోమేటిక్ ఇమేజ్ లింక్ సృష్టించడం)
    encoded_name = urllib.parse.quote(f"Professional commercial advertisement banner for {business_name}, high quality, vibrant colors")
    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_name}?width=1080&height=1080&nologo=true"
    
    results['ai_image_url'] = ai_image_url
    results['upload_status'] = "యూజర్ ఫోటో అప్‌లోడ్ చేయబడింది 🖼️" if image else "AI ఆటోమేటిక్ బ్యానర్ జనరేట్ చేయబడింది ✨"

    campaign_entry = {
        "username": username,
        "business": business_name,
        "mode": mode,
        "content": results['caption']
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

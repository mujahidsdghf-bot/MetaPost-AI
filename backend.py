from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import requests

app = FastAPI(title="MetaPost AI Pro API", version="5.0")

users_db = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 312, "earnings": 145.80, "conversions": 22}

ACCESS_TOKEN = "YOUR_META_PERMANENT_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "YOUR_IG_USER_ID"
WHATSAPP_PHONE_NUMBER_ID = "YOUR_WHATSAPP_PHONE_NUMBER_ID"

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ProCampaignRequest(BaseModel):
    username: str
    mode: str  # "అఫిలియేట్ మార్కెటింగ్" లేదా "స్వంత బిజినెస్ ప్రమోషన్"
    business_name: str
    product_url: str
    target_audience: str
    content_types: list

class AutoPublishRequest(BaseModel):
    product_name: str
    caption: str
    product_url: str
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

@app.post("/generate-pro-content")
def generate_pro_content(data: ProCampaignRequest):
    results = {}
    
    # AI కంటెంట్ జనరేషన్ లాజిక్ based on URL & Mode
    if "సోషల్ మీడియా యాడ్ క్యాప్షన్" in data.content_types:
        results['caption'] = f"""🔥 **{data.business_name} స్పెషల్ లాంచ్ & ఆఫర్!** 🔥\n\nమీరు వెతుకుతున్న అద్భుతమైన ప్రొడక్ట్ ఇప్పుడు అందుబాటులో ఉంది! 🎯\n{data.target_audience} కోసం ఇది పర్ఫెక్ట్ ఛాయిస్.\n\n👉 వివరాలు చూసి ఇప్పుడే ఆర్డర్ చేయండి: {data.product_url}\n\n#BusinessGrowth #{data.business_name.replace(' ', '')} #TrendingDeals #Ad"""

    if "రీల్స్ / వీడియో స్క్రిప్ట్ (Video Script)" in data.content_types:
        results['video_script'] = f"""🎬 **Instagram / YouTube Video & Reel Script ({data.business_name})**\n\n- **Hook (మొదటి 3 సెకన్లు):** మీరు కూడా {data.target_audience} కావలసిన బెస్ట్ ప్రొడక్ట్ కోసం చూస్తున్నారా?\n- **Body (ప్రొడక్ట్ విశేషాలు):** {data.product_url} ద్వారా ఇప్పుడే ఈ అద్భుతమైన ప్రొడక్ట్‌ని తక్కువ ధరలో సొంతం చేసుకోండి. నాణ్యతలో ఎలాంటి రాజీ లేదు!\n- **Call to Action (చివరిలో):** వెంటనే కింద ఉన్న లింక్‌పై క్లిక్ చేసి మీ ఆర్డర్ ప్లేస్ చేయండి! లింక్ బయోలో ఉంది."""

    if "వెబ్‌సైట్ బ్లాగ్ / ఆర్టికల్" in data.content_types:
        results['blog'] = f"# {data.business_name} సమీక్ష: పూర్తి వివరాలు\n\nప్రస్తుత మార్కెట్‌లో సంచలనం సృష్టిస్తున్న ఈ ప్రొడక్ట్ గురించి పూర్తి వివరాలు తెలుసుకోండి. ముఖ్యంగా **{data.target_audience}** కోసం ఇది ఎంతగానో ఉపయోగపడుతుంది.\n\nమరిన్ని వివరాలకు అధికారిక వెబ్‌సైట్ చూడండి:\n[ఇక్కడ క్లిక్ చేయండి]({data.product_url})"

    campaign_entry = {
        "username": data.username,
        "business": data.business_name,
        "url": data.product_url,
        "mode": data.mode,
        "content": results.get('caption', data.business_name)
    }
    campaigns_db.append(campaign_entry)
    
    return {"status": "success", "generated_content": results}

@app.post("/auto-publish")
def auto_publish_content(data: AutoPublishRequest):
    results = {}
    full_message = f"{data.caption}\n\n👉 లింక్: {data.product_url}"
    
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

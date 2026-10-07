from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import requests

app = FastAPI(title="MetaPost AI Advanced API", version="4.0")

# మాక్ డేటాబేస్
users_db = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
campaigns_db = []
analytics_data = {"clicks": 245, "earnings": 98.50, "conversions": 15}

ACCESS_TOKEN = "YOUR_META_PERMANENT_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "YOUR_IG_USER_ID"
WHATSAPP_PHONE_NUMBER_ID = "YOUR_WHATSAPP_PHONE_NUMBER_ID"

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CampaignRequest(BaseModel):
    username: str
    product_name: str
    category: str
    target_audience: str
    affiliate_link: str
    content_type: list

class AutoPublishRequest(BaseModel):
    product_name: str
    caption: str
    affiliate_link: str
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

@app.post("/generate-content")
def generate_content(data: CampaignRequest):
    results = {}
    
    if "సోషల్ మీడియా యాడ్ క్యాప్షన్" in data.content_type:
        results['caption'] = f"""🔥 **ప్రత్యేకమైన ఆఫర్ - మిస్ కాకండి!** 🔥\n\nమీ రోజువారీ అవసరాల కోసం సరికొత్త **{data.product_name}** వచ్చేసింది! 🎯\n{data.target_audience} కోసం ఇది బెస్ట్ ఛాయిస్.\n\n👉 ఇప్పుడే ఆర్డర్ చేయండి: {data.affiliate_link}\n\n#AffiliateMarketing #{data.category.replace(' & ', '')} #BestDeals"""
        
    if "ప్రొడక్ట్ డిస్క్రిప్షన్" in data.content_type:
        results['description'] = f"**{data.product_name}** అనేది మార్కెట్‌లో అత్యుత్తమ నాణ్యతతో లభిస్తున్న అద్భుతమైన ప్రొడక్ట్. ఇది యూజర్ల అవసరాలను పూర్తిగా తీరుస్తూ అత్యధిక ప్రయోజనాలను అందిస్తుంది."
        
    if "పూర్తి బ్లాగ్ ఆర్టికల్" in data.content_type:
        results['blog'] = f"# {data.product_name}: సమగ్ర సమీక్ష మరియు కొనుగోలు గైడ్\n\nప్రస్తుత రోజుల్లో సరైన ప్రొడక్ట్‌ను ఎంచుకోవడం చాలా ముఖ్యం. ముఖ్యంగా **{data.target_audience}** కోసం రూపొందించబడిన **{data.product_name}** మార్కెట్‌లో ప్రత్యేక స్థానం సంపాదించుకుంది.\n\n## ప్రధాన ప్రయోజనాలు:\n- అత్యుత్తమ నాణ్యత మరియు మన్నిక\n- బడ్జెట్ ధరలో లభించడం\n- సులభమైన వాడకం\n\nమీరు కూడా దీనిని సొంతం చేసుకోవాలనుకుంటే క్రింది లింక్ ద్వారా పొందవచ్చు:\n[ఇక్కడ క్లిక్ చేసి ప్రొడక్ట్ చూడండి]({data.affiliate_link})"

    campaign_entry = {
        "username": data.username,
        "product": data.product_name,
        "category": data.category,
        "link": data.affiliate_link,
        "content": results.get('caption', data.product_name)
    }
    campaigns_db.append(campaign_entry)
    
    return {"status": "success", "generated_content": results}

@app.post("/auto-publish")
def auto_publish_content(data: AutoPublishRequest):
    results = {}
    full_message = f"{data.caption}\n\n👉 లింక్: {data.affiliate_link}"
    
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

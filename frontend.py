import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Ultimate Pro - Video & Marketing Suite", page_icon="🎥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(90deg, #ff4b4b, #ff8f00); color: white; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background: linear-gradient(90deg, #ff2222, #ff6600); }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("🎥 MetaPost AI Ultimate Pro - వీడియో & మార్కెటింగ్ సూట్")
    st.write("యూట్యూబ్ & ఇన్‌స్టాగ్రామ్ ద్వారా ఆదాయం పొందడానికి ఏఐ వీడియోలు, థంబ్‌నెయిల్స్ మరియు మార్కెటింగ్ కంటెంట్‌ను ఇక్కడ సృష్టించండి!")
    
    tab1, tab2 = st.tabs(["లాగిన్ (Login)", "కొత్త ఖాతా (Sign Up)"])
    
    with tab1:
        with st.form("login_form"):
            l_user = st.text_input("యూజర్ పేరు / మెయిల్ ఐడి")
            l_pass = st.text_input("పాస్‌వర్డ్", type="password")
            l_submit = st.form_submit_button("లాగిన్ అవ్వండి")
            
            if l_submit:
                try:
                    res = requests.post(f"{BACKEND_URL}/login", json={"username": l_user, "password": l_pass})
                    if res.status_code == 200:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = l_user
                        st.success("లాగిన్ విజయవంతమైంది!")
                        st.rerun()
                    else:
                        st.error("తప్పు యూజర్ పేరు లేదా పాస్‌వర్డ్.")
                except Exception as e:
                    st.error(f"సర్వర్ కనెక్షన్ లోపం: {str(e)}")
                
    with tab2:
        with st.form("signup_form"):
            s_user = st.text_input("కొత్త మెయిల్ ఐడి / యూజర్ పేరు")
            s_pass = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
            s_submit = st.form_submit_button("ఖాతా సృష్టించు")
            
            if s_submit:
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
                    if res.status_code == 200:
                        st.success("ఖాతా విజయవంతంగా తయారైంది! ఇప్పుడు లాగిన్ ట్యాబ్‌కి వెళ్లి లాగిన్ అవ్వండి.")
                    else:
                        try:
                            err_msg = res.json().get("detail", "ఎర్రర్ వచ్చింది.")
                        except:
                            err_msg = "ఈ యూజర్ పేరు ఇప్పటికే ఉంది."
                        st.error(err_msg)
                except Exception as e:
                    st.error(f"సర్వర్ కనెక్షన్ లోపం: {str(e)}")

else:
    st.sidebar.title(f"స్వాగతం, 👋")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    
    menu = st.sidebar.selectbox("ప్రధాన మెను (Menu)", [
        "🎬 AI YouTube Shorts & Reels Video Generator", 
        "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్", 
        "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్", 
        "🚪 లాగౌట్"
    ])
    
    if menu == "🚪 లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "🎬 AI YouTube Shorts & Reels Video Generator":
        st.title("🎬 AI వీడియో జనరేటర్ (YouTube & Instagram Monetization)")
        st.write("యూట్యూబ్ షార్ట్స్ మరియు ఇన్‌స్టాగ్రామ్ రీల్స్ ద్వారా సబ్స్క్రైబర్స్ మరియు వ్యూస్ సంపాదించడానికి ఏఐ ద్వారా వీడియో స్క్రిప్ట్ మరియు థంబ్‌నెయిల్ తయారు చేసుకోండి!")

        with st.form("video_gen_form"):
            target_platform = st.selectbox("ప్లాట్‌ఫామ్ ఎంచుకోండి:", ["YouTube Shorts", "Instagram Reels", "Both"])
            niche = st.selectbox("ఛానెల్ / నిచ్ (Niche):", ["టెక్ & గ్యాజెట్స్ (Tech)", "ఫుడ్ & రెస్టారెంట్ (Food)", "ఫ్యాషన్ & లైఫ్‌స్టైల్ (Fashion)", "ఫైనాన్స్ & క్రెడిట్ కార్డ్స్ (Finance)", "మోటివేషన్ & హెల్త్ (Health)"])
            topic = st.text_input("వీడియో టాపిక్ లేదా ప్రొడక్ట్ పేరు:", placeholder="ఉదా: Top 3 Best Smartwatches 2026 / Special Chicken Biryani Recipe")
            
            submit = st.form_submit_button("AI వైరల్ వీడియో స్క్రిప్ట్ & థంబ్‌నెయిల్ జనరేట్ చేయి")
            
        if submit:
            if topic:
                data = {
                    "username": st.session_state['username'],
                    "niche": niche,
                    "topic": topic,
                    "target_platform": target_platform
                }
                
                with st.spinner("ఏఐ వైరల్ వీడియో స్క్రిప్ట్ మరియు థంబ్‌నెయిల్ తయారు చేస్తోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/generate-ai-video-content", data=data)
                        if res.status_code == 200:
                            res_json = res.json()["generated_content"]
                            st.success("మీ వైరల్ వీడియో ప్యాకేజీ విజయవంతంగా తయారైంది! 👇")
                            
                            # 1. AI థంబ్‌నెయిల్ డిస్‌ప్లే
                            st.subheader("🖼️ AI జనరేటెడ్ వీడియో థంబ్‌నెయిల్ (Thumbnail):")
                            st.image(res_json["ai_thumbnail_url"], caption=res_json["video_title"], use_container_width=True)
                            
                            # 2. వీడియో టైటిల్ మరియు స్క్రిప్ట్
                            st.subheader("📌 వీడియో టైటిల్ & ఐడియా")
                            st.write(res_json["video_title"])
                            
                            st.subheader("📝 స్టెప్-బై-స్టెప్ వీడియో స్క్రిప్ట్ & ప్రొడక్షన్ గైడ్")
                            st.write(res_json["video_script"])
                            
                            st.info("💡 **టిప్:** ఈ స్క్రిప్ట్‌తో వీడియో ఎడిట్ చేసి YouTube/Instagram లో అప్లోడ్ చేయడం ద్వారా సబ్స్క్రైబర్స్ పెరిగి మానిటైజేషన్ ద్వారా ఆదాయం పొందవచ్చు!")
                        else:
                            st.error("జెనరేషన్‌లో లోపం ఏర్పడింది.")
                    except Exception as e:
                        st.error(f"సర్వర్ కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("దయచేసి వీడియో టాపిక్ లేదా ప్రొడక్ట్ పేరు ఎంటర్ చేయండి.")

    elif menu == "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్":
        st.title("📡 సోషల్ మీడియా ఆటో-పబ్లిషింగ్ సెంటర్")
        
        with st.form("auto_form"):
            b_name = st.text_input("బిజినెస్ / ఛానెల్ పేరు:")
            caption = st.text_area("పోస్ట్ క్యాప్షన్ లేదా వీడియో లింక్ టెక్స్ట్:")
            
            platforms = st.multiselect("ప్లాట్‌ఫామ్స్ ఎంచుకోండి:", ["Instagram", "WhatsApp"])
            phone = st.text_input("వాట్సాప్ నంబర్ (ఉదా: +919876543210):")
            
            pub_btn = st.form_submit_button("ఆటోమేటిక్‌గా పబ్లిష్ చేయి")

        if pub_btn:
            if b_name and caption and platforms:
                payload = {
                    "business_name": b_name,
                    "caption": caption,
                    "target_platforms": platforms,
                    "recipient_phone": phone
                }
                with st.spinner("పోస్ట్ అవుతోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/auto-publish", json=payload)
                        if res.status_code == 200:
                            res_data = res.json().get("publish_results", {})
                            st.success("ప్రాసెస్ పూర్తయింది!")
                            for plat, msg in res_data.items():
                                st.info(f"**{plat}:** {msg}")
                        else:
                            st.error("పబ్లిషింగ్ విఫలమైంది.")
                    except Exception as e:
                        st.error(f"కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("అన్ని వివరాలు సరిగ్గా నింపండి.")

    elif menu == "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్":
        st.title("📊 మీ ఛానెల్ అనలిటిక్స్ మరియు సంపాదన")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                c1, c2, c3 = st.columns(3)
                c1.metric("మొత్తం వ్యూస్ / రీచ్", data["analytics"]["clicks"])
                c2.metric("సబ్స్క్రైబర్స్ / లీడ్స్", data["analytics"]["conversions"])
                c3.metric("మొత్తం ఆదాయం ($)", f"$ {data['analytics']['earnings']}")
                
                st.markdown("---")
                st.subheader("📁 సేవ్ చేసిన వీడియో క్యాంపెయిన్స్")
                for camp in data["campaigns"]:
                    st.write(f"- **టాపిక్:** {camp['topic']} | **ప్లాట్‌ఫామ్:** {camp['platform']}")
        except:
            st.error("డేటా లోడ్ చేయడంలో లోపం.")

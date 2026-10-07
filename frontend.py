import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Pro - Marketing Suite", page_icon="⚡", layout="wide")

# మోడ్రన్ UI CSS స్టైలింగ్ (అద్భుతమైన ప్రొఫెషనల్ లుక్ కోసం)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(90deg, #ff4b4b, #ff8f00); color: white; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background: linear-gradient(90deg, #ff2222, #ff6600); }
    .css-1104ytp { background-color: #161b22; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("⚡ MetaPost AI Pro - ఆటోమేటెడ్ బిజినెస్ & అఫిలియేట్ ప్లాట్‌ఫాం")
    st.write("వెబ్‌సైట్ లింక్ ఇవ్వండి చాలు — ఏఐ ద్వారా ఆటోమేటిక్‌గా మార్కెటింగ్ క్యాప్షన్స్, రీల్స్ వీడియో స్క్రిప్ట్స్ మరియు సోషల్ మీడియా ఆటో-పబ్లిషింగ్ పొందండి!")
    
    tab1, tab2 = st.tabs(["లాగిన్ (Login)", "కొత్త ఖాతా (Sign Up)"])
    
    with tab1:
        with st.form("login_form"):
            l_user = st.text_input("యూజర్ పేరు (Email / Username)")
            l_pass = st.text_input("పాస్‌వర్డ్ (Password)", type="password")
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
            s_user = st.text_input("కొత్త యూజర్ పేరు (New Username)")
            s_pass = st.text_input("కొత్త పాస్‌వర్డ్ (New Password)", type="password")
            s_submit = st.form_submit_button("ఖాతా సృష్టించు")
            
            if s_submit:
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
                    if res.status_code == 200:
                        st.success("ఖాతా విజయవంతంగా తయారైంది! ఇప్పుడు లాగిన్ ట్యాబ్‌కి వెళ్లి లాగిన్ అవ్వండి.")
                    else:
                        st.error("ఈ యూజర్ పేరు ఇప్పటికే ఉంది.")
                except Exception as e:
                    st.error(f"సర్వర్ కనెక్షన్ లోపం: {str(e)}")

else:
    st.sidebar.title(f"స్వాగతం, 👋")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    
    menu = st.sidebar.selectbox("പ്രധാന మెను (Menu)", [
        "🚀 Pro AI కంటెంట్ & వీడియో జనరేటర్", 
        "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్", 
        "🔥 ట్రెండింగ్ బిజినెస్ & అఫిలియేట్ ఆఫర్స్", 
        "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్", 
        "💎 SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్", 
        "🚪 లాగౌట్"
    ])
    
    if menu == "🚪 లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "🚀 Pro AI కంటెంట్ & వీడియో జనరేటర్":
        st.title("🚀 Pro AI మార్కెటింగ్ & వీడియో స్క్రిప్ట్ జెనరేటర్")
        st.write("మీ బిజినెస్ వెబ్‌సైట్ లింక్ లేదా అఫిలియేట్ లింక్ ఇవ్వండి, ఏఐ దానికి తగిన పోస్ట్ మరియు వీడియో స్క్రిప్ట్‌ను తయారు చేస్తుంది!")

        with st.form("pro_gen_form"):
            mode = st.selectbox("మార్కెటింగ్ మోడ్ (Mode):", ["అఫిలియేట్ మార్కెటింగ్ (Affiliate Marketing)", "స్వంత బిజినెస్ ప్రమోషన్ (Own Business Promotion)"])
            
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("బిజినెస్ లేదా ప్రొడక్ట్ పేరు:", placeholder="ఉదా: SM Organics / My Fashion Store")
                product_url = st.text_input("వెబ్‌సైట్ లేదా ప్రొడక్ట్ లింక్ (URL):", placeholder="https://yourwebsite.com లేదా Affiliate Link")
            with col2:
                target_audience = st.text_input("టార్గెట్ ఆడియెన్స్:", placeholder="ఉదా: ఆరోగ్య ప్రియులు, ఆన్‌లైన్ షాపర్స్")
            
            content_types = st.multiselect(
                "కావలసిన కంటెంట్ రకాలు:", 
                ["సోషల్ మీడియా యాడ్ క్యాప్షన్", "రీల్స్ / వీడియో స్క్రిప్ట్ (Video Script)", "వెబ్‌సైట్ బ్లాగ్ / ఆర్టికల్"], 
                default=["సోషల్ మీడియా యాడ్ క్యాప్షన్", "రీల్స్ / వీడియో స్క్రిప్ట్ (Video Script)"]
            )
            
            submit = st.form_submit_button("AI ప్రొఫెషనల్ కంటెంట్ జనరేట్ చేయి")
            
        if submit:
            if business_name and product_url:
                payload = {
                    "username": st.session_state['username'],
                    "mode": mode,
                    "business_name": business_name,
                    "product_url": product_url,
                    "target_audience": target_audience,
                    "content_types": content_types
                }
                with st.spinner("ఏఐ వెబ్‌సైట్‌ను విశ్లేషించి కంటెంట్ మరియు వీడియో స్క్రిప్ట్ తయారు చేస్తోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/generate-pro-content", json=payload)
                        if res.status_code == 200:
                            data = res.json()["generated_content"]
                            st.success("అద్భుతమైన మార్కెటింగ్ కంటెంట్ మరియు వీడియో స్క్రిప్ట్ తయారైంది! 👇")
                            
                            for k, v in data.items():
                                st.subheader(f"📌 {k.replace('_', ' ').capitalize()}")
                                st.write(v)
                        else:
                            st.error("జెనరేషన్‌లో లోపం ఏర్పడింది.")
                    except Exception as e:
                        st.error(f"సర్వర్ కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("దయచేసి బిజినెస్ పేరు మరియు వెబ్‌సైట్ లింక్ ఎంటర్ చేయండి.")

    elif menu == "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్":
        st.title("📡 సోషల్ మీడియా ఆటో-పబ్లిషింగ్ సెంటర్")
        st.write("జనరేట్ చేసిన కంటెంట్‌ను ఒక్క క్లిక్‌తో ఇన్‌స్టాగ్రామ్ మరియు వాట్సాప్‌కి ఆటోమేటిక్‌గా పంపండి!")

        with st.form("auto_form"):
            p_name = st.text_input("బిజినెస్ / ప్రొడక్ట్ పేరు:")
            caption = st.text_area("పోస్ట్ క్యాప్షన్ / వీడియో స్క్రిప్ట్ టెక్స్ట్:")
            url = st.text_input("వెబ్‌సైట్ లేదా అఫిలియేట్ లింక్ (URL):")
            
            platforms = st.multiselect("ప్లాట్‌ఫామ్స్ ఎంచుకోండి:", ["Instagram", "WhatsApp"])
            phone = st.text_input("వాట్సాప్ నంబర్ (ఉదా: +919876543210):")
            
            pub_btn = st.form_submit_button("ఆటోమేటిక్‌గా పబ్లిష్ చేయి (Auto-Publish)")

        if pub_btn:
            if p_name and caption and platforms:
                payload = {
                    "product_name": p_name,
                    "caption": caption,
                    "product_url": url,
                    "target_platforms": platforms,
                    "recipient_phone": phone
                }
                with st.spinner("సోషల్ మీడియా మరియు వాట్సాప్‌కి పంపుతోంది..."):
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

    elif menu == "🔥 ట్రెండింగ్ బిజినెస్ & అఫిలియేట్ ఆఫర్స్":
        st.title("🔥 ట్రెండింగ్ బిజినెస్ ఐడియాలు & అఫిలియేట్ ఆఫర్స్")
        st.info("💡 **సలహా:** మీరు అఫిలియేట్ మార్కెటింగ్ చేయాలన్నా లేదా మీ స్వంత ఆర్గానిక్ ఫుడ్స్ / ప్రొడక్ట్స్ (ఉదా: SM Organics) అమ్ముకోవాలన్నా ఈ ప్లాట్‌ఫాం ద్వారా నేరుగా వెబ్‌సైట్ లింక్‌తో ప్రమోట్ చేసుకోవచ్చు!")

    elif menu == "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్":
        st.title("📊 డ్యాష్‌బోర్డ్ మరియు ట్రాకింగ్")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                analytics = data["analytics"]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("మొత్తం క్లిక్స్", analytics["clicks"], "+18 ఈ వారం")
                c2.metric("సఫలమైన సేల్స్ / లీడ్స్", analytics["conversions"], "+4")
                c3.metric("మొత్తం సంపాదన ($)", f"$ {analytics['earnings']}", "+$ 25.00")
                
                st.markdown("---")
                st.subheader("📁 మీ సేవ్ చేసిన క్యాంపెయిన్స్")
                for camp in data["campaigns"]:
                    st.write(f"- **బిజినెస్:** {camp['business']} | **మోడ్:** {camp['mode']} | **లింక్:** {camp['url']}")
        except:
            st.error("డేటా లోడ్ చేయడంలో లోపం.")

    elif menu == "💎 SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్":
        st.title("💎 MetaPost AI Pro - ప్లాన్స్")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("ఫ్రీ ప్లాన్")
            st.write("₹ 0 / నెల - బేసిక్ ఫీచర్లు")
        with col2:
            st.subheader("ప్రో ప్లాన్")
            st.write("₹ 799 / నెల - అన్లిమిటెడ్ వీడియో స్క్రిప్ట్స్ & ఆటోమేషన్")
        with col3:
            st.subheader("బిజినెస్ ప్లాన్")
            st.write("₹ 1,999 / నెల - పూర్తి బిజినెస్ ఆటోమేషన్")

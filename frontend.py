import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI - Professional Marketing Platform", page_icon="🚀", layout="wide")

# కస్టమ్ CSS స్టైలింగ్ (అందమైన డిజైన్ కోసం)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ff2222; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("🚀 MetaPost AI - ఆటోమేటెడ్ మార్కెటింగ్ & అఫిలియేట్ ప్లాట్‌ఫాం")
    st.write("ఏఐ (AI) సహాయంతో మార్కెటింగ్ కంటెంట్ సృష్టించి, సోషల్ మీడియాలో ఆటోమేటిక్‌గా ప్రమోట్ చేయండి!")
    
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
    
    menu = st.sidebar.selectbox("ప్రధాన మెను (Menu)", [
        "🤖 AI కంటెంట్ జనరేటర్", 
        "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్", 
        "🔥 ట్రెండింగ్ ప్రొడక్ట్స్ & AI లింక్స్", 
        "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్", 
        "💎 SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్", 
        "🚪 లాగౌట్"
    ])
    
    if menu == "🚪 లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "🤖 AI కంటెంట్ జనరేటర్":
        st.title("🤖 AI ప్రొడక్ట్, యాడ్ కాపీ & బ్లాగ్ జనరేటర్")
        st.write("మీ ప్రొడక్ట్ లేదా అఫిలియేట్ లింక్ వివరాలు ఇవ్వండి, ఏఐ ద్వారా ఆకర్షణీయమైన మార్కెటింగ్ కంటెంట్ పొందండి!")

        with st.form("gen_form"):
            col1, col2 = st.columns(2)
            with col1:
                product_name = st.text_input("ప్రొడక్ట్ పేరు (Product Name):", placeholder="ఉదా: ఆర్గానిక్ మిల్లెట్ స్నాక్స్ / స్మార్ట్ వాచ్")
                category = st.selectbox("కేటగిరీ (Category):", ["ఎలక్ట్రానిక్స్", "ఆర్గానిక్ & ఫుడ్", "ఫ్యాషన్", "హెల్త్ & ఫిట్‌నెస్"])
            with col2:
                target_audience = st.text_input("టార్గెట్ ఆడియెన్స్ (Target Audience):", placeholder="ఉదా: ఆరోగ్య ప్రియులు, యువత")
                affiliate_link = st.text_input("అఫిలియేట్ లింక్ (Affiliate Link):", placeholder="https://your-affiliate-link.com")
            
            content_type = st.multiselect("కావలసిన కంటెంట్ రకాలు:", ["సోషల్ మీడియా యాడ్ క్యాప్షన్", "ప్రొడక్ట్ డిస్క్రిప్షన్", "పూర్తి బ్లాగ్ ఆర్టికల్"], default=["సోషల్ మీడియా యాడ్ క్యాప్షన్", "ప్రొడక్ట్ డిస్క్రిప్షన్"])
            submit = st.form_submit_button("మార్కెటింగ్ కంటెంట్ జనరేట్ చేయి")
            
        if submit:
            if product_name:
                payload = {
                    "username": st.session_state['username'],
                    "product_name": product_name,
                    "category": category,
                    "target_audience": target_audience,
                    "affiliate_link": affiliate_link,
                    "content_type": content_type
                }
                with st.spinner("ఏఐ కంటెంట్‌ను తయారు చేస్తోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/generate-content", json=payload)
                        if res.status_code == 200:
                            data = res.json()["generated_content"]
                            st.success("కంటెంట్ విజయవంతంగా తయారైంది మరియు మీ అకౌంట్‌లో సేవ్ చేయబడింది! 👇")
                            
                            for k, v in data.items():
                                st.subheader(f"📌 {k.capitalize()}")
                                st.write(v)
                        else:
                            st.error("జెనరేషన్‌లో లోపం ఏర్పడింది.")
                    except Exception as e:
                        st.error(f"సర్వర్ కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("దయచేసి ప్రొడక్ట్ పేరు ఎంటర్ చేయండి.")

    elif menu == "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్":
        st.title("📡 సోషల్ మీడియా ఆటో-పబ్లిషింగ్ సెంటర్")
        st.write("జనరేట్ చేసిన మార్కెటింగ్ కంటెంట్‌ను ఒక్క క్లిక్‌తో ఇన్‌స్టాగ్రామ్ మరియు వాట్సాప్‌కి ఆటోమేటిక్‌గా పంపండి!")

        with st.form("auto_form"):
            p_name = st.text_input("ప్రొడక్ట్ పేరు:")
            caption = st.text_area("పోస్ట్ క్యాప్షన్ / మెసేజ్ టెక్స్ట్:")
            link = st.text_input("அఫిలియేట్ లింక్ (Affiliate Link):")
            
            platforms = st.multiselect("ప్లాట్‌ఫామ్స్ ఎంచుకోండి:", ["Instagram", "WhatsApp"])
            phone = st.text_input("వాట్సాప్ నంబర్ (దేశ కోడ్‌తో సహా ఇవ్వండి, ఉదా: +919876543210):")
            
            pub_btn = st.form_submit_button("ఆటోమేటిక్‌గా పబ్లిష్ చేయి (Auto-Publish)")

        if pub_btn:
            if p_name and caption and platforms:
                payload = {
                    "product_name": p_name,
                    "caption": caption,
                    "affiliate_link": link,
                    "target_platforms": platforms,
                    "recipient_phone": phone
                }
                with st.spinner("సోషల్ మీడియా మరియు వాట్సాప్‌కి పోస్ట్ అవుతోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/auto-publish", json=payload)
                        if res.status_code == 200:
                            res_data = res.json().get("publish_results", {})
                            st.success("ఆటో-పబ్లిషింగ్ ప్రాసెస్ పూర్తయింది!")
                            for plat, msg in res_data.items():
                                st.info(f"**{plat}:** {msg}")
                        else:
                            st.error("పబ్లిషింగ్ విఫలమైంది.")
                    except Exception as e:
                        st.error(f"కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("దయచేసి అన్ని వివరాలు సరిగ్గా నింపండి.")

    elif menu == "🔥 ట్రెండింగ్ ప్రొడక్ట్స్ & AI లింక్స్":
        st.title("🔥 ట్రెండింగ్ ప్రొడక్ట్స్ & బెస్ట్ అఫిలియేట్ ఆఫర్స్")
        st.write("ప్రస్తుతం మార్కెట్‌లో అత్యధిక కమిషన్ మరియు డిమాండ్ ఉన్న ప్రొడక్ట్స్:")

        trending_items = [
            {"name": "ఆర్గానిక్ మిల్లెట్ స్నాక్స్ ప్యాక్", "category": "ఆర్గానిక్ & ఫుడ్", "commission": "12%", "demand": "చాలా ఎక్కువ"},
            {"name": "స్మార్ట్ ఫిట్‌నెస్ వాచ్", "category": "ఎలక్ట్రానిక్స్", "commission": "8%", "demand": "అధికం"},
            {"name": "పోర్టబుల్ వైర్‌లెస్ ఇయర్ బడ్స్", "category": "ఎలక్ట్రానిక్స్", "commission": "10%", "demand": "అధికం"},
            {"name": "హెర్బల్ స్కిన్ కేర్ కిట్", "category": "హెల్త్ & ఫిట్‌నెస్", "commission": "15%", "demand": "మధ్యస్థం"}
        ]

        for item in trending_items:
            with st.expander(f"🌟 {item['name']} ({item['category']})"):
                st.write(f"**కమిషన్ రేటు:** {item['commission']}")
                st.write(f"**మార్కెట్ డిమాండ్:** {item['demand']}")
                st.info("ఈ ప్రొడక్ట్‌ని మీ అఫిలియేట్ లింక్‌తో కనెక్ట్ చేసి నేరుగా వాట్సాప్/ఇన్‌స్టాగ్రామ్‌లో ప్రమోట్ చేసుకోవచ్చు!")

    elif menu == "📊 అనలిటిక్స్ & ఎర్నింగ్స్ డ్యాష్‌బోర్డ్":
        st.title("📊 డ్యాష్‌బోర్డ్ మరియు సంపాదన ట్రాకింగ్")
        
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                analytics = data["analytics"]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("మొత్తం క్లిక్స్ (Clicks)", analytics["clicks"], "+14 ఈ వారం")
                c2.metric("సఫలమైన సేల్స్ (Conversions)", analytics["conversions"], "+3")
                c3.metric("మొత్తం సంపాదన ($)", f"$ {analytics['earnings']}", "+$ 12.50")
                
                st.markdown("---")
                st.subheader("📁 మీ సేవ్ చేసిన మార్కెటింగ్ క్యాంపెయిన్స్")
                campaigns = data["campaigns"]
                if len(campaigns) == 0:
                    st.info("ఇതുవరకు ఎలాంటి క్యాంపెయిన్స్ సేవ్ చేయలేదు. జనరేటర్ ద్వారా క్యాంపెయిన్స్ సృష్టించండి.")
                else:
                    for camp in campaigns:
                        with st.expander(f"ప్రొడక్ట్: {camp['product']} ({camp['category']})"):
                            st.write(f"**అఫిలియేట్ లింక్:** {camp['link']}")
                            st.text(camp['content'])
        except Exception as e:
            st.error(f"డేటా లోడ్ చేయడంలో లోపం: {str(e)}")

    elif menu == "💎 SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్":
        st.title("💎 MetaPost AI - సబ్‌స్క్రిప్షన్ ప్లాన్స్")
        st.write("అధికారిక ఏఐ ఫీచర్లు, అన్లిమిటెడ్ ఆటోమేషన్ మరియు అడ్వాన్స్డ్ అనలిటిక్స్ కోసం తగిన ప్లాన్‌ను ఎంచుకోండి:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("ఫ్రీ ప్లాన్ (Free)")
            st.markdown("**₹ 0 / నెల**")
            st.markdown("- రోజుకు 5 యాడ్ కాపీలు")
            st.markdown("- బేసిక్ టెంప్లేట్లు")
            st.button("ప్రస్తుత ప్లాన్", disabled=True, key="free")
            
        with col2:
            st.subheader("ప్రో ప్లాన్ (Pro)")
            st.markdown("**₹ 799 / నెల**")
            st.markdown("- అన్లిమిటెడ్ యాడ్ కాపీలు & బ్లాగ్స్")
            st.markdown("- ఇన్‌స్టాగ్రామ్ & వాట్సాప్ ఆటో-పబ్లిషింగ్")
            st.markdown("- ప్రయారిటీ సపోర్ట్")
            st.button("ప్రో ప్లాన్‌కు అప్‌గ్రేడ్ చేయి", key="pro")
            
        with col3:
            st.subheader("బిజినెస్ ప్లాన్ (Business)")
            st.markdown("**₹ 1,999 / నెల**")
            st.markdown("- టీమ్ యాక్సెస్ & అడ్వాన్స్డ్ ఆటోమేషన్")
            st.markdown("- పూర్తి సోషల్ మీడియా షెడ్యూలింగ్")
            st.markdown("- అంకితమైన సపోర్ట్")
            st.button("బిజినెస్ ప్లాన్ తీసుకోండి", key="biz")

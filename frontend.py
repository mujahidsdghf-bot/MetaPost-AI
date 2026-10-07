import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Pro - AI Image & Video Suite", page_icon="🎨", layout="wide")

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
    st.title("🎨 MetaPost AI Pro - ఫోటో, వీడియో & మార్కెటింగ్ సూట్")
    st.write("హోటల్, రెస్టారెంట్, మెనూ లేదా బిజినెస్ ఫోటో అప్‌లోడ్ చేయండి — ఏఐ ద్వారా అద్భుతమైన ప్రమోషనల్ ఇమేజ్ బ్యానర్ మరియు వీడియో స్క్రిప్ట్ పొందండి!")
    
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
            s_pass = st.text_input("కొత్త पासवर्ड (Password)", type="password")
            s_submit = st.form_submit_button("ఖాతా సృష్టించు")
            
            if s_submit:
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
                    if res.status_code == 200:
                        st.success("ఖాతా తయారైంది! లాగిన్ అవ్వండి.")
                    else:
                        st.error("ఈ యూజర్ పేరు ఇప్పటికే ఉంది.")
                except Exception as e:
                    st.error(f"సర్వర్ కనెక్షన్ లోపం: {str(e)}")

else:
    st.sidebar.title(f"స్వాగతం, 👋")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    
    menu = st.sidebar.selectbox("ప్రధాన మెను (Menu)", [
        "🎨 AI ఇమేజ్, వీడియో & క్యాప్షన్ జనరేటర్", 
        "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్", 
        "📊 అనలిటిక్స్ & క్యాంపెయిన్స్", 
        "🚪 లాగౌట్"
    ])
    
    if menu == "🚪 లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "🎨 AI ఇమేజ్, వీడియో & క్యాప్షన్ జనరేటర్":
        st.title("🎨 AI ప్రొఫెషనల్ ఇమేజ్, వీడియో స్క్రిప్ట్ & పోస్ట్ జెనరేటర్")
        st.write("మీ రెస్టారెంట్, హోటల్ లేదా బిజినెస్ ఫోటో అప్‌లోడ్ చేయండి లేదా పేరు ఇవ్వండి—ఏఐ అద్భుతమైన డిజైన్ పోస్ట్ మరియు స్క్రిప్ట్ తయారు చేస్తుంది!")

        with st.form("media_gen_form"):
            mode = st.selectbox("బిజినెస్ రకం:", ["హోటల్ / రెస్టారెంట్ (Hotel / Restaurant)", "మెనూ ప్రమోషన్ (Menu)", "స్వంత బిజినెస్ (Business)", "అఫిలియేట్ మార్కెటింగ్"])
            
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("బిజినెస్ / హోటల్ పేరు:", placeholder="ఉదా: Grand Dine Restaurant")
                product_url = st.text_input("వెబ్‌సైట్ లేదా లొకేషన్ లింక్ (Optional):", placeholder="https://yourwebsite.com")
            with col2:
                target_audience = st.text_input("టార్గెట్ ఆడియెన్స్:", placeholder="ఉదా: ఫుడ్ లవర్స్, ఫ్యామిలీస్")
            
            uploaded_image = st.file_uploader("📸 ఫోటో అప్‌లోడ్ చేయండి (మెనూ, హోటల్ లేదా ప్రొడక్ట్ ఫోటో):", type=["jpg", "png", "jpeg"])
            
            submit = st.form_submit_button("AI ఇమేజ్ & వీడియో కంటెంట్ జనరేట్ చేయి")
            
        if submit:
            if business_name:
                files = {"image": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)} if uploaded_image else None
                data = {
                    "username": st.session_state['username'],
                    "mode": mode,
                    "business_name": business_name,
                    "target_audience": target_audience,
                    "product_url": product_url
                }
                
                with st.spinner("ఏఐ ఫోటోను విశ్లేషించి ప్రమోషనల్ ఇమేజ్ మరియు వీడియో స్క్రిప్ట్ తయారు చేస్తోంది..."):
                    try:
                        res = requests.post(f"{BACKEND_URL}/generate-media-content", data=data, files=files)
                        if res.status_code == 200:
                            res_json = res.json()
                            data_content = res_json["generated_content"]
                            st.success("అద్భుతమైన మార్కెటింగ్ కంటెంట్ మరియు విజువల్ తయారైంది! 👇")
                            
                            # 1. AI జనరేటెడ్ ఇమేజ్ / బ్యానర్ డిస్‌ప్లే చేయడం
                            st.subheader("🖼️ AI జనరేటెడ్ ప్రమోషనల్ బ్యానర్ / ఇమేజ్:")
                            st.image(data_content["ai_image_url"], caption=f"{business_name} - AI Promo Banner", use_container_width=True)
                            
                            # 2. క్యాప్షన్ మరియు వీడియో స్క్రిప్ట్ డిస్‌ప్లే చేయడం
                            st.subheader("📌 సోషల్ మీడియా యాడ్ క్యాప్షన్")
                            st.write(data_content["caption"])
                            
                            st.subheader("🎬 రీల్ / వీడియో స్క్రిప్ట్")
                            st.write(data_content["video_script"])
                        else:
                            st.error("జెనరేషన్‌లో లోపం ఏర్పడింది.")
                    except Exception as e:
                        st.error(f"సర్వర్ కనెక్షన్ ఎర్రర్: {str(e)}")
            else:
                st.warning("దయచేసి బిజినెస్ పేరు ఎంటర్ చేయండి.")

    elif menu == "📡 Meta & WhatsApp ఆటో-పబ్లిషింగ్":
        st.title("📡 సోషల్ మీడియా ఆటో-పబ్లిషింగ్ సెంటర్")
        
        with st.form("auto_form"):
            b_name = st.text_input("బిజినెస్ పేరు:")
            caption = st.text_area("పోస్ట్ క్యాప్షన్ టెక్స్ట్:")
            
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

    elif menu == "📊 అనలిటిక్స్ & క్యాంపెయిన్స్":
        st.title("📊 మీ క్యాంపెయిన్స్ మరియు ట్రాకింగ్")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                c1, c2, c3 = st.columns(3)
                c1.metric("మొత్తం రీచ్", data["analytics"]["clicks"])
                c2.metric("లీడ్స్ / బుకింగ్స్", data["analytics"]["conversions"])
                c3.metric("సంపాదన ($)", f"$ {data['analytics']['earnings']}")
                
                st.markdown("---")
                st.subheader("📁 సేవ్ చేసిన క్యాంపెయిన్స్")
                for camp in data["campaigns"]:
                    st.write(f"- **బిజినెస్:** {camp['business']} | **మోడ్:** {camp['mode']}")
        except:
            st.error("డేటా లోడ్ చేయడంలో లోపం.")

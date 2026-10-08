import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Ultimate Pro", page_icon="🚀", layout="wide")

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
    st.title("🚀 MetaPost AI Ultimate Pro - లాగిన్ సూట్")
    tab1, tab2 = st.tabs(["లాగిన్ (Login)", "కొత్త ఖాతా (Sign Up)"])
    
    with tab1:
        with st.form("login_form"):
            l_user = st.text_input("యూజర్ పేరు / మెయిల్ ఐడి")
            l_pass = st.text_input("పాస్‌వర్డ్", type="password")
            if st.form_submit_button("లాగిన్ అవ్వండి"):
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
            if st.form_submit_button("ఖాతా సృష్టించు"):
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
    
    # మీరు కోరిన అన్ని ఆప్షన్‌లు ఇక్కడ ఉన్నాయి
    menu = st.sidebar.selectbox("ప్రధాన మెను (Menu)", [
        "1️⃣ అఫిలియేట్ మార్కెటింగ్", 
        "2️⃣ బిజినెస్ & ఆటో యాడ్స్ (లింక్/ఫోటోలు)", 
        "3️⃣ సోషల్ మీడియా వీడియోలు (ఇన్‌కమ్ కోసం)", 
        "4️⃣ సబ్‌స్క్రిప్షన్ ప్లాన్స్", 
        "⚙️ సెట్టింగ్స్ & అనలిటిక్స్",
        "🚪 లాగౌట్"
    ])
    
    if menu == "🚪 లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "1️⃣ అఫిలియేట్ మార్కెటింగ్":
        st.title("💼 అఫిలియేట్ మార్కెటింగ్ కంటెంట్ జనరేటర్")
        st.write("అఫిలియేట్ ప్రొడక్ట్స్ ప్రమోట్ చేయడానికి ఆకర్షణీయమైన పోస్టులు మరియు బ్యానర్లు సృష్టించండి!")
        
        with st.form("aff_form"):
            t_name = st.text_input("ప్రొడక్ట్ పేరు:")
            desc = st.text_area("ప్రొడక్ట్ వివరాలు / ఆఫర్:")
            link = st.text_input("అఫిలియేట్ లింక్:")
            submitted = st.form_submit_button("అఫిలియేట్ కంటెంట్ జనరేట్ చేయి")
            
            if submitted:
                if t_name:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "అఫిలియేట్ మార్కెటింగ్",
                        "title_name": t_name,
                        "description_text": desc,
                        "link_url": link
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("విజయవంతంగా తయారైంది!")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.write(res_json["content"])
                else:
                    st.warning("దయచేసి ప్రొడక్ట్ పేరు ఇవ్వండి.")

    elif menu == "2️⃣ బిజినెస్ & ఆటో యాడ్స్ (లింక్/ఫోటోలు)":
        st.title("🚀 బిజినెస్ & ఆటో యాడ్స్ డెవలప్‌మెంట్")
        st.write("మీ హోటల్, రెస్టారెంట్ లేదా స్వంత బిజినెస్ కోసం ఫోటోలు లేదా వెబ్‌సైట్ లింక్‌తో ఆటో యాడ్స్ సృష్టించండి!")
        
        with st.form("biz_form"):
            b_name = st.text_input("బిజినెస్ / హోటల్ పేరు:")
            b_desc = st.text_area("ఆఫర్ లేదా సర్వీస్ వివరాలు:")
            b_link = st.text_input("వెబ్‌సైట్ లేదా లొకేషన్ లింక్:")
            up_img = st.file_uploader("ఫోటో లేదా మెనూ అప్‌లోడ్ చేయండి:", type=["jpg", "png", "jpeg"])
            submitted = st.form_submit_button("బిజినెస్ యాడ్ జనరేట్ చేయి")
            
            if submitted:
                if b_name:
                    files = {"image": (up_img.name, up_img.getvalue(), up_img.type)} if up_img else None
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "బిజినెస్ & ఆటో యాడ్స్",
                        "title_name": b_name,
                        "description_text": b_desc,
                        "link_url": b_link
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data, files=files)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("బిజినెస్ యాడ్ తయారైంది!")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.write(res_json["content"])
                else:
                    st.warning("దయచేసి బిజినెస్ పేరు ఇవ్వండి.")

    elif menu == "3️⃣ సోషల్ మీడియా వీడియోలు (ఇన్‌కమ్ కోసం)":
        st.title("🎬 సోషల్ మీడియా వీడియోలు & మానిటైజేషన్")
        st.write("YouTube Shorts మరియు Instagram Reels కోసం వైరల్ వీడియో స్క్రిప్ట్స్ సృష్టించి వ్యూస్ & సబ్‌స్క్రిప్ర్స్ ద్వారా ఆదాయం పొందండి!")
        
        with st.form("vid_form"):
            v_title = st.text_input("వీడియో టాపిక్ / ప్రొడక్ట్ పేరు:")
            v_desc = st.text_input("వీడియో హుక్ లేదా ప్రధాన పాయింట్:")
            submitted = st.form_submit_button("వైరల్ వీడియో స్క్రిప్ట్ జనరేట్ చేయి")
            
            if submitted:
                if v_title:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "సోషల్ మీడియా వీడియోలు",
                        "title_name": v_title,
                        "description_text": v_desc
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("వీడియో స్క్రిప్ట్ తయారైంది!")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.write(res_json["content"])
                else:
                    st.warning("దయచేసి వీడియో టాపిక్ ఇవ్వండి.")

    elif menu == "4️⃣ సబ్‌స్క్రిప్షన్ ప్లాన్స్":
        st.title("💎 MetaPost AI - సబ్‌స్క్రిప్షన్ ప్లాన్స్")
        st.write("అడ్వాన్స్డ్ ఫీచర్లు మరియు అన్లిమిటెడ్ ఆటోమేషన్ కోసం తగిన ప్లాన్‌ను ఎంచుకోండి:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("ఫ్రీ ప్లాన్")
            st.markdown("**₹ 0 / నెల**")
            st.markdown("- బేసిక్ టెంప్లేట్లు")
            st.button("ప్రస్తుత ప్లాన్", disabled=True)
        with c2:
            st.subheader("ప్రో ప్లాన్")
            st.markdown("**₹ 799 / నెల**")
            st.markdown("- అన్లిమిటెడ్ యాడ్స్ & వీడియో స్క్రిప్ట్స్")
            st.button("ప్రో ప్లాన్ తీసుకును", key="p_btn")
        with c3:
            st.subheader("బిజినెస్ ప్లాన్")
            st.markdown("**₹ 1,999 / నెల**")
            st.markdown("- పూర్తి బిజినెస్ ఆటోమేషన్ & సపోర్ట్")
            st.button("బిజినెస్ ప్లాన్ తీసుకును", key="b_btn")

    elif menu == "⚙️ సెట్టింగ్స్ & అనలిటిక్స్":
        st.title("⚙️ సెట్టింగ్స్ మరియు అనలిటిక్స్ డ్యాష్‌బోర్డ్")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                analytics = data["analytics"]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("మొత్తం రీచ్ / క్లిక్స్", analytics["clicks"])
                c2.metric("సఫలమైన క్యాంపెయిన్స్", len(data["campaigns"]))
                c3.metric("మొత్తం సంపాదన ($)", f"$ {analytics['earnings']}")
                
                st.markdown("---")
                st.subheader("📁 మీ సేవ్ చేసిన క్యాంపెయిన్స్")
                for camp in data["campaigns"]:
                    st.write(f"- **టైప్:** {camp['type']} | **పేరు:** {camp['name']}")
        except Exception as e:
            st.error("అనలిటిక్స్ లోడ్ చేయడంలో లోపం.")

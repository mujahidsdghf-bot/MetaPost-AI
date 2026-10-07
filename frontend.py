import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"  # మీ బ్యాక్‌ఎండ్ రెండర్ లింక్ ఇక్కడ ఇవ్వండి

st.set_page_config(page_title="AI Affiliate & Auto-Marketing Platform", page_icon="🚀", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# లాగిన్ / సైన్ అప్ పేజీ
if not st.session_state['logged_in']:
    st.title("🔐 AI మార్కెటింగ్ ప్లాట్‌ఫాం - లాగిన్ / సైన్ అప్")
    tab1, tab2 = st.tabs(["లాగిన్", "కొత్త ఖాతా"])
    
    with tab1:
        l_user = st.text_input("యూజర్ పేరు", key="l_user")
        l_pass = st.text_input("పాస్‌వర్డ్", type="password", key="l_pass")
        if st.button("లాగిన్ అవ్వండి"):
    try:
        res = requests.post(f"{BACKEND_URL}/login", json={"username": l_user, "password": l_pass})
        if res.status_code == 200:
            st.session_state['logged_in'] = True
            st.session_state['username'] = l_user
            st.success("లాగిన్ విజయవంతమైంది!")
            st.rerun()
        else:
            # సేఫ్ గా ఎర్రర్ హ్యాండిల్ చేయడం
            try:
                err_msg = res.json().get("detail", "లాగిన్ విఫలమైంది.")
            except:
                err_msg = f"సర్వర్ ఎర్రర్ (Status Code: {res.status_code})"
            st.error(err_msg)
    except Exception as e:
        st.error(f"సర్వర్ కనెక్షన్ విఫలమైంది: {str(e)}")
                
    with tab2:
        s_user = st.text_input("కొత్త యూజర్ పేరు", key="s_user")
        s_pass = st.text_input("కొత్త పాస్‌వర్డ్", type="password", key="s_pass")
        if st.button("ఖాతా సృష్టించు"):
    try:
        res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
        if res.status_code == 200:
            st.success("ఖాతా తయారైంది! ఇప్పుడు లాగిన్ అవ్వండి.")
        else:
            try:
                err_msg = res.json().get("detail", "ఎర్రర్ వచ్చింది.")
            except:
                err_msg = f"సర్వర్ ఎర్రర్ (Status Code: {res.status_code})"
            st.error(err_msg)
    except Exception as e:
        st.error(f"సర్వర్ కనెక్షన్ విఫలమైంది: {str(e)}")

# మెయిన్ యాప్ (లాగిన్ అయ్యాక)
else:
    st.sidebar.title(f"స్వాగతం, 👋 {st.session_state['username']}")
    menu = st.sidebar.selectbox("మెను", [
        "కంటెంట్ జనరేటర్", 
        "ఆటో-పబ్లిషింగ్ (Meta & WhatsApp)", 
        "ట్రెండింగ్ ప్రొడక్ట్స్", 
        "డ్యాష్‌బోర్డ్ & ట్రాకింగ్", 
        "SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్", 
        "లాగౌట్"
    ])
    
    if menu == "లాగౌట్":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "కంటెంట్ జనరేటర్":
        st.title("🚀 AI ప్రొడక్ట్, యాడ్ కాపీ & బ్లాగ్ జనరేటర్")
        
        with st.form("gen_form"):
            col1, col2 = st.columns(2)
            with col1:
                product_name = st.text_input("ప్రొడక్ట్ పేరు:")
                category = st.selectbox("కేటగిరీ:", ["ఎలక్ట్రానిక్స్", "ఆర్గానిక్ & ఫుడ్", "ఫ్యాషన్", "హెల్త్ & ఫిట్‌నెస్"])
            with col2:
                target_audience = st.text_input("టార్గెట్ ఆడియెన్స్:")
                affiliate_link = st.text_input("అఫిలియేట్ లింక్:")
            
            content_type = st.multiselect("కావలసినవి:", ["సోషల్ మీడియా యాడ్ క్యాప్షన్", "ప్రొడక్ట్ డిస్క్రిప్షన్", "పూర్తి బ్లాగ్ ఆర్టికల్"], default=["సోషల్ మీడియా యాడ్ క్యాప్షన్"])
            submit = st.form_submit_button("కంటెంట్ జనరేట్ చేయి")
            
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
                res = requests.post(f"{BACKEND_URL}/generate-content", json=payload)
                if res.status_code == 200:
                    data = res.json()["generated_content"]
                    st.success("కంటెంట్ విజయవంతంగా జనరేట్ అయి సేవ్ చేయబడింది!")
                    for k, v in data.items():
                        st.subheader(k.capitalize())
                        st.write(v)
                else:
                    st.error("జెనరేషన్‌లో లోపం ఏర్పడింది.")
            else:
                    st.warning("దయచేసి ప్రొడక్ట్ పేరు ఎంటర్ చేయండి.")

    elif menu == "ఆటో-పబ్లిషింగ్ (Meta & WhatsApp)":
        st.title("📡 సోషల్ మీడియా ఆటో-పబ్లిషింగ్ సెంటర్")
        st.write("తయారైన మార్కెటింగ్ కంటెంట్‌ను నేరుగా ఇన్‌స్టాగ్రామ్ మరియు వాట్సాప్‌కి పంపండి!")

        with st.form("auto_form"):
            p_name = st.text_input("ప్రొడక్ట్ పేరు:")
            caption = st.text_area("పోస్ట్ క్యాప్షన్ / మెసేజ్ టెక్స్ట్:")
            link = st.text_input("అఫిలియేట్ లింక్:")
            
            platforms = st.multiselect("ప్లాట్‌ఫామ్స్ ఎంచుకోండి:", ["Instagram", "WhatsApp"])
            phone = st.text_input("వాట్సాప్ నంబర్ (WhatsApp కి పంపాలంటే ఇది నింపండి, ఉదా: +919876543210):")
            
            pub_btn = st.form_submit_button("ఆటోమేటిక్‌గా పబ్లిష్ చేయి")

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
                    res = requests.post(f"{BACKEND_URL}/auto-publish", json=payload)
                    if res.status_code == 200:
                        res_data = res.json().get("publish_results", {})
                        st.success("ప్రాసెస్ పూర్తయింది!")
                        for plat, msg in res_data.items():
                            st.info(f"**{plat}:** {msg}")
                    else:
                        st.error("ఆటో-పబ్లిషింగ్ విఫలమైంది.")
            else:
                st.warning("అన్ని వివరాలు సరిగ్గా నింపండి.")

    elif menu == "ట్రెండింగ్ ప్రొడక్ట్స్":
        st.title("🔥 ట్రెండింగ్ ప్రొడక్ట్స్ & అఫిలియేట్ రికమండేషన్స్")
        trending_items = [
            {"name": "ఆర్గానిక్ మిల్లెట్ స్నాక్స్ ప్యాక్", "category": "ఆర్గానిక్ & ఫుడ్", "commission": "12%"},
            {"name": "స్మార్ట్ ఫిట్‌నెస్ వాచ్", "category": "ఎలక్ట్రానిక్స్", "commission": "8%"},
            {"name": "హెర్బల్ స్కిన్ కేర్ కిట్", "category": "హెల్త్ & ఫిట్‌నెస్", "commission": "15%"}
        ]
        for item in trending_items:
            st.info(f"🌟 **{item['name']}** | కేటగిరీ: {item['category']} | కమిషన్ రేటు: **{item['commission']}**")

    elif menu == "డ్యాష్‌బోర్డ్ & ట్రాకింగ్":
        st.title("📊 డ్యాష్‌బోర్డ్ మరియు అనలిటిక్స్")
        res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
        if res.status_code == 200:
            data = res.json()
            analytics = data["analytics"]
            
            c1, c2, c3 = st.columns(3)
            c1.metric("మొత్తం క్లిక్స్", analytics["clicks"])
            c2.metric("సఫలమైన సేల్స్", analytics["conversions"])
            c3.metric("మొత్తం సంపాదన ($)", analytics["earnings"])
            
            st.subheader("📁 మీ సేవ్ చేసిన క్యాంపెయిన్స్")
            for camp in data["campaigns"]:
                st.write(f"- **ప్రొడక్ట్:** {camp['product']} | **లింక్:** {camp['link']}")

    elif menu == "SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్":
        st.title("💎 SaaS సబ్‌స్క్రిప్షన్ ప్లాన్స్")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("ఫ్రీ ప్లాన్")
            st.write("₹ 0 / నెల - బేసిక్ ఫీచర్లు")
        with col2:
            st.subheader("ప్రో ప్లాన్")
            st.write("₹ 799 / నెల - అన్లిమిటెడ్ ఆటోమేషన్")
        with col3:
            st.subheader("బిజినెస్ ప్లాన్")
            st.write("₹ 1,999 / నెల - అడ్వాన్స్డ్ ఏఐ & సపోర్ట్")

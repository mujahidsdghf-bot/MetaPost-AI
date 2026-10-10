import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Professional Suite", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #07090e; color: #f3f4f6; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); color: white; font-weight: bold; border: none; padding: 12px; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4); }
    .stButton>button:hover { background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("🎬 MetaPost AI Professional Studio - Login")
    st.write("Advanced AI Video Generation & Automated Marketing Platform.")
    
    tab1, tab2 = st.tabs(["Sign In", "Register"])
    
    with tab1:
        with st.form("login_form"):
            l_user = st.text_input("Username / Email ID")
            l_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                try:
                    res = requests.post(f"{BACKEND_URL}/login", json={"username": l_user, "password": l_pass})
                    if res.status_code == 200:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = l_user
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
    with tab2:
        with st.form("signup_form"):
            s_user = st.text_input("Email / Username")
            s_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Create Account"):
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
                    if res.status_code == 200:
                        st.success("Account created! Please sign in.")
                    else:
                        st.error("Username already exists.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.sidebar.title(f"Welcome, 👋")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    
    selected_lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Telugu", "Hindi", "Spanish", "French", "Arabic"])
    selected_duration = st.sidebar.selectbox("⏱️ AI Video Duration", ["2 Minutes", "3 Minutes", "5 Minutes", "10 Minutes"])
    
    menu = st.sidebar.selectbox("Studio Menu", [
        "1️⃣ Affiliate Marketing AI Suite", 
        "2️⃣ Business & Auto Ads Studio", 
        "3️⃣ Cinematic AI Video Generator", 
        "4️⃣ Meta & WhatsApp Auto-Publishing",
        "5️⃣ SaaS Subscription Tiers", 
        "⚙️ Analytics & Settings",
        "🚪 Logout"
    ])
    
    if menu == "🚪 Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "1️⃣ Affiliate Marketing AI Suite":
        st.title("💼 Affiliate Marketing AI Video & Banner Studio")
        
        with st.form("aff_form"):
            t_name = st.text_input("Product Name:")
            desc = st.text_area("Product Details:")
            link = st.text_input("Affiliate Link:")
            submitted = st.form_submit_button("Generate AI Video & Banner")
            
            if submitted:
                if t_name:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Affiliate Marketing",
                        "title_name": t_name,
                        "description_text": desc,
                        "link_url": link,
                        "language": selected_lang,
                        "video_duration": selected_duration
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("AI Package Generated Successfully!")
                        
                        st.subheader(f"🖼️ AI Generated Poster for {t_name}:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Poster]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎬 AI Cinematic {selected_duration} Video (Play & Download):")
                        st.markdown(f'''
                            <video width="100%" controls playsinline style="border-radius: 10px;">
                              <source src="{res_json["video_url"]}" type="video/mp4">
                              Your browser does not support the video tag.
                            </video>
                        ''', unsafe_allow_html=True)
                        st.markdown(f"[📥 Download MP4 Video File]({res_json['video_url']})")
                        
                        st.subheader("📌 Marketing Caption")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter product name.")

    elif menu == "2️⃣ Business & Auto Ads Studio":
        st.title("🚀 Business & Auto Ads AI Studio")
        
        with st.form("biz_form"):
            b_name = st.text_input("Business / Brand Name:")
            b_desc = st.text_area("Service Description:")
            b_link = st.text_input("Website Link:")
            
            submitted = st.form_submit_button("Generate Business AI Ad")
            
            if submitted:
                if b_name:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Business & Auto Ads",
                        "title_name": b_name,
                        "description_text": b_desc,
                        "link_url": b_link,
                        "language": selected_lang,
                        "video_duration": selected_duration
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("Business AI Ad Generated!")
                        
                        st.subheader("🖼️ AI Generated Business Poster:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Poster]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎬 AI Ad Video ({selected_duration}):")
                        st.markdown(f'''
                            <video width="100%" controls playsinline style="border-radius: 10px;">
                              <source src="{res_json["video_url"]}" type="video/mp4">
                              Your browser does not support the video tag.
                            </video>
                        ''', unsafe_allow_html=True)
                        st.markdown(f"[📥 Download MP4 Video File]({res_json['video_url']})")
                        
                        st.subheader("📌 Ad Copy")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter business name.")

    elif menu == "3️⃣ Cinematic AI Video Generator":
        st.title(f"🎬 Cinematic AI Video Generator ({selected_duration})")
        
        with st.form("vid_form"):
            v_title = st.text_input("Video Topic / Category:")
            v_desc = st.text_input("Video Storyline / Prompt:")
            submitted = st.form_submit_button(f"Generate {selected_duration} Cinematic Video")
            
            if submitted:
                if v_title:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Social Media Videos",
                        "title_name": v_title,
                        "description_text": v_desc,
                        "language": selected_lang,
                        "video_duration": selected_duration
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success(f"Cinematic {selected_duration} Video Ready!")
                        
                        st.subheader("🖼️ AI Thumbnail:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Thumbnail]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎥 Preview & Download {selected_duration} Video:")
                        st.markdown(f'''
                            <video width="100%" controls playsinline style="border-radius: 10px;">
                              <source src="{res_json["video_url"]}" type="video/mp4">
                              Your browser does not support the video tag.
                            </video>
                        ''', unsafe_allow_html=True)
                        st.markdown(f"[📥 Download MP4 Video File]({res_json['video_url']})")
                        
                        st.subheader("📝 Production Guide")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter video topic.")

    elif menu == "4️⃣ Meta & WhatsApp Auto-Publishing":
        st.title("📡 Meta & WhatsApp Auto-Publishing Studio")
        
        with st.form("auto_pub_form"):
            b_name = st.text_input("Business Name:")
            caption = st.text_area("Caption / Message:")
            platforms = st.multiselect("Platforms:", ["Facebook (Meta)", "Instagram", "WhatsApp"])
            phone = st.text_input("WhatsApp Number (with country code):")
            pub_btn = st.form_submit_button("Publish Now")
            
            if pub_btn:
                if b_name and caption and platforms:
                    payload = {
                        "business_name": b_name,
                        "caption": caption,
                        "target_platforms": platforms,
                        "recipient_phone": phone
                    }
                    res = requests.post(f"{BACKEND_URL}/auto-publish", json=payload)
                    if res.status_code == 200:
                        res_data = res.json().get("publish_results", {})
                        st.success("Published successfully!")
                        for plat, msg in res_data.items():
                            st.info(f"**{plat}:** {msg}")
                    else:
                        st.error("Publishing failed.")
                else:
                    st.warning("Please fill in all required fields.")

    elif menu == "5️⃣ SaaS Subscription Tiers":
        st.title("💎 SaaS Tiers")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Free")
            st.button("Active", disabled=True)
        with c2:
            st.subheader("Pro")
            st.button("Upgrade", key="p_btn")
        with c3:
            st.subheader("Enterprise")
            st.button("Get Started", key="e_btn")

    elif menu == "⚙️ Analytics & Settings":
        st.title("⚙️ Analytics Dashboard")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                analytics = data["analytics"]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Reach", analytics["clicks"])
                c2.metric("Campaigns", len(data["campaigns"]))
                c3.metric("Earnings ($)", f"$ {analytics['earnings']}")
        except Exception as e:
            st.error("Error loading analytics.")

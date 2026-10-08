import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Ultimate Pro - Official Suite", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; font-weight: bold; border: none; padding: 12px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4); }
    .stButton>button:hover { background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%); }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("⚡ MetaPost AI Ultimate Pro - Official Portal")
    st.write("Welcome to the next-generation AI marketing, video generation, and auto-publishing suite.")
    
    tab1, tab2 = st.tabs(["Secure Login", "Create New Account"])
    
    with tab1:
        with st.form("login_form"):
            l_user = st.text_input("Username / Email ID")
            l_pass = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                try:
                    res = requests.post(f"{BACKEND_URL}/login", json={"username": l_user, "password": l_pass})
                    if res.status_code == 200:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = l_user
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                
    with tab2:
        with st.form("signup_form"):
            s_user = st.text_input("New Email / Username")
            s_pass = st.text_input("New Password", type="password")
            if st.form_submit_button("Register Account"):
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={"username": s_user, "password": s_pass})
                    if res.status_code == 200:
                        st.success("Account created successfully! Please sign in.")
                    else:
                        st.error("Username already exists.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

else:
    st.sidebar.title(f"Welcome, 👋")
    st.sidebar.markdown(f"**{st.session_state['username']}**")
    
    selected_lang = st.sidebar.selectbox("🌐 Select Output Language", ["English", "Telugu", "Hindi", "Spanish", "French", "Arabic"])
    selected_duration = st.sidebar.selectbox("⏱️ Select AI Video Duration", ["2 Minutes", "3 Minutes", "5 Minutes", "10 Minutes"])
    
    menu = st.sidebar.selectbox("Main Dashboard Menu", [
        "1️⃣ Affiliate Marketing Suite (Video & Ad)", 
        "2️⃣ Business & Auto Ads (Link/Photos/Videos/Create AI)", 
        "3️⃣ Social Media Videos & Download", 
        "4️⃣ Meta & WhatsApp Auto-Publishing",
        "5️⃣ SaaS Subscription Plans", 
        "⚙️ Analytics & Settings",
        "🚪 Logout"
    ])
    
    if menu == "🚪 Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "1️⃣ Affiliate Marketing Suite (Video & Ad)":
        st.title("💼 Affiliate Marketing Content, Banner & Video Generator")
        st.write(f"Generate high-converting promotional posts, matching banners, and custom {selected_duration} promotional videos for your affiliate links.")
        
        with st.form("aff_form"):
            t_name = st.text_input("Product Name:")
            desc = st.text_area("Product Details / Offers:")
            link = st.text_input("Affiliate Tracking Link:")
            submitted = st.form_submit_button("Generate Affiliate Ad, Banner & Video")
            
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
                        st.success("Affiliate Package Generated Successfully!")
                        
                        st.subheader(f"🖼️ AI Generated Banner for {t_name}:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download High-Res Banner]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎬 Generated {selected_duration} Promotional Video (Play & Download):")
                        st.video(res_json["video_url"])
                        st.markdown(f"[📥 Download MP4 Video]({res_json['video_url']})")
                        
                        st.subheader("📌 Generated Caption & Copy")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter product name.")

    elif menu == "2️⃣ Business & Auto Ads (Link/Photos/Videos/Create AI)":
        st.title("🚀 Business & Auto Ads Suite")
        st.write(f"Provide your website link, upload media, or let AI auto-create a {selected_duration} commercial video ad for Meta & WhatsApp.")
        
        with st.form("biz_form"):
            b_name = st.text_input("Business / Hotel Name:")
            b_desc = st.text_area("Offer or Service Description:")
            b_link = st.text_input("Website or Location Link (AI will extract content if no media provided):")
            
            col1, col2 = st.columns(2)
            with col1:
                up_img = st.file_uploader("Upload Business Photo (Optional):", type=["jpg", "png", "jpeg"])
            with col2:
                up_vid = st.file_uploader("Upload Business Video (Optional):", type=["mp4", "mov", "avi"])
                
            submitted = st.form_submit_button("Generate Business Ad Package")
            
            if submitted:
                if b_name:
                    files = {}
                    if up_img:
                        files["image"] = (up_img.name, up_img.getvalue(), up_img.type)
                    if up_vid:
                        files["video"] = (up_vid.name, up_vid.getvalue(), up_vid.type)
                        
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Business & Auto Ads",
                        "title_name": b_name,
                        "description_text": b_desc,
                        "link_url": b_link,
                        "language": selected_lang,
                        "video_duration": selected_duration
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data, files=files if files else None)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("Business Ad Package Generated Successfully!")
                        
                        st.subheader(f"🖼️ AI Generated Business Banner for {b_name}:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download High-Res Ad Image]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎬 Ad Video ({selected_duration} - {res_json['video_source']}):")
                        st.video(res_json["video_url"])
                        st.markdown(f"[📥 Download MP4 Video]({res_json['video_url']})")
                        
                        st.subheader("📌 Ad Copy & Details")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter business name.")

    elif menu == "3️⃣ Social Media Videos & Download":
        st.title(f"🎬 Social Media Videos ({selected_duration}) & Download Suite")
        with st.form("vid_form"):
            v_title = st.text_input("Video Topic / Product Name:")
            v_desc = st.text_input("Video Hook or Key Message:")
            submitted = st.form_submit_button(f"Generate {selected_duration} Video & Thumbnail")
            
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
                        st.success(f"Viral {selected_duration} Video & Script Generated!")
                        
                        st.subheader(f"🖼️ AI Generated Thumbnail for {v_title}:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Thumbnail]({res_json['ai_image_url']})")
                        
                        st.subheader(f"🎥 Preview & Download {selected_duration} Generated Video:")
                        st.video(res_json["video_url"])
                        st.markdown(f"[📥 Download MP4 Video]({res_json['video_url']})")
                        
                        st.subheader("📝 Script & Production Guide")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter video topic.")

    elif menu == "4️⃣ Meta & WhatsApp Auto-Publishing":
        st.title("📡 Meta & WhatsApp Auto-Publishing Center")
        st.write("Automatically publish your generated business ads and videos directly to Facebook, Instagram, and WhatsApp!")
        
        with st.form("auto_pub_form"):
            b_name = st.text_input("Business / Brand Name:")
            caption = st.text_area("Post Caption / Message Text:")
            platforms = st.multiselect("Select Target Platforms:", ["Facebook (Meta)", "Instagram", "WhatsApp"])
            phone = st.text_input("WhatsApp Number (with country code, e.g., +919876543210):")
            pub_btn = st.form_submit_button("Auto-Publish Now")
            
            if pub_btn:
                if b_name and caption and platforms:
                    payload = {
                        "business_name": b_name,
                        "caption": caption,
                        "target_platforms": platforms,
                        "recipient_phone": phone
                    }
                    with st.spinner("Publishing to Meta & WhatsApp..."):
                        res = requests.post(f"{BACKEND_URL}/auto-publish", json=payload)
                        if res.status_code == 200:
                            res_data = res.json().get("publish_results", {})
                            st.success("Auto-publishing completed successfully!")
                            for plat, msg in res_data.items():
                                st.info(f"**{plat}:** {msg}")
                        else:
                            st.error("Auto-publishing failed.")
                else:
                    st.warning("Please fill in all required fields and select at least one platform.")

    elif menu == "5️⃣ SaaS Subscription Plans":
        st.title("💎 SaaS Subscription Tiers")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Free Tier")
            st.markdown("**$0 / month**")
            st.button("Current Plan", disabled=True)
        with c2:
            st.subheader("Pro Creator")
            st.markdown("**$19 / month**")
            st.button("Upgrade to Pro", key="p_btn")
        with c3:
            st.subheader("Enterprise")
            st.markdown("**$49 / month**")
            st.button("Get Enterprise", key="e_btn")

    elif menu == "⚙️ Analytics & Settings":
        st.title("⚙️ Enterprise Analytics & Configuration")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{st.session_state['username']}")
            if res.status_code == 200:
                data = res.json()
                analytics = data["analytics"]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Reach / Clicks", analytics["clicks"])
                c2.metric("Active Campaigns", len(data["campaigns"]))
                c3.metric("Total Earnings ($)", f"$ {analytics['earnings']}")
                
                st.markdown("---")
                st.subheader("📁 Saved Campaign History")
                for camp in data["campaigns"]:
                    st.write(f"- **Type:** {camp['type']} | **Name:** {camp['name']} | **Duration:** {camp.get('duration', 'N/A')}")
        except Exception as e:
            st.error("Failed to load analytics data.")

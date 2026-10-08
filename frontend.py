import streamlit as st
import requests

BACKEND_URL = "https://metapost-backend.onrender.com"

st.set_page_config(page_title="MetaPost AI Ultimate Pro - Official Suite", page_icon="⚡", layout="wide")

# High Official UI CSS Theme (Professional Corporate Look)
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; font-weight: bold; border: none; padding: 12px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4); }
    .stButton>button:hover { background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%); }
    .css-1104ytp { background-color: #111827; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("⚡ MetaPost AI Ultimate Pro - Official Portal")
    st.write("Welcome to the next-generation AI marketing, video generation, and monetization suite.")
    
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
    
    # Global Language Selector
    selected_lang = st.sidebar.selectbox("🌐 Select Output Language", ["English", "Telugu", "Hindi", "Spanish", "French", "Arabic"])
    
    menu = st.sidebar.selectbox("Main Dashboard Menu", [
        "1️⃣ Affiliate Marketing Suite", 
        "2️⃣ Business & Auto Ads (Link/Photos)", 
        "3️⃣ Social Media Videos (Monetization)", 
        "4️⃣ SaaS Subscription Plans", 
        "⚙️ Analytics & Settings",
        "🚪 Logout"
    ])
    
    if menu == "🚪 Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    elif menu == "1️⃣ Affiliate Marketing Suite":
        st.title("💼 Affiliate Marketing Content Generator")
        st.write("Generate high-converting promotional posts and professional banners for your affiliate links.")
        
        with st.form("aff_form"):
            t_name = st.text_input("Product Name:")
            desc = st.text_area("Product Details / Offers:")
            link = st.text_input("Affiliate Tracking Link:")
            submitted = st.form_submit_button("Generate Affiliate Content")
            
            if submitted:
                if t_name:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Affiliate Marketing",
                        "title_name": t_name,
                        "description_text": desc,
                        "link_url": link,
                        "language": selected_lang
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("Content Generated Successfully!")
                        
                        st.subheader("🖼️ AI Generated Promotional Banner:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Banner Image]({res_json['ai_image_url']})")
                        
                        st.subheader("📌 Generated Caption & Copy")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter the product name.")

    elif menu == "2️⃣ Business & Auto Ads (Link/Photos)":
        st.title("🚀 Business & Auto Ads Suite")
        st.write("Develop professional advertisements for hotels, restaurants, or businesses using website links or uploaded photos.")
        
        with st.form("biz_form"):
            b_name = st.text_input("Business / Hotel Name:")
            b_desc = st.text_area("Offer or Service Description:")
            b_link = st.text_input("Website or Location Link:")
            up_img = st.file_uploader("Upload Menu / Business Photo:", type=["jpg", "png", "jpeg"])
            submitted = st.form_submit_button("Generate Business Ad")
            
            if submitted:
                if b_name:
                    files = {"image": (up_img.name, up_img.getvalue(), up_img.type)} if up_img else None
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Business & Auto Ads",
                        "title_name": b_name,
                        "description_text": b_desc,
                        "link_url": b_link,
                        "language": selected_lang
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data, files=files)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("Business Ad Generated Successfully!")
                        
                        st.subheader("🖼️ AI Generated Business Banner:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Ad Image]({res_json['ai_image_url']})")
                        
                        st.subheader("📌 Ad Copy & Details")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter your business name.")

    elif menu == "3️⃣ Social Media Videos (Monetization)":
        st.title("🎬 Social Media Videos & Monetization Suite")
        st.write("Create viral scripts for YouTube Shorts & Instagram Reels to drive views, subscribers, and revenue.")
        
        with st.form("vid_form"):
            v_title = st.text_input("Video Topic / Product Name:")
            v_desc = st.text_input("Video Hook or Key Message:")
            submitted = st.form_submit_button("Generate Viral Video Script & Visual")
            
            if submitted:
                if v_title:
                    data = {
                        "username": st.session_state['username'],
                        "option_type": "Social Media Videos",
                        "title_name": v_title,
                        "description_text": v_desc,
                        "language": selected_lang
                    }
                    res = requests.post(f"{BACKEND_URL}/generate-content", data=data)
                    if res.status_code == 200:
                        res_json = res.json()["generated_content"]
                        st.success("Video Script & Thumbnail Generated!")
                        
                        st.subheader("🖼️ AI Generated Video Thumbnail:")
                        st.image(res_json["ai_image_url"], use_container_width=True)
                        st.markdown(f"[📥 Download Thumbnail]({res_json['ai_image_url']})")
                        
                        st.subheader("📝 Production Guide & Script")
                        st.write(res_json["content"])
                else:
                    st.warning("Please enter a video topic.")

    elif menu == "4️⃣ SaaS Subscription Plans":
        st.title("💎 SaaS Subscription Tiers")
        st.write("Upgrade your workspace for unlimited automation, advanced AI generation, and priority publishing.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Free Tier")
            st.markdown("**$0 / month**")
            st.markdown("- Basic Templates")
            st.markdown("- Community Support")
            st.button("Current Plan", disabled=True)
        with c2:
            st.subheader("Pro Creator")
            st.markdown("**$19 / month**")
            st.markdown("- Unlimited AI Ads & Scripts")
            st.markdown("- High-Res Banner Downloads")
            st.button("Upgrade to Pro", key="p_btn")
        with c3:
            st.subheader("Enterprise")
            st.markdown("**$49 / month**")
            st.markdown("- Full Business Automation")
            st.markdown("- Priority API Access")
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
                    st.write(f"- **Type:** {camp['type']} | **Name:** {camp['name']}")
        except Exception as e:
            st.error("Failed to load analytics data.")

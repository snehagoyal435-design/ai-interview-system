# ============================================
# AI Interview System - Premium Frontend
# By Khushi Goyal
# ============================================

import streamlit as st
import requests
import time
import plotly.graph_objects as go
import pandas as pd
import base64


API_URL = "https://khushi-ai-interview-api.onrender.com"

st.set_page_config(
    page_title="AI Interview System - Khushi Goyal",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================
# PAGE BACKGROUNDS
# ============================================

PAGE_BACKGROUNDS = {
    "Login": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=1920&q=80",
    "ProfileSetup": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920&q=80",
    "Dashboard": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1920&q=80",
    "Profile": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920&q=80",
    "Resume": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=1920&q=80",
    "Interview": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920&q=80",
    "History": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=80",
    "Database": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80",
    "Admin": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=80",
}


def set_page_background(key):
    img = PAGE_BACKGROUNDS.get(key, PAGE_BACKGROUNDS["Dashboard"])
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: 
                linear-gradient(rgba(10, 15, 35, 0.85), rgba(25, 20, 60, 0.88)),
                url('{img}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================
# GLOBAL CSS
# ============================================

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stApp, .block-container, [data-testid="stVerticalBlock"], 
    [data-testid="stHorizontalBlock"], [data-testid="stVerticalBlockBorderWrapper"],
    .element-container { background: transparent !important; }
    
    .block-container {padding-top: 2rem; max-width: 1300px;}
    
    .hero {
        background: rgba(10, 15, 35, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 50px 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.25);
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.85em;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
        color: #c4b5fd;
        border: 1px solid rgba(196, 181, 253, 0.4);
    }
    .hero-title {
        font-size: 3em;
        font-weight: 900;
        margin: 10px 0;
        color: white;
        text-shadow: 0 4px 30px rgba(0,0,0,0.7);
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.15em;
        color: rgba(255,255,255,0.9);
        margin-top: 15px;
        font-weight: 400;
    }
    .hero-brand {
        font-size: 0.85em;
        color: rgba(196, 181, 253, 0.9);
        margin-top: 20px;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    .card {
        background: rgba(10, 15, 35, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        color: white;
    }
    .card h1, .card h2, .card h3, .card h4, .card p, .card li, .card span, .card div {
        color: white !important;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.45);
    }
    .stat-icon { font-size: 2.4em; }
    .stat-value { font-size: 2.4em; font-weight: 900; margin: 5px 0; color: white; }
    .stat-label { font-size: 0.85em; opacity: 0.95; text-transform: uppercase; letter-spacing: 1.5px; color: white; }
    
    .feature-card {
        background: rgba(10, 15, 35, 0.8);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .feature-icon { font-size: 2.8em; margin-bottom: 15px; }
    .feature-title { font-size: 1.15em; font-weight: 700; color: white !important; margin-bottom: 8px; }
    .feature-desc { color: rgba(255,255,255,0.75) !important; font-size: 0.9em; line-height: 1.5; }
    
    .question-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.9) 0%, rgba(99, 102, 241, 0.9) 100%);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.5);
    }
    .question-number {
        color: rgba(255,255,255,0.9);
        font-weight: 800;
        font-size: 0.85em;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .question-text {
        font-size: 1.35em;
        color: white;
        line-height: 1.6;
        margin-top: 12px;
        font-weight: 600;
    }
    
    .fb-box {
        padding: 18px;
        border-radius: 14px;
        margin: 12px 0;
        color: white;
        background: rgba(10, 15, 35, 0.85);
        backdrop-filter: blur(10px);
    }
    .fb-strength { border-left: 5px solid #10b981; }
    .fb-weakness { border-left: 5px solid #ef4444; }
    .fb-tips { border-left: 5px solid #3b82f6; }
    .fb-box strong { color: white !important; }
    
    .score-badge {
        display: inline-block;
        padding: 10px 24px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.15em;
    }
    .score-excellent { background: rgba(16, 185, 129, 0.9); color: white; }
    .score-good { background: rgba(59, 130, 246, 0.9); color: white; }
    .score-average { background: rgba(245, 158, 11, 0.9); color: white; }
    .score-poor { background: rgba(239, 68, 68, 0.9); color: white; }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95em !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        width: 100%;
        margin: 3px 0;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(10, 15, 35, 0.7) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
        .stDownloadButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95em !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6) !important;
    }
    .stDownloadButton > button p,
    .stDownloadButton > button span,
    .stDownloadButton > button div {
        color: white !important;
        font-weight: 700 !important;
    }
    
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        color: #1e293b !important;
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1em !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #94a3b8 !important; }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    }
    
    .stSelectbox > div > div {
        background-color: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    .stSelectbox > div > div > div { color: #1e293b !important; }
    
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stFileUploader label, .stRadio label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1em !important;
    }
    
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp li, .stApp span, .stApp label, .stApp .stMarkdown {
        color: white;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 15, 35, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 5px;
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 35, 0.96) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {color: white !important;}
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: white !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(139, 92, 246, 0.4) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
        border: none !important;
    }
    
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        background: rgba(10, 15, 35, 0.7) !important;
    }
    .streamlit-expanderHeader {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stAlert { border-radius: 12px; background: rgba(10, 15, 35, 0.85) !important; }
    .stAlert * { color: white !important; }
    
    .stFileUploader section {
        background: rgba(10, 15, 35, 0.8) !important;
        border: 2px dashed rgba(139, 92, 246, 0.6) !important;
        border-radius: 12px;
    }
    .stFileUploader span, .stFileUploader div, .stFileUploader small { color: white !important; }
    
    .stDataFrame { background: rgba(10, 15, 35, 0.85) !important; border-radius: 12px; }
    
    hr { border-color: rgba(255,255,255,0.15) !important; }
    .stSpinner > div { border-top-color: #8b5cf6 !important; }
    .stSpinner span { color: white !important; }
    
    .info-card {
        background: rgba(10, 15, 35, 0.85);
        border-left: 4px solid #8b5cf6;
        padding: 16px;
        border-radius: 12px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# SESSION STATE
# ============================================

for key, val in {
    "token": None, "user": None, "profile": None, "interview": None,
    "current_q": 0, "page": "Dashboard", "admin_view_user": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ============================================
# HELPERS
# ============================================

def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def api_call(method, endpoint, **kwargs):
    url = f"{API_URL}{endpoint}"
    headers = get_headers()
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, timeout=60, **kwargs)
        else:
            r = requests.post(url, headers=headers, timeout=60, **kwargs)

        if r.status_code == 401:
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.profile = None
            st.session_state.interview = None
            st.warning("Your session has expired. Please log in again.")
            time.sleep(1.5)
            st.rerun()
            return {"error": "Session expired"}

        if r.status_code in [200, 201]:
            return r.json()
        return {"error": r.json().get("detail", "Error"), "status": r.status_code}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Is the server running?"}
    except Exception as e:
        return {"error": str(e)}


def load_profile():
    r = api_call("GET", "/profile/me")
    if isinstance(r, dict) and r.get("exists"):
        st.session_state.profile = r["profile"]
    else:
        st.session_state.profile = None


def score_class(s):
    if s is None: return "score-average"
    if s >= 9: return "score-excellent"
    if s >= 7: return "score-good"
    if s >= 5: return "score-average"
    return "score-poor"


def score_label(s):
    if s is None: return "N/A"
    if s >= 9: return "Excellent"
    if s >= 7: return "Good"
    if s >= 5: return "Average"
    return "Needs Improvement"


def is_admin():
    u = st.session_state.user or {}
    return u.get("is_admin") or u.get("role") == "admin"


# ============================================
# LOGIN PAGE
# ============================================

def show_login():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Powered by Google Gemini AI</div>
        <div class="hero-title">AI Interview System</div>
        <div class="hero-subtitle">Land your dream job with AI-powered mock interviews</div>
        <div class="hero-brand">Crafted by Khushi Goyal</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Questions</div>
            <div class="feature-desc">Role-specific questions generated by Gemini AI</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Instant Scoring</div>
            <div class="feature-desc">Real-time feedback on every answer</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">PDF Reports</div>
            <div class="feature-desc">Download professional feedback reports</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                pwd = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if email and pwd:
                    with st.spinner("Logging in..."):
                        r = requests.post(f"{API_URL}/auth/login",
                                          data={"username": email, "password": pwd}, timeout=30)
                    if r.status_code == 200:
                        st.session_state.token = r.json()["access_token"]
                        me = api_call("GET", "/auth/me")
                        if "error" not in me:
                            st.session_state.user = me
                        load_profile()
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(f"Login failed: {r.json().get('detail', 'Try again')}")
                else:
                    st.warning("Please enter email and password")

        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name", placeholder="John Doe")
                email2 = st.text_input("Email", placeholder="you@example.com")
                pwd2 = st.text_input("Password (min 6 characters)", type="password")
                role = st.selectbox("Role", ["candidate", "recruiter"])
                submit = st.form_submit_button("Create Account", use_container_width=True)

            if submit:
                if name and email2 and len(pwd2) >= 6:
                    with st.spinner("Creating account..."):
                        r = requests.post(f"{API_URL}/auth/signup", json={
                            "email": email2, "password": pwd2,
                            "full_name": name, "role": role
                        }, timeout=30)
                    if r.status_code == 201:
                        st.success("Account created! Please log in.")
                    else:
                        st.error(f"Signup failed: {r.json().get('detail', 'Try again')}")
                else:
                    st.warning("Fill all fields (password 6+ characters)")

        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# PROFILE SETUP
# ============================================

def show_profile_setup():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Welcome</div>
        <div class="hero-title">Set Up Your Profile</div>
        <div class="hero-subtitle">Tell us about yourself — this personalizes your interviews</div>
        <div class="hero-brand">AI Interview System — by Khushi Goyal</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Basic Information")

        with st.form("profile_form"):
            full_name = st.text_input("Full Name *",
                                       value=st.session_state.user.get("full_name", "") if st.session_state.user else "")
            status = st.selectbox("Current Status *",
                                   ["Student", "Fresher (0-1 years)", "Experienced (1-3 years)",
                                    "Experienced (3-5 years)", "Experienced (5+ years)"])
            education = st.text_input("Education / Degree", placeholder="e.g., B.Tech CSE, MBA")
            target_role = st.text_input("Target Job Role *", placeholder="e.g., Python Developer")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=30, value=0)
            skills = st.text_area("Your Skills (comma-separated)",
                                   placeholder="Python, SQL, Django, React", height=80)
            bio = st.text_area("Short Bio", placeholder="Tell us about yourself in 2-3 lines", height=80)

            submit = st.form_submit_button("Save Profile & Continue", use_container_width=True)

        if submit:
            if not full_name or not target_role:
                st.error("Name and Target Role are required")
            else:
                payload = {
                    "full_name": full_name,
                    "status": status,
                    "education": education,
                    "target_role": target_role,
                    "experience_years": experience_years,
                    "skills": skills,
                    "bio": bio,
                }
                r = api_call("POST", "/profile/me", json=payload)
                if "error" in r:
                    st.error(f"Error: {r['error']}")
                else:
                    st.success("Profile saved successfully!")
                    load_profile()
                    time.sleep(0.5)
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# SIDEBAR
# ============================================

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 15px 0;">
            <div style="font-size: 3.5em;">🎤</div>
            <div style="font-size: 1.35em; font-weight: 800;">AI Interview</div>
            <div style="font-size: 0.7em; opacity: 0.6; letter-spacing: 2px;">BY KHUSHI GOYAL</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        profile = st.session_state.get("profile") or {}
        name = profile.get("full_name") or st.session_state.user.get("full_name", "User")
        email = st.session_state.user.get("email", "")
        target = profile.get("target_role", "")

        st.markdown(f"""
        <div style="background: rgba(139,92,246,0.2); padding: 15px; border-radius: 14px; 
                    text-align: center; margin-bottom: 15px;">
            <div style="font-size: 2em;">👤</div>
            <div style="font-weight: 700; font-size: 1em;">{name}</div>
            <div style="font-size: 0.75em; opacity: 0.7;">{email}</div>
            {f'<div style="font-size: 0.75em; opacity: 0.85; margin-top: 5px; color: #c4b5fd;">🎯 {target}</div>' if target else ''}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Navigation")

        pages = [
            ("🏠 Dashboard", "Dashboard"),
            ("👤 My Profile", "Profile"),
            ("📄 Upload Resume", "Resume"),
            ("🎯 Start Interview", "Interview"),
            ("📊 My Interviews", "History"),
            ("💾 Database Viewer", "Database"),
        ]

        if is_admin():
            pages.append(("🛡️ Admin Panel", "Admin"))

        for label, key in pages:
            is_active = st.session_state.page == key
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_type):
                st.session_state.page = key
                st.rerun()

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            for k in ["token", "user", "profile", "interview", "admin_view_user"]:
                st.session_state[k] = None
            st.session_state.current_q = 0
            st.session_state.page = "Dashboard"
            st.rerun()

        st.markdown("""
        <div style="text-align: center; padding: 20px 0; font-size: 0.7em; opacity: 0.5;">
            v2.0 • by Khushi Goyal
        </div>
        """, unsafe_allow_html=True)


# ============================================
# DASHBOARD
# ============================================

def show_dashboard():
    profile = st.session_state.get("profile") or {}
    name = profile.get("full_name") or st.session_state.user.get("full_name", "User")

    st.markdown(f"""
    <div class="hero">
        <div class="hero-title" style="font-size: 2.6em;">Welcome, {name}</div>
        <div class="hero-subtitle">Let's get you interview-ready</div>
    </div>
    """, unsafe_allow_html=True)

    r = api_call("GET", "/interviews/")
    interviews = r.get("interviews", []) if isinstance(r, dict) and "error" not in r else []
    total = len(interviews)
    scores = [i["total_score"] for i in interviews if i.get("total_score")]
    avg = round(sum(scores) / len(scores), 1) if scores else 0
    best = max(scores) if scores else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{total}</div>
            <div class="stat-label">Interviews</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">{avg}</div>
            <div class="stat-label">Average</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">{best}</div>
            <div class="stat-label">Best Score</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        exp = profile.get("experience_years", 0)
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <div class="stat-icon">💼</div>
            <div class="stat-value">{exp}</div>
            <div class="stat-label">Years Exp</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if interviews:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Your Progress")
        sorted_i = sorted(interviews, key=lambda x: x.get("created_at", ""))
        dates = [str(i.get("created_at", ""))[:10] for i in sorted_i]
        sc = [i.get("total_score", 0) for i in sorted_i]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=sc, mode='lines+markers+text',
            line=dict(color='#a78bfa', width=4),
            marker=dict(size=14, color='#8b5cf6', line=dict(color='white', width=2)),
            text=[f"{v}/10" for v in sc],
            textposition="top center",
            textfont=dict(color='white', size=12),
            fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.25)',
        ))
        fig.update_layout(
            plot_bgcolor='rgba(10, 15, 35, 0.6)',
            paper_bgcolor='rgba(10, 15, 35, 0.6)',
            font=dict(color='white', size=13),
            height=350, margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white', title='Date'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)',
                       range=[0, 10.5], color='white', title='Score / 10'),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Upload Resume</div>
            <div class="feature-desc">Extract your skills automatically</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Start Interview</div>
            <div class="feature-desc">Get AI-generated questions</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📥</div>
            <div class="feature-title">Download Report</div>
            <div class="feature-desc">Get PDF feedback instantly</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# PROFILE PAGE
# ============================================

def show_profile_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-title" style="font-size: 2.3em;">My Profile</div>
        <div class="hero-subtitle">Your saved information</div>
    </div>
    """, unsafe_allow_html=True)

    profile = st.session_state.get("profile") or {}

    st.markdown('<div class="card">', unsafe_allow_html=True)

    with st.form("update_profile"):
        full_name = st.text_input("Full Name", value=profile.get("full_name", ""))
        status_opts = ["Student", "Fresher (0-1 years)", "Experienced (1-3 years)",
                       "Experienced (3-5 years)", "Experienced (5+ years)"]
        cur = profile.get("status", "Student")
        idx = status_opts.index(cur) if cur in status_opts else 0
        status = st.selectbox("Status", status_opts, index=idx)
        education = st.text_input("Education", value=profile.get("education", "") or "")
        target_role = st.text_input("Target Role", value=profile.get("target_role", "") or "")
        exp = st.number_input("Years of Experience", 0, 30, value=int(profile.get("experience_years", 0)))
        skills_list = profile.get("skills", [])
        if isinstance(skills_list, str):
            skills_list = [s.strip() for s in skills_list.split(",") if s.strip()]
        skills_str = st.text_area("Skills (comma-separated)", value=", ".join(skills_list), height=80)
        bio = st.text_area("Bio", value=profile.get("bio", "") or "", height=100)

        submit = st.form_submit_button("Update Profile", use_container_width=True)

    if submit:
        payload = {
            "full_name": full_name, "status": status, "education": education,
            "target_role": target_role, "experience_years": exp,
            "skills": skills_str, "bio": bio,
        }
        r = api_call("POST", "/profile/me", json=payload)
        if "error" in r:
            st.error(f"Error: {r['error']}")
        else:
            st.success("Profile updated successfully!")
            load_profile()
            time.sleep(0.5)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# UPLOAD RESUME
# ============================================

def show_upload_resume():
    st.markdown("""
    <div class="hero">
        <div class="hero-title" style="font-size: 2.3em;">Upload Resume</div>
        <div class="hero-subtitle">AI will extract your skills automatically</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Upload your Resume (PDF)")
    uploaded = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

    if uploaded:
        st.info(f"Selected: **{uploaded.name}** ({uploaded.size/1024:.1f} KB)")
        if st.button("Upload & Parse", use_container_width=True):
            with st.spinner("Uploading and parsing..."):
                files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
                r = requests.post(f"{API_URL}/resume/upload",
                                  headers=get_headers(), files=files, timeout=180)
            if r.status_code == 200:
                st.session_state.parsed_resume = r.json()
                st.success("Resume parsed successfully!")
            else:
                st.error(f"Error: {r.json().get('detail', 'Upload failed')}")
    st.markdown('</div>', unsafe_allow_html=True)

    if "parsed_resume" in st.session_state:
        d = st.session_state.parsed_resume
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Extracted Information")

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Skills Found")
            skills = d.get("skills", [])
            if skills:
                for s in skills:
                    st.markdown(f"- {s}")
            else:
                st.info("No skills detected. Try a different PDF.")
        with c2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">💼</div>
                <div class="stat-value">{d.get('experience_years', 0)}</div>
                <div class="stat-label">Years Exp</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Summary")
        st.info(d.get("summary", "No summary available"))
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# START INTERVIEW
# ============================================

def show_start_interview():
    if not st.session_state.interview:
        st.markdown("""
        <div class="hero">
            <div class="hero-title" style="font-size: 2.3em;">Start New Interview</div>
            <div class="hero-subtitle">AI will generate 5 customized questions</div>
        </div>
        """, unsafe_allow_html=True)

        profile = st.session_state.get("profile") or {}

        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("start_int"):
            role = st.text_input("Job Role *",
                                 value=profile.get("target_role", "") or "",
                                 placeholder="e.g., Python Developer")

            skills_list = profile.get("skills", [])
            if isinstance(skills_list, str):
                skills_list = [s.strip() for s in skills_list.split(",") if s.strip()]
            default_skills = ", ".join(skills_list)

            skills = st.text_input("Skills (comma-separated)",
                                   value=default_skills,
                                   placeholder="Python, SQL, Django")
            difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], index=1)
            submit = st.form_submit_button("Generate Questions", use_container_width=True)

        if submit:
            if role:
                sk = [x.strip() for x in skills.split(",") if x.strip()]
                with st.spinner("AI is generating questions..."):
                    r = api_call("POST", "/interviews/start",
                                 json={"job_role": role, "skills": sk, "difficulty": difficulty})
                if "error" in r:
                    st.error(f"Error: {r['error']}")
                else:
                    st.session_state.interview = r
                    st.session_state.current_q = 0
                    st.rerun()
            else:
                st.warning("Please enter a job role")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        interview = st.session_state.interview
        questions = interview.get("questions", [])
        total = len(questions)
        idx = st.session_state.current_q

        pct = (idx / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div class="card" style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 1.4em; font-weight: 800; color: #a78bfa;">
                        {interview['job_role']}
                    </div>
                    <div style="color: rgba(255,255,255,0.8);">Question {idx + 1} of {total}</div>
                </div>
                <div class="score-badge score-good">{int(pct)}% Complete</div>
            </div>
            <div style="background: rgba(255,255,255,0.2); height: 10px; border-radius: 10px; margin-top: 15px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #8b5cf6, #6366f1); 
                            height: 100%; width: {pct}%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if idx < total:
            q = questions[idx]
            qid = q["id"]

            st.markdown(f"""
            <div class="question-card">
                <div class="question-number">Question {idx + 1}</div>
                <div class="question-text">{q['question_text']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Listen button
            c1, c2 = st.columns([2, 1])
            with c2:
                if st.button("🔊 Listen to Question", key=f"listen_{qid}", use_container_width=True):
                    with st.spinner("Generating audio..."):
                        try:
                            rr = requests.post(f"{API_URL}/speech/speak",
                                               headers=get_headers(),
                                               json={"text": q['question_text'],
                                                     "filename": f"q_{qid}.mp3"},
                                               timeout=60)
                            if rr.status_code == 200:
                                st.audio(rr.content, format="audio/mp3")
                            else:
                                st.error("Audio generation failed")
                        except Exception as e:
                            st.error(f"Error: {e}")

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Your Answer")

            input_mode = st.radio("Choose input method:",
                                   ["Type answer", "Record or Upload audio"],
                                   horizontal=True, key=f"mode_{qid}")

            answer = ""

            if input_mode == "Type answer":
                answer = st.text_area("Your answer", height=180, key=f"ans_{qid}",
                                       placeholder="Type your answer here...",
                                       label_visibility="collapsed")
            else:
                st.markdown("**Record your answer on your phone and upload the audio file.**")
                st.caption("Supported formats: .m4a, .mp3, .wav, .ogg")
                audio_file = st.file_uploader("Upload audio file",
                                               type=["m4a", "mp3", "wav", "ogg"],
                                               key=f"audio_{qid}")
                if audio_file:
                    if st.button("Transcribe Audio", key=f"trans_{qid}", use_container_width=True):
                        with st.spinner("Transcribing your voice..."):
                            try:
                                files = {"file": (audio_file.name, audio_file.getvalue(), "audio/mpeg")}
                                rr = requests.post(f"{API_URL}/speech/transcribe",
                                                   headers=get_headers(),
                                                   files=files, timeout=180)
                                if rr.status_code == 200:
                                    transcribed = rr.json().get("text", "")
                                    st.session_state[f"ans_{qid}"] = transcribed
                                    st.success("Transcription complete!")
                                    st.rerun()
                                else:
                                    st.error(f"Transcription failed: {rr.json().get('detail', '')}")
                            except Exception as e:
                                st.error(f"Error: {e}")

                answer = st.text_area("Edit transcribed text (optional)",
                                       height=120, key=f"ans_{qid}",
                                       placeholder="Transcribed text appears here...",
                                       label_visibility="collapsed")

            c1, c2 = st.columns([2, 1])
            with c1:
                if st.button("Submit Answer", key=f"sub_{qid}", use_container_width=True):
                    if answer.strip():
                        with st.spinner("AI is evaluating your answer..."):
                            r = api_call("POST",
                                         f"/interviews/{interview['interview_id']}/answer",
                                         json={"question_id": qid, "answer_text": answer})
                        if "error" in r:
                            st.error(f"Error: {r['error']}")
                        else:
                            st.success(f"Score: {r['score']}/10")
                            d = r.get("details", {})
                            st.markdown(f"""
                            <div class="fb-box fb-strength">
                                <strong>Strengths:</strong> {d.get('strengths', 'N/A')}
                            </div>
                            <div class="fb-box fb-weakness">
                                <strong>Weaknesses:</strong> {d.get('weaknesses', 'N/A')}
                            </div>
                            <div class="fb-box fb-tips">
                                <strong>Improvement Tips:</strong> {d.get('improvement_tips', 'N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                            time.sleep(3)
                            st.session_state.current_q += 1
                            st.rerun()
                    else:
                        st.warning("Please provide an answer")
            with c2:
                if st.button("Skip", key=f"skip_{qid}", use_container_width=True):
                    st.session_state.current_q += 1
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.balloons()
            st.markdown("""
            <div class="hero">
                <div class="hero-title" style="font-size: 2.3em;">Interview Complete!</div>
                <div class="hero-subtitle">Great job! Let's finalize your results.</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Finish & View Results", use_container_width=True, key="finish_btn"):
                    with st.spinner("Finalizing your interview..."):
                        r = api_call("POST", f"/interviews/{interview['interview_id']}/complete")

                    # Fix: check for actual error value, not just key existence
                    if isinstance(r, dict) and r.get("error"):
                        st.error(f"Error: {r['error']}")
                    else:
                        final_score = r.get("final_score", 0) if isinstance(r, dict) else 0
                        st.success(f"Final Score: {final_score}/10")
                        st.session_state.interview = None
                        st.session_state.current_q = 0
                        st.session_state.page = "History"
                        time.sleep(1.5)
                        st.rerun()

            with c2:
                if st.button("New Interview", use_container_width=True, key="new_btn"):
                    st.session_state.interview = None
                    st.session_state.current_q = 0
                    st.rerun()


# ============================================
# MY INTERVIEWS
# ============================================

def show_my_interviews():
    st.markdown("""
    <div class="hero">
        <div class="hero-title" style="font-size: 2.3em;">My Interviews</div>
        <div class="hero-subtitle">Your complete interview history</div>
    </div>
    """, unsafe_allow_html=True)

    r = api_call("GET", "/interviews/")
    if isinstance(r, dict) and r.get("error"):
        st.error(f"Error: {r['error']}")
        return

    interviews = r.get("interviews", [])
    if not interviews:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("You haven't taken any interviews yet. Go to Start Interview.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for iv in interviews:
        score = iv.get("total_score", 0)
        badge = score_class(score)
        label = score_label(score)

        st.markdown(f"""
        <div class="card" style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 1.25em; font-weight: 800; color: #a78bfa;">
                        #{iv['id']} — {iv['job_role']}
                    </div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 5px;">
                        {str(iv['created_at'])[:19]} • {iv['status'].title()}
                    </div>
                </div>
                <div style="text-align: center;">
                    <div class="score-badge {badge}">{score}/10</div>
                    <div style="margin-top: 5px; color: rgba(255,255,255,0.8); font-size: 0.85em;">{label}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("View Details", key=f"v_{iv['id']}", use_container_width=True):
                d = api_call("GET", f"/interviews/{iv['id']}")
                if isinstance(d, dict) and "error" not in d:
                    st.session_state[f"det_{iv['id']}"] = d
                    st.rerun()
        with c2:
            if st.button("Get PDF Report", key=f"p_{iv['id']}", use_container_width=True):
                try:
                    rr = requests.get(f"{API_URL}/interviews/{iv['id']}/report",
                                      headers=get_headers(), timeout=60)
                    if rr.status_code == 200:
                        st.session_state[f"pdf_{iv['id']}"] = rr.content
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with c3:
            if st.button("Hide Details", key=f"h_{iv['id']}", use_container_width=True):
                if f"det_{iv['id']}" in st.session_state:
                    del st.session_state[f"det_{iv['id']}"]
                st.rerun()

        if f"pdf_{iv['id']}" in st.session_state:
            st.download_button(
                "Download PDF Report",
                data=st.session_state[f"pdf_{iv['id']}"],
                file_name=f"interview_{iv['id']}_report.pdf",
                mime="application/pdf",
                key=f"dl_{iv['id']}",
                use_container_width=True,
            )

        if f"det_{iv['id']}" in st.session_state:
            d = st.session_state[f"det_{iv['id']}"]
            if isinstance(d, dict) and "error" not in d:
                with st.expander(f"Questions & Answers — {iv['job_role']}", expanded=True):
                    for i, q in enumerate(d.get("questions", []), 1):
                        st.markdown(f"**Q{i}:** {q.get('question_text', 'N/A')}")
                        if q.get("answer_text"):
                            st.markdown(f"*Your answer:* {q['answer_text'][:400]}...")
                        if q.get("score") is not None:
                            s_cls = score_class(q['score'])
                            st.markdown(
                                f'<span class="score-badge {s_cls}">Score: {q["score"]}/10</span>',
                                unsafe_allow_html=True
                            )
                        if q.get("feedback"):
                            st.markdown(f"*Feedback:* {q['feedback'][:300]}...")
                        st.markdown("---")

        st.markdown("<br>", unsafe_allow_html=True)


# ============================================
# DATABASE VIEWER
# ============================================

def show_database_viewer():
    st.markdown("""
    <div class="hero">
        <div class="hero-title" style="font-size: 2.3em;">Database Viewer</div>
        <div class="hero-subtitle">Your interview data at a glance</div>
    </div>
    """, unsafe_allow_html=True)

    interviews_r = api_call("GET", "/interviews/")
    interviews = interviews_r.get("interviews", []) if isinstance(interviews_r, dict) and "error" not in interviews_r else []

    total = len(interviews)
    completed = len([i for i in interviews if i.get("status") == "completed"])
    in_progress = total - completed
    scores = [i["total_score"] for i in interviews if i.get("total_score")]
    avg = round(sum(scores) / len(scores), 1) if scores else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card"><div class="stat-icon">📊</div>
        <div class="stat-value">{total}</div>
        <div class="stat-label">Total</div></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
        <div class="stat-icon">✅</div>
        <div class="stat-value">{completed}</div>
        <div class="stat-label">Completed</div></div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
        <div class="stat-icon">⏳</div>
        <div class="stat-value">{in_progress}</div>
        <div class="stat-label">In Progress</div></div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);">
        <div class="stat-icon">🎯</div>
        <div class="stat-value">{avg}</div>
        <div class="stat-label">Average</div></div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Interview Records")

    if interviews:
        rows = []
        for iv in interviews:
            rows.append({
                "ID": iv.get("id"),
                "Job Role": iv.get("job_role"),
                "Status": iv.get("status", "").title(),
                "Score": f"{iv.get('total_score', 0)}/10",
                "Date": str(iv.get("created_at", ""))[:10],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv,
                           file_name="interviews_data.csv", mime="text/csv",
                           use_container_width=True)
    else:
        st.info("No records yet")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# ADMIN PANEL
# ============================================

def show_admin_panel():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Administrator</div>
        <div class="hero-title" style="font-size: 2.3em;">Admin Panel</div>
        <div class="hero-subtitle">System-wide analytics and user activity</div>
    </div>
    """, unsafe_allow_html=True)

    # Global stats
    stats = api_call("GET", "/admin/stats")
    if "error" in stats:
        st.error(f"Failed to load stats: {stats['error']}")
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="stat-card"><div class="stat-icon">👥</div>
        <div class="stat-value">{stats.get('total_users', 0)}</div>
        <div class="stat-label">Users</div></div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);">
        <div class="stat-icon">📊</div>
        <div class="stat-value">{stats.get('total_interviews', 0)}</div>
        <div class="stat-label">Interviews</div></div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
        <div class="stat-icon">✅</div>
        <div class="stat-value">{stats.get('completed_interviews', 0)}</div>
        <div class="stat-label">Completed</div></div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
        <div class="stat-icon">🎯</div>
        <div class="stat-value">{stats.get('average_score', 0)}</div>
        <div class="stat-label">Avg Score</div></div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
        <div class="stat-icon">🔑</div>
        <div class="stat-value">{stats.get('logins_today', 0)}</div>
        <div class="stat-label">Logins Today</div></div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Users list
    users_r = api_call("GET", "/admin/users")
    if "error" in users_r:
        st.error(f"Failed to load users: {users_r['error']}")
        return

    users = users_r.get("users", [])
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### All Users ({len(users)})")

    if users:
        rows = []
        for u in users:
            rows.append({
                "ID": u["id"],
                "Name": u.get("full_name") or "-",
                "Email": u["email"],
                "Role": "Admin" if u.get("is_admin") else u.get("role", "candidate").title(),
                "Target Role": u.get("target_role") or "-",
                "Interviews": u.get("total_interviews", 0),
                "Avg Score": u.get("avg_score", 0),
                "Activities": u.get("total_activities", 0),
                "Joined": str(u.get("created_at", ""))[:10],
                "Last Login": str(u.get("last_login", ""))[:19] if u.get("last_login") else "Never",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No users yet")

    st.markdown('</div>', unsafe_allow_html=True)

    # User detail drilldown
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### User Activity Details")

    if users:
        user_ids = [u["id"] for u in users]
        selected = st.selectbox("Select user to view details", user_ids,
                                format_func=lambda x: next((u["email"] for u in users if u["id"] == x), str(x)))

        if selected:
            detail = api_call("GET", f"/admin/user/{selected}")
            if isinstance(detail, dict) and "error" not in detail:
                u = detail.get("user", {})
                p = detail.get("profile")

                st.markdown(f"""
                <div class="info-card">
                    <strong>{u.get('full_name', 'User')}</strong> — {u.get('email')}<br>
                    Role: {u.get('role')} • Joined: {str(u.get('created_at', ''))[:10]}<br>
                    Last Login: {str(u.get('last_login', 'Never'))[:19]}
                </div>
                """, unsafe_allow_html=True)

                if p:
                    st.markdown(f"""
                    <div class="info-card">
                        <strong>Profile:</strong><br>
                        Status: {p.get('status', '-')}<br>
                        Education: {p.get('education', '-')}<br>
                        Target Role: {p.get('target_role', '-')}<br>
                        Experience: {p.get('experience_years', 0)} years<br>
                        Skills: {p.get('skills', '-')}
                    </div>
                    """, unsafe_allow_html=True)

                # Interviews
                ivs = detail.get("interviews", [])
                if ivs:
                    st.markdown("**Interview History:**")
                    rows = [{"ID": i["id"], "Role": i["job_role"], "Status": i["status"].title(),
                             "Score": f"{i['total_score']}/10", "Date": str(i["created_at"])[:10]} for i in ivs]
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                # Activities
                acts = detail.get("activities", [])
                if acts:
                    st.markdown("**Recent Activity:**")
                    rows = [{"Action": a["action"], "Details": a.get("details", ""),
                             "Time": str(a["timestamp"])[:19]} for a in acts]
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# MAIN
# ============================================

def main():
    if not st.session_state.token:
        set_page_background("Login")
        show_login()
        return

    if st.session_state.profile is None:
        # Try loading once
        load_profile()

    # If still no profile, show setup
    if not st.session_state.profile:
        set_page_background("ProfileSetup")
        show_profile_setup()
        return

    page = st.session_state.page

    bg_map = {
        "Dashboard": "Dashboard",
        "Profile": "Profile",
        "Resume": "Resume",
        "Interview": "Interview",
        "History": "History",
        "Database": "Database",
        "Admin": "Admin",
    }
    set_page_background(bg_map.get(page, "Dashboard"))

    show_sidebar()

    if page == "Dashboard":
        show_dashboard()
    elif page == "Profile":
        show_profile_page()
    elif page == "Resume":
        show_upload_resume()
    elif page == "Interview":
        show_start_interview()
    elif page == "History":
        show_my_interviews()
    elif page == "Database":
        show_database_viewer()
    elif page == "Admin":
        if is_admin():
            show_admin_panel()
        else:
            st.error("Admin access required")


if __name__ == "__main__":
    main()
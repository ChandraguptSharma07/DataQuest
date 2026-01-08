import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Zero-Day Sentinel",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .metric-card {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #464b5d;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🛡️ Zero-Day Cyber Sentinel")
    with col2:
        st.caption("Live Threat Intelligence Feed")
        st.caption("System Status: ONLINE")

def render_dashboard_structure():
    dashboard, alerts = st.columns([2, 1])
    
    with dashboard:
        st.subheader("📡 Live Threat Stream")
        live_feed_container = st.empty()
        
        st.subheader("📊 Risk Velocity")
        chart_container = st.empty()
        
    with alerts:
        st.subheader("🚨 Critical Alerts")
        alerts_container = st.empty()
        
    return live_feed_container, chart_container, alerts_container

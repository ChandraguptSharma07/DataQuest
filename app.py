import time
import json
import pandas as pd
import streamlit as st
from datetime import datetime
from ui.layout import setup_page, render_header
from ui.chat import render_chat
from utils.email_alerts import send_alert_email

setup_page()
render_header()

# Sidebar with Settings + Chat only
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.toggle("🚫 No Duplicates", value=False, help="Stop showing the same threat twice"):
        with open("stream_config.json", "w") as f:
            json.dump({"deduplicate": True}, f)
    else:
        with open("stream_config.json", "w") as f:
            json.dump({"deduplicate": False}, f)
            
    st.divider()
    render_chat()

if "last_alert_count" not in st.session_state:
    st.session_state.last_alert_count = 0
if "email_sent_ids" not in st.session_state:
    st.session_state.email_sent_ids = set()

def load_jsonl(path):
    try:
        data = []
        with open(path, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return data
    except FileNotFoundError:
        return []

# Demo button in main area
col_button, col_space = st.columns([1, 3])
with col_button:
    if st.button("🔥 Inject Demo Threat"):
        test_threat = {
            "threat_id": f"DEMO-{int(time.time())}",
            "description": "DEMO: Critical nginx vulnerability detected in production server",
            "score": 10.0,
            "timestamp": time.time()
        }
        with open("stream.jsonl", "a") as f:
            f.write(json.dumps(test_threat) + "\n")
        st.success("✅ Threat injected!")


# --- SECTION 1: NIST DATA STREAM ---
st.markdown("## 📡 Live NIST Threat Intelligence")
st.caption("Real-time CVE data from NVD + Simulated threats")
stream_placeholder = st.empty()

# Historical trend chart
st.markdown("### 📈 Threat Detection Timeline")
trend_placeholder = st.empty()

st.markdown("---")

# --- SECTION 2: MATCHED ALERTS ---
st.markdown("## 🎯 Matched Alerts (AI-Analyzed)")
st.caption("Threats that match your inventory • Analyzed by Gemini")

col_alerts, col_stats = st.columns([2, 1])

with col_alerts:
    alerts_placeholder = st.empty()

with col_stats:
    stats_placeholder = st.empty()

# Main Loop
while True:
    # Load data
    stream_data = load_jsonl("stream.jsonl")
    alerts_data = load_jsonl("alerts.jsonl")
    
    # Section 1: Raw Stream
    with stream_placeholder.container():
        if stream_data:
            df = pd.DataFrame(stream_data[-10:])
            if "timestamp" in df.columns:
                df["time"] = pd.to_datetime(df["timestamp"], unit='s').dt.strftime('%H:%M:%S')
            
            cols_to_show = ["time", "threat_id", "description", "score"]
            cols_available = [c for c in cols_to_show if c in df.columns]
            st.dataframe(df[cols_available], use_container_width=True, hide_index=True, height=300)
        else:
            st.info("⏳ Waiting for stream data...")
    
    # Historical trend
    with trend_placeholder.container():
        if stream_data and len(stream_data) > 5:
            df_full = pd.DataFrame(stream_data)
            if "timestamp" in df_full.columns:
                df_full["time"] = pd.to_datetime(df_full["timestamp"], unit='s')
                # Count threats per minute
                df_full['minute'] = df_full['time'].dt.floor('T')
                counts = df_full.groupby('minute').size().reset_index(name='threats')
                counts = counts.tail(20)  # Last 20 minutes
                st.line_chart(counts.set_index('minute')['threats'])
    
    # Section 2: Matched Alerts
    with alerts_placeholder.container():
        st.markdown("### 🎯 AI-Analyzed Alerts")
        if alerts_data:
            for item in alerts_data[-5:]:
                product = item.get('product', 'Unknown')
                desc = item.get('description', '')
                score = item.get('score', 0)
                analysis = item.get('analysis', 'Pending...')
                
                # Determine status
                status_class = "info"
                badge_html = '<span class="alert-badge badge-info">INFO</span>'
                
                if score >= 9.0:
                    status_class = "critical"
                    badge_html = '<span class="alert-badge badge-critical">CRITICAL</span>'
                elif score >= 7.0:
                    status_class = "warning"
                    badge_html = '<span class="alert-badge badge-warning">HIGH</span>'

                # Render Card HTML
                st.markdown(f"""
                <div class="alert-card {status_class}">
                    <div class="alert-header">
                        <span class="alert-product">{product}</span>
                        {badge_html}
                    </div>
                    <div style="color: #888; font-size: 0.8rem; margin-bottom: 8px;">{desc[:100]}...</div>
                    <div class="ai-box">
                        <div class="ai-label">🤖 Gemini Insight</div>
                        <div class="ai-text">{analysis}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.container(border=True).info("✅ System Secure. No active threats.")
    
    # Stats Panel
    with stats_placeholder.container():
        total_stream = len(stream_data)
        total_alerts = len(alerts_data)
        match_rate = (total_alerts / total_stream * 100) if total_stream > 0 else 0
        
        st.metric("Stream Events", total_stream)
        st.metric("Matched Alerts", total_alerts)
        st.metric("Match Rate", f"{match_rate:.1f}%")
    
    # Toast on NEW alerts + Email for ALL threats
    if len(alerts_data) > st.session_state.last_alert_count:
        new_items = alerts_data[st.session_state.last_alert_count:]
        for item in new_items:
            st.toast(f"🚨 Match: {item.get('product', 'Unknown')}", icon="🔥")
            
            # Send email for ALL threats
            threat_id = item.get('threat_id', '')
            if threat_id not in st.session_state.email_sent_ids:
                if send_alert_email(item):
                    st.session_state.email_sent_ids.add(threat_id)
        
        st.session_state.last_alert_count = len(alerts_data)
    
    # Slower refresh = faster UI (increase from 2 to 5 seconds)
    time.sleep(5)

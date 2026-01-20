import time
import html
import streamlit as st

def trigger_alert(data: dict):
    """
    Shows a toast for serious threats.
    Safe (XSS escaped) + Throttled (3s).
    """
    # 1. Anti-Flood: Don't spam toasts
    now = time.time()
    last = st.session_state.get("last_toast", 0)
    
    if now - last < 3.0:
        return 

    score = data.get("score", 0)
    # 2. XSS Fix: Escape the product name!
    prod_safe = html.escape(data.get("product", "Unknown"))
    
    if score >= 9.0:
        st.session_state.last_toast = now
        st.toast(f"🚨 CRITICAL: {prod_safe} (Score: {score})", icon="🔥")
        
    elif score >= 7.0:
        st.session_state.last_toast = now
        st.toast(f"⚠️ Risk: {prod_safe}", icon="⚠️")

def render_critical_section(alerts: list):
    """Render premium styled critical alerts."""
    criticals = [a for a in alerts if a.get("score", 0) >= 9.0]
    
    if not criticals:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #065f46 0%, #047857 100%);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        ">
            <span style="font-size: 2rem;">✅</span>
            <p style="color: #fff; margin: 0.5rem 0 0 0; font-weight: 500;">All Systems Secure</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for item in criticals[-3:]:
        product = html.escape(str(item.get('product', 'Unknown')))
        analysis = html.escape(str(item.get('analysis', 'N/A')))[:200]
        threat_id = html.escape(str(item.get('threat_id', 'N/A')))
        score = item.get('score', 0)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid #ef4444;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #fca5a5; font-weight: 600;">🔥 {product}</span>
                <span style="
                    background: #dc2626;
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-size: 0.7rem;
                    color: #fff;
                ">SCORE: {score}</span>
            </div>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin: 0.5rem 0 0 0;">{analysis}</p>
            <p style="color: rgba(255,255,255,0.5); font-size: 0.7rem; margin-top: 0.5rem;">ID: {threat_id}</p>
        </div>
        """, unsafe_allow_html=True)

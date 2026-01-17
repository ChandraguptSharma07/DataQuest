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
    st.markdown("### 🚨 Critical Alerts")
    
    # Filter for >= 9.0
    criticals = [a for a in alerts if a.get("score", 0) >= 9.0]
    
    if not criticals:
        st.success("System Secure.")
        return

    # Show last 3 only
    for item in criticals[-3:]:
        with st.container(border=True):
            st.markdown(f"**{item['product']}**")
            st.error(item['analysis'])
            st.caption(f"ID: {item['threat_id']} | Score: {item['score']}")

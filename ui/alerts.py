import streamlit as st
import time

def trigger_alert(threat_data: dict):
    """
    Triggers UI alerts for high-priority threats.
    1. Visual Toast Notification.
    2. (Optional) Audio Alert.
    """
    score = threat_data.get("score", 0)
    
    if score >= 9.0:
        # CRITICAL ALERT
        msg = f"🚨 CRITICAL THREAT: {threat_data.get('product', 'Unknown')} (Score: {score})"
        st.toast(msg, icon="🔥")
        # In a real app, play a siren sound here
        # play_sound("siren.mp3") 
        
    elif score >= 7.0:
        # HIGH ALERT
        msg = f"⚠️ High Risk: {threat_data.get('product', 'Unknown')}"
        st.toast(msg, icon="⚠️")

def render_critical_section(alerts: list):
    """
    Renders the 'Critical Alerts' request in the sidebar or main dashboard.
    """
    st.markdown("### 🚨 Critical Alerts")
    
    criticals = [a for a in alerts if a.get("score", 0) >= 9.0]
    
    if not criticals:
        st.success("No Critical Threats Detected (System Secure)")
        return

    for alert in criticals[-3:]: # Show last 3
        with st.container(border=True):
            st.markdown(f"**{alert['product']}**")
            st.error(alert['analysis'])
            st.caption(f"Threat ID: {alert['threat_id']} | Score: {alert['score']}")

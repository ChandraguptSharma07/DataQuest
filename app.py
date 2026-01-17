import time
import json
import pandas as pd
import streamlit as st
from ui.layout import setup_page, render_header, render_dashboard_structure
from ui.alerts import trigger_alert, render_critical_section

setup_page()
render_header()
live_container, chart_container, alerts_container = render_dashboard_structure()

# Session State to track seen alerts (avoid re-toasting)
if "last_count" not in st.session_state:
    st.session_state.last_count = 0

def load_alerts():
    try:
        data = []
        with open("alerts.jsonl", "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue # Skip partial lines
        return data
    except FileNotFoundError:
        return []

placeholder = st.empty()

while True:
    alerts = load_alerts()
    current_count = len(alerts)
    
    # CHECK FOR NEW ALERTS
    if current_count > st.session_state.last_count:
        new_items = alerts[st.session_state.last_count:]
        for item in new_items:
            trigger_alert(item)
        st.session_state.last_count = current_count
    
    if alerts:
        df = pd.DataFrame(alerts)
        
        with live_container:
            st.dataframe(
                df[["timestamp", "description", "product", "analysis"]].tail(10),
                use_container_width=True,
                hide_index=True
            )
            
        with chart_container:
            if not df.empty and "product" in df.columns:
                counts = df.groupby("product").size()
                st.bar_chart(counts)
            
        with alerts_container:
            render_critical_section(alerts)
    
    else:
        with live_container:
            st.info("Waiting for Logic Engine to produce alerts...")

    time.sleep(1)

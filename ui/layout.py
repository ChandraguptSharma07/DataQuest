import streamlit as st

def setup_page():
    """Configure Streamlit for premium obsidian theme."""
    st.set_page_config(
        page_title="Zero-Day Sentinel",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Deep Obsidian Theme - Minimalist & High Contrast
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
    
    /* Global Reset */
    .stApp {
        background-color: #050505; /* True Black */
        color: #e0e0e0;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    p, div {
        font-family: 'Inter', sans-serif;
    }
    
    code {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Hero Section */
    .hero-box {
        border-bottom: 1px solid #333;
        padding-bottom: 2rem;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3rem !important;
        background: linear-gradient(90deg, #ffffff 0%, #a5a5a5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    .hero-subtitle {
        color: #666;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Cards */
    .stCard {
        background: #111;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }

    /* Buttons */
    .stButton > button {
        background: #fff !important;
        color: #000 !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255,255,255,0.3);
    }
    
    /* Success/Error/Warning override */
    .stAlert {
        background: #111 !important;
        border: 1px solid #333 !important;
    }
    
    /* DataFrame */
    div[data-testid="stDataFrame"] {
        border: 1px solid #333;
        border-radius: 8px;
    }
    
    /* Custom Alert Card */
    .alert-card {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid #333;
    }
    
    .alert-card.critical { border-left-color: #ff3b30; }
    .alert-card.warning { border-left-color: #ffcc00; }
    
    .alert-header {
        display: flex;
        justify_content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .alert-product {
        font-weight: 700;
        font-size: 0.95rem;
        color: #fff;
    }
    
    .alert-badge {
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .badge-critical { background: rgba(255, 59, 48, 0.2); color: #ff3b30; }
    .badge-warning { background: rgba(255, 204, 0, 0.2); color: #ffcc00; }
    .badge-info { background: rgba(0, 122, 255, 0.2); color: #007aff; }

    .ai-box {
        margin-top: 12px;
        padding: 10px;
        background: #111;
        border-radius: 6px;
        border-left: 2px solid #007aff;
    }
    
    .ai-label {
        font-size: 0.7rem;
        color: #007aff;
        font-weight: 700;
        margin-bottom: 4px;
        text-transform: uppercase;
    }
    
    .ai-text {
        font-size: 0.85rem;
        color: #ccc;
        line-height: 1.4;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #fff !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #666 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the high-contrast header."""
    st.markdown("""
    <div class="hero-box">
        <h1 class="hero-title">Zero-Day Sentinel</h1>
        <div class="hero-subtitle">Real-Time Threat Intelligence & AI Analysis</div>
    </div>
    """, unsafe_allow_html=True)

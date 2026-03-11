"""
theme.py — Design system moderno e accattivante
"""

import streamlit as st

def apply_theme():
    """Applica il tema moderno all'intera app"""
    st.set_page_config(
        page_title="Tennis Challenge",
        page_icon="🎾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # CSS moderno e minimalista
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #F8FAFB 0%, #FFFFFF 100%);
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header/Title */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid rgba(15, 23, 42, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Metric boxes */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.4) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(15, 23, 42, 0.1);
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        transform: translateY(-2px);
    }
    
    /* Container */
    .stContainer {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(15, 23, 42, 0.1), transparent);
        margin: 2rem 0;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        box-shadow: 0 12px 24px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Radio/Select */
    .stRadio > label, .stSelectbox > label {
        color: #0F172A;
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);
        border-radius: 10px;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Plotly chart */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Captions e text */
    .stCaption {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 400;
    }
    
    /* Link */
    a {
        color: #3B82F6;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #2563EB;
        text-decoration: underline;
    }
    
    /* Data frame */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    }
    
    </style>
    """, unsafe_allow_html=True)

# Colori moderni
COLORS = {
    "primary": "#3B82F6",      # Blu vibrante
    "secondary": "#8B5CF6",    # Viola
    "success": "#10B981",      # Verde
    "danger": "#EF4444",       # Rosso
    "warning": "#F59E0B",      # Arancione
    "dark": "#0F172A",         # Grigio scuro
    "light": "#F8FAFB",        # Grigio chiaro
}

def metric_card(label: str, value, suffix: str = ""):
    """Crea una card metrica elegante"""
    st.metric(label, f"{value}{suffix}")

def section_header(title: str, description: str = ""):
    """Header di sezione con stile"""
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        st.markdown("▸")
    with col2:
        st.markdown(f"## {title}")
        if description:
            st.caption(description)


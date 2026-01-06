import streamlit as st
import styles

st.set_page_config(
    page_title="Medical Advisor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

styles.load_css()

import streamlit as st
import styles

st.set_page_config(
    page_title="Medical Advisor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

styles.load_css()

# --- HERO SECTION ---
st.markdown("<br><br>", unsafe_allow_html=True)
col_hero_L, col_hero_R = st.columns([2, 1])

with col_hero_L:
    st.markdown('<h1 style="font-size: 3.5rem; line-height: 1.2;">Your Personal <br> <span class="gradient-text">AI Medical Assistant</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: #64748b; margin-top: 1rem; margin-bottom: 2rem; max-width: 600px;">Unlock insights from your prescriptions instantly. Private, accurate, and available 24/7 in your preferred language.</p>', unsafe_allow_html=True)
    
    if st.button("Start New Analysis 🚀", type="primary"):
        st.switch_page("pages/1_Analyze.py")

with col_hero_R:
    # Minimalistic Illustration or visual
    st.image("https://img.freepik.com/free-vector/telemedicine-concept-illustration_114360-1691.jpg?w=740", width=400)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- FEATURES ---
st.markdown('<h3 style="text-align:center; font-weight:600; margin-bottom: 2rem; color:#1e293b;">Why choose us?</h3>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(styles.card("📄", "Smart Extraction", "Upload any PDF or Image. We extract text with high precision."), unsafe_allow_html=True)

with c2:
    st.markdown(styles.card("🧠", "Medical Intelligence", "Get simplified explanations of dosages, side effects, and care instructions."), unsafe_allow_html=True)

with c3:
    st.markdown(styles.card("🛡️", "Privacy First", "Your health data is processed securely and never stored permanently."), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

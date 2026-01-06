import streamlit as st
import styles

st.set_page_config(page_title="Settings", page_icon="⚙️")

# Load Styles
styles.load_css()

st.title("⚙️ Personalization Settings")

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Language & format")
    
    # Initialize session state for settings if not present
    if 'language' not in st.session_state:
        st.session_state.language = "English"
    if 'detail_level' not in st.session_state:
        st.session_state.detail_level = "Standard"
    if 'focus_area' not in st.session_state:
        st.session_state.focus_area = "General Overview"

    # Languages
    LANGUAGES = {
        "English": "English",
        "हिंदी (Hindi)": "Hindi",
        "தமிழ் (Tamil)": "Tamil",
        "తెలుగు (Telugu)": "Telugu",
        "ಕನ್ನಡ (Kannada)": "Kannada",
        "മലയാളം (Malayalam)": "Malayalam",
        "বাংলা (Bengali)": "Bengali",
        "मराठी (Marathi)": "Marathi",
        "ગુજરાતી (Gujarati)": "Gujarati",
        "ਪੰਜਾਬੀ (Punjabi)": "Punjabi"
    }

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Language**")
        selected_lang_key = st.selectbox(
            "Select language:",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state.language) if st.session_state.language in LANGUAGES else 0,
            label_visibility="collapsed"
        )
        st.session_state.language = selected_lang_key

    with col2:
        st.markdown("**Focus Area**")
        focus_options = [
            "General Overview", 
            "Medication Focus", 
            "Diet & Lifestyle Focus",
            "Side Effects & Safety",
            "Drug Interactions",
            "Daily Routine Plan"
        ]
        selected_focus = st.selectbox(
            "Focus:",
            options=focus_options,
            index=focus_options.index(st.session_state.focus_area) if st.session_state.focus_area in focus_options else 0,
            label_visibility="collapsed"
        )
        st.session_state.focus_area = selected_focus

    st.divider()

    st.subheader("Report Detail")
    detail_options = ["ELI5 (Child-like)", "Simple Summary", "Standard", "Detailed", "Medical Professional"]
    selected_detail = st.select_slider(
        "Select complexity:",
        options=detail_options,
        value=st.session_state.detail_level if st.session_state.detail_level in detail_options else "Standard"
    )
    st.session_state.detail_level = selected_detail
    
    st.markdown('</div>', unsafe_allow_html=True)

# st.success("✅ Preferences saved automatically. Navigate to **Home** or **Analyze**.")

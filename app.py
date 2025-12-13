import streamlit as st
import requests
import base64
from PIL import Image
import io
import json

# Page configuration
st.set_page_config(
    page_title="Medical Prescription Analyzer",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1e88e5;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1e88e5;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prescription_text' not in st.session_state:
    st.session_state.prescription_text = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""

# Supported languages
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

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def extract_text_gemini(image, api_key):
    """Extract text from image using Gemini Vision API"""
    try:
        base64_image = encode_image_to_base64(image)
        
        # ✅ Updated model and endpoint
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Extract all text from this medical prescription image. "
                                "Include medicine names, dosages, instructions, and doctor's notes. "
                                "Be accurate and preserve structure."
                            )
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2000}
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            extracted_text = result['candidates'][0]['content']['parts'][0]['text']
            return extracted_text, None
        else:
            return None, f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return None, f"Error: {str(e)}"


def analyze_prescription_gemini(prescription_text, language, api_key):
    """Analyze prescription using Gemini Text Model"""
    try:
        # ✅ Updated to latest text-capable model
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        prompt = f"""You are an experienced medical advisor. A patient has shared their prescription:

{prescription_text}

Provide a clear and patient-friendly analysis in {language}:

1. Medical Condition Diagnosis  
2. Medication Explanation  
3. Precautions & Side Effects  
4. Dietary Recommendations (foods to eat/avoid)  
5. Lifestyle Advice (exercise, sleep, habits)  
6. When to Seek Immediate Help  
7. General Care Tips

If the language is not English, write the entire response naturally in that language."""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 3000}
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['candidates'][0]['content']['parts'][0]['text']
            return analysis, None
        else:
            return None, f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return None, f"Error: {str(e)}"


# ---------- UI ----------
st.markdown('<h1 class="main-header">🏥 Medical Prescription Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload your prescription and get personalized health guidance</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    gemini_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Get your FREE API key from https://makersuite.google.com/app/apikey"
    )
    
    if not gemini_api_key:
        st.info("👆 Enter your Gemini API key to continue.")
    
    selected_language = st.selectbox("🌐 Select Language for Analysis", list(LANGUAGES.keys()), index=0)
    
    st.markdown("---")
    st.markdown("""
    ### 📋 Instructions
    1. Get a FREE API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Enter API key above
    3. Choose your language
    4. Upload or capture your prescription
    5. Get your analysis
    
    ⚠️ **Disclaimer**: Informational use only. Always consult a doctor.
    """)

# Main area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload Prescription")
    
    upload_option = st.radio("Choose input method:", ["Upload Image", "Capture from Camera"])
    
    uploaded_image = None
    if upload_option == "Upload Image":
        uploaded_file = st.file_uploader("Choose image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
    else:
        camera_image = st.camera_input("Capture prescription")
        if camera_image:
            uploaded_image = Image.open(camera_image)
    
    if uploaded_image:
        st.image(uploaded_image, caption="Prescription Image", use_container_width=True)
        
        if st.button("🔍 Extract & Analyze Prescription"):
            if not gemini_api_key:
                st.error("⚠️ Please enter your Gemini API key first!")
            else:
                with st.spinner("Extracting text..."):
                    extracted_text, error = extract_text_gemini(uploaded_image, gemini_api_key)
                    
                    if error:
                        st.error(error)
                    else:
                        st.session_state.prescription_text = extracted_text
                        st.success("✅ Text extracted successfully!")
                        
                        with st.spinner(f"Analyzing in {LANGUAGES[selected_language]}..."):
                            analysis, error = analyze_prescription_gemini(
                                extracted_text, LANGUAGES[selected_language], gemini_api_key
                            )
                            
                            if error:
                                st.error(error)
                            else:
                                st.session_state.analysis_result = analysis
                                st.success("✅ Analysis complete!")

with col2:
    st.subheader("📄 Results")
    
    if st.session_state.prescription_text:
        with st.expander("📝 Extracted Prescription Text", expanded=False):
            st.text_area(
                "Prescription Content:",
                st.session_state.prescription_text,
                height=200,
                disabled=True
            )
    
    if st.session_state.analysis_result:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 🩺 Medical Analysis & Guidance")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(st.session_state.analysis_result)
        
        st.download_button(
            label="📥 Download Analysis",
            data=st.session_state.analysis_result,
            file_name="prescription_analysis.txt",
            mime="text/plain"
        )



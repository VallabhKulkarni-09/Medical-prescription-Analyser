import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
import pypdf
import styles

# Load Custom Styles
styles.load_css()

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Page configuration
st.set_page_config(page_title="Analysis", page_icon="🧬", layout="wide")

# Session State for History
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Helper Functions
def extract_text_from_pdf(pdf_file):
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip(), None
    except Exception as e:
        return None, f"Error: {str(e)}"

def analyze_prescription(content, input_type, settings):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Simple Prompt Construction
        lang = settings.get('language', 'English')
        detail = settings.get('detail_level', 'Standard')
        detail_level = settings.get('detail_level', 'Standard') # Renamed 'detail' to 'detail_level' for clarity
        focus_area = settings.get('focus_area', 'General Overview')
        
        detail_instruction = ""
        if detail_level == "ELI5 (Child-like)":
             detail_instruction = "Explain like I'm 5 years old. Use analogies, very simple words, and friendly tone."
        elif detail_level == "Simple Summary":
             detail_instruction = "Provide a very simple, easy-to-understand summary. Avoid complex medical jargon."
        elif detail_level == "Detailed":
             detail_instruction = "Provide a comprehensive report including mechanism of action and detailed side effects."
        elif detail_level == "Medical Professional":
             detail_instruction = "Provide a highly technical analysis suitable for a doctor, using precise medical terminology."
        else: # Standard
             detail_instruction = "Provide a clear and balanced patient-friendly analysis."
        
        focus_instruction = ""
        if focus_area == "Medication Focus":
            focus_instruction = "Prioritize explaining medications, dosage, and biological effects."
        elif focus_area == "Diet & Lifestyle Focus":
            focus_instruction = "Prioritize dietary changes and lifestyle modifications suitable for the condition."
        elif focus_area == "Side Effects & Safety":
            focus_instruction = "Prioritize a detailed analysis of potential side effects, contraindications, and warning signs."
        elif focus_area == "Drug Interactions":
            focus_instruction = "Prioritize checking for interactions between prescribed drugs and common foods, supplements, or other drugs."
        elif focus_area == "Daily Routine Plan":
            focus_instruction = "Create a structured daily schedule (Morning, Afternoon, Evening) for taking medicines and following care tips."
            
        prompt = f"""You are a helpful medical assistant.
User Context: Language={lang}, Detail={detail_level}, Focus={focus_area}.
Instruction: {detail_instruction}
Focus Analysis on: {focus_instruction}

Task: Analyze the provided medical prescription.
Output: strictly cleanly formatted Markdown. Using bolding for key terms.
"""
        if input_type == "text":
             response = model.generate_content([prompt, content])
        elif input_type == "image":
             response = model.generate_content([prompt, content])
             
        return response.text, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# --- Layout ---

# Display Chat History
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.download_button(
                label="📥 Download Report",
                data=message["content"],
                file_name=f"medical_report_{i}.md",
                mime="text/markdown",
                key=f"download_{i}"
            )

# If no history, show welcome
if not st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Upload a prescription to begin</h2>", unsafe_allow_html=True)


# File Uploader (acting as input) - Placed in a container to mimic bottom input bar
with st.container():
    uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg', 'pdf'], key="uploader", label_visibility="collapsed")
    
    if uploaded_file:
        file_type = "pdf" if uploaded_file.type == "application/pdf" else "image"
        
        # Preview and Action Button
        col_prev, col_btn = st.columns([3, 1])
        with col_prev:
            st.caption(f"Ready to analyze: {uploaded_file.name}")
            
        with col_btn:
            analyze_clicked = st.button("🚀 Analyze", type="primary", use_container_width=True)
            
        if analyze_clicked:
            # Add User Message to History immediately
            user_msg = f"📄 **Uploaded:** {uploaded_file.name}"
            
            # Logic to handle Image in history? For now, we stick to text references to save state size,
            # but we show the preview during processing.
            
            with st.spinner("Analyzing document..."):
                settings = {
                    "language": st.session_state.get('language', 'English'),
                    "detail_level": st.session_state.get('detail_level', 'Standard'),
                    "focus_area": st.session_state.get('focus_area', 'General Overview')
                }
                
                analysis = ""
                error = None
                
                if file_type == "pdf":
                    text, err = extract_text_from_pdf(uploaded_file)
                    if err: error = err
                    else: analysis, error = analyze_prescription(text, "text", settings)
                else:
                    img = Image.open(uploaded_file)
                    analysis, error = analyze_prescription(img, "image", settings)

                if error:
                    st.error(error)
                else:
                    # Success: Update History
                    st.session_state.messages.append({"role": "user", "content": user_msg})
                    st.session_state.messages.append({"role": "assistant", "content": analysis})
                    st.rerun()

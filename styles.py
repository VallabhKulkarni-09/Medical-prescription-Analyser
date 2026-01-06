import streamlit as st

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Animation */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            color: #1e293b; 
        }

        /* ---------------------------------
           1. CORE ELEMENTS & OVERRIDES
           --------------------------------- */
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Header cleaner */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9; 
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8; 
        }

        /* ---------------------------------
           2. TYPOGRAPHY & HERO
           --------------------------------- */
        .gradient-text {
            background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* ---------------------------------
           3. UI COMPONENTS (Cards, Buttons)
           --------------------------------- */
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            animation: fadeIn 0.6s ease-out;
        }

        .hover-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border: 1px solid #f1f5f9;
            height: 100%;
        }
        
        .hover-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #e2e8f0;
        }

        /* Primary Button Upgrade */
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
            color: white; /* Ensure text stays white */
        }
        
        /* ---------------------------------
           4. CHAT INTERFACE
           --------------------------------- */
        [data-testid="stChatMessage"] {
            background: transparent;
            padding: 1.5rem;
            border-radius: 12px;
            transition: background 0.2s;
        }
        
        /* User Bubble */
        [data-testid="stChatMessage"][data-testid="user"] {
            background-color: transparent; 
        }
        
        /* Assistant Bubble */
        [data-testid="stChatMessage"][data-testid="assistant"] {
            background: #f8fafc;
        }

        /* File Uploader Customization */
        [data-testid="stFileUploader"] section {
            background-color: #f8fafc;
            border: 1px dashed #cbd5e1;
            box-shadow: none;
        }
        [data-testid="stFileUploader"] section:hover {
            background-color: #f1f5f9;
            border-color: #94a3b8;
        }
        </style>
    """, unsafe_allow_html=True)

def card(icon, title, desc):
    return f"""
    <div class="hover-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="font-size: 1.1rem; font-weight: 600; color: #0f172a; margin: 0 0 0.5rem 0;">{title}</h3>
        <p style="font-size: 0.9rem; color: #64748b; margin: 0; line-height: 1.5;">{desc}</p>
    </div>
    """

import streamlit as st
import PyPDF2
import dspy

# 1. Configure page for a sleek, app-like feel
st.set_page_config(
    page_title="RoastMyResume | Brutal AI Feedback",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inject High-Contrast, Minimalist CSS
st.markdown("""
    <style>
    /* Clean up the canvas */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 750px;
    }
    
    /* Hide default Streamlit branding for a white-label look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Typography */
    h1 {
        font-weight: 900 !important;
        letter-spacing: -1.5px;
        text-align: center;
        margin-bottom: 0rem;
        font-size: 3.5rem !important;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 3rem;
        letter-spacing: -0.5px;
    }
    
    /* High-contrast dropzone to draw the eye */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #ff4b4b !important;
        border-radius: 12px;
        background-color: transparent;
        transition: all 0.3s ease;
        padding: 2rem;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        background-color: rgba(255, 75, 75, 0.05);
        border-color: #ff0000 !important;
    }
    
    /* Styled Roast Output Card */
    .roast-card {
        background-color: #1e1e1e; /* Dark theme card */
        color: #f1f1f1;
        border-left: 4px solid #ff4b4b;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        font-size: 1.05rem;
        line-height: 1.7;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Minimalist Footer */
    .custom-footer {
        text-align: center;
        margin-top: 4rem;
        font-size: 0.85rem;
        color: #666;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1.5rem;
    }
    .custom-footer a {
        color: #ff4b4b;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
    }
    .custom-footer a:hover {
        color: #ff0000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Setup LLM Backend
@st.cache_resource(show_spinner=False)
def configure_dspy_llm(gemini_api_key):
    llm = dspy.LM(model='gemini/gemini-1.5-flash-latest', api_key=gemini_api_key)
    dspy.settings.configure(lm=llm)
    return llm

# Initialize without disrupting the UI
llm = configure_dspy_llm(st.secrets["GEMINI_API"])

class RoastSignature(dspy.Signature):
    """You are professional resume roaster that delivers scathing critiques as much as you can based on uploaded content."""
    content: str = dspy.InputField(desc="The user's uploaded resume content.")
    roast_answer: str = dspy.OutputField(desc="The roast for the user's resume as badly as you can")

# 4. Hero Section
st.markdown("<h1>RoastMyResume.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload your weak resume. Get brutally honest AI feedback. 🔥</p>", unsafe_allow_html=True)

# 5. Interactive Uploader
uploaded_file = st.file_uploader(
    label="Drop your PDF here", 
    type="pdf", 
    accept_multiple_files=False,
    label_visibility="hidden" # Hides the default label for a cleaner look
)

# 6. Core Logic & Micro-interactions
if uploaded_file:
    try:
        # Custom loading state to build anticipation
        with st.spinner("Analyzing your life choices..."):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            content = ''.join([page.extract_text() for page in pdf_reader.pages])
            
            roast_chain = dspy.ChainOfThought(signature=RoastSignature)
            roast = roast_chain(content=content).roast_answer
        
        # Immediate visual feedback upon completion
        st.toast("Ouch. That's gonna leave a mark.", icon="🔥")
        
        # Display output in the styled card
        st.markdown(f"""
            <div class="roast-card">
                {roast}
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Something broke. Probably your resume formatting: {e}")
else:
    # Empty state placeholder
    st.markdown("<div style='text-align: center; color: #555; margin-top: 2rem; font-size: 0.9rem;'>Waiting for a victim...</div>", unsafe_allow_html=True)

# 7. Sleek Footer
st.markdown(f"""
    <div class="custom-footer">
        Transforming weak resumes into job-winning powerhouses.<br><br>
        <a href="https://www.linkedin.com/in/tanay--gupta/" target="_blank">LinkedIn</a> • 
        <a href="https://tanay-gupta.github.io/MyPortfolio" target="_blank">Portfolio</a> • 
        <a href="https://www.instagram.com/tanaywhooodes/" target="_blank">Instagram</a>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import PyPDF2
import dspy

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="RoastMyResume",
    page_icon="🔥",
    layout="centered"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    color: #f5f5f5;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit default header */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Hero Title */
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
}

.hero-sub {
    text-align: center;
    font-size: 1.1rem;
    color: #aaaaaa;
    margin-bottom: 3rem;
}

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Roast Output */
.roast-box {
    background: rgba(255, 87, 87, 0.08);
    border: 1px solid rgba(255, 87, 87, 0.3);
    padding: 1.5rem;
    border-radius: 16px;
    margin-top: 2rem;
    font-size: 1.05rem;
}

/* Upload Button */
.stFileUploader > div {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 0.5rem;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #777;
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DSPY CONFIG --------------------
@st.cache_resource
def configure_dspy_llm(gemini_api_key):
    llm = dspy.LM(model='gemini/gemini-1.5-flash-latest', api_key=gemini_api_key)
    dspy.settings.configure(lm=llm)
    return llm

llm = configure_dspy_llm(st.secrets["GEMINI_API"])

# -------------------- HERO SECTION --------------------
st.markdown('<div class="hero-title">🔥 RoastMyResume</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Where weak resumes get fired up. Brutally honest AI feedback that actually helps.</div>',
    unsafe_allow_html=True
)

# -------------------- ROAST SIGNATURE --------------------
class RoastSignature(dspy.Signature):
    """You are a professional resume roaster who delivers brutally honest but insightful critiques."""
    content: str = dspy.InputField()
    roast_answer: str = dspy.OutputField()

# -------------------- MAIN CARD --------------------
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type="pdf",
        accept_multiple_files=False
    )

    if uploaded_file:
        try:
            with st.spinner("Analyzing... sharpening the knives 🔪"):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                content = ''.join([page.extract_text() or "" for page in pdf_reader.pages])

                roast_resume = dspy.ChainOfThought(signature=RoastSignature)
                roast = roast_resume(content=content).roast_answer

            st.markdown(
                f'<div class="roast-box"><strong>🔥 Here’s your roast:</strong><br><br>{roast}</div>',
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error processing file: {e}")

    else:
        st.markdown("Drop your PDF resume above and let’s see if it survives.")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("""
<div class="footer">
Built by Tanay Gupta •
<a href="https://www.linkedin.com/in/tanay--gupta/" target="_blank">LinkedIn</a> •
<a href="https://tanay-gupta.github.io/MyPortfolio" target="_blank">Portfolio</a> •
<a href="https://www.instagram.com/tanaywhooodes/" target="_blank">Instagram</a>
</div>
""", unsafe_allow_html=True)

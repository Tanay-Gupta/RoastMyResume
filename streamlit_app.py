import streamlit as st
# Configure Streamlit page
st.set_page_config(
    page_title="RoastMyResume – Where Weak Resumes Get Fired Up!",
    page_icon="🔥",
    layout="centered"
)
import PyPDF2
import dspy

# Function to set up the Google Gemini model and configure dspy
@st.cache_resource
def configure_dspy_llm(gemini_api_key):
    llm = dspy.LM(model='gemini/gemini-1.5-flash-latest', api_key=gemini_api_key)
    dspy.settings.configure(lm=llm)
    return llm  # Return the configured llm if you need it later

# Configure DSPy and get the llm
llm = configure_dspy_llm(st.secrets["GEMINI_API"])

# Display the app title and description
st.title("RoastMyResume – Where Weak Resumes Get Fired Up!")
st.write(
    """
    Welcome to **RoastMyResume**, where AI brings the heat! 🔥
    Upload your resume and get a witty, brutally honest roast that helps you level up your job hunt.
    """
)

# Define the roast signature with input and output fields
class RoastSignature(dspy.Signature):
    """You are professional resume roaster that delivers scathing critiques as much as you can based on uploaded content."""
    content: str = dspy.InputField(desc="The user's uploaded resume content.")
    roast_answer: str = dspy.OutputField(desc="The roast for the user's resume as badly as you can")

# Resume file uploader
uploaded_file = st.file_uploader(
    label="Upload Your Resume (PDF format)", type="pdf", accept_multiple_files=False
)

# If a file is uploaded, process it
if uploaded_file:
    try:
        # Extract text content from the uploaded PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        content = ''.join([page.extract_text() for page in pdf_reader.pages])

        # Generate the roast using the AI model
        roast_resume = dspy.ChainOfThought(signature=RoastSignature)
        roast = roast_resume(content=content).roast_answer

        # Display the roast in markdown format
        st.markdown(f"### 🔥 Here's your roast: \n{roast}")
    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Please upload a PDF resume to get started.")

# Footer with links
st.markdown("---")
st.caption("RoastMyResume – Transforming weak resumes into job-winning powerhouses, one roast at a time.")
st.caption("Connect with me: [LinkedIn](https://www.linkedin.com/in/tanay--gupta/) | [Portfolio](https://tanay-gupta.github.io/MyPortfolio) | [Instagram](https://www.instagram.com/tanaywhooodes/) | )")

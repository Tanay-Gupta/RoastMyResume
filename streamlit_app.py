import streamlit as st
import PyPDF2
import dspy 
# Show title and description.
st.title("RoastMyResume – Where Weak Resumes Get Fired Up!")
st.write(
    "At RoastMyResume, we take your lackluster resume and turn it into a masterpiece through witty, honest, and constructive feedback. Whether you're looking for a career boost or just want to see your CV go up in flames (in the best way possible), we’ve got the perfect roast for you. Get ready for tough love that transforms weak resumes into job-winning powerhouses. Your next big opportunity starts here! "
)
llm = dspy.Google(model = 'gemini-1.5-flash-latest', api_key=st.secrets["GEMINI_API "])

class RoastSignature(dspy.Signature):
    """You are professional roaster, you have to roast the user's resume as much as you can based upon the content"""
    content: str = dspy.InputField(desc="containing the user uploaded resume text")
    roast_answer: str = dspy.OutputField(desc="Roast the user's resume as badly as you can")



uploaded_file = st.file_uploader(
        "Upload a Resume (.pdf)", type=("pdf"), accept_multiple_files=False
    )
if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    content=''
    for page in range(len(pdf_reader.pages)):
            content += pdf_reader.pages[page].extract_text()
            
  
    result= dspy.ChainOfThought(signature=RoastSignature)
    roast=result(content=content).roast_answer
        # Stream the response to the app using `st.write_stream`.
    st.write_stream(roast)

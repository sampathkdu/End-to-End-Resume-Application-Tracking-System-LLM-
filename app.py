import streamlit as st 
import google.generativeai as genai 
import os 
import PyPDF2 as pdf 
from dotenv import load_dotenv
import json 

# Load environment variables
load_dotenv() 

# API Key Configuration
#genai.configure(api_key="")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Display the sidebar content
st.sidebar.markdown("""
    ### Developing Team
    
    - **Name:** Hettiarachchi C.L.  
      **Student No:** EC/2020/020  
         
    <hr>

     - **Name:** Premarathna N.R.  
      **Student No:** EC/2020/010  
     
    <hr>

    - **Name:** Jayathilaka P.J.L. 
    **Student No:** EC/2020/027 
    
    <hr>

    - **Name:** Magedara T.T.
      **Student No:** EC/2020/079 
    
    <hr>

    - **Name:** Jayangani H.A.A.
      **Student No:** EC/2020/028

    <hr>
    BECS 32253- Artificial Intelligence
    University of Kelaniya, Sri Lanka


    """, unsafe_allow_html=True)



###########################################################################
#Hide default deploy Button
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}  /* Hides the "Deploy" button and menu */
    footer {visibility: hidden;}    /* Hides the footer */
    header {visibility: hidden;}    /* Hides the header */
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}  /* Hides the "Deploy" button and menu */
    footer {visibility: hidden;}    /* Hides the footer */
    header {visibility: hidden;}    /* Hides the header */
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
##############################################################################


def get_gemini_response(jd, resume_text):
    # Construct a fresh prompt for each submission to avoid context carryover
    prompt = f"""
    You are an ATS (Application Tracking System) that evaluates resumes based on a job description.
    Evaluate the resume's match with the provided job description.
    
    Job Description: {jd}
    Resume: {resume_text}
    
    Provide the following:
    - The match percentage between the job description and the resume.
    - A list of missing keywords or skills based on the job description.
    - A brief profile summary of the candidate, highlighting strengths and weaknesses relative to the job description.
    
    Format the response as:
    {{
        "JD Match": "%", 
        "MissingKeywords": [list of missing keywords],
        "ProfileSummary": "Candidate's summary"
    }}
    """
    # Request to the model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    # Extract text from uploaded PDF resume
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Streamlit app
st.title("QualiMatch(Scan. Match. Hire)")
st.text("Scan Your Resume Through ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the resume as a PDF")

submit = st.button("Scan")

if submit:
    if uploaded_file is not None and jd:
        # Extract text from the uploaded resume PDF
        resume_text = input_pdf_text(uploaded_file)
        
        # Check if the resume is empty
        if not resume_text.strip():
            st.subheader("The uploaded resume is empty.")
        else:
            # Get the response from the AI model
            response = get_gemini_response(jd, resume_text)
            
            # Display the response
            st.subheader(response)
    else:
        st.subheader("Please provide both a job description and a resume.")

import streamlit as st
import google.generativeai as genai
import datetime
import PyPDF2

# --- Page Configuration ---
st.set_page_config(page_title="AI Legal Assistant Bot 🇮🇳", page_icon="⚖️", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
        .stTextArea textarea {font-size: 1.1em;}
        .stButton>button {background-color: #4CAF50; color: white; font-size: 16px; padding: 10px 20px; border-radius: 8px;}
        .stDownloadButton button {background-color: #2196F3; color: white; border-radius: 8px;}
        .main {background-color: #f5f5f5; padding: 20px; border-radius: 15px;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size: 2.5em;'>👩‍⚖️ AI Legal Assistant Bot (India)</h1>
    <p style='font-size: 1.2em;'>Ask about <b>Consumer Rights</b>, <b>Employment Law</b>, <b>RTI</b>, etc.</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("🔐 API Key Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.markdown("[Get a free API key](https://makersuite.google.com/app/apikey)")
    st.markdown("---")
    st.subheader("📄 Upload Legal Document (optional)")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    st.markdown("---")
    st.caption("Built with ❤️ by Suraj")

# --- PDF Extraction Helper ---
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Main Interface ---
st.subheader("📝 Ask Your Legal Question")
question = st.text_area("Type your legal query here:", height=150)

if pdf_file:
    extracted_text = extract_text_from_pdf(pdf_file)
    with st.expander("📃 Extracted Text from PDF"):
        st.write(extracted_text)
    if question.strip() == "":
        question = extracted_text.strip()

# Optional Date Display
st.caption(f"🕒 {datetime.datetime.now().strftime('%A, %d %B %Y %I:%M %p')}")

# --- Action ---
if st.button("🎯 Get Answer"):
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
    elif not question.strip():
        st.warning("Please enter a valid legal question or upload a PDF.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            
            # Add simple keyword hint logic (Indian legal topics)
            if any(keyword in question.lower() for keyword in ["consumer", "rti", "employment", "contract", "section", "ipc", "right"]):
                question = f"Answer according to Indian law: {question}"

            response = model.generate_content(question)

            st.success("✅ Answer:")
            st.markdown(f"**{response.text.strip()}**")

            with st.expander("📋 Copy Answer"):
                st.code(response.text.strip(), language='markdown')

            st.download_button(
                label="📄 Download Answer",
                data=response.text.strip(),
                file_name="legal_answer.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")

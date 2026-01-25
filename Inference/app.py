import json
import streamlit as st
import asyncio
import io
import PyPDF2
from PIL import Image
import pytesseract 
import os
import requests 

# Environment Variables
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:3000") 
LLM_MODEL = os.getenv("LLM_MODEL", "mistral-small-latest")

st.set_page_config(page_title="AI Sales Assistant", page_icon="📝", layout="wide")

# --- UI HEADER ---
st.title("🚀 AI-Powered Commercial Offer Generator")
st.markdown("Upload documents or paste text to generate a commercial proposal.")

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(file_buffer):
    try:
        pdf_reader = PyPDF2.PdfReader(file_buffer)
        return "".join([page.extract_text() or "" for page in pdf_reader.pages])
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def perform_ocr_on_image(image_buffer):
    try:
        image = Image.open(image_buffer).convert("RGB")
        return pytesseract.image_to_string(image)
    except Exception as e:
        st.error(f"OCR Error: {e}")
        return None

async def poll_for_result(submission_id):
    """Wait for backend and return the data."""
    status_placeholder = st.empty()
    for _ in range(45): # 90 seconds timeout
        try:
            res = requests.get(f"{BACKEND_URL}/result/{submission_id}")
            data = res.json()
            status = data.get("Status")
            
            status_placeholder.info(f"System Status: **{status}**")

            if status == "Completed":
                status_placeholder.empty()
                return data.get("FinalOffer")
            
            if status == "Error":
                status_placeholder.empty()
                st.error(f"Backend Error: {data.get('FinalOffer')}")
                return None
        except Exception as e:
            st.error(f"Connection failed: {e}")
            return None
        await asyncio.sleep(2)
    return None

# --- SIDEBAR ---
st.sidebar.header("Configuration")
st.sidebar.info(f"Model: {LLM_MODEL}")

# --- INPUT SECTION ---
input_data = ""
tabs = st.tabs(["📄 Document Upload", "✍️ Raw Text"])

with tabs[0]:
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file:
        file_buffer = io.BytesIO(uploaded_file.getvalue())
        if "pdf" in uploaded_file.type:
            input_data = extract_text_from_pdf(file_buffer)
        else:
            input_data = perform_ocr_on_image(file_buffer)
        if input_data: st.success("Text extracted!")

with tabs[1]:
    input_text_area = st.text_area("Paste request here:", height=200)
    if input_text_area:
        input_data = input_text_area

# --- EXECUTION SECTION ---
if st.button("✨ Generate Commercial Proposal ✨", type="primary", use_container_width=True):
    if not input_data:
        st.error("Please provide some input data first.")
    else:
        with st.status("AI is working...", expanded=True) as status:
            st.write("Submitting request to backend...")
            try:
                payload = {
                    "UsingLLM": LLM_MODEL,
                    "ClientRequest": input_data,
                    "BusinessRules": "Standard margin 15%, include warranty",
                    "Language": "en"
                }
                resp = requests.post(f"{BACKEND_URL}/submit", json=payload)
                resp.raise_for_status()
                task_id = resp.json().get("SubmissionId")
                
                st.write("Processing LLM Inference...")
                final_offer = asyncio.run(poll_for_result(task_id))
                
                if final_offer:
                    st.session_state['final_result'] = final_offer
                    status.update(label="Proposal Generated!", state="complete")
                else:
                    status.update(label="Failed to get result", state="error")
            except Exception as e:
                st.error(f"Execution error: {e}")

# --- DISPLAY & DOWNLOAD SECTION ---
if 'final_result' in st.session_state:
    res = st.session_state['final_result']
    
    proposal_text = res.get("RawMarkdown")
    
    st.divider()
    
    if proposal_text:
        st.subheader("📋 Final Proposal")
        st.markdown(proposal_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Markdown",
                data=proposal_text,
                file_name="proposal.md",
                mime="text/markdown"
            )
        with col2:
            st.download_button(
                label="📥 Download JSON Data",
                data=json.dumps(res, indent=4),
                file_name="offer_data.json",
                mime="application/json"
            )
    else:
        st.warning("⚠️ The backend returned metadata, but the 'RawMarkdown' text field is missing.")
        st.subheader("Raw Data Received:")
        st.json(res)
        
        st.download_button(
            label="📥 Download JSON for Debugging",
            data=json.dumps(res, indent=4),
            file_name="debug_offer.json",
            mime="application/json"
        )
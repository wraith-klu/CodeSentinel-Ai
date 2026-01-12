import requests
import streamlit as st

def download_pdf(discussion_text: str):
    url = "http://127.0.0.1:8000/download-pdf"

    response = requests.post(
        url,
        json={"text": discussion_text},
        timeout=60
    )
    response.raise_for_status()

    st.download_button(
        label="⬇️ Download PDF",
        data=response.content,
        file_name="analysis_report.pdf",
        mime="application/pdf",
    )

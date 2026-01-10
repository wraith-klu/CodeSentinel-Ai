import streamlit as st

def show_analysis(analysis: str):
    """
    Displays formatted LLM + FastAI analysis beautifully.
    """
    st.subheader("🧩 Analysis Results")
    st.markdown(analysis, unsafe_allow_html=True)

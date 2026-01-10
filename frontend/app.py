import streamlit as st
import requests
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
import time

# -------------------------------
# BACKEND ENDPOINTS
# -------------------------------
ANALYZE_URL = "http://127.0.0.1:8000/analyze"
FOLLOWUP_URL = "http://127.0.0.1:8000/followup"

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title=" CodeSentinel AI - 🧠 A Code Smell Detection Agent",
    page_icon="🧩",
    layout="wide",
)

# -------------------------------
# LOAD LOTTIE ANIMATION
# -------------------------------
def load_lottie_url(url: str):
    try:
        return requests.get(url).json()
    except:
        return None

ai_anim = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_t24tpvcu.json")
success_anim = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# -------------------------------
# CUSTOM CSS + POPUP STYLE
# -------------------------------
st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top left, #e6f0ff, #f9fbff); font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #fdfdfd, #eef3ff); border-right: 1px solid #d4d8e0; box-shadow: 2px 0px 8px rgba(0,0,0,0.05); }
section[data-testid="stFileUploader"] { background: rgba(255,255,255,0.7); border-radius: 12px; padding: 16px; border: 1px solid #dcdcdc; backdrop-filter: blur(10px); }
div[data-testid="stExpander"] { background: rgba(255,255,255,0.85); border-radius: 14px !important; border: 1px solid #dce0e8; box-shadow: 0 3px 10px rgba(0,0,0,0.05); }
div.stButton > button { background: linear-gradient(90deg, #0072ff, #00c6ff); color: white; border-radius: 8px; padding: 0.5em 1em; font-weight: 600; border: none; box-shadow: 0 3px 8px rgba(0,0,0,0.15); transition: all 0.2s ease-in-out; font-size: 0.9em; }
div.stButton > button:hover { transform: scale(1.07); background: linear-gradient(90deg, #00c6ff, #0072ff); }
h2, h3, h4 { color: #111; font-weight: 700; }
hr { border: 1px solid #d3d8e0; }
#popup-message { position: fixed; top: 20px; right: 20px; background: white; color: #111; padding: 12px 20px; border-radius: 10px; box-shadow: 0 3px 15px rgba(0,0,0,0.1); font-weight: 600; z-index: 9999; animation: fadeInOut 3s ease-in-out; }
@keyframes fadeInOut { 0% {opacity: 0; transform: translateY(-10px);} 10% {opacity: 1; transform: translateY(0);} 90% {opacity: 1;} 100% {opacity: 0; transform: translateY(-10px);} }
</style>
""", unsafe_allow_html=True)

def popup_message(message, icon="ℹ️"):
    st.markdown(f"<div id='popup-message'>{icon} {message}</div>", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
colored_header(
    label="🧠 Code Smell Detection & Refactoring Dashboard",
    description="Empowered by Hybrid Intelligence — AST + FastAI + LLM (Polaris Alpha)",
    color_name="blue-70",
)
st_lottie(ai_anim, height=180, key="ai_header")

# -------------------------------
# SESSION STATE
# -------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3296/3296716.png", width=120)
    st.markdown("### ⚙️ Project Overview")
    st.markdown("""
    - 🧩 **Analyzes code** for smells & inefficiencies  
    - 🧠 **AI-powered suggestions** using FastAI + LLM  
    - 🔍 **AST-based structure checks**  
    - 🔁 **Interactive follow-up Q&A**
    """)
    st.markdown("---")
    st.markdown("👨‍💻 *Developed by:* **Wraith**")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.markdown("## 📂 Upload & Analyze Code")
uploaded_file = st.file_uploader(
    "Upload your source code file (.py, .java, .cpp, .js):",
    type=["py", "java", "cpp", "js"]
)

col_query, col_buttons = st.columns([3, 1])
with col_query:
    initial_query = st.text_input("💭 Ask about your code:", placeholder="E.g. What smells exist in this file?")
with col_buttons:
    col_analyze, col_reset = st.columns(2)
    analyze_clicked = col_analyze.button("🔍 Analyze", use_container_width=True)
    reset_clicked = col_reset.button("🧹 Reset", use_container_width=True)

# -------------------------------
# RESET BUTTON
# -------------------------------
if reset_clicked:
    popup_message("🔄 Refreshing page...", "♻️")
    time.sleep(1)
    st.session_state.clear()
    st.experimental_rerun()

# -------------------------------
# ANALYZE BUTTON ACTION
# -------------------------------
if analyze_clicked:
    if uploaded_file is None:
        popup_message("⚠️ Please upload a file first.", "⚠️")
    elif not initial_query.strip():
        popup_message("💬 Please enter your question before analyzing.", "💬")
    else:
        with st.spinner("🧠 AI is analyzing your code..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                data = {"user_query": initial_query}
                response = requests.post(ANALYZE_URL, data=data, files=files)
                response.raise_for_status()
                result = response.json()

                st.session_state.session_id = result["llm_analysis"]["session_id"]
                st.session_state.analysis_done = True
                st.session_state.last_result = result

                popup_message("✅ Analysis completed successfully!", "✅")
                st_lottie(success_anim, height=160, key="success")

            except Exception as e:
                st.error(f"❌ Error: {e}")
                popup_message("🚨 Something went wrong during analysis!", "🚨")

# -------------------------------
# RESULTS SECTION
# -------------------------------
if st.session_state.analysis_done and st.session_state.last_result:
    result = st.session_state.last_result
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    # AST Findings
    with st.expander("🧩 AST-Based Findings", expanded=True):
        ast_findings = result["llm_analysis"].get("ast_findings", [])
        if ast_findings:
            for i, finding in enumerate(ast_findings, 1):
                st.markdown(f"* {i}. {finding}")
        else:
            st.info("✅ No AST issues detected.")

    # LLM Insights
    with st.expander("🤖 LLM Insights", expanded=True):
        st.write(result["llm_analysis"].get("llm_response", "No insights available."))

    # FastAI Prediction
    with st.expander("🧠 FastAI Model Prediction", expanded=True):
        model_pred = result["llm_analysis"].get("model_prediction", {})
        if isinstance(model_pred, dict):
            col1, col2 = st.columns(2)
            col1.metric("Detected Smell", model_pred.get("smell_type", "N/A"))
            col2.metric("Confidence", f"{model_pred.get('confidence', 0):.2f}")
            st.json(model_pred.get("all_probs", {}))
        else:
            st.code(model_pred, language="text")

    # Optimized Code
    with st.expander("🧰 Suggested Optimized Code", expanded=True):
        optimized_code = result["llm_analysis"].get("optimized_code", "")
        if optimized_code and "No optimized code" not in optimized_code:
            st.code(optimized_code, language="python")
        else:
            st.info("💡 No optimized version available.")

    # FOLLOW-UP QUERY
    st.markdown("---")
    st.subheader("🔁 Follow-Up Query")
    followup_query = st.text_input(
        "💬 Ask a follow-up question:", key="followup_input", placeholder="E.g. Why is this function smelly?"
    )

    if st.button("📝 Ask Follow-Up", use_container_width=True):
        if not followup_query.strip():
            popup_message("💬 Please enter a follow-up question first.", "⚠️")
        else:
            with st.spinner("Processing your follow-up query... ⏳"):
                try:
                    data = {"user_query": followup_query, "session_id": st.session_state.session_id}
                    response = requests.post(FOLLOWUP_URL, data=data)
                    response.raise_for_status()
                    followup_result = response.json()

                    popup_message("✅ Follow-up answer received!", "📬")
                    st.markdown("### 🤖 Response")
                    st.write(followup_result["llm_analysis"].get("llm_response", ""))

                    optimized_code = followup_result["llm_analysis"].get("optimized_code", "")
                    if optimized_code and "No optimized code" not in optimized_code:
                        st.markdown("### 🧰 Updated Optimized Code")
                        st.code(optimized_code, language="python")

                except Exception as e:
                    popup_message("🚨 Error during follow-up!", "🚨")
                    st.error(f"⚠️ {e}")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#444; font-size:14px;'>"
    "💡 Built with ❤️ by <b>Wraith</b> | Powered by Streamlit + FastAPI + FastAI + Polaris Alpha"
    "</div>",
    unsafe_allow_html=True
)

import streamlit as st
import requests
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
import time
<<<<<<< HEAD
import requests

import threading

=======
import threading
>>>>>>> 4771ee8 (update)

# -------------------------------
# BACKEND ENDPOINTS
# -------------------------------
<<<<<<< HEAD
# ANALYZE_URL = "http://127.0.0.1:8000/analyze"
# FOLLOWUP_URL = "http://127.0.0.1:8000/followup"
=======
# Local testing:
# BASE_API_URL = "http://127.0.0.1:8000"

BASE_API_URL = "https://codesentinel-ai.onrender.com"

ANALYZE_URL = f"{BASE_API_URL}/analyze"
FOLLOWUP_URL = f"{BASE_API_URL}/followup"
DOWNLOAD_URL = f"{BASE_API_URL}/download-pdf"


# -------------------------------
# WAKE BACKEND (NON-BLOCKING)
# -------------------------------
def wake_backend():
    try:
        requests.get(BASE_API_URL, timeout=5)
    except Exception:
        pass

threading.Thread(target=wake_backend, daemon=True).start()

>>>>>>> 4771ee8 (update)

BASE_API_URL = "https://codesentinel-ai.onrender.com"

ANALYZE_URL = f"{BASE_API_URL}/analyze"
FOLLOWUP_URL = f"{BASE_API_URL}/followup"


def wake_backend():
    try:
        requests.get(BASE_API_URL, timeout=5)
    except:
        pass

threading.Thread(target=wake_backend).start()
# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="CodeSentinel AI",
    page_icon="🧩",
    layout="wide",
)

theme_mode = st.toggle("🌗 Dark / Light Mode", value=False)

# -------------------------------
# LOAD LOTTIE (CACHED)
# -------------------------------
@st.cache_data
def load_lottie_url(url: str):
    try:
        return requests.get(url, timeout=10).json()
    except Exception:
        return None


ai_anim = load_lottie_url(
    "https://assets4.lottiefiles.com/packages/lf20_t24tpvcu.json"
)
success_anim = load_lottie_url(
    "https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json"
)

# -------------------------------
# CUSTOM CSS + POPUP STYLE
# -------------------------------
st.markdown(f"""
<style>

/* ==================================================
   THEME VARIABLES
================================================== */
:root {{
    --sky: #38bdf8;
    --indigo: #6366f1;
}}

/* ==================================================
   APP BACKGROUND
================================================== */
.stApp {{
    background:
        {"radial-gradient(circle at top, #0f172a 0%, #020617 45%, #020617 100%)"
        if theme_mode else
        "radial-gradient(circle at top, #f8fbff 0%, #ffffff 60%, #ffffff 100%)"};
    color: {"#e5e7eb" if theme_mode else "#0f172a"};
    font-family: "Inter", system-ui, -apple-system;
    animation: appFade 0.35s ease-in;
}}

/* ==================================================
   HEADER
================================================== */
header[data-testid="stHeader"] {{
    background:
        {"linear-gradient(90deg, #020617, #0f172a)"
        if theme_mode else
        "linear-gradient(90deg, #ffffff, #f1f7ff)"};
    border-bottom: 1px solid
        {"rgba(255,255,255,0.06)" if theme_mode else "rgba(56,189,248,0.25)"};
}}
header * {{
    color: {"#e5e7eb" if theme_mode else "#0f172a"} !important;
}}

/* Remove Streamlit chrome */
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {{
    display: none;
}}

/* ==================================================
   SIDEBAR
================================================== */
section[data-testid="stSidebar"] {{
    background:
        {"linear-gradient(180deg, #020617, #0f172a)"
        if theme_mode else
        "linear-gradient(180deg, #ffffff, #f1f7ff)"};
    border-right: 1px solid
        {"rgba(255,255,255,0.08)" if theme_mode else "rgba(56,189,248,0.25)"};
}}
section[data-testid="stSidebar"] * {{
    color: {"#e5e7eb" if theme_mode else "#0f172a"} !important;
}}

/* ==================================================
   CARDS / EXPANDERS / UPLOADER
================================================== */
section[data-testid="stFileUploader"],
div[data-testid="stExpander"],
div[data-testid="stContainer"] {{
    background:
        {"linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03))"
        if theme_mode else
        "linear-gradient(145deg, #ffffff, #f5faff)"};
    border-radius: 20px;
    padding: 20px;
    border: 1px solid
        {"rgba(255,255,255,0.14)" if theme_mode else "rgba(56,189,248,0.25)"};
    box-shadow:
        {"0 25px 60px rgba(0,0,0,0.55), 0 0 40px rgba(56,189,248,0.15)"
        if theme_mode else
        "0 12px 35px rgba(15,23,42,0.08)"};
}}

/* ==================================================
   TEXT
================================================== */
h1, h2, h3 {{
    color: {"#f9fafb" if theme_mode else "#0f172a"} !important;
    font-weight: 700;
}}
p, li {{
    color: {"#cbd5f5" if theme_mode else "#334155"} !important;
}}
small, .stCaption {{
    color: {"#94a3b8" if theme_mode else "#64748b"} !important;
}}

/* ==================================================
   INPUTS
================================================== */
input, textarea {{
    background:
        {"rgba(2,6,23,0.95)" if theme_mode else "#ffffff"} !important;
    color:
        {"#f9fafb" if theme_mode else "#0f172a"} !important;
    border-radius: 14px !important;
    border: 1px solid
        {"rgba(255,255,255,0.18)" if theme_mode else "rgba(56,189,248,0.35)"} !important;
    padding: 12px 14px !important;
}}
input:focus, textarea:focus {{
    border: 1px solid var(--sky) !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.35);
}}
::placeholder {{
    color: {"#94a3b8" if theme_mode else "#94a3b8"} !important;
}}

/* ==================================================
   BUTTONS (FIXED SIZE)
================================================== */
.stButton > button {{
    min-height: 44px;
    padding: 0.55em 2.2em;
    border-radius: 999px;
    font-weight: 700;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
}}

/* ANALYZE */
.stButton > button[kind="primary"] {{
    background:
        {"linear-gradient(135deg, #38bdf8, #6366f1)"
        if theme_mode else
        "linear-gradient(135deg, #7dd3fc, #60a5fa)"} !important;
    color:
        {"#020617" if theme_mode else "#0f172a"} !important;
    border: none;
}}

/* RESET */
.stButton > button[kind="secondary"] {{
    background:
        {"rgba(255,255,255,0.08)" if theme_mode else "#ffffff"} !important;
    color:
        {"#e5e7eb" if theme_mode else "#0f172a"} !important;
    border: 1px solid
        {"rgba(255,255,255,0.25)" if theme_mode else "rgba(56,189,248,0.35)"} !important;
}}

/* ==================================================
   METRICS
================================================== */
[data-testid="stMetric"] {{
    background:
        {"linear-gradient(160deg, rgba(56,189,248,0.22), rgba(99,102,241,0.22))"
        if theme_mode else
        "linear-gradient(160deg, #ffffff, #f1f7ff)"};
    border-radius: 20px;
    padding: 20px;
}}
[data-testid="stMetricValue"] {{
    color: {"#ffffff" if theme_mode else "#0f172a"} !important;
    font-weight: 800;
}}
[data-testid="stMetricLabel"] {{
    color: {"#c7d2fe" if theme_mode else "#475569"} !important;
}}

/* ==================================================
   CODE BLOCKS
================================================== */
pre {{
    background:
        {"rgba(2,6,23,0.96)" if theme_mode else "#f8fafc"} !important;
    border-radius: 16px;
    border: 1px solid
        {"rgba(255,255,255,0.12)" if theme_mode else "rgba(56,189,248,0.25)"};
}}

/* ==================================================
   PAGE LOAD
================================================== */
@keyframes appFade {{
    from {{ opacity: 0; transform: scale(0.985); }}
    to   {{ opacity: 1; transform: scale(1); }}
}}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# POPUP MESSAGE
# -------------------------------
def popup_message(message, icon="ℹ️"):
    st.markdown(
        f"<div style='padding:10px;border-radius:8px;background:#eef2ff;'>"
        f"{icon} {message}</div>",
        unsafe_allow_html=True,
    )

# -------------------------------
# SESSION STATE
# -------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "loading" not in st.session_state:
    st.session_state.loading = False


# -------------------------------
# HEADER
# -------------------------------
colored_header(
    label="CodeSentinel AI 🧠",
    description="AST + FastAI + LLM powered Code Smell Detection",
    color_name="blue-70",
)
st_lottie(ai_anim, height=180)

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Project Overview")
    st.markdown(
        """
        - 🧩 Code smell detection  
        - 🧠 AI-based refactoring advice  
        - 🔍 AST + ML hybrid analysis  
        - 💬 Multi-turn follow-up chat
        """
    )
    st.markdown("---")
    st.markdown("Developed By👨‍💻: **Wraith**")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.markdown("## 📂 Upload & Analyze Code")

uploaded_file = st.file_uploader(
    "Upload a source file",
    type=["py", "java", "cpp", "js"],
)

col_q, col_btn = st.columns([3, 1])

with col_q:
    initial_query = st.text_input(
        "💭 Ask about your code",
        placeholder="What smells exist in this file?",
    )

# with col_btn:
#     analyze_clicked = st.button("🔍 Analyze", use_container_width=True)
#     reset_clicked = st.button("🧹 Reset", use_container_width=True)
with col_btn:
<<<<<<< HEAD

    if "loading" not in st.session_state:
        st.session_state.loading = False

    analyze_clicked = st.button(
        "🔍 Analyze",
        use_container_width=True,
        disabled=st.session_state.loading   # 🔥 IMPORTANT
=======
    analyze_clicked = st.button(
        "🔍 Analyze",
        use_container_width=True,
        disabled=st.session_state.loading
>>>>>>> 4771ee8 (update)
    )

    reset_clicked = st.button(
        "🧹 Reset",
        use_container_width=True,
        disabled=st.session_state.loading
    )
<<<<<<< HEAD

=======
>>>>>>> 4771ee8 (update)

# -------------------------------
# RESET
# -------------------------------
if reset_clicked:
    st.session_state.clear()
    st.rerun()

# -------------------------------
# ANALYZE ACTION
# -------------------------------
if analyze_clicked:
    if not uploaded_file:
        popup_message("Please upload a file", "⚠️")
    elif not initial_query.strip():
        popup_message("Please enter a question", "⚠️")
    else:
        with st.status("Analyzing code...", expanded=True) as status:
<<<<<<< HEAD
            status.write("Uploading file...")
            status.write("Running AST analysis...")
            status.write("Calling AI model...")

=======
            st.session_state.loading = True
>>>>>>> 4771ee8 (update)
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "text/plain",
                    )
                }
                data = {"user_query": initial_query}

                response = requests.post(
                    ANALYZE_URL,
                    data=data,
                    files=files,
<<<<<<< HEAD
                    timeout=600   # Increased timeout for large files
=======
                    timeout=600
>>>>>>> 4771ee8 (update)
                )
                response.raise_for_status()
                result = response.json()

                st.session_state.session_id = result.get(
                    "llm_analysis", {}
                ).get("session_id")

                st.session_state.last_result = result
                st.session_state.analysis_done = True
                st.session_state.chat_history = []

                popup_message("Analysis complete", "✅")
                st_lottie(success_anim, height=150)

            except Exception as e:
                st.error(str(e))

            finally:
                st.session_state.loading = False

# -------------------------------
# RESULTS
# -------------------------------
if st.session_state.analysis_done:
    result = st.session_state.last_result or {}
    llm = result.get("llm_analysis", {})

    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    with st.expander("🧩 AST Findings", expanded=True):
        for f in llm.get("ast_findings", []):
            st.markdown(f"- {f}")

    with st.expander("🤖 LLM Insights", expanded=True):
        st.write(llm.get("llm_response", ""))

    with st.expander("🧠 Model Prediction", expanded=True):
        pred = llm.get("model_prediction", {})
        if isinstance(pred, dict):
            c1, c2 = st.columns(2)
            c1.metric("Smell", pred.get("smell_type", "N/A"))
            c2.metric("Confidence", f"{pred.get('confidence', 0):.2f}")
            st.json(pred.get("all_probs", {}))

    with st.expander("🧰 Optimized Code", expanded=True):
        code = llm.get("optimized_code", "")
        if code and "No optimized" not in code:
            st.code(code, language="python")
        else:
            st.info("No optimized code generated")

    # -------------------------------
    # FOLLOW-UP CHATBOT
    # -------------------------------
    st.markdown("---")
    st.subheader("💬 Follow-Up Chat")

    def question_box(text: str):
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #eef2ff, #e0e7ff);
                border-left: 6px solid #6366f1;
                padding: 14px 18px;
                margin: 12px 0;
                border-radius: 10px;
                font-weight: 600;
                color: #111827;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            ">
                🧑 <b>Your Question</b><br/>
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            question_box(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    user_message = st.chat_input(
        "Ask any question about the analyzed code…"
    )

    if user_message:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_message}
        )
        question_box(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    payload = {
                        "user_query": user_message,
                        "session_id": st.session_state.session_id,
                    }
                    response = requests.post(
                        FOLLOWUP_URL,
                        data=payload,
                        timeout=300
                    )
                    response.raise_for_status()
                    data = response.json()

                    llm_block = data.get("llm_analysis", {})
                    answer = llm_block.get(
                        "llm_response", "No response generated."
                    )
                    optimized = llm_block.get("optimized_code", "")

                    st.markdown(answer)

                    if optimized and "No optimized" not in optimized:
                        st.code(optimized, language="python")

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except Exception as e:
                    st.error(f"Follow-up failed: {e}")

<<<<<<< HEAD


=======
# -------------------------------
# DOWNLOAD PDF
# -------------------------------
>>>>>>> 4771ee8 (update)
if st.button("📄 Download Discussion"):

    if not st.session_state.analysis_done:
        st.warning("Please analyze code first!")
    else:
        result = st.session_state.last_result or {}
        llm = result.get("llm_analysis", {})

        followup_text = ""
        for msg in st.session_state.chat_history:
            role = "USER" if msg["role"] == "user" else "AI"
            followup_text += f"\n{role}:\n{msg['content']}\n"

        full_text = f"""
===========================
INITIAL ANALYSIS
===========================

AI RESPONSE:
{llm.get('llm_response','')}

OPTIMIZED CODE:
{llm.get('optimized_code','')}

===========================
FOLLOW-UP DISCUSSION
===========================
{followup_text}
"""

<<<<<<< HEAD
        response = requests.post(
            "https://codesentinel-ai.onrender.com/download-pdf",
            json={"text": full_text}
        )

        st.download_button(
            label="⬇️ Download PDF",
            data=response.content,
            file_name="analysis_report.pdf",
            mime="application/pdf"
        )

=======
        try:
            response = requests.post(
                DOWNLOAD_URL,
                json={"text": full_text},
                timeout=120
            )

            st.download_button(
                label="⬇️ Download PDF",
                data=response.content,
                file_name="analysis_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"PDF download failed: {e}")
>>>>>>> 4771ee8 (update)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:14px;'>"
    "Built by <b>Wraith</b> • Streamlit + FastAPI + LLM"
    "</div>",
    unsafe_allow_html=True,
)

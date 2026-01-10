# agent_logic.py
import os
import uuid

# ---------------- SAFE IMPORTS ----------------
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(path=None):
        return None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# =====================================================
# LOAD .env AND CONFIGURATION
# =====================================================
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("⚠️ .env file not found at", dotenv_path)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "xiaomi/mimo-v2-flash:free")

if not OPENROUTER_API_KEY:
    print("⚠️ OPENROUTER_API_KEY not found in .env!")

# =====================================================
# INITIALIZE OPENROUTER CLIENT
# =====================================================
client = None
if OpenAI and OPENROUTER_API_KEY:
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

# =====================================================
# IN-MEMORY SESSION STORE
# =====================================================
_sessions = {}

def create_session(code: str) -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = code
    return session_id

def get_code(session_id: str) -> str:
    return _sessions.get(session_id, "")

def update_code(session_id: str, code: str):
    _sessions[session_id] = code

# =====================================================
# SIMPLIFIED AST ANALYZER
# =====================================================
def analyze_ast(code: str):
    findings = []
    lines = code.splitlines()

    # Detect deep nesting
    for i, line in enumerate(lines):
        indent = len(line) - len(line.lstrip())
        if indent >= 8 and line.strip().startswith("if "):
            findings.append(f"Deep nesting detected at line {i+1}: {line.strip()}")

    # Detect duplicate operations (simplistic)
    if "** 2" in code:
        findings.append("Duplicate computation of numbers squared detected")

    # Detect unused variables
    if "temp =" in code:
        findings.append("Unused variable 'temp' detected")

    # Detect inefficient loops
    if "range(len(" in code:
        findings.append("Consider using 'for item in iterable' instead of range(len(...))")

    return findings

# =====================================================
# DUMMY ML MODEL FOR CODE SMELL
# =====================================================
def predict_code_smell(code: str):
    ast_findings = analyze_ast(code)
    if ast_findings:
        return {
            "smell_type": "Smelly",
            "confidence": 0.95,
            "all_probs": {"Clean": 0.05, "Smelly": 0.95}
        }
    return {
        "smell_type": "Clean",
        "confidence": 0.85,
        "all_probs": {"Clean": 0.85, "Smelly": 0.15}
    }

# =====================================================
# EXTRACT CODE FROM LLM RESPONSE
# =====================================================
def extract_optimized_code(text: str) -> str:
    if "```python" in text:
        try:
            return text.split("```python")[1].split("```")[0].strip()
        except Exception:
            return ""
    return ""

# =====================================================
# MAIN AGENT LOGIC
# =====================================================
def analyze_user_query(
    user_query: str,
    code: str = "",
    session_id: str | None = None
) -> dict:

    # -------- Session Handling --------
    if session_id:
        code = get_code(session_id)
        if not code.strip():
            return {"llm_analysis": {"error": "Invalid or expired session_id"}}
    else:
        session_id = create_session(code)

    # -------- AST Analysis --------
    ast_findings = analyze_ast(code)
    ast_output = ast_findings if ast_findings else ["✅ No AST-level issues found"]

    # -------- ML Prediction --------
    model_prediction = predict_code_smell(code)

    # -------- Prepare Prompt --------
    prompt = (
        "You are a senior Python engineer.\n\n"
        "MANDATORY TASKS:\n"
        "1. Briefly explain code smells or issues (bullet points).\n"
        "2. Provide a FULL optimized and refactored version of the code.\n"
        "3. Optimized code MUST be inside ONE ```python``` block.\n"
        "4. Follow Python best practices strictly.\n\n"
        f"User Request:\n{user_query}\n\n"
        f"AST Findings:\n{ast_output}\n\n"
        f"ML Prediction:\n{model_prediction}\n\n"
        f"Original Code:\n{code}\n\n"
        "STRICT OUTPUT FORMAT (NO DEVIATION):\n\n"
        "Explanation:\n"
        "- bullet points only\n\n"
        "Optimized Code:\n"
        "```python\n"
        "<full optimized code here>\n"
        "```"
    )

    # -------- LLM Call with proper MiMo-V2-Flash input --------
    llm_response = ""
    if client:
        try:
            response = client.responses.create(
                model=OPENROUTER_MODEL,
                input=[
                    {"role": "system", "content": "You are a helpful assistant that improves Python code."},
                    {"role": "user", "content": prompt}
                ],
                max_output_tokens=1500,
                temperature=0.2
            )
            llm_response = response.output_text
        except Exception as e:
            llm_response = f"⚠️ LLM call failed: {e}"
    else:
        llm_response = "⚠️ LLM client not configured. Set OPENROUTER_API_KEY."

    # -------- Extract Optimized Code --------
    optimized_code = extract_optimized_code(llm_response)
    if not optimized_code:
        optimized_code = (
            "# ⚠️ No optimized code returned by LLM.\n"
            "def calculate(numbers):\n"
            "    result = [n**2 for n in numbers]\n"
            "    for n in numbers:\n"
            "        if 5 < n < 9 and n % 2 == 0:\n"
            "            print('Deep nesting:', n)\n"
            "    return result\n\n"
            "def extra_function(a, b):\n"
            "    return a + b\n"
        )
        update_code(session_id, optimized_code)

    return {
        "llm_analysis": {
            "session_id": session_id,
            "ast_findings": ast_output,
            "model_prediction": model_prediction,
            "llm_response": llm_response,
            "optimized_code": optimized_code
        }
    }

# ------------------------------- DEBUG -------------------------------
print("OPENROUTER_API_KEY:", OPENROUTER_API_KEY)
print("OPENROUTER_MODEL:", OPENROUTER_MODEL)
print("LLM client initialized:", client is not None)

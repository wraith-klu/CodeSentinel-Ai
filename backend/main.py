from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    UploadFile,
    Form,
    HTTPException,
    Body,
    BackgroundTasks,
    File,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from agent_logic import analyze_user_query
import os, uuid, asyncio, traceback

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ======================
# ENV
# ======================
load_dotenv()

app = FastAPI(title="CodeSentinel AI")

# =====================
# CORS
# =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

# =====================
# LANGUAGE DETECTION (optional future use)
# =====================
def detect_language(filename: str) -> str:
    ext = filename.lower().split(".")[-1]
    return {
        "py": "python",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "cc": "cpp",
        "h": "c",
        "js": "javascript",
        "ts": "typescript",
    }.get(ext, "generic")

# =====================
# HEALTH
# =====================
@app.get("/health")
def health():
    return {"status": "alive"}

# =====================
# ROOT
# =====================
@app.get("/")
def root():
    return {"status": "API running"}

# =====================
# ANALYZE
# =====================
@app.post("/analyze")
async def analyze_code(
    user_query: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        code_bytes = await file.read()

        # Safe decode
        try:
            code = code_bytes.decode("utf-8", errors="ignore")
        except Exception:
            raise HTTPException(400, "Unable to read file as text")

        # (Language detected but not passed — reserved for future)
        _language = detect_language(file.filename)

        result = await asyncio.to_thread(
            analyze_user_query,
            user_query=user_query,
            code=code
        )

        return JSONResponse(content=result)

    except Exception:
        print("❌ Analyze error:")
        print(traceback.format_exc())
        raise HTTPException(500, "Analysis failed")

# =====================
# FOLLOW-UP
# =====================
@app.post("/followup")
async def followup_query(
    user_query: str = Form(...),
    session_id: str = Form(...)
):
    try:
        result = await asyncio.to_thread(
            analyze_user_query,
            user_query=user_query,
            session_id=session_id
        )

        return JSONResponse(content=result)

    except Exception:
        print("❌ Follow-up error:")
        print(traceback.format_exc())
        raise HTTPException(500, "Follow-up failed")

# =====================
# AUTO DELETE FILE
# =====================
def cleanup_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

# =====================
# DOWNLOAD PDF
# =====================
@app.post("/download-pdf")
async def download_pdf(
    payload: dict = Body(...),
    background_tasks: BackgroundTasks = None
):
    text = payload.get("text")
    if not text:
        raise HTTPException(400, "No text provided")

    file_path = os.path.join(
        PDF_DIR,
        f"discussion_{uuid.uuid4().hex}.pdf"
    )

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    elements = []

    for line in text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    # Auto delete after response
    if background_tasks:
        background_tasks.add_task(cleanup_file, file_path)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="discussion.pdf"
    )

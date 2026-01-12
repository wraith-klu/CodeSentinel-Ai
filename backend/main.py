from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from agent_logic import analyze_user_query
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from fastapi.responses import FileResponse
from fastapi import Body
import uuid

# Load env
load_dotenv()

app = FastAPI(title="Code Smell Detection API")

# ================================
# CORS
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# FAVICON
# ================================
@app.get("/favicon.ico")
def favicon():
    path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse(content={"msg": "No favicon"}, status_code=404)

# ================================
# ROOT
# ================================
@app.get("/")
def read_root():
    return {"status": "API running 🚀"}

# ================================
# ANALYZE
# ================================
@app.post("/analyze")
async def analyze_code(
    user_query: str = Form(...),
    file: UploadFile = None
):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        code = (await file.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File read failed: {e}"
        )

    try:
        result = analyze_user_query(
            user_query=user_query,
            code=code
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {e}"
        )

# ================================
# FOLLOW-UP (FIXED)
# ================================
@app.post("/followup")
async def followup_query(
    user_query: str = Form(...),
    session_id: str = Form(...)
):
    try:
        result = analyze_user_query(
            user_query=user_query,
            session_id=session_id   # 🔥 IMPORTANT FIX
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Follow-up failed: {e}"
        )

# ================================
# DOWNLOAD PDF REPORT
# ================================
@app.post("/download-pdf")
async def download_pdf(payload: dict = Body(...)):

    text = payload.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_DIR = os.path.join(BASE_DIR, "pdfs")
    os.makedirs(PDF_DIR, exist_ok=True)

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

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="discussion.pdf"
    )

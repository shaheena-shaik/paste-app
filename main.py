from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

app = FastAPI()   # ✅ app MUST be here first

# Root route — add this to fix 404
@app.get("/")
def root():
    return {"message": "App is running!"}


# Health check
@app.get("/api/healthz")
def health():
    return {"ok": True}


# Request model
class PasteCreate(BaseModel):
    content: str


# Temporary storage (memory)
pastes = {}


# Create paste
@app.post("/api/pastes")
def create_paste(paste: PasteCreate):
    if not paste.content.strip():
        raise HTTPException(status_code=400, detail="Content required")

    paste_id = str(uuid.uuid4())
    pastes[paste_id] = paste.content

    return {
        "id": paste_id,
        "url": f"http://127.0.0.1:8000/p/{paste_id}"
    }


# View paste (HTML)
@app.get("/p/{paste_id}", response_class=HTMLResponse)
def view_paste(paste_id: str):
    if paste_id not in pastes:
        return HTMLResponse("Paste not found", status_code=404)

    content = pastes[paste_id]
    return f"""
    <html>
      <body>
        <pre>{content}</pre>
      </body>
    </html>
    """

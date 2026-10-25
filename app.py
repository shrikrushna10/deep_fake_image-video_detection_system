import os
import io
import tempfile
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import forensic_engine

app = FastAPI(
    title="Deep Fake Image and Video Detection System",
    description="Advanced multi-spectral forensic verification system for detecting camera captured, AI generated, and reshared media."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("samples", exist_ok=True)

# Mount static and sample files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/samples", StaticFiles(directory="samples"), name="samples")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Deep Fake Image and Video Detection System</h1><p>Frontend initializing...</p>")


@app.post("/api/analyze/image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """Analyze uploaded image file against the 3 core criteria."""
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        result = forensic_engine.analyze_image(contents, file.filename or "image.jpg")
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Forensic analysis error: {str(e)}"}
        )


@app.post("/api/analyze/video")
async def analyze_video_endpoint(file: UploadFile = File(...)):
    """Analyze uploaded video file against the 3 core criteria."""
    suffix = os.path.splitext(file.filename or "video.mp4")[1]
    if not suffix:
        suffix = ".mp4"
        
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty video file uploaded")
        
        temp_file.write(contents)
        temp_file.close()

        result = forensic_engine.analyze_video(temp_file.name, file.filename or "video.mp4")
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Video analysis error: {str(e)}"}
        )
    finally:
        if os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
            except Exception:
                pass


@app.get("/api/test-sample/{sample_name}")
async def analyze_sample(sample_name: str):
    """Run forensic analysis directly on built-in samples."""
    sample_path = os.path.join("samples", sample_name)
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample not found")

    ext = os.path.splitext(sample_name)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        with open(sample_path, "rb") as f:
            content = f.read()
        res = forensic_engine.analyze_image(content, sample_name)
        return JSONResponse(content=res)
    elif ext in [".mp4", ".mov", ".avi", ".webm"]:
        res = forensic_engine.analyze_video(sample_path, sample_name)
        return JSONResponse(content=res)
    else:
        raise HTTPException(status_code=400, detail="Unsupported sample format")


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)

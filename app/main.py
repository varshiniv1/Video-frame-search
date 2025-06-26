from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

import os
import shutil
import uuid
import threading
import webbrowser

from app.video_utils import extract_frames
from app.features import compute_feature_vector
from app.vector_db import setup_collection, add_vector, search_similar

# FastAPI app setup
app = FastAPI()

# Template and static directory setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Output directory for extracted frames
OUTPUT_DIR = "static/frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the vector database collection
setup_collection()

# Home route - index.html page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Video upload endpoint
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    temp_video = f"temp_{uuid.uuid4().hex}.mp4"
    with open(temp_video, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frame_paths = extract_frames(temp_video, OUTPUT_DIR)

    for idx, frame_path in enumerate(frame_paths):
        vec = compute_feature_vector(frame_path)
        add_vector(id=idx, vector=vec, metadata={"path": frame_path})

    os.remove(temp_video)
    return {"frames_saved": len(frame_paths)}

# Query by image API endpoint (JSON response)
@app.post("/query/")
async def query_by_image(file: UploadFile = File(...)):
    temp_path = f"temp_query_{uuid.uuid4().hex}.jpg"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        feature_vec = compute_feature_vector(temp_path)
        results = search_similar(feature_vec)

        return [
            {"image_path": res.payload["path"], "score": res.score}
            for res in results
        ]
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Query by image via UI - render results in index.html
@app.post("/query-ui/", response_class=HTMLResponse)
async def query_ui(request: Request, file: UploadFile = File(...)):
    temp_path = f"temp_{uuid.uuid4().hex}.jpg"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        vec = compute_feature_vector(temp_path)
        results = search_similar(vec)
        results_info = [{"image_path": r.payload["path"], "score": round(r.score, 4)} for r in results]
    except Exception as e:
        results_info = []

    os.remove(temp_path)
    return templates.TemplateResponse("index.html", {"request": request, "results": results_info})

# Open browser automatically to FastAPI docs
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/docs")

# Run app if script is executed directly
if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

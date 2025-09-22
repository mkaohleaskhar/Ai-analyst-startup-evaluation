import uvicorn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os
from dotenv import load_dotenv
from typing import List
import vertexai

# Get the absolute path of the directory containing web_server.py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file in the same directory
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

# Import agents and parsers after loading .env
from main import run_analysis
from agents import deal_notes_agent
from utils import file_parser

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(base_dir, "web/templates"))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "web/static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        report = run_analysis(temp_file_path)

        if "error" in report:
            return JSONResponse(status_code=500, content=report)

        return JSONResponse(content=report)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/deal-notes")
async def create_deal_notes(files: List[UploadFile] = File(...)):
    print(f"--- DEBUG: Initializing Vertex AI with project: {os.getenv('GOOGLE_CLOUD_PROJECT')} ---")
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))

    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    texts = []
    temp_files = []

    try:
        for file in files:
            temp_file_path = os.path.join(temp_dir, file.filename)
            temp_files.append(temp_file_path)

            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        for temp_file_path in temp_files:
            texts.append(file_parser.parse_file(temp_file_path))

        notes = deal_notes_agent.generate_notes(texts)

        if "error" in notes:
            return JSONResponse(status_code=500, content=notes)

        return JSONResponse(content=notes)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})
    finally:
        for temp_file_path in temp_files:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

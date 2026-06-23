from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.rag import create_vector_db, ask_question, load_uploaded_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI PDF Chatbot Running 🚀"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()

    temp_path = "uploaded.pdf"

    with open(temp_path, "wb") as f:
        f.write(content)

    load_uploaded_pdf(temp_path)

    return {"message": "PDF uploaded successfully"}

@app.get("/chat")
def chat(query: str):
    return {"response": ask_question(query)}

from backend.rag import (
    create_vector_db,
    ask_question,
    load_uploaded_pdf
)
from fastapi import FastAPI
from rag import create_vector_db, ask_question

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ollama Chatbot Running 🚀"}

@app.get("/setup")
def setup():
    create_vector_db()
    return {"message": "Vector DB created"}

@app.get("/chat")
def chat(query: str):
    response = ask_question(query)
    return {"response": response}
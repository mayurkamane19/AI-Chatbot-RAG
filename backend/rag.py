import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

DB_PATH = "db"

EMBEDDINGS = OllamaEmbeddings(
    model="nomic-embed-text"
)

LLM = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

DB = None

def create_vector_db():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(BASE_DIR, "data", "pdf_checker.pdf")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        print(f"Loaded {len(docs)} pages")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        split_docs = splitter.split_documents(docs)

        print(f"Total chunks: {len(split_docs)}")

        db = Chroma.from_documents(
            documents=split_docs,
            embedding=EMBEDDINGS,
            persist_directory=DB_PATH
        )

        print("Vector DB created successfully")
        return db

    except Exception as e:
        print("Error in create_vector_db:", e)
        raise e
def load_db():
    global DB

    if DB is None:
        DB = Chroma(
            persist_directory=DB_PATH,
            embedding_function=EMBEDDINGS
        )

    return DB


def ask_question(query: str):
    try:
        db = load_db()

        retriever = db.as_retriever(
            search_kwargs={"k": 3}
        )

        docs = retriever.invoke(query)

        if not docs:
            return "I don't know based on the provided data."

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI customer support assistant.

Rules:
- Answer ONLY from the given context
- If answer is not present, say:
  "I don't know based on the provided data."
- Keep answer short and clear
- Do NOT use outside knowledge

Context:
{context}

Question:
{query}
"""

        response = LLM.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"
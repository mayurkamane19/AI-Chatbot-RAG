import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

DB_PATH = "db"

# 🔥 FAST & FREE MODELS (Ollama)
EMBEDDINGS = OllamaEmbeddings(model="nomic-embed-text")
LLM = OllamaLLM(model="mistral")

# 🔥 GLOBAL DB CACHE (speed boost)
DB = None


# ✅ CREATE VECTOR DB
def create_vector_db():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(BASE_DIR, "data", "pdf_checker.pdf")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"❌ PDF not found at: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        print(f"📄 Loaded {len(docs)} pages")

        # ⚡ OPTIMIZED CHUNKING
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        split_docs = splitter.split_documents(docs)

        print(f"⚡ Total chunks: {len(split_docs)}")

        db = Chroma.from_documents(
            split_docs,
            embedding=EMBEDDINGS,
            persist_directory=DB_PATH
        )

        return db

        print("✅ Vector DB created successfully 🚀")

    except Exception as e:
        print("❌ Error in create_vector_db:", e)
        raise e


# ✅ LOAD DB (ONLY ONCE)
def load_db():
    global DB
    if DB is None:
        DB = Chroma(
            persist_directory=DB_PATH,
            embedding_function=EMBEDDINGS
        )
    return DB


# ✅ ASK QUESTION (FAST + SAFE)
def ask_question(query: str):
    try:
        db = load_db()

        # ⚡ FAST RETRIEVAL
        retriever = db.as_retriever(search_kwargs={"k": 3})

        docs = retriever.invoke(query)

        # ❗ NO CONTEXT = SAFE RESPONSE
        if not docs:
            return "I don't know based on the provided data."

        # ⚡ CLEAN CONTEXT
        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔒 STRICT PROMPT (NO HALLUCINATION)
        prompt = f"""
You are an AI customer support assistant.

Rules:
- Answer ONLY from the given context
- If answer is not present, say: "I don't know based on the provided data."
- Keep answer short and clear
- Do NOT use outside knowledge

Context:
{context}

Question:
{query}
"""

        response = LLM.invoke(prompt)

        return response.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"
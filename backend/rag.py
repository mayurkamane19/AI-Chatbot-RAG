import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq

load_dotenv()

LLM = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

PDF_TEXT = ""


def create_vector_db():
    global PDF_TEXT

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "data", "pdf_checker.pdf")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF not found at: {pdf_path}"
            )

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        PDF_TEXT = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        print(f"Loaded {len(docs)} pages successfully")
        return True

    except Exception as e:
        print("Error:", e)
        raise e


def load_uploaded_pdf(pdf_path):
    global PDF_TEXT

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        PDF_TEXT = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        print(
            f"Uploaded PDF loaded successfully ({len(docs)} pages)"
        )

        print("CURRENT PDF LENGTH:", len(PDF_TEXT))
        print(PDF_TEXT[:500])

        return True

    except Exception as e:
        print("Upload Error:", e)
        raise e

    except Exception as e:
        print("Upload Error:", e)
        raise e


def ask_question(query: str):
    global PDF_TEXT

    try:
        if PDF_TEXT == "":
            create_vector_db()

        context = PDF_TEXT[:12000]

        prompt = f"""
You are an AI customer support assistant.

Rules:
- Answer ONLY from the given context.
- If the answer is not present in the context, say:
  "I don't know based on the provided data."
- Keep answers short and clear.
- Do NOT use outside knowledge.

Context:
{context}

Question:
{query}
"""

        response = LLM.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"
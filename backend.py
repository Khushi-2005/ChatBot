# backend.py
import os
from dotenv import load_dotenv
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Load environment variables
load_dotenv()

# Initialize embeddings & Chroma
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

def query_llm(question: str, k: int = 3) -> str:
    """
    Retrieve relevant chunks and generate an answer with citations.
    """
    # Query vectorstore
    results = collection.similarity_search(question, k=k)

    if not results:
        return " No relevant content found in the PDF."

    # Combine chunks with citations
    context = ""
    for doc in results:
        page = doc.metadata.get("page", "unknown")
        source = doc.metadata.get("source", "PDF")
        # Markdown clickable link to local PDF
        context += f"{doc.page_content}\n\n*(Source: [Page {page}]({source}))*\n\n"

    # Create a simple prompt for a HuggingFace model or local LLM
    prompt = f"""
You are a helpful assistant. Answer the question using the context below. Include citations with page numbers.

Context:
{context}

Question: {question}

Answer:
"""
    try:
        # If using a local HuggingFace model:
        # from transformers import pipeline
        # llm = pipeline("text-generation", model="your-model-name")
        # response = llm(prompt, max_length=500)[0]['generated_text']

        # For demonstration, we'll just return the prompt + context
        response = f"{prompt}\n\n(Answer generation goes here...)"
        return response
    except Exception as e:
        return f"Error: {str(e)}"

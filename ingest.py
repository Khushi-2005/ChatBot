# ingest.py
import os
import argparse
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def ingest_pdf_to_chroma(pdf_path):
    # 1️ Load PDF
    print(f" Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # 2️ Split into chunks
    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # adjust chunk size if needed
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)

    # 3️Create embeddings
    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4 Store in Chroma
    print("Adding documents to ChromaDB...")
    db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
    for i, doc in enumerate(docs):
        db.add_documents([doc])

    # 5 Persist
    db.persist()
    print("Ingestion complete! Vector store saved in 'vectorstore' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDF into ChromaDB using HuggingFace embeddings.")
    parser.add_argument("--pdf", type=str, required=True, help="Path to the PDF file")
    args = parser.parse_args()

    ingest_pdf_to_chroma(args.pdf)

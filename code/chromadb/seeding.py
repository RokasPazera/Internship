import os
from pathlib import Path

import chromadb
from pypdf import PdfReader


host = os.getenv("CHROMADB_HOST", "chromadb")
port = int(os.getenv("CHROMADB_PORT", "8000"))
collection_name = os.getenv("CHROMADB_COLLECTION", "documents")
pdf_dir = Path(os.getenv("CHROMADB_PDF_DIR", "/app/testpdf"))

client = chromadb.HttpClient(host=host, port=port)
collection = client.get_or_create_collection(name=collection_name)

if collection.count() > 0:
    print("Seed data already present, skipping.")
else:
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {pdf_dir}")

    documents = []
    metadatas = []
    ids = []

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text or not text.strip():
                continue
            documents.append(text)
            metadatas.append({"source": pdf_file.name, "page": page_number})
            ids.append(f"{pdf_file.name}-page-{page_number}")

    if not documents:
        raise ValueError(f"No extractable text found in PDF files under {pdf_dir}")

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Seeded {len(documents)} page(s) from {len(pdf_files)} PDF file(s).")

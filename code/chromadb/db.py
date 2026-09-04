import os

import chromadb


host = os.getenv("CHROMADB_HOST", "chromadb")
port = int(os.getenv("CHROMADB_PORT", "8000"))
collection_name = os.getenv("CHROMADB_COLLECTION", "documents")

client = chromadb.HttpClient(host=host, port=port)
collection = client.get_or_create_collection(name=collection_name)

result = collection.get(include=["documents", "metadatas"])

for doc_id, document, metadata in zip(result["ids"], result["documents"], result["metadatas"]):
    source = metadata.get("source")
    page = metadata.get("page")
    print(f"[{doc_id}] {source} (page {page}):")
    for word in document.split():
        print(word)

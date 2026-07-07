"""À lancer une seule fois pour construire la base vectorielle persistante
à partir de 05_corpus_rag.csv (colonnes : id, text, source, categorie)."""

import csv

from src.vector_store import VectorStore

with open("05_corpus_rag.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    chunks = [
        {"id": row["id"], "text": row["text"], "source": row["source"]}
        for row in reader
    ]

VectorStore(chunks, persist_directory="chroma_db")
print(f"Base créée avec {len(chunks)} chunks dans ./chroma_db")

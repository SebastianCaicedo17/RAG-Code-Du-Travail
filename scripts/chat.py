"""Boucle interactive pour tester le RAG en ligne de commande.
Suppose que build_db.py a déjà été lancé au moins une fois."""

from src.rag import RAG

rag = RAG(persist_directory="chroma_db")

print("Pose ta question (ligne vide pour quitter).")
while True:
    question = input("\n> ").strip()
    if not question:
        break
    print(rag.answer_question(question))

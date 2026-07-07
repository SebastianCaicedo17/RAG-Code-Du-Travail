import uuid

import chromadb
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL


class VectorStore:
    """Base vectorielle persistante construite à partir d'une liste de chunks."""

    def __init__(
        self,
        chunks: list[dict],
        persist_directory: str = "chroma_db",
        collection_name: str = "code_du_travail",
        model_name: str = EMBEDDING_MODEL,
    ) -> None:
        self.model = SentenceTransformer(model_name)

        self.client = chromadb.PersistentClient(path=persist_directory)

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine", "model_name": model_name},
        )

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        # 5. Insertion : un identifiant unique, le texte, le vecteur et la
        # métadonnée de source pour chaque chunk.
        ids = [chunk.get("id", str(uuid.uuid4())) for chunk in chunks]
        metadatas = [{"source": chunk["source"]} for chunk in chunks]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    @classmethod
    def load(
        cls,
        persist_directory: str = "chroma_db",
        collection_name: str = "code_du_travail",
    ) -> "VectorStore":
        """Recharge une base déjà persistée, sans ré-encoder de chunks."""
        store = cls.__new__(cls)

        store.client = chromadb.PersistentClient(path=persist_directory)
        store.collection = store.client.get_collection(name=collection_name)

        model_name = store.collection.metadata["model_name"]
        store.model = SentenceTransformer(model_name)

        return store

    def retrieve(self, question: str, n: int = 5) -> list[dict]:
        """Retourne les n chunks les plus proches de `question`."""
        query_embedding = self.model.encode(
            question, normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n,
        )

        return [
            {"text": document, "source": metadata["source"]}
            for document, metadata in zip(
                results["documents"][0], results["metadatas"][0]
            )
        ]

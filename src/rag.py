from pathlib import Path

from groq import Groq

from src.config import GROQ_API_KEY, LLM_MODEL
from src.moderator_agent import ModeratorAgent
from src.vector_store import VectorStore

SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"
CHUNKS_PLACEHOLDER = "{{Chunks}}"
INJECTION_REFUSAL = "Je ne peux pas répondre à cette demande."


class RAG:
    def __init__(
        self,
        persist_directory: str = "chroma_db",
        collection_name: str = "code_du_travail",
        n_chunks: int = 3,
    ) -> None:
        # config.py charge déjà le .env et vérifie GROQ_API_KEY à l'import.
        self.client = Groq(api_key=GROQ_API_KEY)
        self.moderator = ModeratorAgent()

        # Rouvre la base vectorielle déjà construite (étape 3.2), sans
        # ré-encoder aucun chunk.
        self.vector_store = VectorStore.load(
            persist_directory=persist_directory,
            collection_name=collection_name,
        )

        self.n_chunks = n_chunks

    def _build_system_prompt(self, question: str) -> str:
        chunks = self.vector_store.retrieve(question, n=self.n_chunks)

        formatted_chunks = "\n\n".join(
            f"[{chunk['source']}] {chunk['text']}" for chunk in chunks
        )

        template = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
        return template.replace(CHUNKS_PLACEHOLDER, formatted_chunks)

    def answer_question(self, question: str) -> str:
        moderation = self.moderator.moderate(question)
        if moderation["is_prompt_injection"]:
            return INJECTION_REFUSAL

        system_prompt = self._build_system_prompt(question)

        response = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )

        return response.choices[0].message.content

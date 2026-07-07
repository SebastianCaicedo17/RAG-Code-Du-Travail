import os
from dotenv import load_dotenv

load_dotenv()

def _require(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(
            f"Variable d'environnement manquante : '{var}'. "
            f"Vérifie ton fichier .env (voir .env.example)."
        )
    return value

GROQ_API_KEY: str = _require("GROQ_API_KEY")

STT_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"
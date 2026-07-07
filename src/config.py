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

EMBEDDING_MODEL = "distiluse-base-multilingual-cased-v2"
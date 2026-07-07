import json
from pathlib import Path

from groq import Groq

from src.config import GROQ_API_KEY, MODERATION_MODEL

SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "moderator_system_prompt.txt"


class ModeratorAgent:
    def __init__(self) -> None:
        self.client = Groq(api_key=GROQ_API_KEY)
        self.system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

    def moderate(self, question: str) -> dict:
        response = self.client.chat.completions.create(
            model=MODERATION_MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )

        return json.loads(response.choices[0].message.content)

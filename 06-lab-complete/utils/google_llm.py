"""Google GenAI client helper for chatbot responses."""
# pyright: reportMissingImports=false
import google.genai as genai

from app.config import settings


_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not settings.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured")
        _client = genai.Client(api_key=settings.google_api_key)
    return _client


def ask(prompt: str) -> str:
    client = _get_client()
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
    )

    text = (response.text or "").strip()
    if not text:
        return "Model returned an empty response."
    return text

# backend/app/services/llm_service.py
from google import genai
from app.config.settings import settings

print(">>> GEMINI_API_KEY LOADED:", bool(settings.GEMINI_API_KEY))
print(">>> GEMINI_MODEL:", settings.GEMINI_MODEL)

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def call_gemini(system_prompt: str, user_input: str) -> str:
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[
            system_prompt,
            user_input
        ]
    )
    return response.text

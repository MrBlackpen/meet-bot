# backend/app/agents/intent_agent.py
import json
import re
from app.services.llm_service import call_gemini
from app.schemas.intent_schema import IntentResponse

def load_prompt() -> str:
    with open("app/prompts/intent_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def extract_json_from_llm(text: str) -> dict:
    """
    Extract JSON from LLM output (handles ```json ... ```)
    """
    # Remove markdown code fences
    text = text.strip()

    # If wrapped in ```json ``` or ``` ```
    if text.startswith("```"):
        text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()

    return json.loads(text)

def detect_intents(transcript: str) -> IntentResponse:
    system_prompt = load_prompt()
    user_prompt = f"""
Meeting Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    raw_output = call_gemini(system_prompt, user_prompt)

    print("===== RAW LLM OUTPUT =====")
    print(raw_output)
    print("===== END =====")

    parsed = extract_json_from_llm(raw_output)
    return IntentResponse(**parsed)

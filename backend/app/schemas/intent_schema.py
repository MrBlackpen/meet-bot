# backend/app/schemas/intent_schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Intent(BaseModel):
    intent_type: str
    speaker: str
    source_sentence: str
    details: Dict[str, Any]
    confidence: Optional[float] = 0.9

class IntentResponse(BaseModel):
    intents: List[Intent]

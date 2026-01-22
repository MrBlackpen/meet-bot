# backend/app/api/intent.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.intent_agent import detect_intents
from app.schemas.intent_schema import IntentResponse
from app.automation.action_dispatcher import execute_intents

router = APIRouter()

class IntentRequest(BaseModel):
    transcript: str

@router.post("/intent/detect", response_model=IntentResponse)
def detect_intent_api(request: IntentRequest):
    return detect_intents(request.transcript)

@router.post("/intent/execute")
def detect_and_execute(request: IntentRequest):
    intent_response = detect_intents(request.transcript)
    execution_result = execute_intents(intent_response)

    return {
        "intents": intent_response,
        "automation": execution_result
    }

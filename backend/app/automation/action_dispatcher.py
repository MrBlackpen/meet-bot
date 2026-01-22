# backend/app/automation/action_dispatcher.py
from app.automation.router import route_intent
from app.automation.safety_guard import should_execute
from app.automation.logger import log_execution

def execute_intents(intent_response):
    results = []

    for intent in intent_response.intents:
        allowed, reason = should_execute(intent)

        if not allowed:
            log_id = log_execution(
                intent,
                status="pending",
                error=reason
            )

            results.append({
                "intent_type": intent.intent_type,
                "status": "pending",
                "log_id": log_id,
                "reason": reason,
                "intent": intent.dict()
            })
            continue

        try:
            result = route_intent(intent)
            log_execution(intent, "executed", result=result, approved=True)
            
            results.append({
                "intent_type": intent.intent_type,
                "status": "executed",
                "result": result
            })
        except Exception as e:
            log_execution(intent, "failed", error=str(e))
            
            results.append({
                "intent_type": intent.intent_type,
                "status": "failed",
                "error": str(e)
            })

    return results

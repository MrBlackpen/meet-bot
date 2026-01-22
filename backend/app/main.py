# backend/app/main.py
from fastapi import FastAPI
from app.api.intent import router as intent_router
from app.db.database import engine
from app.db.models import ExecutionLog, Base
from app.api.logs import router as logs_router
from app.api.confirm import router as confirm_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.transcript import router as transcript_router

app = FastAPI(title="Agentic Meeting Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meet.google.com", "http://localhost:8000"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(intent_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(confirm_router, prefix="/api")
app.include_router(transcript_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

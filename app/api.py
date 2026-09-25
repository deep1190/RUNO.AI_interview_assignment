
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.copilot import ask_copilot


app = FastAPI(
    title="RUNO CRM AI Copilot",
    description="Natural-language queries across CRM records.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "RUNO CRM AI Copilot API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: QuestionRequest):
    try:
        return ask_copilot(request.question)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the request.",
        ) from error

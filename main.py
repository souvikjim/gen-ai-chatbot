from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://llm-ui-eight.vercel.app",  # your frontend prod URL
        "http://localhost:5173"             # for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int | None = 500  # default 500


class QueryRequest(BaseModel):
    prompt: str


GENAI_API_KEY = os.getenv("GENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")  # e.g. "gemini-2.0-flash"


BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


@app.post("/ask_llm")
def ask_llm(data: PromptRequest):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {"parts": [{"text": data.prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": data.max_tokens or 500,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = requests.post(
        f"{BASE_URL}/{MODEL_NAME}:generateContent?key={GENAI_API_KEY}",
        headers=headers,
        json=body
    )
    return {"response": response.json()}



@app.post("/search")
def search(query_request: QueryRequest):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [{"text": query_request.prompt}]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 100,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = requests.post(
        f"{BASE_URL}/{MODEL_NAME}:generateContent?key={GENAI_API_KEY}",
        headers=headers,
        json=body
    )
    return {"response": response.json()}

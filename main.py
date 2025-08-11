from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()
origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com",  # when deployed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


class QueryRequest(BaseModel):
    prompt: str


TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


@app.post("/ask_llm")
def ask_llm(data: PromptRequest):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": f"{MODEL_NAME}",
        "prompt": data.prompt,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(
        "https://api.together.xyz/v1/completions", headers=headers, json=body)
    return {"response": response.json()}

# Endpoint: /search


@app.post("/search")
def search(query_request: QueryRequest):
    query = query_request.query
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": query,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = requests.post(
        "https://api.together.xyz/v1/completions", headers=headers, json=body)
    return {"response": response.json()}

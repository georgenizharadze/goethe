import os
from fastapi import FastAPI  # type: ignore
from fastapi.responses import PlainTextResponse  # type: ignore
from pydantic import BaseModel  # type: ignore
from openai import OpenAI  # type: ignore
from langgraph_sdk.client import get_client

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_API_URL = os.getenv("LANGSMITH_API_URL")
LANGSMITH_AGENT_ID = os.getenv("LANGSMITH_AGENT_ID")

langsmith_client = get_client(
    url=LANGSMITH_API_URL,
    api_key=LANGSMITH_API_KEY,
    headers={
        "X-Auth-Scheme": "langsmith-api-key",
    },
)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/api", response_class=PlainTextResponse)
def ask(body: QuestionRequest):
    client = OpenAI()
    prompt = [{"role": "user", "content": body.question}]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=prompt)
    return response.choices[0].message.content

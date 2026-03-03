from fastapi import FastAPI  # type: ignore
from fastapi.responses import PlainTextResponse  # type: ignore
from pydantic import BaseModel  # type: ignore
from openai import OpenAI  # type: ignore
from langgraph_sdk.client import get_client

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/api", response_class=PlainTextResponse)
def ask(body: QuestionRequest):
    client = OpenAI()
    prompt = [{"role": "user", "content": body.question}]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=prompt)
    return response.choices[0].message.content

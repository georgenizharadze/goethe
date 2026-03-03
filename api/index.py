import os
from fastapi import FastAPI  # type: ignore
from fastapi.responses import PlainTextResponse  # type: ignore
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  # type: ignore
from openai import OpenAI  # type: ignore
from langgraph_sdk.client import get_client

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_API_URL = os.getenv("LANGSMITH_API_URL")
LANGSMITH_AGENT_ID = os.getenv("LANGSMITH_AGENT_ID")

app = FastAPI()

# langsmith_client = get_client(
#     url=LANGSMITH_API_URL,
#     api_key=LANGSMITH_API_KEY,
#     headers={
#         "X-Auth-Scheme": "langsmith-api-key",
#     },
# )

# # Start a new thread
# def get_thread_id():
#     thread = langsmith_client.threads.create()
#     return thread['thread_id']

class QuestionRequest(BaseModel):
    question: str

@app.post("/api")
def ask(body: QuestionRequest):
    client = OpenAI()
    prompt = [{"role": "user", "content": body.question}]
    stream = client.chat.completions.create(model="gpt-5-nano", messages=prompt, stream=True)


    # langsmith_client = get_client(
    #     url=LANGSMITH_API_URL,
    #     api_key=LANGSMITH_API_KEY,
    #     headers={
    #         "X-Auth-Scheme": "langsmith-api-key",
    #         },
    #     )
    
    # thread_id = get_thread_id()

    # # Start a streaming run
    # query = {"messages": [{"role": "human", "content": body.question}]}
    
    def event_stream():
        for chunk in stream: # langsmith_client.runs.stream(thread_id, LANGSMITH_AGENT_ID, input=query):
            # text = chunk.data['messages'][1]['content']
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from models import UserDetails
from agent import get_plan, get_chat_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-plan")
def generate_plan(details: UserDetails):
    plan = get_plan(details.dict())
    return {"plan": plan}

@app.post("/ask-question")
def ask_question(query: str = Body(...)):
    answer = get_chat_response(query)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
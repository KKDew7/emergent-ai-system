from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator import run_pipeline
from memory import SessionMemory

app = FastAPI(title="Agentic Educational AI System")

class StudentInput(BaseModel):
    topic: str
    question: str

@app.post("/run-session")
def run_session(data: StudentInput):
    # Initialize the shared blackboard memory[cite: 1]
    memory = SessionMemory(
        topic=data.topic, 
        student_question=data.question
    )
    
    # Execute the multi-agent pipeline[cite: 1]
    final_memory = run_pipeline(memory)
    
    return final_memory
from fastapi import FastAPI, HTTPException
from app.generator import retrieve_questions, template_questions
import json
import uuid
from pydantic import BaseModel
import os

# Load configuration
CONFIG = {
    "default_num_questions": 5,
    "max_questions": 20,
    "supported_difficulties": ["beginner", "intermediate", "advanced"],
    "version": "1.0.1",
    "generator_mode": "retrieval"
}

# Try loading external config if exists
if os.path.exists("config.json"):
    try:
        with open("config.json") as f:
            CONFIG.update(json.load(f))
    except Exception as e:
        print(f"⚠️ Using default config. Error loading config.json: {e}")

app = FastAPI()

class QuizRequest(BaseModel):
    goal: str
    difficulty: str
    num_questions: int = CONFIG["default_num_questions"]

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Smart Quiz Generator"}

@app.get("/version")
def version_info():
    return {"version": CONFIG["version"], "mode": CONFIG["generator_mode"]}

@app.post("/generate")
def generate_quiz(request: QuizRequest):
    # Validate input
    if request.difficulty.lower() not in [d.lower() for d in CONFIG["supported_difficulties"]]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported difficulty. Choose from {CONFIG['supported_difficulties']}"
        )
    
    if request.num_questions > CONFIG["max_questions"]:
        raise HTTPException(
            status_code=400,
            detail=f"Max questions allowed is {CONFIG['max_questions']}"
        )
    
    # Generate quiz
    if CONFIG["generator_mode"] == "retrieval":
        questions = retrieve_questions(
            request.goal, 
            request.difficulty, 
            request.num_questions
        )
        # Fallback to templates if no questions found
        if not questions:
            questions = template_questions(
                request.goal, 
                request.difficulty, 
                request.num_questions
            )
    else:
        questions = template_questions(
            request.goal, 
            request.difficulty, 
            request.num_questions
        )
    
    return {
        "quiz_id": f"quiz_{uuid.uuid4().hex[:6]}",
        "goal": request.goal,
        "difficulty": request.difficulty,
        "count": len(questions),
        "questions": questions
    }

# New endpoint for debugging
@app.get("/questions/count")
def count_questions():
    from app.generator import load_question_bank
    questions = load_question_bank()
    return {
        "total_questions": len(questions),
        "goals": list(set(q["goal"] for q in questions)),
        "difficulties": list(set(q["difficulty"] for q in questions))
    }
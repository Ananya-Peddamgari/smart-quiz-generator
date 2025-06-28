import json
import random
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_question_bank():
    """Load questions from JSON file with error handling"""
    try:
        file_path = "data/question_bank.json"
        if not os.path.exists(file_path):
            print(f"❌ Error: File not found at {file_path}")
            return []
        
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading question bank: {e}")
        return []

def retrieve_questions(goal, difficulty, num_questions):
    """Retrieve relevant questions based on goal and difficulty"""
    questions = load_question_bank()
    if not questions:
        print("⚠️ Question bank is empty")
        return []
    
    # Normalize inputs
    goal = goal.lower().strip()
    difficulty = difficulty.lower().strip()
    
    # Filter questions
    filtered = [
        q for q in questions
        if q["difficulty"].lower() == difficulty and q["goal"].lower() == goal
    ]
    
    print(f"🔍 Found {len(filtered)} questions for {goal} ({difficulty})")
    
    if not filtered:
        return []
    
    # Use TF-IDF to find most relevant questions
    corpus = [f"{q['topic']} {q['question']}" for q in filtered]
    vectorizer = TfidfVectorizer()
    try:
        X = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([goal])
        similarities = cosine_similarity(query_vec, X).flatten()
        
        # Combine questions with their similarity scores
        scored_questions = list(zip(similarities, filtered))
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        
        # Select top questions
        selected = [q for _, q in scored_questions[:num_questions]]
        return selected
    except Exception as e:
        print(f"❌ Error in TF-IDF processing: {e}")
        return random.sample(filtered, min(num_questions, len(filtered)))

def template_questions(goal, difficulty, num_questions):
    """Fallback template questions if no matches found"""
    return [{
        "goal": goal,
        "difficulty": difficulty,
        "type": "short_answer",
        "question": f"Explain key concepts of {goal} at {difficulty} level",
        "topic": goal,
        "answer": f"Key concepts would be explained here for {goal} at {difficulty} level."
    } for _ in range(num_questions)]
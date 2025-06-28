# 🧠 Smart Quiz Generator

Smart Quiz Generator is a domain-specific, offline microservice that generates quizzes based on user-defined learning goals like **Amazon SDE**, **GATE ECE**, or **CAT Verbal**. It dynamically produces **MCQs** and **short-answer** questions using **TF-IDF-based retrieval** and **template-based generation** techniques.

This project is built using **FastAPI**, fully containerized with **Docker**, and operates 100% offline — with a validated question bank in JSON format.

---

## 🚀 Features

- ✅ Supports **MCQ and Short Answer** formats  
- ✅ **Offline** operation (no OpenAI/GPT API)  
- ✅ REST APIs built with **FastAPI**  
- ✅ Custom **TF-IDF Engine** + template logic  
- ✅ Structured dataset (JSON)  
- ✅ Schema validation script  
- ✅ Portable via **Docker**  
- ✅ Toggle between **retrieval** and **template** modes via config

---

## 🧰 Technologies Used

| Tech         | Role                         |
|--------------|------------------------------|
| FastAPI      | API framework                |
| Python 3.11  | Core language                |
| scikit-learn | TF-IDF similarity engine     |
| Docker       | Containerization             |
| Swagger UI   | API testing interface        |

---

## 📐 System Architecture

```
User Request → FastAPI → TF-IDF Engine  
           ↳ Question Bank (JSON)  
Response ← Quiz Generation
```

## 🗃️ Dataset Format

Each entry in the `question_bank.json` file includes the following:

```json
{
  "goal": "Amazon SDE",
  "questions": [
    {
      "type": "mcq",
      "question": "[BEGINNER] What is the time complexity of binary search?",
      "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
      "answer": "O(log n)",
      "difficulty": "beginner",
      "topic": "Algorithms"
    },
    {
      "type": "short_answer",
      "question": "[BEGINNER] Explain the time complexity of binary search.",
      "answer": "O(log n) because the search space is halved at each step.",
      "difficulty": "beginner",
      "topic": "Algorithms"
    }
  ]
}
```

✅ All questions validated using `test_generate.py`.

---

## ⚙️ Installation & Setup

### Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

### 📦 Install requirements

```bash
pip install -r requirements.txt
```

### ▶️ Run FastAPI app locally

```bash
uvicorn app.main:app --reload
```

Then visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger interface.

---

## 🐳 Docker Setup

### 📦 Build Docker image

```bash
docker build -t smart-quiz .
```

### 🚀 Run the container

```bash
docker run -p 8000:8000 smart-quiz
```

Then open `http://localhost:8000/docs` in your browser.

---

## Configuration

The `config.json` file controls quiz generation logic.

```json
{
  "generator_mode": "retrieval",   // or "template"
  "default_num_questions": 5,
  "max_questions": 20,
  "supported_difficulties": ["beginner", "intermediate", "advanced"]
}
```

---

## API Usage

### 📤 `POST /generate`

Request body:

```json
{
  "goal": "Amazon SDE",
  "difficulty": "beginner",
  "num_questions": 5
}
```

Response:

```json
{
  "quiz_id": "quiz_a1c142",
  "goal": "Amazon SDE",
  "questions": [
    {
      "type": "mcq",
      "question": "What is the output of this code snippet?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A",
      "difficulty": "beginner",
      "topic": "Algorithms"
    }
  ]
}
```

---

## Validation

Run the dataset schema checker before generating quizzes:

```bash
python tests/test_generate.py
```

✅ This ensures all entries meet structural and logical consistency.

---

## 📁 Project Structure

```
smart_quiz_project/
│
├── app/
│   ├── main.py             # FastAPI app
│   └── generator.py        # TF-IDF and template logic
│
├── data/
│   └── question_bank.json  # Dataset
│
├── tests/
│   └── test_generate.py    # Schema validator
│
├── config.json             # App config
├── Dockerfile              # Docker setup
├── requirements.txt
└── README.md
```

---

## Contributors

- **Ananya Peddamgari** – Intern & Developer  
- **ChatGPT, Claude AI, DeepSeek** – Assisted in debugging and generation

---

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com)  
- [Scikit-learn](https://scikit-learn.org)  
- [GeeksforGeeks](https://www.geeksforgeeks.org)  
- [Docker Docs](https://docs.docker.com)

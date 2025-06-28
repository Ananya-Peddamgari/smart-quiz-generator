import json

def validate_question_format(q):
    required_fields = ["type", "question", "answer", "goal", "difficulty", "topic"]
    for field in required_fields:
        if field not in q:
            raise AssertionError(f"Missing field: {field}")
            
    if q["type"] not in ["mcq", "short_answer"]:
        raise AssertionError(f"Invalid type: {q['type']}")
        
    if q["type"] == "mcq":
        if "options" not in q or not isinstance(q["options"], list):
            raise AssertionError("MCQ must include a list of options")
        if len(q["options"]) < 2:
            raise AssertionError("MCQ must have at least two options")
    else:
        if "options" in q and q["options"] != []:
            raise AssertionError("Short answer should not have options")
            
    if q["difficulty"] not in ["beginner", "intermediate", "advanced"]:
        raise AssertionError("Invalid difficulty level")
        
    if not isinstance(q["question"], str):
        raise AssertionError("Question must be a string")
        
    if not isinstance(q["answer"], str):
        raise AssertionError("Answer must be a string")

def run_tests():
    try:
        with open("data/question_bank.json", encoding="utf-8") as f:
            dataset = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return

    count = 0
    goals = set()
    errors = []
    
    for i, q in enumerate(dataset, 1):
        try:
            # Ensure goal exists before validation
            if "goal" not in q:
                raise AssertionError("Missing 'goal' field")
                
            validate_question_format(q)
            count += 1
            goals.add(q["goal"])
        except AssertionError as e:
            errors.append({
                "index": i,
                "question": q.get("question", "Unknown question"),
                "goal": q.get("goal", "Unknown goal"),
                "error": str(e)
            })

    if errors:
        print("\n❌ Validation errors found:")
        for error in errors:
            print(f"\nQuestion #{error['index']} ({error['goal']}):")
            print(f"  Question: {error['question']}")
            print(f"  Error: {error['error']}")
        print(f"\n🚫 Total errors: {len(errors)}")
        print(f"✅ Valid questions: {count}/{len(dataset)}")
        return

    print(f"\n✅ All {count} questions passed schema validation!")
    print(f"• Goals: {len(goals)} ({', '.join(goals)})")
    print(f"• Total questions: {len(dataset)}")

if __name__ == "__main__":
    run_tests()

          
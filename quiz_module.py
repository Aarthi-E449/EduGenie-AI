
import json
from ai_client import generate_text


def generate_quiz(topic: str) -> list:

    prompt = f"""
You are EduGenie, an AI quiz generator.

Generate exactly 3 multiple-choice questions
based on the following topic or passage:

{topic}

Each question must have:
- question
- 4 options
- correct_answer (index from 0 to 3)
- explanation

Return only a valid JSON array.

Example:
[
    {{
        "question": "What is Python?",
        "options": [
            "Programming language",
            "Operating system",
            "Database",
            "Web browser"
        ],
        "correct_answer": 0,
        "explanation": "Python is a programming language."
    }}
]
"""

    response = generate_text(
        prompt,
        temperature=0.3,
        json_mode=True
    )

    try:
        questions = json.loads(response)

        if not isinstance(questions, list):
            raise ValueError("Invalid quiz format")

        if len(questions) != 3:
            raise ValueError("Expected exactly 3 questions")

        for item in questions:
            if not isinstance(item, dict):
                raise ValueError("Invalid question")

            if not isinstance(item.get("question"), str):
                raise ValueError("Invalid question text")

            options = item.get("options")

            if not isinstance(options, list) or len(options) != 4:
                raise ValueError("Each question needs 4 options")

            if not all(isinstance(o, str) for o in options):
                raise ValueError("Invalid option")

            answer = item.get("correct_answer")

            if type(answer) is not int or answer not in range(4):
                raise ValueError("Invalid correct answer")

            if not isinstance(item.get("explanation"), str):
                raise ValueError("Missing explanation")

        return questions

    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(
            f"Invalid quiz response: {exc}"
        ) from exc
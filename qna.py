
from ai_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a helpful AI learning assistant.

Answer the student's question accurately.
Use simple and clear English.
Explain difficult terms.
Provide examples when necessary.

Student's question:
{question}
"""

    return generate_text(prompt)
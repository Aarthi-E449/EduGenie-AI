
from ai_client import generate_text


def explain_concept(topic: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Explain the following concept in simple English.

Include:
1. Simple definition
2. Detailed explanation
3. Real-life example
4. Important points
5. Short summary

Make the explanation easy for beginners.

Topic:
{topic}
"""

    return generate_text(prompt)

from ai_client import generate_text


def summarize_text(content: str) -> str:
    prompt = f"""
You are EduGenie, an AI educational assistant.

Summarize the following educational content.

Instructions:
1. Provide a short overview.
2. Identify the important points.
3. Explain them in simple English.
4. Preserve important facts.
5. Remove unnecessary information.
6. Provide a short revision summary.

Do not add information that is not present
in the original content.

Educational content:
{content}
"""

    return generate_text(prompt)
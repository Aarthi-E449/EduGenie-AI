
from ai_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner"
) -> str:

    prompt = f"""
You are EduGenie, an AI educational mentor.

Create a personalized learning path
for the following subject.

Subject: {topic}
Student level: {level}

Include the following sections:

1. Learning objectives
2. Prerequisites
3. Beginner-level topics
4. Intermediate-level topics
5. Advanced-level topics
6. Four-week study timetable
7. Practical exercises
8. Recommended learning resources
9. Mini-project ideas
10. Tips for improving knowledge

Explain each section clearly.

Make the learning plan suitable
for the student's current level.

Use simple English.
"""

    return generate_text(prompt)
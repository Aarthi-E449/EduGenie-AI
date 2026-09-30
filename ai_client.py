
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class AIError(Exception):
    pass


def generate_text(prompt, temperature=0.4, json_mode=False):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "PASTE_YOUR_API_KEY_HERE":
        raise AIError("Please add your Gemini API key to .env")

    try:
        client = genai.Client(api_key=api_key)

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4096,
            response_mime_type=(
                "application/json" if json_mode else "text/plain"
            )
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=config
        )

        if not response.text:
            raise AIError("Gemini returned an empty response")

        return response.text.strip()

    except AIError:
        raise
    except Exception as exc:
        raise AIError(f"Gemini request failed: {exc}") from exc
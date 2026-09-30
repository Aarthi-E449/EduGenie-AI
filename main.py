
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field

from ai_client import AIError
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class TextRequest(BaseModel):
    text: str = Field(min_length=2, max_length=20000)


class LearningRequest(TextRequest):
    level: str = "Beginner"


class TextResponse(BaseModel):
    result: str


class QuizResponse(BaseModel):
    questions: list


def handle_error(exc: Exception):
    if isinstance(exc, AIError):
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    if isinstance(exc, ValueError):
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    raise HTTPException(
        status_code=500,
        detail="An unexpected error occurred.",
    ) from exc


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "EduGenie",
    }


@app.post("/qa", response_model=TextResponse)
def qa_endpoint(data: TextRequest):
    try:
        return {
            "result": answer_question(data.text)
        }
    except Exception as exc:
        handle_error(exc)


@app.post("/explain", response_model=TextResponse)
def explain_endpoint(data: TextRequest):
    try:
        return {
            "result": explain_concept(data.text)
        }
    except Exception as exc:
        handle_error(exc)


@app.post("/quiz", response_model=QuizResponse)
def quiz_endpoint(data: TextRequest):
    try:
        return {
            "questions": generate_quiz(data.text)
        }
    except Exception as exc:
        handle_error(exc)


@app.post("/summarize", response_model=TextResponse)
def summarize_endpoint(data: TextRequest):
    try:
        return {
            "result": summarize_text(data.text)
        }
    except Exception as exc:
        handle_error(exc)


@app.post(
    "/learn/recommendations",
    response_model=TextResponse,
)
def recommendations_endpoint(data: LearningRequest):
    try:
        return {
            "result": get_learning_recommendations(
                data.text,
                data.level,
            )
        }
    except Exception as exc:
        handle_error(exc)
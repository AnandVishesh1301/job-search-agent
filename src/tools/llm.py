import os
import json
from typing import Any, Dict
from google import genai
from google.genai import types
#from openai import OpenAI
from .schemas import JobPosting

def get_client() -> genai.Client:
    # Picks up GEMINI_API_KEY from env automatically
    return genai.Client()

def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def extract_job_structured(url: str, source_title: str | None, cleaned_text: str) -> JobPosting:
    """
    Calls Gemini with structured output so we get a validated JobPosting.
    Handles both dict and Pydantic return types from resp.parsed.
    """
    client = get_client()
    model = get_model_name()

    system = (
        "You are an expert ATS parser. Extract only job-specific info and avoid legal/EEO/"
        "benefits boilerplate. Fill all fields you can. Return concise bullets for lists."
    )

    resp = client.models.generate_content(
        model=model,
        contents=[
            f"{system}\nURL: {url}\nPAGE_TITLE: {source_title or ''}\nTEXT:\n{cleaned_text}"
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JobPosting,           # <- structured output via Pydantic
            thinking_config=types.ThinkingConfig( # <- optional, speeds things up
                thinking_budget=0
            ),
        ),
    )

    # resp.parsed may be a dict OR an instance of JobPosting depending on SDK/runtime
    parsed = resp.parsed

    if isinstance(parsed, JobPosting):
        job = parsed
    elif isinstance(parsed, dict):
        job = JobPosting(**parsed)
    else:
        # Fallback if parsing failed or came back empty
        job = JobPosting(
            url=url,
            source_title=source_title,
            notes="Structured parse returned empty/unknown; filled minimal fields."
        )

    # Ensure key context fields are set in case the model omitted them
    if not job.url:
        job.url = url
    if source_title and not job.source_title:
        job.source_title = source_title

    return job
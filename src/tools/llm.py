import os
import json
from typing import Any, Dict
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from google.genai import types
from .schemas import JobPosting


def _llm():
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
    )

def extract_job_structured(url: str, source_title: str | None, cleaned_text: str, config: Dict | None = None) -> JobPosting:
    system = (
        "You are an expert ATS parser. Extract only job-specific info and avoid "
        "legal/EEO/benefits boilerplate. Fill all the fields you can. Return concise bullets for lists."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "URL: {url}\nPAGE_TITLE: {title}\nTEXT:\n{text}")
    ])

    # Gemini returns a Pydantic object
    structured_llm = _llm().with_structured_output(JobPosting)  # validated output
    chain = prompt | structured_llm

    job = chain.invoke(
        {"url": url, "title": source_title or "", "text": cleaned_text},
        config=config,  # <- carries the Langfuse CallbackHandler
    )
    
    # job is already a JobPosting instance
    if not job.url:
        job.url = url
    if source_title and not job.source_title:
        job.source_title = source_title
    return job

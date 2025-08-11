from typing import Dict, Any
from selectolax.parser import HTMLParser
import trafilatura
from ..tools.fetchers import get_page
from ..tools.cleaners import strip_boilerplate
from ..tools.llm import extract_job_structured

def _html_title(html: str) -> str | None:
    try:
        tree = HTMLParser(html)
        t = tree.css_first("title")
        return t.text(strip=True) if t else None
    except Exception:
        return None

# ---------- Nodes ----------

def fetch_node(state: Dict[str, Any]) -> Dict[str, Any]:
    url = state["url"]
    final_url, html = get_page(url)
    return {"final_url": final_url, "raw_html": html}

def parse_node(state: Dict[str, Any]) -> Dict[str, Any]:
    html = state["raw_html"]
    title = _html_title(html)
    # Extract main text using Trafilatura (robust article/JD extraction)
    extracted = trafilatura.extract(html, include_comments=False, include_tables=False) or ""
    # Fall back to basic visible text if Trafilatura fails
    text = extracted.strip()
    return {"raw_text": text, "page_title": title}

def clean_node(state: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = strip_boilerplate(state["raw_text"])
    return {"cleaned_text": cleaned}

def extract_node(state, config):
    text = state.get("cleaned_text") or state["raw_text"]
    job = extract_job_structured(
        url=state["final_url"],
        source_title=state.get("page_title"),
        cleaned_text=text,
        config=config,  
    ).model_dump()
    return {"job": job}

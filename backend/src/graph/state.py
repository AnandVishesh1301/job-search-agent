from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict, total=False):
    url: str
    final_url: str
    raw_html: str
    page_title: Optional[str]
    raw_text: str
    cleaned_text: str
    job: Dict[str, Any]   # JSON version of JobPosting
    error: Optional[str]

from pydantic import BaseModel, Field
from typing import List, Optional

class JobPosting(BaseModel):
    url: str = Field(..., description="Original job URL")
    source_title: Optional[str] = Field(None, description="Page title or job title scraped")
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = Field(None, description="Full-time, Internship, Contract...")
    seniority: Optional[str] = Field(None, description="Entry/Mid/Senior/Principal/Intern")
    salary: Optional[str] = None
    posted_date: Optional[str] = None
    apply_url: Optional[str] = None

    # Core content
    responsibilities: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    must_have_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)

    # Context
    about_team: Optional[str] = None
    about_company_short: Optional[str] = None

    # For traceability
    notes: Optional[str] = Field(None, description="Any assumptions or ambiguities found by the model")

from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReviewRequest(BaseModel):
    file_name: str
    language: str
    code: str


class ReviewComment(BaseModel):
    line: int
    severity: Severity
    issue: str
    suggestion: str


class ReviewResponse(BaseModel):
    id: str
    file_name: str
    comments: list[ReviewComment]

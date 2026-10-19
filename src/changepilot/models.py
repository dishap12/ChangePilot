"""Simple, auditable domain objects used throughout the project."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Requirement:
    id: str
    text: str
    version: str


@dataclass(frozen=True)
class Change:
    id: str
    status: str
    old_text: str
    new_text: str
    similarity: float


@dataclass(frozen=True)
class TraceLink:
    requirement_id: str
    system: str
    owner: str
    user_story: str
    test_case: str
    link_type: str = "verified"

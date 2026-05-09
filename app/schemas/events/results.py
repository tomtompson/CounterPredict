# app/schemas/events/results.py

from typing import List, Optional

from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class EventResultDetails(HLTVBaseModel):
    """Schema for a single match result within an event."""

    match_url: HttpUrl
    match_id: Optional[str]
    match_date: Optional[str]

    team1_name: Optional[str]
    team1_logo: Optional[HttpUrl]
    team1_score: Optional[int]

    team2_name: Optional[str]
    team2_logo: Optional[HttpUrl]
    team2_score: Optional[int]

    match_type: Optional[str]
    match_won: Optional[bool]


class EventResults(HLTVBaseModel, AuditMixin):
    """Schema for event results response."""

    event_id: str
    results: List[EventResultDetails]
    result_count: int

from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class EventResultDetails(HLTVBaseModel):
    """Schema for a single match result within an event."""

    match_url: HttpUrl
    match_id: int | None
    match_date: str | None

    team1_name: str | None
    team1_logo: HttpUrl | None
    team1_score: int | None

    team2_name: str | None
    team2_logo: HttpUrl | None
    team2_score: int | None

    match_type: str | None
    match_won: bool | None


class EventResults(HLTVBaseModel, AuditMixin):
    """Schema for event results response."""

    event_id: int
    results: list[EventResultDetails]
    result_count: int

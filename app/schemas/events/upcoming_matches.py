from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class EventUpcomingMatchDetails(HLTVBaseModel):
    match_id: str | None = None
    match_url: HttpUrl | None = None
    team1_name: str | None = None
    team1_id: str | None = None
    team1_logo: HttpUrl | None = None
    team2_name: str | None = None
    team2_id: str | None = None
    team2_logo: HttpUrl | None = None
    event_name: str | None = None
    match_timestamp: float | None = None
    match_type: str | None = None
    display_time: str | None = None
    display_date: str | None = None
    is_tbd: bool
    match_status: str
    local_date: str | None = None
    local_time: str | None = None
    local_weekday: str | None = None
    local_timezone: str | None = None


class EventUpcomingMatches(HLTVBaseModel, AuditMixin):
    event_id: str
    matches: list[EventUpcomingMatchDetails] | None = None
    match_count: int
    timezone: str

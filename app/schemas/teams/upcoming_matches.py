from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class UpcomingMatchDetails(HLTVBaseModel):
    match_id: str
    match_url: HttpUrl | None = None
    event_name: str | None = None
    event_id: str | None = None
    rival_team_name: str | None = None
    rival_team_id: str | None = None
    match_type: str | None = None

    match_timestamp: float | None = None
    local_date: str | None = None
    local_time: str | None = None
    local_weekday: str | None = None
    local_timezone: str | None = None


class UpcomingMatches(HLTVBaseModel, AuditMixin):
    team_id: str
    upcoming_matches: list[UpcomingMatchDetails] | None = None
    match_count: int
    timezone: str

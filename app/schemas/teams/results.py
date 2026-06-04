from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class TeamResultDetails(HLTVBaseModel):
    match_url: HttpUrl
    match_id: int | None
    match_date: str | None
    team1_name: str | None
    team1_logo: HttpUrl | None
    team1_score: int | None
    team2_name: str | None
    team2_logo: HttpUrl | None
    team2_score: int | None
    event_name: str | None
    event_logo: HttpUrl | None
    match_type: str | None
    match_won: bool | None


class TeamResults(HLTVBaseModel, AuditMixin):
    team_id: int
    results: list[TeamResultDetails]
    result_count: int

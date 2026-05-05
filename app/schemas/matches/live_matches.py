from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class LiveMatchsDetails(HLTVBaseModel):
    match_id: str | None = None
    team_a: str | None = None
    team_a_id: str | None = None
    team_a_map_score: int | None = None
    team_a_current_map_score: int | None = None
    team_b_current_map_score: int | None = None
    team_b_map_score: int | None = None
    team_b_id: str | None = None
    team_b: str | None = None
    tournament_name: str | None = None
    tournament_id: str | None = None
    match_type: str | None = None
    match_url: HttpUrl | None = None


class LiveMatches(AuditMixin, HLTVBaseModel):
    live_matchs_count: int | None = None
    live_matchs: list[LiveMatchsDetails] | None = None

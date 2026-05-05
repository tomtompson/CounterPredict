from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class CoachDetails(HLTVBaseModel):
    id: str
    nickname: str


class LineupDetails(HLTVBaseModel):
    id: str
    nickname: str


class TeamProfileDetails(HLTVBaseModel):
    name: str
    valve_ranking: int | None
    world_ranking: int | None
    weeks_in_top30_for_core: int | None
    average_player_age: float | None
    lineup: list[LineupDetails]
    coach: list[CoachDetails]
    logo_url: HttpUrl | None = None
    social_media: list[HttpUrl] | None


class TeamProfile(HLTVBaseModel, AuditMixin):
    id: str
    team_profile: TeamProfileDetails | None

from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class TeamAchievementDetail(HLTVBaseModel):
    id: str
    name: str


class TeamAchievementDetails(HLTVBaseModel):
    placement: str
    team: TeamAchievementDetail
    tournament: TeamAchievementDetail
    player_stats_url: HttpUrl


class PlayerTeamAchievements(HLTVBaseModel, AuditMixin):
    id: str
    achievement_count: int | None = None
    achievements: list[TeamAchievementDetails] | None = None

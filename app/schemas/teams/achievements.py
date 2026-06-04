from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class TeamAchievementsDetails(HLTVBaseModel):
    id: int
    tournament_name: str
    placement: str
    team_event_stats: HttpUrl


class TeamAchievements(HLTVBaseModel, AuditMixin):
    id: int
    achievement_count: int | None
    team_achievements: list[TeamAchievementsDetails] | None

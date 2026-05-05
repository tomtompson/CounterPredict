from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class TeamAchievementsDetails(HLTVBaseModel):
    id: str
    tournament_name: str
    placement: str
    team_event_stats: HttpUrl


class TeamAchievements(HLTVBaseModel, AuditMixin):
    id: str
    achievement_count: int | None
    team_achievements: list[TeamAchievementsDetails] | None

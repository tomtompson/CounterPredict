from typing import TYPE_CHECKING

from app.schemas.base import AuditMixin, HLTVBaseModel

if TYPE_CHECKING:
    from pydantic import HttpUrl


class teamAchievementDetail(HLTVBaseModel):
    id: str
    name: str


class teamAchievementDetails(HLTVBaseModel):
    placement: str
    team: teamAchievementDetail
    tournament: teamAchievementDetail
    player_stats_url: HttpUrl


class PlayerTeamAchievements(HLTVBaseModel, AuditMixin):
    id: str
    achievement_count: int | None = None
    achievements: list[teamAchievementDetails] | None = None

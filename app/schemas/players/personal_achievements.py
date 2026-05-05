from typing import TYPE_CHECKING

from app.schemas.base import AuditMixin, HLTVBaseModel

if TYPE_CHECKING:
    from pydantic import HttpUrl


class Top20Achievement(HLTVBaseModel):
    placement: str
    year: str
    article: HttpUrl


class personalAchievementDetail(HLTVBaseModel):
    major_winner_count: int | None = None
    major_mvp_count: int | None = None
    mvp_winner_count: int | None = None
    evp_count: int | None = None
    top_20_count: int | None = None
    mvp_winner: list[str] | None = None
    evp_at: list[str] | None = None
    top_20: list[Top20Achievement] | None = None


class PlayerPersonalAchievements(HLTVBaseModel, AuditMixin):
    id: str
    personal_achievements: personalAchievementDetail | None = None

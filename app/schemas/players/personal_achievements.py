from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class Top20Achievement(HLTVBaseModel):
    placement: str
    year: str
    article: HttpUrl


class PersonalAchievementDetail(HLTVBaseModel):
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
    personal_achievements: PersonalAchievementDetail | None = None

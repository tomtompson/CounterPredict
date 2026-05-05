from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class PlayerProfile(HLTVBaseModel, AuditMixin):
    id: str
    url: HttpUrl
    nickname: str
    name: str
    age: int | None
    nationality: str
    rating: float | None
    current_team: str | None
    current_team_url: HttpUrl | None
    image_url: HttpUrl | None
    social_media: list[str] | None

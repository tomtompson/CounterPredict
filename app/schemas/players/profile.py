from pydantic import HttpUrl, field_validator

from app.schemas.base import AuditMixin, HLTVBaseModel


class PlayerProfile(HLTVBaseModel, AuditMixin):
    id: int
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

    @field_validator("age", mode="before")
    @classmethod
    def parse_age(cls, v: str | int) -> int | None:
        if isinstance(v, int):
            return v
        if v and v.isdigit():
            return int(v)
        return None

    @field_validator("rating", mode="before")
    @classmethod
    def parse_rating(cls, v: str) -> float | None:
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

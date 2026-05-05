from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class TrophiesDetails(HLTVBaseModel):
    tournament_id: str | None = None
    tournament_name: str
    tournament_url: HttpUrl
    tournament_img_url: HttpUrl


class PlayerTrophies(HLTVBaseModel, AuditMixin):
    id: str
    trophy_count: int | None = None
    trophies: list[TrophiesDetails] | None = None

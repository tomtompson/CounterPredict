from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class TeamSearchPlayersDetails(HLTVBaseModel):
    id: str
    nickname: str
    name: str
    nationality: str
    profile_url: HttpUrl


class TeamSearchResult(HLTVBaseModel):
    id: str
    name: str
    country: str
    url: HttpUrl
    team_logo_url: HttpUrl
    lineup: list[TeamSearchPlayersDetails] | None


class TeamSearch(HLTVBaseModel, AuditMixin):
    query: str
    results: list[TeamSearchResult] | None

from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


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


class TeamListItem(HLTVBaseModel):
    id: str
    name: str
    country: str | None
    url: HttpUrl
    team_logo_url: HttpUrl | None
    lineup: list[TeamSearchPlayersDetails] | None
    placement: int | None
    hltv_points: int | None

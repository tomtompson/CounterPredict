from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class EventsSearchResult(HLTVBaseModel):
    id: int
    name: str
    url: HttpUrl
    event_location: str
    prize_pool: str
    flag_url: HttpUrl
    event_logo_url: HttpUrl
    event_type: str
    event_matches_url: str


class EventsSearch(HLTVBaseModel, AuditMixin):
    query: str
    results: list[EventsSearchResult] | None

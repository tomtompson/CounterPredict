from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class EventEvpsDetails(HLTVBaseModel):
    id: int
    nickname: str
    event_stats: HttpUrl


class EventMvpDetail(HLTVBaseModel):
    id: int | None
    nickname: str | None
    event_stats: HttpUrl | None


class EventTeamDetail(HLTVBaseModel):
    id: int
    name: str
    team_placement: str


class EventProfileDetail(HLTVBaseModel):
    name: str
    start_date: str
    end_date: str
    team_count: int
    prize_pool: int
    location: str
    location_flag_url: HttpUrl
    mvp: list[EventMvpDetail] | None
    evps: list[EventEvpsDetails] | None
    teams: list[EventTeamDetail]


class EventProfile(HLTVBaseModel, AuditMixin):
    id: int
    event_profile: EventProfileDetail

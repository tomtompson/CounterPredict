from app.schemas.base import AuditMixin, HLTVBaseModel

from pydantic import HttpUrl


class EventEvpsDetails(HLTVBaseModel):
    id: str
    nickname: str
    event_stats: HttpUrl


class EventMvpDetail(HLTVBaseModel):
    id: str | None
    nickname: str | None
    event_stats: HttpUrl | None


class EventTeamDetail(HLTVBaseModel):
    id: str
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
    id: str
    event_profile: EventProfileDetail

from pydantic import HttpUrl

from app.schemas.base import AuditMixin, HLTVBaseModel


class PrizeDetails(HLTVBaseModel):
    prize: int | None
    club_share: int | None


class VrsDetails(HLTVBaseModel):
    vrs_date: str | None
    points_before_event: int | None
    points_after_event: int | None
    points_acquired: int | None
    placement_before_event: int | None
    placement_after_event: int | None


class CoachDetails(HLTVBaseModel):
    id: str
    nickname: str


class LineupDetails(HLTVBaseModel):
    id: str
    nickname: str
    event_stats: HttpUrl


class EventTeamStatsDetails(HLTVBaseModel, AuditMixin):
    team_placement: str
    prize: list[PrizeDetails] | None
    vrs: list[VrsDetails] | None
    qualify_method: str | None
    lineup: list[LineupDetails]
    coach: list[CoachDetails] | None


class EventTeamStats(HLTVBaseModel, AuditMixin):
    event_id: str
    team_id: str
    stats: EventTeamStatsDetails

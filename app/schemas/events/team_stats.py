from typing import TYPE_CHECKING

from app.schemas.base import AuditMixin, HLTVBaseModel

if TYPE_CHECKING:
    from pydantic import HttpUrl


class prizeDetails(HLTVBaseModel):
    prize: int | None
    club_share: int | None


class vrsDetails(HLTVBaseModel):
    vrs_date: str | None
    points_before_event: int | None
    points_after_event: int | None
    points_acquired: int | None
    placement_before_event: int | None
    placement_after_event: int | None


class coachDetails(HLTVBaseModel):
    id: str
    nickname: str


class lineupDetails(HLTVBaseModel):
    id: str
    nickname: str
    event_stats: HttpUrl


class eventTeamStatsDetails(HLTVBaseModel, AuditMixin):
    team_placement: str
    prize: list[prizeDetails] | None
    vrs: list[vrsDetails] | None
    qualify_method: str | None
    lineup: list[lineupDetails]
    coach: list[coachDetails] | None


class EventTeamStats(HLTVBaseModel, AuditMixin):
    event_id: str
    team_id: str
    stats: eventTeamStatsDetails

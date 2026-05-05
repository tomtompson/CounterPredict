from typing import TYPE_CHECKING

from app.schemas.base import AuditMixin, HLTVBaseModel

if TYPE_CHECKING:
    from pydantic import HttpUrl


class TodayMatchesDetails(HLTVBaseModel):
    match_id: str
    match_url: HttpUrl | None = None

    team1_name: str | None = None
    team1_id: str | None = None
    team1_logo: str | None = None

    team2_name: str | None = None
    team2_id: str | None = None
    team2_logo: str | None = None

    tournament_name: str | None = None
    tournament_id: str | None = None
    tournament_logo: str | None = None

    match_type: str | None = None
    match_timestamp: float | None = None
    is_tbd: bool | None = None
    match_status: str | None = None

    local_date: str | None = None  # YYYY-MM-DD
    local_time: str | None = None  # HH:MM (24h)
    local_weekday: str | None = None  # Monday, Tuesday, etc.
    local_timezone: str | None = None  # IANA timezone, ex: America/Sao_Paulo
    local_datetime_iso: str | None = (
        None  # ISO 8601 com offset, ex: 2026-04-29T22:00:00-03:00
    )


class TodayMatches(HLTVBaseModel, AuditMixin):
    match_count: int = 0
    matches: list[TodayMatchesDetails] | None = None

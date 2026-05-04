from typing import Optional, List
from pydantic import HttpUrl

from app.schemas.base import HLTVBaseModel, AuditMixin


class TodayMatchesDetails(HLTVBaseModel):
    match_id: str
    match_url: Optional[HttpUrl] = None

    team1_name: Optional[str] = None
    team1_id: Optional[str] = None
    team1_logo: Optional[str] = None

    team2_name: Optional[str] = None
    team2_id: Optional[str] = None
    team2_logo: Optional[str] = None

    tournament_name: Optional[str] = None
    tournament_id: Optional[str] = None
    tournament_logo: Optional[str] = None

    match_type: Optional[str] = None
    match_timestamp: Optional[float] = None
    is_tbd: Optional[bool] = None
    match_status: Optional[str] = None

    local_date: Optional[str] = None          # YYYY-MM-DD
    local_time: Optional[str] = None          # HH:MM (24h)
    local_weekday: Optional[str] = None       # Monday, Tuesday, etc.
    local_timezone: Optional[str] = None      # IANA timezone, ex: America/Sao_Paulo
    local_datetime_iso: Optional[str] = None  # ISO 8601 com offset, ex: 2026-04-29T22:00:00-03:00


class TodayMatches(HLTVBaseModel, AuditMixin):
    match_count: int = 0
    matches: List[TodayMatchesDetails] = []
# app/schemas/team_upcoming_matches.py

from typing import List, Optional
from pydantic import HttpUrl

from app.schemas.base import HLTVBaseModel, AuditMixin


class UpcomingMatchDetails(HLTVBaseModel):

    match_id: str
    match_url: HttpUrl
    event_name: Optional[str]
    event_id: Optional[str]
    rival_team_name: Optional[str]
    rival_team_id: Optional[str]
    match_type: Optional[str]

    match_timestamp: Optional[float]          
    local_date: Optional[str]                 
    local_time: Optional[str]                 
    local_weekday: Optional[str]              
    local_timezone: Optional[str]             


class UpcomingMatches(HLTVBaseModel, AuditMixin):

    team_id: str
    upcoming_matches: List[UpcomingMatchDetails]
    match_count: int
    timezone: str                             
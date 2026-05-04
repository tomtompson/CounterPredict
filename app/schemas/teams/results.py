from typing import List, Optional
from pydantic import HttpUrl

from app.schemas.base import HLTVBaseModel, AuditMixin


class TeamResultDetails(HLTVBaseModel):
    match_url: HttpUrl
    match_id: Optional[str]
    match_date: Optional[str]
    team1_name: Optional[str]
    team1_logo: Optional[HttpUrl]
    team1_score: Optional[int]
    team2_name: Optional[str]
    team2_logo: Optional[HttpUrl]
    team2_score: Optional[int]
    event_name: Optional[str]
    event_logo: Optional[HttpUrl]
    match_type: Optional[str]
    match_won: Optional[bool]


class TeamResults(HLTVBaseModel, AuditMixin):
    team_id: str
    results: List[TeamResultDetails]
    result_count: int
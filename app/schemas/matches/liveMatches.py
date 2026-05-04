from typing import Optional, List
from pydantic import HttpUrl

from app.schemas.base import HLTVBaseModel, AuditMixin

class LiveMatchsDetails(HLTVBaseModel):
    match_id: str = None
    team_a: Optional[str] = None
    team_a_id: Optional[str] = None
    team_a_map_score: Optional[int] = None 
    team_a_current_map_score: Optional[int] = None
    team_b_current_map_score: Optional[int] = None
    team_b_map_score: Optional[int] = None
    team_b_id: Optional[str] = None
    team_b: Optional[str] = None
    tournament_name: Optional[str] = None
    tournament_id: Optional[str] = None
    match_type: Optional[str] =None
    match_url: Optional[HttpUrl] = None

class LiveMatches(AuditMixin,HLTVBaseModel):
    live_matchs_count: int = None
    live_matchs: List[LiveMatchsDetails] = None
from fastapi import APIRouter,Query
from typing import List



from app.schemas.matches.liveMatches import LiveMatches
from app.schemas.matches.todayMatches import TodayMatches

from app.services.matches.liveMatches import HLTVLiveMatches
from app.services.matches.todayMatches import HLTVTodayMatches

from app.utils.utils import get_common_timezones

router = APIRouter()

@router.get("/live", response_model=LiveMatches, response_model_exclude_none=True)
def get_live_matches():
    
    hltv = HLTVLiveMatches()
    found_matches = hltv.get_live_matches()
    return found_matches

@router.get("/today/", response_model=TodayMatches, response_model_exclude_none=True)
def get_today_matches(
    timezone: str = Query("UTC", description = "list of timezones  (first is used)", enum=get_common_timezones())
):
    hltv = HLTVTodayMatches()
    found_matches = hltv.get_today_matches(user_timezone=timezone)
    return found_matches
from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.matches import (
    LiveMatches,
    MatchPastPlayersStats,
    MatchStats,
    TodayMatches,
)
from app.services.matches import HLTVLiveMatches, HLTVMatchStats, HLTVTodayMatches, HLTVMatchPastPlayersStats
from app.utils.utils import get_common_timezones

router = APIRouter()


@router.get(
    "/live",
    response_model=LiveMatches,
)
def get_live_matches():

    hltv = HLTVLiveMatches()
    return hltv.get_live_matches()


@router.get(
    "/today/",
    response_model=TodayMatches,
)
def get_today_matches(
    timezone: Annotated[
        str,
        Query(
            description="list of timezones  (first is used)",
            enum=get_common_timezones(),
        ),
    ] = "UTC",
):
    hltv = HLTVTodayMatches()
    return hltv.get_today_matches(user_timezone=timezone)


@router.get(
    "/stats/{match_id}",
    response_model=MatchStats,
)
def get_match_stats(match_id: int):
    hltv = HLTVMatchStats(match_id=match_id)
    return hltv.get_match_stats()

@router.get(
    "stats/past/players/{match_id}/",
    response_model=MatchPastPlayersStats,
)
def get_past_players_stats(match_id: int):
    hltv = HLTVMatchPastPlayersStats(match_id=match_id)
    return hltv.get_past_players_stats()

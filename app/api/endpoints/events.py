from fastapi import APIRouter

from app.schemas.events import EventProfile, EventResults, EventsSearch, EventTeamStats
from app.services.events import (
    HLTVEventProfile,
    HLTVEventResults,
    HLTVEventsSearch,
    HLTVEventTeamStats,
)

router = APIRouter()


@router.get(
    "/search/{event_name}",
    response_model=EventsSearch,
)
def search_events(event_name: str):
    hltv = HLTVEventsSearch(query=event_name)
    return hltv.search_events()


@router.get(
    "/{event_id}/profile",
    response_model=EventProfile,
)
def get_event_profile(event_id: str):
    hltv = HLTVEventProfile(event_id=event_id)
    return hltv.get_event_profile()


@router.get(
    "/{event_id}/team/{team_id}/stats",
    response_model=EventTeamStats,
)
def get_team_event_stats(event_id: str, team_id: str):
    hltv = HLTVEventTeamStats(event_id=event_id, team_id=team_id)
    return hltv.get_team_event_stats()


@router.get(
    "/{event_id}/results",
    response_model=EventResults,
)
def get_event_results(event_id: str):
    hltv = HLTVEventResults(event_id=event_id)
    return hltv.get_event_results()

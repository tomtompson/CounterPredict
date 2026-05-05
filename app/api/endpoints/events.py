from fastapi import APIRouter

from app.schemas.events.profile import EventProfile
from app.schemas.events.search import EventsSearch
from app.schemas.events.team_stats import EventTeamStats
from app.services.events.profile import HLTVEventProfile
from app.services.events.search import HLTVEventsSearch
from app.services.events.team_stats import HLTVEventTeamStats

router = APIRouter()


@router.get(
    "/search/{event_name}",
    response_model=EventsSearch,
    response_model_exclude_none=True,
)
def search_events(event_name: str):
    hltv = HLTVEventsSearch(query=event_name)
    return hltv.search_events()


@router.get(
    "/{event_id}/profile",
    response_model=EventProfile,
    response_model_exclude_none=True,
)
def get_event_profile(event_id: str):
    hltv = HLTVEventProfile(event_id=event_id)
    return hltv.get_event_profile()


@router.get(
    "/{event_id}/team/{team_id}/stats",
    response_model=EventTeamStats,
    response_model_exclude_none=True,
)
def get_team_event_stats(event_id: str, team_id: str):
    hltv = HLTVEventTeamStats(event_id=event_id, team_id=team_id)
    return hltv.get_team_event_stats()

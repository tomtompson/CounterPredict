from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.teams import (
    TeamListItem,
    TeamAchievements,
    TeamProfile,
    TeamResults,
    TeamSearch,
    UpcomingMatches,
    TeamMapStatsResponse,
)
from app.services.teams import (
    HLTVTeamAchievements,
    HLTVTeamProfile,
    HLTVTeamResults,
    HLTVTeamSearch,
    HLTVTeamUpcomingMatches,
    HLTVTeamMapStats,
)
from app.utils.utils import get_common_timezones

router = APIRouter()


@router.get("/hltv-ranking", response_model=list[TeamListItem])
def list_hltv_ranking(top_n: int = 50):
    hltv = HLTVTeamSearch(top_n=top_n, ranking_type="hltv")
    return hltv.get_hltv_teams()


@router.get("/world-ranking", response_model=list[TeamListItem])
def list_world_ranking(top_n: int = 50):
    hltv = HLTVTeamSearch(top_n=top_n, ranking_type="valve")
    return hltv.get_world_ranking_teams()


@router.get(
    "/{team_name}/search",
    response_model=TeamSearch,
)
def search_teams(team_name: str):
    hltv = HLTVTeamSearch(query=team_name)
    return hltv.search_teams()


@router.get(
    "/{team_id}/profile",
    response_model=TeamProfile,
)
def get_team_profile(team_id: str):
    hltv = HLTVTeamProfile(team_id=team_id)
    return hltv.get_team_profile()


@router.get(
    "/{team_id}/achievements",
    response_model=TeamAchievements,
)
def get_team_achievements(team_id: str):
    hltv = HLTVTeamAchievements(team_id=team_id)
    return hltv.get_team_achievements()


@router.get(
    "/{team_id}/upcoming-matches",
    response_model=UpcomingMatches,
)
def get_team_upcoming_matches(
    team_id: str,
    timezone: Annotated[
        str,
        Query(
            description="list of timezeones (first is used)",
            enum=get_common_timezones(),
        ),
    ] = "UTC",
):
    hltv = HLTVTeamUpcomingMatches(team_id=team_id)
    return hltv.get_team_upcoming_matches(user_timezone=timezone)


@router.get(
    "/{team_id}/results/",
    response_model=TeamResults,
)
def get_team_results(
    team_id: str,
    limit: Annotated[
        int | None,
        Query(description="Maximum number of results to return (all if omitted)", ge=1),
    ] = None,
):
    """Get past results for a team (first page = 100 most recent matches)."""
    service = HLTVTeamResults(team_id=team_id)
    results_data = service.get_team_results()

    # Apply limit if provided
    if limit and limit < len(results_data["results"]):
        results_data["results"] = results_data["results"][:limit]
        results_data["result_count"] = len(results_data["results"])

    return results_data

@router.get(
    "/{team_id}/map-stats",
    response_model=TeamMapStatsResponse,
)
def get_team_map_stats(team_id: str):
    service = HLTVTeamMapStats(team_id=team_id)
    return service.get_team_map_stats()
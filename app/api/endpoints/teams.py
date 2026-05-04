from typing import Optional

from fastapi import APIRouter, Query

from app.schemas.teams.search import TeamSearch
from app.schemas.teams.profile import TeamProfile
from app.schemas.teams.achievements import TeamAchievements
from app.schemas.teams.upcomingMatches import UpcomingMatches
from app.schemas.teams.results import TeamResults

from app.services.teams.search import HLTVTeamSearch
from app.services.teams.profile import HLTVTeamProfile
from app.services.teams.achievements import HLTVTeamAchievements
from app.services.teams.upcomingMatches import HLTVTeamUpcomingMatches
from app.services.teams.results import HLTVTeamResults

from app.utils.utils import get_common_timezones


router = APIRouter()

@router.get("/{team_name}/search", response_model=  TeamSearch, response_model_exclude_none=True)
def search_teams(team_name : str):
    hltv = HLTVTeamSearch(query = team_name)
    found_teams = hltv.search_teams()
    return found_teams

@router.get("/{team_id}/profile", response_model = TeamProfile, response_model_exclude_none= True)
def get_team_profile(team_id : str):
    hltv = HLTVTeamProfile (team_id = team_id)
    team_profile = hltv.get_team_profile()
    return team_profile

@router.get("/{team_id}/achievements", response_model = TeamAchievements, response_model_exclude_none = True )
def get_team_achievements(team_id : str):
    hltv = HLTVTeamAchievements(team_id = team_id)
    team_achievements = hltv.get_team_achievements()
    return team_achievements

@router.get("/{team_id}/upcomingmatches/", response_model = UpcomingMatches, response_model_exclude_none = True )
def get_team_upcoming_matches(
    team_id : str,
    timezone: str = Query("UTC", description = "list of timezeones (first is used)", enum =get_common_timezones())
    ):
    hltv = HLTVTeamUpcomingMatches(team_id = team_id)
    upcoming_matches = hltv.get_team_upcoming_matches(user_timezone=timezone)
    return upcoming_matches

@router.get("/{team_id}/results/", response_model=TeamResults, response_model_exclude_none=True)
def get_team_results(
    team_id: str,
    limit: int = Query(None, description="Maximum number of results to return (all if omitted)", ge=1),
):
    """
    Get past results for a team (first page = 100 most recent matches).
    """
    service = HLTVTeamResults(team_id=team_id)
    results_data = service.get_team_results()
    
    # Apply limit if provided
    if limit and limit < len(results_data["results"]):
        results_data["results"] = results_data["results"][:limit]
        results_data["result_count"] = len(results_data["results"])
    
    return results_data
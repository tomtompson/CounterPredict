from fastapi import APIRouter

from app.schemas.players import (
    PlayerCareerStats,
    PlayerPersonalAchievements,
    PlayerProfile,
    PlayerSearch,
    PlayerStats,
    PlayerTeamAchievements,
    PlayerTrophies,
)
from app.services.players import (
    HLTVPlayerCareerStats,
    HLTVPlayerPersonalAchievements,
    HLTVPlayerProfile,
    HLTVPlayerSearch,
    HLTVPlayerStats,
    HLTVPlayersTrophies,
    HLTVPlayerTeamAchievements,
)

router = APIRouter()


@router.get(
    "/{player_name}/search",
    response_model=PlayerSearch,
)
def search_players(player_name: str):

    hltv = HLTVPlayerSearch(query=player_name)
    return hltv.search_players()


@router.get(
    "/{player_id}/profile",
    response_model=PlayerProfile,
)
def get_player_profile(player_id: str):
    hltv = HLTVPlayerProfile(player_id=player_id)
    return hltv.get_player_profile()


@router.get(
    "/{player_id}/team-achievements",
    response_model=PlayerTeamAchievements,
)
def get_player_team_achievements(player_id: str):
    hltv = HLTVPlayerTeamAchievements(player_id=player_id)
    return hltv.get_player_team_achievements()


@router.get(
    "/{player_id}/personal-achievements",
    response_model=PlayerPersonalAchievements,
)
def get_player_personal_achievements(player_id: str):
    hltv = HLTVPlayerPersonalAchievements(player_id=player_id)
    return hltv.get_player_personal_achievements()


@router.get(
    "/{player_id}/trophies",
    response_model=PlayerTrophies,
)
def get_player_trophies(player_id: str):
    hltv = HLTVPlayersTrophies(player_id=player_id)
    return hltv.get_player_trophies()


@router.get(
    "/{player_id}/stats",
    response_model=PlayerStats,
)
def get_player_stats(player_id: str):
    hltv = HLTVPlayerStats(player_id=player_id)
    return hltv.get_player_stats()


@router.get(
    "/{player_id}/career-stats",
    response_model=PlayerCareerStats,
)
def get_player_career_stats(player_id: str):
    hltv = HLTVPlayerCareerStats(player_id=player_id)
    return hltv.get_player_career_stats()

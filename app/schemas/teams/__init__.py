from app.schemas.teams.achievements import TeamAchievements, TeamAchievementsDetails
from app.schemas.teams.profile import (
    CoachDetails,
    LineupDetails,
    TeamProfile,
    TeamProfileDetails,
)
from app.schemas.teams.results import TeamResultDetails, TeamResults
from app.schemas.teams.search import (
    TeamListItem,
    TeamSearch,
    TeamSearchPlayersDetails,
    TeamSearchResult,
)
from app.schemas.teams.upcoming_matches import UpcomingMatchDetails, UpcomingMatches

__all__ = [
    "CoachDetails",
    "LineupDetails",
    "TeamAchievements",
    "TeamAchievementsDetails",
    "TeamListItem",
    "TeamProfile",
    "TeamProfileDetails",
    "TeamResultDetails",
    "TeamResults",
    "TeamSearch",
    "TeamSearchPlayersDetails",
    "TeamSearchResult",
    "UpcomingMatchDetails",
    "UpcomingMatches",
]

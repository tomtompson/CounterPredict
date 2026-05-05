# app/services/player_team_achievements.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url, trim
from app.utils.xpath import Players


@dataclass
class HLTVPlayerTeamAchievements(HLTVBase):
    """class for getting team achievements from a player profile.

    Attributes:
        player_id: hltv player id

    """

    player_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup achievements with player id."""
        super().__post_init__()

        self.URL = (
            f"https://www.hltv.org/player/{self.player_id}/who#tab-achievementBox"
        )
        self.response["id"] = self.player_id

        self.logger.info(f"loading achievements for player {self.player_id}")

        self.page = self.request_url_page()

        self.raise_exception_if_not_found(xpath=Players.Profile.URL)

        self.logger.info(f"page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def __parse_player_team_achievements(self) -> list[dict]:
        """Parse team achievements from player profile.

        Returns:
            list of achievement dictionaries

        """
        achievements_data = []

        try:
            achievement_rows = self.page.xpath(Players.TeamAchievements.ROWS)
            self.logger.info(f"found {len(achievement_rows)} achievement rows")

            for idx, row in enumerate(achievement_rows):
                try:
                    placement_list = row.xpath(Players.TeamAchievements.PLACEMENT)
                    placement = trim(placement_list[0]) if placement_list else None

                    team_name_list = row.xpath(Players.TeamAchievements.TEAM_NAME)
                    team_name = trim(team_name_list[0]) if team_name_list else None

                    team_url_list = row.xpath(Players.TeamAchievements.TEAM_URL)
                    team_url = trim(team_url_list[0]) if team_url_list else None
                    team_id = extract_from_url(team_url, "id") if team_url else None

                    tourney_name_list = row.xpath(
                        Players.TeamAchievements.TOURNAMENT_NAME,
                    )
                    tourney_name = (
                        trim(tourney_name_list[0]) if tourney_name_list else None
                    )

                    tourney_url_list = row.xpath(
                        Players.TeamAchievements.TOURNAMENT_URL,
                    )
                    tourney_url = (
                        trim(tourney_url_list[0]) if tourney_url_list else None
                    )
                    tourney_id = (
                        extract_from_url(tourney_url, "id") if tourney_url else None
                    )

                    stats_url_list = row.xpath(
                        Players.TeamAchievements.PLAYER_STATS_URL,
                    )
                    stats_path = trim(stats_url_list[0]) if stats_url_list else None
                    player_stats_url = (
                        f"https://www.hltv.org/{stats_path}" if stats_path else None
                    )

                    achievement = {
                        "placement": placement,
                        "team": {"id": team_id, "name": team_name},
                        "tournament": {
                            "id": tourney_id,
                            "name": tourney_name,
                        },
                        "player_stats_url": player_stats_url,
                    }

                    achievements_data.append(achievement)

                except Exception as e:
                    self.logger.exception(f"error parsing achievement row {idx}: {e}")
                    continue

            self.logger.info(
                f"successfully parsed {len(achievements_data)} achievements",
            )

        except Exception as e:
            self.logger.exception(f"error parsing achievements: {e}")

        return achievements_data

    # ==================== PUBLIC METHODS ====================

    def get_player_team_achievements(self) -> dict:
        """Get team achievements for player.

        Returns:
            dict with player id and achievements list

        """
        try:
            achievements = self.__parse_player_team_achievements()

            self.response["id"] = self.player_id
            self.response["achievement_count"] = len(achievements)
            self.response["achievements"] = achievements

            self.logger.info(
                f"returning {len(achievements)} achievements for player {self.player_id}",
            )

        except Exception as e:
            self.logger.exception(f"error in get_player_team_achievements: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error processing player achievements: {e!s}",
            )

        return self.response

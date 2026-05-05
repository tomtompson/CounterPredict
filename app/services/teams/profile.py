# app/services/team_profile.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import clear_number_str, extract_from_url, trim
from app.utils.xpath import Teams


@dataclass
class HLTVTeamProfile(HLTVBase):
    """class for getting team profile from hltv.

    Attributes:
        team_id: hltv team id

    """

    team_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup team profile with team id."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/team/{self.team_id}/who"
        self.response["id"] = self.team_id

        self.logger.info(f"loading team profile for team {self.team_id}")

        self.page = self.request_url_page()

        self.logger.info(f"team page loaded for {self.team_id}")

    # ==================== PARSING METHODS ====================

    def __parse_team_profile(self) -> dict:
        """Parse team profile data from page.

        Returns:
            dict with all team profile data (name, rankings, lineup, coach, logo, social)

        """
        self.logger.info("parsing team profile")

        try:
            team_name = self.get_text_by_xpath(Teams.TeamProfile.NAME)
            valve_ranking = clear_number_str(
                self.get_text_by_xpath(Teams.TeamProfile.VALVE_RANKING),
            )
            world_ranking = clear_number_str(
                self.get_text_by_xpath(Teams.TeamProfile.WORLD_RANKING),
            )
            weeks_in_top30 = self.get_text_by_xpath(
                Teams.TeamProfile.WEEKS_IN_TOP30_FOR_CORE,
            )

            logo_url = self.get_text_by_xpath(Teams.TeamProfile.LOGO_URL)
            social_media = self.get_all_by_xpath(Teams.TeamProfile.SOCIAL_MEDIA)
            average_age = self.get_text_by_xpath(Teams.TeamProfile.AVERAGE_PLAYER_AGE)

            self.logger.debug(
                f"basic info: {team_name}, ranking: {world_ranking}, age: {average_age}",
            )

            player_nicknames = self.get_all_by_xpath(Teams.TeamProfile.PLAYER_NICKNAME)
            player_urls = self.get_all_by_xpath(Teams.TeamProfile.PLAYER_URL)

            self.logger.debug(f"found {len(player_nicknames)} players in lineup")

            lineup = []
            for i, (nickname, url) in enumerate(
                zip(player_nicknames, player_urls, strict=False)
            ):
                try:
                    player_id = extract_from_url(url, "id") if url else None

                    if player_id and nickname:
                        lineup.append(
                            {
                                "id": player_id,
                                "nickname": nickname,
                            },
                        )
                    else:
                        self.logger.warning(
                            f"skipping player {i}: missing id or nickname",
                        )
                except Exception as e:
                    self.logger.exception(f"error parsing player {i}: {e}")
                    continue

            coach_data = []
            try:
                coach_nickname = trim(
                    self.get_text_by_xpath(Teams.TeamProfile.COACH_NICKNAME),
                )
                coach_url_suffix = self.get_text_by_xpath(Teams.TeamProfile.COACH_URL)

                if coach_nickname and coach_url_suffix:
                    coach_full_url = f"https://www.hltv.org{coach_url_suffix}"
                    coach_id = extract_from_url(coach_full_url, "id")

                    if coach_id:
                        coach_data.append(
                            {
                                "id": coach_id,
                                "nickname": coach_nickname,
                            },
                        )
                        self.logger.debug(f"coach: {coach_nickname}")
            except Exception as e:
                self.logger.exception(f"error parsing coach: {e}")

            result = {
                "name": team_name,
                "valve_ranking": valve_ranking,
                "world_ranking": world_ranking,
                "weeks_in_top30_for_core": weeks_in_top30,
                "average_player_age": average_age,
                "lineup": lineup,
                "coach": coach_data,
                "logo_url": logo_url,
                "social_media": social_media or [],
            }

            self.logger.info(
                f"team profile parsed: {len(lineup)} players, coach: {len(coach_data) > 0}",
            )

            return result

        except Exception as e:
            self.logger.exception(f"error parsing team profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error parsing team profile: {e!s}",
            )

    # ==================== PUBLIC METHODS ====================

    def get_team_profile(self) -> dict:
        """Get team profile data.

        Returns:
            dict with team id and profile data

        """
        try:
            team_data = self.__parse_team_profile()

            self.response["id"] = self.team_id
            self.response["team_profile"] = team_data

            self.logger.info(f"returning profile for team {self.team_id}")

        except Exception as e:
            self.logger.exception(f"error in get_team_profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting team profile: {e!s}",
            )

        return self.response

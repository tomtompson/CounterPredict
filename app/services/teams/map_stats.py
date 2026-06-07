# app/services/team_profile.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import clear_number_str, extract_from_url, trim
from app.xpaths import Teams


@dataclass
class HLTVTeamMapStats(HLTVBase):
    """class for getting team map stats from hltv.

    Attributes:
        team_id: hltv team id

    """

    team_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Set up team profile with team id."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/stats/teams/maps/{self.team_id}/who"
        self.response["id"] = self.team_id

        self.logger.info(f"loading team map stats for team {self.team_id}")

        self.page = self.request_url_page()

        self.logger.info(f"team page loaded for {self.team_id}")

    # ==================== PARSING METHODS ====================

    def __parse_team_map_stats(self) -> dict:
    """
    Parse team map stats data from page.

    Returns:
        dict: map name mapped to its statistics.
    """
    self.logger.info("parsing team map stats")

    try:
        map_blocks = self.page.xpath(Teams.MapStats.MAP_BLOCKS)

        team_map_stats = {}

        for block in map_blocks:
            map_name = block.xpath(Teams.MapStats.MAP_NAME)

            if not map_name:
                continue

            map_name = trim(map_name[0])

            stats = {}

            rows = block.xpath(Teams.MapStats.STATS_ROWS)

            for row in rows:
                spans = row.xpath(".//span/text()")

                if len(spans) < 2:
                    continue

                key = trim(spans[0])
                value = trim(spans[1])

                normalized_key = (
                    key.lower()
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("%", "percentage")
                    .replace("/", "_")
                )

                stats[normalized_key] = value

            team_map_stats[map_name] = stats

        return team_map_stats

    except Exception as e:
        self.logger.exception(f"error parsing team map stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"error parsing team map stats: {e!s}",
        )

    # ==================== PUBLIC METHODS ====================

    def get_team_map_stats(self) -> dict:
        """
        Get team map stats data.

        Returns:
            dict: team id and map stats data.
        """
        try:
            team_data = self.__parse_team_map_stats()

            self.response["id"] = self.team_id
            self.response["team_map_stats"] = team_data

            self.logger.info(f"returning map stats for team {self.team_id}")

        except Exception as e:
            self.logger.exception(f"error in get_team_map_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting team map stats: {e!s}",
            )

        return self.response

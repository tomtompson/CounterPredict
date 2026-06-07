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
        self.use_flaresolverr = True
        self.URL = f"https://www.hltv.org/stats/teams/maps/{self.team_id}/who"
        self.response["id"] = self.team_id

        self.logger.info(f"loading team map stats for team {self.team_id}")

        self.page = self.request_url_page(url=self.URL)

        self.logger.info(f"team page loaded for {self.team_id}")

    # ==================== PARSING METHODS ====================

    def __parse_team_map_stats(self) -> list[dict]:
        self.logger.info("parsing team map stats")

        try:
            map_blocks = self.page.xpath(Teams.MapStats.MAP_BLOCKS)

            team_map_stats = []

            for block in map_blocks:
                map_name = block.xpath(Teams.MapStats.MAP_NAME)

                if not map_name:
                    continue

                map_name = trim(map_name[0])

                stats = {
                    "wins_draws_losses": None,
                    "win_rate": None,
                    "total_rounds": None,
                    "round_win_after_first_kill": None,
                    "round_win_after_first_death": None,
                    "pick_rate": None,
                    "ban_rate": None,
                }

                rows = block.xpath(Teams.MapStats.STATS_ROWS)

                for row in rows:
                    spans = row.xpath(".//span/text()")

                    if len(spans) < 2:
                        continue

                    key = trim(spans[0])
                    value = trim(spans[1])

                    if key == "Wins / draws / losses":
                        stats["wins_draws_losses"] = value
                    elif key == "Win rate":
                        stats["win_rate"] = float(value.replace("%", ""))
                    elif key == "Total rounds":
                        stats["total_rounds"] = int(value)
                    elif key == "Round win-% after getting first kill":
                        stats["round_win_after_first_kill"] = float(value.replace("%", ""))
                    elif key == "Round win-% after receiving first death":
                        stats["round_win_after_first_death"] = float(value.replace("%", ""))
                    elif key == "Pick %":
                        stats["pick_rate"] = float(value.replace("%", ""))
                    elif key == "Ban %":
                        stats["ban_rate"] = float(value.replace("%", ""))

                team_map_stats.append(
                    {
                        "map_name": map_name,
                        "stats": stats,
                    }
                )

            return team_map_stats

        except Exception as e:
            self.logger.exception(f"error parsing team map stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error parsing team map stats: {e!s}",
            )

    # ==================== PUBLIC METHODS ====================

    def get_team_map_stats(self) -> dict:
        try:
            team_data = self.__parse_team_map_stats()

            self.response["id"] = int(self.team_id)
            self.response["maps"] = team_data

            self.logger.info(f"returning map stats for team {self.team_id}")

        except Exception as e:
            self.logger.exception(f"error in get_team_map_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting team map stats: {e!s}",
            )

        return self.response

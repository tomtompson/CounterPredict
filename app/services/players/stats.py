from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import (
    convert_minutes_to_seconds,
    extract_float_from_percentage_number,
    parse_float,
)
from app.utils.xpath import Players


@dataclass
class HLTVPlayerStats(HLTVBase):
    """class for getting player statistics from hltv.

    Attributes:
        player_id: hltv player id

    """

    player_id: str

    def __post_init__(self) -> None:
        """Setup stats with player id."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/stats/players/{self.player_id}/diddy"
        self.response["id"] = self.player_id

        self.logger.info(f"loading stats for player {self.player_id}")

        try:
            self.page = self.request_url_page()
        except HTTPException as e:
            if e.status_code == 403:
                self.logger.exception(
                    f"403 Forbidden for player {self.player_id}. Saving response for debugging.",
                )
            ##self._debug_fetch_and_save(self.URL)
            raise

        self.logger.info(f"stats page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def __parse_firepower_stats(self) -> dict:
        """Parse firepower stats section."""
        stats = {}

        try:
            stats["kills_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.KILLS_PER_ROUND),
            )
            stats["kills_per_round_win"] = parse_float(
                self.get_text_by_xpath(Players.Stats.KILLS_PER_ROUND_WIN),
            )
            stats["damage_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.DAMAGE_PER_ROUND),
            )
            stats["damage_per_round_win"] = parse_float(
                self.get_text_by_xpath(Players.Stats.DAMAGE_PER_ROUND_WIN),
            )
            stats["rounds_with_a_kill_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(Players.Stats.ROUNDS_WITH_A_KILL_PERCENTAGE),
                )
            )
            stats["rating_1_0"] = parse_float(
                self.get_text_by_xpath(Players.Stats.RATING_1_0),
            )
            stats["rounds_with_multi_kill_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(
                        Players.Stats.ROUNDS_WITH_MULTI_KILL_PERCENTAGE,
                    ),
                )
            )
            stats["pistol_round_rating"] = parse_float(
                self.get_text_by_xpath(Players.Stats.PISTOL_ROUND_RATING),
            )

            self.logger.debug("firepower stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing firepower stats: {e}")

        return stats

    def __parse_entrying_stats(self) -> dict:
        """Parse entrying stats section."""
        stats = {}

        try:
            stats["saved_by_teammate_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.SAVED_BY_TEAMMATE_PER_ROUND),
            )
            stats["traded_deaths_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.TRADED_DEATHS_PER_ROUND),
            )
            stats["traded_deaths_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.TRADED_DEATHS_PERCENTAGE),
            )
            stats["opening_deaths_traded_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(
                        Players.Stats.OPENING_DEATHS_TRADED_PERCENTAGE,
                    ),
                )
            )
            stats["assists_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.ASSISTS_PER_ROUND),
            )
            stats["support_rounds_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.SUPPORT_ROUNDS_PERCENTAGE),
            )

            self.logger.debug("entrying stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing entrying stats: {e}")

        return stats

    def __parse_trading_stats(self) -> dict:
        """Parse trading stats section."""
        stats = {}

        try:
            stats["saved_teammate_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.SAVED_TEAMMATE_PER_ROUND),
            )
            stats["trade_kills_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.TRADE_KILLS_PER_ROUND),
            )
            stats["trade_kills_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.TRADE_KILLS_PERCENTAGE),
            )
            stats["assisted_kills_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.ASSISTED_KILLS_PERCENTAGE),
            )
            stats["damage_per_kill"] = parse_float(
                self.get_text_by_xpath(Players.Stats.DAMAGE_PER_KILL),
            )

            self.logger.debug("trading stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing trading stats: {e}")

        return stats

    def __parse_opening_stats(self) -> dict:
        """Parse opening stats section."""
        stats = {}

        try:
            stats["opening_kills_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.OPENING_KILLS_PER_ROUND),
            )
            stats["opening_deaths_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.OPENING_DEATHS_PER_ROUND),
            )
            stats["opening_attempts_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.OPENING_ATTEMPTS_PERCENTAGE),
            )
            stats["opening_success_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.OPENING_SUCCESS_PERCENTAGE),
            )
            stats["win_after_opening_kill_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(
                        Players.Stats.WIN_AFTER_OPENING_KILL_PERCENTAGE,
                    ),
                )
            )
            stats["attacks_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.ATTACKS_PER_ROUND),
            )

            self.logger.debug("opening stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing opening stats: {e}")

        return stats

    def __parse_clutching_stats(self) -> dict:
        """Parse clutching stats section."""
        stats = {}

        try:
            stats["clutch_points_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.CLUTCH_POINTS_PER_ROUND),
            )
            stats["last_alive_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.LAST_ALIVE_PERCENTAGE),
            )
            stats["1v1_win_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats._1v1_WIN_PERCENTAGE),
            )
            stats["time_alive_per_round"] = convert_minutes_to_seconds(
                self.get_text_by_xpath(Players.Stats.TIME_ALIVE_PER_ROUND),
            )
            stats["saves_per_round_loss_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(
                        Players.Stats.SAVES_PER_ROUND_LOSS_PERCENTAGE,
                    ),
                )
            )

            self.logger.debug("clutching stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing clutching stats: {e}")

        return stats

    def __parse_sniping_stats(self) -> dict:
        """Parse sniping stats section."""
        stats = {}

        try:
            stats["sniper_kills_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.SNIPER_KILLS_PER_ROUND),
            )
            stats["sniper_kills_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.Stats.SNIPER_KILLS_PERCENTAGE),
            )
            stats["rounds_with_sniper_kills_percentage"] = (
                extract_float_from_percentage_number(
                    self.get_text_by_xpath(
                        Players.Stats.ROUNDS_WITH_SNIPER_KILLS_PERCENTAGE,
                    ),
                )
            )
            stats["sniper_multi_kill_rounds"] = parse_float(
                self.get_text_by_xpath(Players.Stats.SNIPER_MULTI_KILL_ROUNDS),
            )
            stats["sniper_opening_kills_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.SNIPER_OPENING_KILLS_PER_ROUND),
            )

            self.logger.debug("sniping stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing sniping stats: {e}")

        return stats

    def __parse_utility_stats(self) -> dict:
        """Parse utility stats section."""
        stats = {}

        try:
            stats["utility_damage_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.UTILITY_DAMAGE_PER_ROUND),
            )
            stats["utility_kills_per_100_rounds"] = parse_float(
                self.get_text_by_xpath(Players.Stats.UTILITY_KILLS_PER_100_ROUNDS),
            )
            stats["flashes_thrown_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.FLASHES_THROWN_PER_ROUND),
            )
            stats["flash_assists_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.FLASH_ASSISTS_PER_ROUND),
            )
            stats["time_opponent_flashed_per_round"] = parse_float(
                self.get_text_by_xpath(Players.Stats.TIME_OPPONENT_FLASHED_PER_ROUND),
            )

            self.logger.debug("utility stats parsed")
        except Exception as e:
            self.logger.exception(f"error parsing utility stats: {e}")

        return stats

    def __parse_all_stats(self) -> dict:
        """Parse all player stats sections.

        Returns:
            dict with all stats organized by category

        """
        self.logger.info("parsing all player stats")

        player_stats = {
            "firepower": self.__parse_firepower_stats(),
            "entrying": self.__parse_entrying_stats(),
            "trading": self.__parse_trading_stats(),
            "opening": self.__parse_opening_stats(),
            "clutching": self.__parse_clutching_stats(),
            "sniping": self.__parse_sniping_stats(),
            "utility": self.__parse_utility_stats(),
        }

        self.logger.info("all stats parsed successfully")
        return player_stats

    # ==================== PUBLIC METHODS ====================

    def get_player_stats(self) -> dict:
        """Get all stats for player.

        Returns:
            dict with player id and stats by category

        """
        try:
            player_stats = self.__parse_all_stats()

            self.response["id"] = self.player_id
            self.response["stats"] = player_stats  # note: returns dict, not list

            self.logger.info(f"returning stats for player {self.player_id}")

        except Exception as e:
            self.logger.exception(f"error in get_player_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error processing player stats: {e!s}",
            )

        return self.response

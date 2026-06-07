# app/services/matches/past_players_stats.py

import re
import time
from calendar import monthrange
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import (
    convert_minutes_to_seconds,
    extract_float_from_percentage_number,
    extract_from_url,
    parse_float,
)
from app.xpaths import Matches


@dataclass
class HLTVMatchPastPlayersStats(HLTVBase):
    """Class for getting each past player's stats before a given match."""

    MAX_WORKERS = 4
    MAX_PLAYER_RETRIES = 3
    RETRY_SLEEP_SECONDS = 10
    ROLE_SECTIONS = (
        "firepower",
        "entrying",
        "trading",
        "opening",
        "clutching",
        "sniping",
        "utility",
    )
    ROLE_SIDES = {
        "combined": "stats-side-combined",
        "ct": "stats-side-ct",
        "t": "stats-side-t",
    }

    match_id: int

    def __post_init__(self) -> None:
        """Set up match stats with match ID."""
        super().__post_init__()

        self.use_flaresolverr = True
        self.URL = f"https://www.hltv.org/matches/{self.match_id}/na-vs-na"

        self.logger.info(f"loading match stats for match {self.match_id}")
        self.page = self.request_url_page()
        self.logger.info(f"match page loaded for {self.match_id}")

    @staticmethod
    def __normalize_stat_key(label: str | None) -> str | None:
        """Normalize HLTV summary labels into predictable snake_case keys."""
        if not label:
            return None

        normalized = re.sub(r"[^a-z0-9]+", "_", label.strip().lower()).strip("_")
        if normalized == "1on1_win_percentage":
            return "1v1_win_percentage"
        if normalized == "win_after_opening_kill":
            return "win_after_opening_kill_percentage"
        if normalized == "support_rounds":
            return "support_rounds_percentage"
        if normalized == "saves_per_round_loss":
            return "saves_per_round_loss_percentage"
        if normalized == "opening_success":
            return "opening_success_percentage"
        if normalized == "opening_attempts":
            return "opening_attempts_percentage"
        return normalized or None

    @staticmethod
    def __parse_stat_value(value: str | None):
        """Convert HLTV stat values into typed values where possible."""
        if value is None or value == "-":
            return None
        if "%" in value:
            return extract_float_from_percentage_number(value)
        if "m" in value and "s" in value:
            return convert_minutes_to_seconds(value)

        numeric_value = parse_float(value)
        return numeric_value if numeric_value is not None else value

    @staticmethod
    def __get_stats_date_range(match_date: str) -> tuple[str, str]:
        end_date = datetime.strptime(match_date, "%Y-%m-%d")
        month = end_date.month - 3
        year = end_date.year

        while month <= 0:
            month += 12
            year -= 1

        day = min(end_date.day, monthrange(year, month)[1])
        start_date = end_date.replace(year=year, month=month, day=day)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def __parse_players(self) -> tuple[str | None, list[str]]:
        """Extract match date and unique player URLs from the match page."""
        try:
            date_string = self.get_text_by_xpath(Matches.MatchStats.MATCH_DATE)
            cleaned_string = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_string or "")
            dt_object = datetime.strptime(cleaned_string, "%d of %B %Y")
            formatted_date = dt_object.strftime("%Y-%m-%d")
            player_urls = self.get_all_by_xpath(Matches.MatchPastPlayersStats.PLAYER_ID)
            unique_player_urls = list(dict.fromkeys(player_urls))

            self.logger.info(
                f"found {len(unique_player_urls)} players for match {self.match_id}",
            )
            return formatted_date, unique_player_urls
        except Exception as e:
            self.logger.error(f"Error parsing players for match {self.match_id}: {e}")
            raise HTTPException(status_code=500, detail="Error parsing players stats")

    def get_player_stats(
        self,
        player_id: str,
        player_name: str,
        match_date: str,
    ) -> dict:
        """Get past summary and role stats for a player before the match date."""
        player_slug = (player_name or "unknown").strip().strip("/")
        start_date, end_date = self.__get_stats_date_range(match_date.strip())
        url = (
            f"https://www.hltv.org/stats/players/{player_id}/{player_slug}"
            f"?startDate={start_date}&endDate={end_date}"
        )
        self.logger.info(
            f"requesting past stats for player {player_id} from {start_date} to {end_date} from url {url}",
        )
        page = self.request_url_page(url=url)
        stats = {"summary": {}, "roles": {}}

        try:
            stat_boxes = self.get_elements_by_xpath(
                Matches.MatchPastPlayersStats.SUMMARY_STAT_BOXES,
                element=page,
            )

            for stat_box in stat_boxes:
                stat_label = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_STAT_TITLE,
                    element=stat_box,
                )
                stat_value = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_STAT_VALUE,
                    element=stat_box,
                )
                stat_key = self.__normalize_stat_key(stat_label)

                if not stat_key or stat_value is None:
                    continue

                stats["summary"][stat_key] = self.__parse_stat_value(stat_value)

                t_rating = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_STAT_T_VALUE,
                    element=stat_box,
                )
                if t_rating is not None:
                    stats["summary"][f"{stat_key}_t_rating"] = self.__parse_stat_value(
                        t_rating,
                    )

                ct_rating = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_STAT_CT_VALUE,
                    element=stat_box,
                )
                if ct_rating is not None:
                    stats["summary"][f"{stat_key}_ct_rating"] = self.__parse_stat_value(
                        ct_rating,
                    )

            summary_rows = self.get_elements_by_xpath(
                Matches.MatchPastPlayersStats.SUMMARY_DATA_ROWS,
                element=page,
            )

            for summary_row in summary_rows:
                stat_label = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_DATA_TITLE,
                    element=summary_row,
                )
                stat_value = self.get_text_by_xpath(
                    Matches.MatchPastPlayersStats.SUMMARY_DATA_VALUE,
                    element=summary_row,
                )
                stat_key = self.__normalize_stat_key(stat_label)

                if not stat_key or stat_value is None:
                    continue

                stats["summary"][stat_key] = self.__parse_stat_value(stat_value)

            for role_name in self.ROLE_SECTIONS:
                role_section_xpath = (
                    Matches.MatchPastPlayersStats._ROLE_SECTION_BASE.format(
                        role=role_name,
                    )
                )
                role_section = self.get_elements_by_xpath(
                    role_section_xpath,
                    element=page,
                )

                if not role_section:
                    continue

                role_data = {}
                section_element = role_section[0]

                for side_name, side_class in self.ROLE_SIDES.items():
                    side_score = None
                    side_stats = {}
                    score_xpath = Matches.MatchPastPlayersStats.ROLE_SECTION_SCORE.format(
                        side_class=side_class,
                    )
                    score = self.get_text_by_xpath(
                        score_xpath,
                        element=section_element,
                    )
                    if score is not None:
                        side_score = self.__parse_stat_value(score)

                    row_xpath = Matches.MatchPastPlayersStats.ROLE_ROWS.format(
                        side_class=side_class,
                    )
                    rows = self.get_elements_by_xpath(
                        row_xpath,
                        element=section_element,
                    )

                    for row in rows:
                        row_title = self.get_text_by_xpath(
                            Matches.MatchPastPlayersStats.ROLE_ROW_TITLE,
                            element=row,
                        )
                        row_value = self.get_text_by_xpath(
                            Matches.MatchPastPlayersStats.ROLE_ROW_VALUE,
                            element=row,
                        )
                        stat_key = self.__normalize_stat_key(row_title)
                        if not stat_key:
                            continue
                        side_stats[stat_key] = self.__parse_stat_value(row_value)

                    if side_score is not None or side_stats:
                        role_data[side_name] = {
                            "score": side_score,
                            "stats": side_stats or None,
                        }

                if role_data:
                    stats["roles"][role_name] = role_data
        except Exception as e:
            self.logger.error(f"Error parsing past stats for player {player_id}: {e}")
            raise HTTPException(status_code=500, detail="Error parsing player past stats")

        return stats

    def __fetch_player_result(self, player: str, match_date: str) -> dict | None:
        self.logger.info(
            f"getting past stats for player {player} in match {self.match_id}",
        )

        player_id_clean = extract_from_url(player, "id") if player else None
        player_name = extract_from_url(player, "nickname") if player else None

        if not player_id_clean or not match_date:
            return None

        last_error = None

        for attempt in range(1, self.MAX_PLAYER_RETRIES + 1):
            try:
                player_stats = self.get_player_stats(
                    player_id=player_id_clean,
                    player_name=player_name,
                    match_date=match_date,
                )

                return {
                    "id": player_id_clean,
                    "name": player_name,
                    "stats": player_stats,
                }

            except Exception as exc:
                last_error = exc
                self.logger.warning(
                    f"failed player {player_id_clean} in match {self.match_id} "
                    f"attempt {attempt}/{self.MAX_PLAYER_RETRIES}: {exc}",
                )

                if attempt < self.MAX_PLAYER_RETRIES:
                    time.sleep(self.RETRY_SLEEP_SECONDS)

        self.logger.error(
            f"giving up on player {player_id_clean} in match {self.match_id}: {last_error}",
        )

        return None

    def get_past_players_stats(self) -> dict:
        """Get past summary stats for all players in the match."""
        try:
            match_date, players = self.__parse_players()

            self.response["match_id"] = self.match_id
            self.response["match_date"] = match_date
            self.response["players"] = []

            max_workers = min(self.MAX_WORKERS, len(players)) or 1
            ordered_results: list[dict | None] = [None] * len(players)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_index = {
                    executor.submit(self.__fetch_player_result, player, match_date): index
                    for index, player in enumerate(players)
                }

                for future in as_completed(future_to_index):
                    index = future_to_index[future]

                    try:
                        ordered_results[index] = future.result()
                    except Exception as exc:
                        self.logger.warning(
                            f"skipping one player result in match {self.match_id}: {exc}",
                        )
                        ordered_results[index] = None

            self.response["players"] = [
                result for result in ordered_results if result is not None
            ]

        except Exception as e:
            self.logger.error(
                f"Error getting past players stats for match {self.match_id}: {e}",
            )
            raise HTTPException(
                status_code=500,
                detail="Error getting past players stats",
            )

        return self.response

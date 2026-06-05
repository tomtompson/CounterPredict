# app/services/matches/upcoming_players_stats.py

import re
from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import (
    convert_minutes_to_seconds,
    extract_float_from_percentage_number,
    parse_float,
)
from app.xpaths import Matches


@dataclass
class HLTVMatchUpcomingPlayersStats(HLTVBase):
    """Class for getting each upcoming match player's current stats."""

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
        super().__post_init__()

        self.use_flaresolverr = True
        self.URL = f"https://www.hltv.org/matches/{self.match_id}/na-vs-na"

        self.logger.info(f"loading upcoming match page for match {self.match_id}")
        self.page = self.request_url_page()
        self.logger.info(f"upcoming match page loaded for {self.match_id}")

    @staticmethod
    def __normalize_stat_key(label: str | None) -> str | None:
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
    def __normalize_player_slug(value: str | None) -> str | None:
        if not value:
            return None
        slug = value.strip().lower()
        slug = re.sub(r"'([^']+)'", r"\1", slug)
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        return slug or None

    @staticmethod
    def __parse_stat_value(value: str | None):
        if value is None or value == "-":
            return None
        if "%" in value:
            return extract_float_from_percentage_number(value)
        if "m" in value and "s" in value:
            return convert_minutes_to_seconds(value)

        numeric_value = parse_float(value)
        return numeric_value if numeric_value is not None else value

    @staticmethod
    def __get_stats_date_range() -> tuple[str, str]:
        today = datetime.now()
        month = today.month - 3
        year = today.year

        while month <= 0:
            month += 12
            year -= 1

        day = min(today.day, monthrange(year, month)[1])
        start_date = today.replace(year=year, month=month, day=day)
        return start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

    def __parse_players(self) -> tuple[str, str, list[dict[str, str]]]:
        try:
            player_elements = self.get_elements_by_xpath(
                Matches.MatchUpcomingPlayersStats.PLAYER_COMPARE,
            )
            start_date, end_date = self.__get_stats_date_range()
            seen_ids = set()
            players = []

            for player_element in player_elements:
                player_id = self.get_text_by_xpath(
                    Matches.MatchUpcomingPlayersStats.PLAYER_ID,
                    element=player_element,
                )
                player_name = self.get_text_by_xpath(
                    Matches.MatchUpcomingPlayersStats.PLAYER_NICKNAME,
                    element=player_element,
                )
                player_slug = self.__normalize_player_slug(player_name)

                if not player_id or not player_slug or player_id in seen_ids:
                    continue

                seen_ids.add(player_id)
                players.append({"id": player_id, "slug": player_slug})

            self.logger.info(
                f"found {len(players)} players for upcoming match {self.match_id}",
            )
            return start_date, end_date, players
        except Exception as e:
            self.logger.error(
                f"Error parsing players for upcoming match {self.match_id}: {e}",
            )
            raise HTTPException(
                status_code=500,
                detail="Error parsing upcoming players stats",
            )

    def get_player_stats(
        self,
        player_id: str,
        player_name: str,
        start_date: str,
        end_date: str,
    ) -> dict:
        url = (
            f"https://www.hltv.org/stats/players/{player_id}/{player_name}"
            f"?startDate={start_date}&endDate={end_date}"
        )
        self.logger.info(
            f"requesting upcoming stats for player {player_id}/{player_name} from {start_date} to {end_date} from url {url}",
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

                section_element = role_section[0]
                role_data = {}

                for side_name, side_class in self.ROLE_SIDES.items():
                    side_score = None
                    side_stats = {}
                    score_xpath = Matches.MatchPastPlayersStats.ROLE_SECTION_SCORE.format(
                        side_class=side_class,
                    )
                    score = self.get_text_by_xpath(score_xpath, element=section_element)
                    if score is not None:
                        side_score = self.__parse_stat_value(score)

                    row_xpath = Matches.MatchPastPlayersStats.ROLE_ROWS.format(
                        side_class=side_class,
                    )
                    rows = self.get_elements_by_xpath(row_xpath, element=section_element)

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
            self.logger.error(
                f"Error parsing upcoming stats for player {player_id}: {e}",
            )
            raise HTTPException(
                status_code=500,
                detail="Error parsing upcoming player stats",
            )

        return stats

    def get_upcoming_players_stats(self) -> dict:
        try:
            start_date, end_date, players = self.__parse_players()

            self.response["match_id"] = self.match_id
            self.response["match_date"] = end_date
            self.response["players"] = []

            for player in players:
                player_stats = self.get_player_stats(
                    player_id=player["id"],
                    player_name=player["slug"],
                    start_date=start_date,
                    end_date=end_date,
                )
                self.response["players"].append(
                    {
                        "id": player["id"],
                        "name": player["slug"],
                        "stats": player_stats,
                    },
                )
        except Exception as e:
            self.logger.error(
                f"Error getting upcoming players stats for match {self.match_id}: {e}",
            )
            raise HTTPException(
                status_code=500,
                detail="Error getting upcoming players stats",
            )

        return self.response
